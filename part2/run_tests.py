import sys
import unittest

from test.test_amenities_api import TestAmenityEndpoints
from test.test_places_api import TestPlaceEndpoints
from test.test_reviews_api import TestReviewEndpoints
from test.test_users_api import TestUserEndpoints


def run_tests():
    """Run all API endpoint tests and generate a report"""
    # Create test suite
    test_suite = unittest.TestSuite()

    # Add test cases
    test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestUserEndpoints))
    test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestPlaceEndpoints))
    test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestReviewEndpoints))
    test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestAmenityEndpoints))

    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # Print summary
    print("\n=== Test Summary ===")
    print(f"Total tests run: {result.testsRun}")
    print(f"Successful: {result.testsRun - len(result.errors) - len(result.failures)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    # Return appropriate exit code
    return 0 if len(result.failures) == 0 and len(result.errors) == 0 else 1


if __name__ == "__main__":
    sys.exit(run_tests())
