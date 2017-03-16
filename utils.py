import os


def prepare_directory(dirname):
    if not os.path.isdir(dirname):
        msg = 'Creating {}'.format(dirname)
        print(msg)
        os.mkdir(dirname)
    else:
        msg = 'Already exists: {}'.format(dirname)
        print(msg)
