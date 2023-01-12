from sympy import isprime

class ArrowNetworkDB:
    def __init__(self):
        self.lines = []
        def getFile():
            with open('ArrowNetworkDB', 'r') as f:
                strLines = f.read()
                strLines = strLines.splitlines()
                for line in strLines:
                    line = eval(line)
                    line[1] = dict(line[1])
                    line[2] = list(line[2])
                    self.lines.append(line)
        getFile()


    def areYouOwner(self,inObj,byOwner):
        owners = self.lines[inObj][1]
        ownerNumber = len(owners)
        count = 0
        for id in byOwner.keys():
            if id in owners:
                if byOwner.get(id) in owners.values():
                    count += 1
        return True if ownerNumber // 2 < count else False

    def putAccessArrow(self,fromObj, byOwner, toObj):
        def judgeAccess(self):
            rootsFO,rootsTO = []
            for path in self.lines[fromObj][2]:
                rootsFO.append(path[0])
            for path in self.lines[toObj][2]:
                rootsTO.append(path[0])
            for rfo in rootsFO:
                for rto in rootsTO:
                    if rfo.equal(rto):
                        return True
            return False

        def giveCiteTo(self):
            setLines = set(self.lines[fromObj][2]).add(self.lines[toObj][2])
            self.lines[fromObj][2] = list(setLines)

        def giveCiteFrom():
            self.lines[toObj][3].append(fromObj)
            
        if self.areYouOwner(fromObj, byOwner):
            if judgeAccess():
                giveCiteTo()
                giveCiteFrom()
            return True
        else:
            return False
            
    def deleteAccessArrow(self, fromObj, byOwner, toObj):
        if self.areYouOwner(fromObj, byOwner): 
            return True
        else:
            return False
                

    def runAccessAuthority(self):
        pass

class DBServer:
    def __init__(self):
        self.lines = []
        def getFile():
            with open('ArrowNetworkDB', 'r') as f:
                strLines = f.read()
                strLines = strLines.splitlines()
                for line in strLines:
                    line = eval(line)
                    line[1] = dict(line[1])
                    line[2] = list(line[2])
                    self.lines.append(line)
        getFile()
        self.andb = ArrowNetworkDB()


class RootOwner:
    iamOwner = [{'8':'rootpassword'}]
    def __init__(self):
        self.andb = ArrowNetworkDB()
        self.length = len(self.andb.lines)
        if isprime(self.length):
            if self.andb.putAccessArrow(self.length,self.iamOwner,'10'):
                print('success connect')
            else:
                print('Error connect')
                

    def passMeInitialObj(self, OwnerPassword,data = None):
        pass

    def passMeObj(self, OwnerObjId, OwnerPassword, accessId, data = None):
        pass






ro = RootOwner()




#5 - 3 → 5 + (-3) → 1101 + 0101 → 10010 → 2

#784 - 638 = 1100010000 - 1001111110 = 1100010000 + 110000010 = 10010010010 = 146

#784 - 638 = 784 + 362 = 1146