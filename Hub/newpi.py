
import json
from pathlib import Path

with open("..//Hub/Storage/cameras.json") as f:
  data = json.load(f)
  
idip=[]
for p_id in data:
    idip.append((p_id['id'], p_id['ip']))
    
print( all("92.35.224.111" == a[1] for a in idip))
print(idip)
print((idip[-1][0] + 1))
#structure example
class Newpi:
    
    #adds the ip to the json calling on help methods to do we want it to 
    def join(ip):
        with open("..//Hub/Storage/cameras.json") as f:
            data = json.load(f)
        temp = idiplist(data)
        if idlist(data):
            
            return "already exists"
        else:
            id = assignid()
            generatefolder(id)
            return "Join succ"
    
    #generates the list of all ids
    def idiplist(data):
       idip=[]
       for p_id in data:
        ids.append((p_id['id'], p_id['ip']))
       return idip
    
    #Generates a folder in  if one doesnt exist to store all the 
    def generatefolder(id):
        Path("..//Hub/Storage/Cameras/" + str(id) ).mkdir(parents=True, exist_ok=True)
    
    #tror inte jag behöver metod för detta bestämmer mig senare (lägger till 1 i id från sista numret i listan av cameror)
    def assignid(list):
        return  (list[-1][0] + 1)
    
    #tror inte jag behöver metod för detta bestämmer mig senare (kollar om ipt finns sen innan så det inte sker dupes )
    def ipexists(data, ip):
        return all("92.35.224.111" == a[1] for a in idip)
    