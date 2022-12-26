import json
from pathlib import Path

class Tools:
    
    def rename(self,id,name):
        with open("..//Hub/Storage/cameras.json") as f:
            data = json.load(f)
        print(data)
        for a in data:
            print(a)
            if a['id'] == id:
                a['name'] = name
                
            with open("..//Hub/Storage/cameras.json", "w") as outfile:
                json.dump(data, outfile, 
                        indent=4,  
                        separators=(',',': '))