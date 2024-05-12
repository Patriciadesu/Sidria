import json
import os
class talking_log:
    def __init__(self,outfile_path) -> None:
        self.filename = outfile_path
        self.prompt = {"memory":[{
                "role": "system",
                "content": "you have to role play and talk to users as his little step sister \nYou can answer in Thai and English, but your user are Thai. You should answer in Thai only."
                }]}
        if os.path.isfile(self.filename)==False:
            data = json.dumps(self.prompt,indent=4)
            with open (self.filename, 'w+') as fp:
                fp.write(data)

    def write_log(self,speaker,content):
        with open(self.filename,'r+') as file:
            file_data = json.load(file)["memory"]
            file_data.append({"role":speaker,"content":content})
            file.seek(0)
            # convert back to json.
            json.dump({"memory":file_data}, file, indent = 4,ensure_ascii=False)

    def get_log(self):
        with open(self.filename,'r') as file:
            file_data = json.load(file)["memory"]
        return file_data