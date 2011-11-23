#!/usr/bin/env python
import unittest
import db
import sabsub
import sys
import os
import shutil

workdir = '/tmp/sabsub_test/'
interm = os.path.join(workdir, 'interm')
final = os.path.join(workdir, 'final')

sab_argv = [os.path.join(os.path.abspath('.'), sys.argv[0]),
        os.path.join(interm, 'White.Collar.S02E04.DVDRip.XviD-SAiNTS.avi'),
        'White.Collar.S02E05.DVDRip.XviD-SAiNTS.nzb',
        'White.Collar.S02E05.DVDRip.XviD-SAiNTS',
        '',
        'tv',
        'alt.binaries.multimedia',
        '0']

sick_argv = [os.path.join(os.path.abspath('.'), sys.argv[0]),
        '/tmp/sabsub_test/final/White.Collar.S02E04.By.the.Book.avi',
        'White.Collar.S02E04.DVDRip.XviD-SAiNTS.avi',
        '108611',
        '2',
        '5',
        '03-09-2010'
        ]

class SabSubTests(unittest.TestCase):
    def setUp(self):
        self.conn = db.initialize('/tmp/sabsub_test/test.db')
        os.makedirs(interm)
        os.makedirs(final)
        os.system('touch ' + os.path.join(interm, 'White.Collar.S02E04.DVDRip.XviD-SAiNTS.avi'))
        os.system('touch ' + os.path.join(final, 'White.Collar.S02E04.By.the.Book.avi '))
    def tearDown(self):
        shutil.rmtree(workdir)

    def test_sabnzbd_run(self):
        sys.argv = sab_argv
        sabsub.sabnzbd_run(self.conn)
        with self.conn:
            c = self.conn.cursor()
            c.execute(u'''SELECT * FROM eps''')
            all_eps = c.fetchall()
            self.assertEqual(all_eps, [(u'White.Collar.S02E05.DVDRip.XviD-SAiNTS', u'/tmp/sabsub_test/interm/White.Collar.S02E04.DVDRip.XviD-SAiNTS.avi', None, None)])

    def test_sickbeard_run(self):
        self.test_sabnzbd_run()
        sys.argv = sick_argv
        sabsub.sickbeard_run(self.conn)
        with self.conn:
            c = self.conn.cursor()
            c.execute(u'''SELECT * FROM eps''')
            all_eps = c.fetchall()
            self.assertEqual(all_eps, [(u'White.Collar.S02E05.DVDRip.XviD-SAiNTS', u'/tmp/sabsub_test/interm/White.Collar.S02E04.DVDRip.XviD-SAiNTS.avi', '/tmp/sabsub_test/final/White.Collar.S02E04.By.the.Book.avi', '108611')])

    def test_cron_run(self):
        self.test_sickbeard_run()
        sabsub.cron_run(self.conn)
        self.assertTrue(os.path.exists('/tmp/sabsub_test/final/White.Collar.S02E04.By.the.Book.srt'))

if __name__ == '__main__':
    tests = unittest.main()
