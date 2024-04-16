import json 

global shrimps_data
f = open('shrimps.json')
shrimps_data = json.load(f)
f.close()
  
global users_data
f = open('users.json')
users_data = json.load(f)
f.close()

def db_commit(data, filename):
     with open(filename, "w") as json_file:
        json.dump(data, json_file, indent=4)