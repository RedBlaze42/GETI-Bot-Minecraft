import json
import os

class json_file():

    def __init__(self,file_path="config.json",create_file=True):
        self.file_path=file_path
        if not os.path.isfile(file_path) and create_file:
            open(file_path,"w").close()
        with open(file_path,"r") as file:
            json_data=file.read()
        self.__dict__ = json.loads(json_data)
        self.json_data=json_data

    def __setattr__(self,name,value):
        if name=="__dict__" and hasattr(self,"file_path"):
            with open(self.file_path,"w") as file:
                json.dump(self.__dict__,file)