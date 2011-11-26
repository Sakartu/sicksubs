#!/usr/bin/env python
import unittest
import db
import sicksubs
import sys
import os
import shutil

workdir = '/tmp/sicksubs_test/'
interm = os.path.join(workdir, 'interm')
final = os.path.join(workdir, 'final')

sick_argv = [os.path.join(os.path.abspath('.'), sys.argv[0]),
        '/tmp/sicksubs_test/final/White.Collar.S02E04.By.the.Book.avi',
        '/tmp/sicksubs_test/interm/White.Collar.S02E04.DVDRip.XviD-SAiNTS.avi',
        '108611',
        '2',
        '5',
        '03-09-2010'
        ]

class SickSubsTests(unittest.TestCase):
    def setUp(self):
        self.conn = db.initialize('/tmp/sicksubs_test/test.db')
        os.makedirs(interm)
        os.makedirs(final)
        os.system('touch ' + os.path.join(interm, 'White.Collar.S02E04.DVDRip.XviD-SAiNTS.avi'))
        os.system('touch ' + os.path.join(final, 'White.Collar.S02E04.By.the.Book.avi '))

    def tearDown(self):
        shutil.rmtree(workdir)

    def test_sickbeard_run(self):
        sys.argv = sick_argv
        sicksubs.sickbeard_run(self.conn)
        with self.conn:
            c = self.conn.cursor()
            c.execute(u'''SELECT * FROM eps''')
            all_eps = c.fetchall()
            self.assertEqual(all_eps, [(u'/tmp/sicksubs_test/interm/White.Collar.S02E04.DVDRip.XviD-SAiNTS.avi', '/tmp/sicksubs_test/final/White.Collar.S02E04.By.the.Book.avi', '108611')])

    def test_cron_run(self):
        self.test_sickbeard_run()
        sicksubs.cron_run(self.conn)
        self.assertTrue(os.path.exists('/tmp/sicksubs_test/final/White.Collar.S02E04.By.the.Book.srt'))

if __name__ == '__main__':
    tests = unittest.main()
