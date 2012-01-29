#!/usr/bin/env python
import unittest
import db
import sicksubs
import sys
import os
import glob
import shutil

workdir = '/tmp/sicksubs_test/'
interm = os.path.join(workdir, 'interm')
final = os.path.join(workdir, 'final')


class SickSubsTests(unittest.TestCase):
    def setUp(self):
        self.conn = db.initialize('/tmp/sicksubs_test/test.db')
        os.makedirs(interm)
        os.makedirs(final)
        os.system('touch ' + os.path.join(interm, 'White.Collar.S02E04.DVDRip.XviD-SAiNTS.avi'))
        os.system('touch ' + os.path.join(final, 'White.Collar.S02E04.By.the.Book.avi '))

    def tearDown(self):
        shutil.rmtree(workdir)

    def test_found(self):
        # existing ep
        sys.argv = [os.path.join(os.path.abspath('.'), sys.argv[0]),
        '/tmp/sicksubs_test/final/White.Collar.S02E04.By.the.Book.avi',
        '/tmp/sicksubs_test/interm/White.Collar.S02E04.DVDRip.XviD-SAiNTS.avi',
        '108611',
        '2',
        '5',
        '03-09-2010'
        ]
        # no need to run the cron run, the sickbeard run will do that for us
        sicksubs.sickbeard_run(self.conn)
        self.assertTrue(os.path.exists(final + '/White.Collar.S02E04.By.the.Book.srt'))
        self.assertTrue(os.path.exists(final + '/White.Collar.S02E04.By.the.Book.avi.works'))

    def test_not_found(self):
        # use a non existing ep
        sys.argv = [os.path.join(os.path.abspath('.'), sys.argv[0]),
        '/tmp/sicksubs_test/final/White.Collar.S02E40.By.the.Book.avi',
        '/tmp/sicksubs_test/interm/White.Collar.S02E40.DVDRip.XviD-SAiNTS.avi',
        '108611',
        '2',
        '5',
        '03-09-2010'
        ]
        # no need to run the cron run, the sickbeard run will do that for us
        sicksubs.sickbeard_run(self.conn)
        self.assertEqual([], glob.glob(final + '/*.srt'))
        self.assertEqual([], glob.glob(final + '/*.works'))

if __name__ == '__main__':
    tests = unittest.main()
