import json
import jsonpickle

def saveData(channel, groups, roles):
  with open("roles.json",'w') as file:
    file.write(jsonpickle.encode([channel, groups, roles]))
  file.close()
  
def loadData():
  with open('roles.json') as file:
    data = json.load(file)
  file.close()
  return data
