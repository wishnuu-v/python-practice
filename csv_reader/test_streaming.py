
import csv
import os
import tempfile
import unittest

from main import read_csv_batches, process_csv


class TestCSVStreaming(unittest.TestCase):

    def setUp(self):

        self.file = tempfile.NamedTemporaryFile(
            mode="w",
            newline="",
            encoding="utf-8",
            delete=False
        )

        writer = csv.writer(self.file)

        writer.writerow(["name", "salary"])

        writer.writerow(["Alice", "50000"])
        writer.writerow(["Bob", "60000"])
        writer.writerow(["Charlie", "70000"])
        writer.writerow(["David", ""])

        self.file.close()

        self.filepath = self.file.name

    def tearDown(self):

        if os.path.exists(self.filepath):
            os.remove(self.filepath)

    def test_batch_size(self):

        batches = list(
            read_csv_batches(self.filepath, batch_size=2)
        )

        self.assertEqual(len(batches), 2)
        self.assertEqual(len(batches[0]), 2)
        self.assertEqual(len(batches[1]), 2)

    def test_column_names(self):

        batches = list(
            read_csv_batches(self.filepath, batch_size=2)
        )

        self.assertIn("name", batches[0][0])
        self.assertIn("salary", batches[0][0])

    def test_invalid_batch_size(self):

        with self.assertRaises(ValueError):
            list(read_csv_batches(self.filepath, 0))

    def test_invalid_batch_type(self):

        with self.assertRaises(TypeError):
            list(read_csv_batches(self.filepath, 1.5))

    def test_statistics(self):

        results = process_csv(
            self.filepath,
            column="salary",
            batch_size=2
        )

        self.assertEqual(results["total_records"], 4)
        self.assertEqual(results["mean"], 60000)
        self.assertEqual(results["minimum"], 50000)
        self.assertEqual(results["maximum"], 70000)
        self.assertEqual(results["missing_values"], 1)

    def test_partial_batch(self):

        batches = list(
            read_csv_batches(self.filepath, batch_size=3)
        )

        self.assertEqual(len(batches), 2)
        self.assertEqual(len(batches[1]), 1)


if __name__ == "__main__":
    unittest.main()
