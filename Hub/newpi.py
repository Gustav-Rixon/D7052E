
import json
from pathlib import Path

#structure example
class Newpi:
    
    #generates the list of all ids
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
    
    #tror inte jag behöver metod för detta bestämmer mig senare (kollar om ipt finns sen innan så det inte sker dupes )
    def ipexists(self, list, ip):
        return all("92.35.224.111" == a[1] for a in list)
    
        #adds the ip to the json calling on help methods to do we want it to 
    def joinnet(self, ip):
        with open("..//Hub/Storage/cameras.json") as f:
            data = json.load(f)
        temp = self.idiplist(data)
        if self.ipexists(temp, ip):
            
            return "already exists"
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
            return "Join succ"
    