import unittest
import os
import json
import datetime
from tefillin_tracker import record_tefillin_date, view_tefillin_history

class TestDateRecording(unittest.TestCase):
    TEST_DATA_FILE = 'test_tefillin_dates.json'
    TODAY_STR = datetime.date.today().strftime('%Y-%m-%d')

    def setUp(self):
        """Create a temporary test JSON file before each test."""
        # Ensure the file is clean before each test
        if os.path.exists(self.TEST_DATA_FILE):
            os.remove(self.TEST_DATA_FILE)

    def tearDown(self):
        """Remove the temporary test JSON file after each test."""
        if os.path.exists(self.TEST_DATA_FILE):
            os.remove(self.TEST_DATA_FILE)

    def test_record_single_date(self):
        """Test recording a single date."""
        record_tefillin_date(data_file=self.TEST_DATA_FILE)
        self.assertTrue(os.path.exists(self.TEST_DATA_FILE))
        with open(self.TEST_DATA_FILE, 'r') as f:
            dates = json.load(f)
        self.assertEqual(len(dates), 1)
        self.assertEqual(dates[0], self.TODAY_STR)

    def test_record_multiple_dates_no_duplicates(self):
        """Test that recording the same date twice does not create duplicates."""
        record_tefillin_date(data_file=self.TEST_DATA_FILE)
        record_tefillin_date(data_file=self.TEST_DATA_FILE) # Record again
        with open(self.TEST_DATA_FILE, 'r') as f:
            dates = json.load(f)
        self.assertEqual(len(dates), 1)
        self.assertEqual(dates[0], self.TODAY_STR)

    def test_view_history_empty_file_non_existent(self):
        """Test viewing history when the data file does not exist."""
        # Ensure file does not exist by calling setUp and then explicitly deleting if necessary
        if os.path.exists(self.TEST_DATA_FILE):
            os.remove(self.TEST_DATA_FILE)
        history = view_tefillin_history(data_file=self.TEST_DATA_FILE)
        self.assertEqual(history, "No tefillin dates recorded yet (data file not found).")

    def test_view_history_empty_file_exists_empty_json_array(self):
        """Test viewing history when the data file exists but is an empty JSON array."""
        with open(self.TEST_DATA_FILE, 'w') as f:
            json.dump([], f)
        history = view_tefillin_history(data_file=self.TEST_DATA_FILE)
        self.assertEqual(history, "No tefillin dates recorded yet.")

    def test_view_history_empty_file_exists_invalid_json(self):
        """Test viewing history when the data file exists but contains invalid JSON."""
        with open(self.TEST_DATA_FILE, 'w') as f:
            f.write("invalid json")
        history = view_tefillin_history(data_file=self.TEST_DATA_FILE)
        self.assertEqual(history, "No tefillin dates recorded yet (file is empty or corrupted).")


    def test_view_history_with_data(self):
        """Test viewing history when there is recorded data."""
        record_tefillin_date(data_file=self.TEST_DATA_FILE)
        # Manually add another date to test multiple entries
        yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        with open(self.TEST_DATA_FILE, 'r') as f:
            dates = json.load(f)
        dates.append(yesterday)
        dates.sort()
        with open(self.TEST_DATA_FILE, 'w') as f:
            json.dump(dates, f)

        history = view_tefillin_history(data_file=self.TEST_DATA_FILE)
        self.assertIsInstance(history, list)
        self.assertEqual(len(history), 2)
        self.assertIn(self.TODAY_STR, history)
        self.assertIn(yesterday, history)
        self.assertEqual(history, sorted([self.TODAY_STR, yesterday]))


if __name__ == '__main__':
    unittest.main()
