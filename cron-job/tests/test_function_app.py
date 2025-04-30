"""Test to see if the Azure function can grab data and upload it to a database."""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "azure_function")))

from azure_function import function_app


class FunctionAppTests(unittest.TestCase):

    def test_get_and_upload_scores(self):
        print(f"{FunctionAppTests.test_get_and_upload_scores.__name__.upper()}:")
        function_app.get_and_upload_scores()


if __name__ == "__main__":
    unittest.main()
