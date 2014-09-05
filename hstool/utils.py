import os


def path_and_rename(path):
    def wrapper(instance, filename):
        filename = filename.replace(' ', '_')
        return os.path.join(path, filename)
    return wrapper
