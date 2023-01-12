
class Object:
    def __init__(self, data,keys, owners = 0, accesses = 0):
        self.data = data
        self.keys = [str(keys)]
        self.owners = [str(owners)]
        self.accesses = [str(accesses)]

    def accessObj(self):
        return (self.data, self.keys, self.owners, self.accesses)


class MachineSystem:
    datas =[]
    def __init__(self):
        self.readFile()

    def readFile(self):
        with open('Root/way0') as f:
            self.datas = [s.strip() for s in f.readlines()]

    def writeFile(self,obj):
        with open('Root/way0','a') as f:
            print(obj,file = f)

class RootSystem(MachineSystem):
    def createObject(self,data, ownerKey = None, ownerId = None, accessId = None):
        if ownerId == None:
            ownerId = str(len(self.datas))
            newUser = Object(data,ownerKey,ownerId,0)
            self.writeFile(newUser.accessObj())


obj = Object('a','b','c','d')
m = MachineSystem()
print(m.readFile())
print(m.datas)

r = RootSystem()
print(r.readFile())
print(r.datas)
r.createObject('hi','0123')
r = RootSystem()
print(r.datas)

