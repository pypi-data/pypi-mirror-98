import unittest
from filecreate import FileCreate
import os

TEST_FOLDER = r'test_data\test_files'
TEST_MASK = 'test##.txt'


class TestFileCreate(unittest.TestCase):
    def test1_filecreate(self):
        if os.path.isdir(TEST_FOLDER) and len(os.listdir(TEST_FOLDER)) > 0:
            raise FileExistsError('Test directory {} must be empty'.format(TEST_FOLDER))

        files_created = []
        for i in range(10):
            with FileCreate(os.path.join(TEST_FOLDER, TEST_MASK),
                            create_directory=True,
                            leading_zeros=i % 2) as file:
                files_created.append(file.name)
        real_created = os.listdir(TEST_FOLDER)
        new_filename = FileCreate.get_filename(TEST_FOLDER, TEST_MASK)
        new_filename_no_zeros = FileCreate.get_filename(TEST_FOLDER, TEST_MASK, leading_zeros=False)

        for x in os.listdir(TEST_FOLDER):
            os.remove(os.path.join(TEST_FOLDER, x))
        os.rmdir(TEST_FOLDER)
        os.rmdir(os.path.split(TEST_FOLDER)[0])

        self.assertEqual('test06.txt', new_filename)
        self.assertEqual('test6.txt', new_filename_no_zeros)
        self.assertEqual([os.path.split(x)[1] for x in files_created].sort(), real_created.sort())


if __name__ == '__main__':
    unittest.main()
