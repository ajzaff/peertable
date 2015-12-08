import unittest
import coverage


if __name__ == '__main__':
    cov = coverage.Coverage(omit='*test_*.py')
    runner = unittest.TextTestRunner()
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir='.')
    cov.start()
    runner.run(suite)
    cov.stop()
    cov.report()