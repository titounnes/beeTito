import yaml 
from .file import File

class Yaml(object):    
    def load(self, path):
        path_file = File().get_path(path)
        if path_file:
            with open(path_file, 'r') as f:
                return yaml.load(f, Loader=yaml.FullLoader)
        else:
            return "File %s is not exists"%(path)     