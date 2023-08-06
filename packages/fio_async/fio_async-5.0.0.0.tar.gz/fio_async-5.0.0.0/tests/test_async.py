# -*- coding: utf-8 -*-
import unittest
import subprocess
import threading

import trytond.tests.test_tryton
from trytond.tests.test_tryton import activate_module, with_transaction
from trytond.pool import Pool


class Command(object):
    """
    Wrapper around subprocess to execute on a different thread and use the
    threads timeout capability to effect a timeout.
    """
    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None

    def run(self, timeout=30):
        def target():
            print('Thread started')
            self.process = subprocess.Popen(self.cmd, shell=True)
            self.process.communicate()
            print('Thread finished')

        thread = threading.Thread(target=target)
        thread.start()

        thread.join(timeout)
        if thread.is_alive():
            print('Terminating process')
            self.process.terminate()
            thread.join()
        print(self.process.returncode)


class TestAsync(unittest.TestCase):
    '''
    Test Async
    '''

    def setUp(self):
        """
        Set up data used in the tests.
        this method is called before each test function execution.
        """
        activate_module('async')

    @with_transaction()
    def test0005_test_apply_async(self):
        """Test apply async method.
        """
        View = Pool().get('ir.ui.view')
        Async = Pool().get('async.async')

        expected = View.search_read([])
        result = Async.apply_async(
            method='search_read', model=View.__name__,
            args=[[]],
        )

        # Will be pending because there is no worker running
        self.assertEqual(result.status, 'PENDING')

        # Now launch the worker and kill it after 15 seconds
        command = Command('celery -l info -A trytond_async.tasks worker')
        command.run(15)

        # Now the task should be done. So check status and the
        # returned value to make sure its what we need.
        self.assertEqual(result.status, 'SUCCESS')
        self.assertEqual(result.result, expected)

    @with_transaction()
    def test0006_test_apply_async_ar(self):
        """Test apply async method. But move around active records.
        """
        View = Pool().get('ir.ui.view')
        Async = Pool().get('async.async')

        expected = View.search([])
        result = Async.apply_async(
            method='search', model=View.__name__,
            args=[[]],
        )

        # Will be pending because there is no worker running
        self.assertEqual(result.status, 'PENDING')

        # Now launch the worker and kill it after 15 seconds
        command = Command('celery -l info -A trytond_async.tasks worker')
        command.run(15)

        # Now the task should be done. So check status and the
        # returned value to make sure its what we need.
        self.assertEqual(result.status, 'SUCCESS')
        self.assertEqual(result.result, expected)


def suite():
    """
    Define suite
    """
    test_suite = trytond.tests.test_tryton.suite()
    test_suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(TestAsync)
    )
    return test_suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
