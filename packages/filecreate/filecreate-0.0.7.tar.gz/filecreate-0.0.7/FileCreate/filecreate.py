import os


def get_drive(path):
    if isinstance(path, str):
        path = os.path.split(path)
    if not path[1]:
        return path[0]
    return get_drive(os.path.split(path[0]))


def list_dirs_of_path(path):
    """
    Lists all directories of given path. If path is relative - it's resolved to absolute

    For example:
    r = list_dirs_of_path('C:\temp\test\passed.txt')
    r will contain:
    [ 'C:\\', 'C:\\temp', 'C:\\temp\\test' ]

    :param path: relative or absolute path to directory or a file
    :return: list of absolute paths of all directories in the given path sorted
    """
    dirs = []
    if not os.path.isabs(path):
        path = os.path.abspath(path)

    def _get_dir(path):
        p = []
        if isinstance(path, str):
            if not os.path.isfile(path):
                dirs.append(path)
            p = os.path.split(path)
        if not p[1]:
            return
        return _get_dir(p[0])

    _get_dir(path)
    return sorted(dirs, key=lambda x: len(x))


class FileCreate:
    def __init__(self, file_mask,
                 create_directory=False,
                 overwrite=False,
                 leading_zeros=True):
        self.directory, self.file_mask = os.path.split(os.path.abspath(file_mask))
        if not os.path.isdir(self.directory):
            if create_directory:
                for d in list_dirs_of_path(self.directory):
                    if not os.path.isdir(d):
                        os.mkdir(d)
            else:
                raise FileNotFoundError('Directory {} does not exist. '
                                        'To create automatically - set create_directory=True'.format(self.directory))

        self.overwrite = overwrite
        self.leading_zeros = leading_zeros
        self.filename = None
        self.handle = None

    def __enter__(self):
        self.filename = os.path.join(self.directory, self.get_filename(self.directory, self.file_mask,
                                                                       leading_zeros=self.leading_zeros))
        if os.path.isfile(self.filename) and not self.overwrite:
            raise FileExistsError('File already exists. To overwrite - set overwrite=True ')
        self.handle = open(self.filename, 'w')

        return self.handle

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.handle.close()

    @staticmethod
    def get_filename(directory, file_mask, leading_zeros=True):
        file_mask = os.path.basename(file_mask)
        cnt = file_mask.count('#')
        if not leading_zeros:
            file_mask = file_mask.replace('#', '', cnt - 1)
        file_mask = file_mask.replace('#', '{}')
        files = set(os.listdir(directory))
        fmt = '{:0' + str(cnt) + 'd}' if leading_zeros else '{}'
        next_num_int = 1
        while True:
            next_num = fmt.format(next_num_int)
            if len(next_num) > cnt:
                raise FileExistsError('File cannot be created as maximum number in sequence is reached')

            filename = file_mask.format(*[x for x in next_num])
            if filename not in files:
                return filename
            next_num_int += 1
