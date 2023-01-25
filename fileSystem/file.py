import os

class File(object):

    def get_path(self, path):
        if os.path.isfile(path):
            return path
        
        return False