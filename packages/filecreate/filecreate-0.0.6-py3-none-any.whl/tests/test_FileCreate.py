import unittest
from filecreate import FileCreate
from random import randint
import os

TEST_FOLDER = 'test_files'
TEST_MASK = 'test##.txt'

class MyTestCase(unittest.TestCase):
    def test1_filecreate(self):
        if os.path.isdir(TEST_FOLDER) and len(os.listdir(TEST_FOLDER)) > 0:
            raise FileExistsError('Test directory {} must be empty'.format(TEST_FOLDER))

        files_created = []
        for _ in range(10):
            with FileCreate(os.path.join(TEST_FOLDER, TEST_MASK)) as file:
                files_created.append(file.name)
                file.writelines([str(randint(0, 1000)) for _ in range(20)])
        real_created = os.listdir(TEST_FOLDER)
        new_filename = FileCreate.get_filename(TEST_FOLDER, TEST_MASK)

        for x in os.listdir(TEST_FOLDER):
            os.remove(os.path.join(TEST_FOLDER, x))
        os.rmdir(TEST_FOLDER)

        self.assertEqual('test11.txt', new_filename)
        self.assertEqual([os.path.split(x)[1] for x in files_created], real_created)

if __name__ == '__main__':
    unittest.main()
