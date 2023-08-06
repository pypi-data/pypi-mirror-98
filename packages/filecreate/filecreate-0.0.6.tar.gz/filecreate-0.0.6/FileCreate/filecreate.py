import os


class FileCreate:
    def __init__(self, file_mask, create_directory=True, overwrite=True):
        self.directory, self.file_mask = os.path.split(os.path.abspath(file_mask))
        if not os.path.isdir(self.directory):
            if create_directory:
                #TODO create all directories in path
                os.mkdir(self.directory)
            else:
                raise FileNotFoundError('Directory {} does not exist'.format(self.directory))

        self.overwrite = overwrite
        self.filename = None
        self.handle = None

    def __enter__(self):
        self.filename = os.path.join(self.directory, self.get_filename(self.directory, self.file_mask))
        if os.path.isfile(self.filename) and not self.overwrite:
            raise FileExistsError('File already exists')
        self.handle = open(self.filename, 'w')

        return self.handle

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.handle.close()

    @staticmethod
    def get_filename(directory, file_mask):
        p = os.path.basename(file_mask).replace('#', '{}')

        files = set(os.listdir(directory))
        cnt = p.count('{}')
        fmt = '{:0' + str(cnt) + 'd}'
        next_num_int = 1
        while True:
            next_num = fmt.format(next_num_int)
            if len(next_num) > cnt:
                raise FileExistsError('File cannot be created as maximum number in sequence is reached')

            filename = p.format(*[x for x in next_num])
            if filename not in files:
                return filename
            next_num_int += 1
