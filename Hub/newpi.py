
import json
from pathlib import Path

#structure example
class Newpi:
    
    #generates the list of all ids and ips
    def idiplist(self, data):
       idip=[]
       for p_id in data:
        idip.append((p_id['id'], p_id['ip']))
       return idip
    
    #Generates a folder in  if one doesnt exist to store all the 
    def generatefolder(self, id):
        Path("..//Hub/Storage/Cameras/" + str(id) ).mkdir(parents=True, exist_ok=True)
    
    #tror inte jag behöver metod för detta bestämmer mig senare (lägger till 1 i id från sista numret i listan av cameror)
    def assignid(self, list):
        return  (list[-1][0] + 1)
    
    #Checks if an ip already exists and returns a id if it does and 0 otherwise
    def ipexists(self, list, ip):
        for a in list:
            for b in a:
                if b == ip:
                    return a[0]
        return 0
    
    #adds the ip to the json and assigns an id if it already exists it returns your old id if its new you get a new one
    def joinnet(self, ip):
        with open("..//Hub/Storage/cameras.json") as f:
            data = json.load(f)
        temp = self.idiplist(data)
        dupe = self.ipexists(temp, ip)
        #print(dupe)
        if 0 < dupe:
            return dupe
        #print(len(temp))
        if len(temp)== 0:
            self.generatefolder(1)
            data.append({
                "id": 1,
                "ip": ip,
                "name": ""
            }) 
            with open("..//Hub/Storage/cameras.json", "w") as outfile:
                json.dump(data, outfile, 
                        indent=4,  
                        separators=(',',': '))
            return 1
        else:
            id = self.assignid(temp)
            self.generatefolder(id)
            # Data to be written
            data.append({
                "id": id,
                "ip": ip,
                "name": ""
            }) 
            with open("..//Hub/Storage/cameras.json", "w") as outfile:
                json.dump(data, outfile, 
                        indent=4,  
                        separators=(',',': '))
            return id
    
#TODO behöver en endpoint som connectar detta med kameror sen behöver jag fixa camerakoden som connectar till detta.