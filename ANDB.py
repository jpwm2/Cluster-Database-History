from sympy import isprime

class DBServer:
    def __init__(self):
        self.lines = []
        def getFile():
            with open('ArrowNetworkDB','r') as f:
                strLines = f.read()
            self.lines = eval(strLines)

        getFile()

    def saveFile(self):
        with open('ArrowNetworkDB','w') as f:
            f.write(str(self.lines))
        with open('Log2','w') as f:
            f.write(str(self.lines))
            

    def areYouOwners(self,inObj,byOwners):
        if self.doDBHaveObj(inObj):
            rootOwner = {'8':'rootpassword'}
            return True if byOwners == rootOwner else False
        else:
            owners = self.lines[inObj][2]
            ownerNumber = len(owners)
            count = 0
            for id in byOwners.keys():
                if id in owners:
                    if byOwners.get(id) in owners.values():
                        count += 1
            return True if ownerNumber // 2 < count else False

    def doYouHaveAnOwner(self,obj,ownerId,ownerKey):
        if ownerId in self.lines[obj][2].keys():
            return True if ownerKey == self.lines[obj][2].get(ownerId) else False

        
    
    def judgeAccess(self,fromObj,toObj):
        fromObj = int(fromObj)
        toObj = int(toObj)
        rootsFO = []
        rootsTO = []
        for path in self.lines[fromObj][3]:
            rootsFO.append(path[0])
        for path in self.lines[toObj][3]:
            rootsTO.append(path[0])
        for rfo in rootsFO:
            for rto in rootsTO:
                if rfo == rto:
                    return True
        return False

    def giveCites(self,fromObj,toObj):
        fromObj = int(fromObj)
        toObj = int(toObj)
        def giveCiteTo():
            toObjPathes = self.lines[toObj][3]
            fromObjPathes = self.lines[fromObj][3]
            for top in toObjPathes:
                for fop in fromObjPathes:
                    if top != fop:
                        self.lines[fromObj][3].append(top)

        def giveCiteFrom():
            self.lines[toObj][3].append(str(fromObj))

        giveCiteTo()
        giveCiteFrom()
        self.saveFile()

    def doDBHaveObj(self,obj):
        length = len(self.lines)
        for i in range(length):
            return True if obj == self.lines[i][0] else False
                

    def changeData0(self,obj,data):
        data = str(data)
        if self.doDBHaveObj(obj):
            newLine = [[obj],data,{'8':'rootpassword'},[['8']],[]]
            self.lines.append(newLine)
        else:
            self.lines[obj][1] = data

    def addOwners0(self, toObj, fromObj):
        self.lines[toObj][2].update(self.lines[fromObj][2])
        
    def delteOwner0(self, obj, ownerId):
        del self.lines[obj][2][ownerId]


class ArrowNetworkDB(DBServer):
    def putAccessArrow(self,fromObj,byOwners,toObj):
        if self.areYouOwners(fromObj,byOwners):
            if self.judgeAccess(fromObj,toObj):
                self.giveCites(fromObj,toObj)
            
    def changeData(self,obj,byOwners,data):
        if self.areYouOwners(obj,byOwners):
            self.changeData0(obj,data)

    def addOwners(self, toObj, fromObj, byOwners):
        if self.areYouOwners(toObj, byOwners):
            self.addOwners0(toObj, fromObj)

    def deleteOwner(self,obj,ownerId,ownerKey):
        if self.doYouHaveAnOwner(obj,ownerId,ownerKey):
            self.deleteOwner0(obj,ownerId)
    
    
class RootOwner():
    iamtheOwner = {'8':'rootpassword'}
    def __init__(self):
        self.andb = ArrowNetworkDB()
        self.length = self.pickNumber()
        if isprime(self.length):
            self.andb.changeData(self.length,self.iamtheOwner,self.length)
            self.andb.putAccessArrow(self.length,self.iamtheOwner,'9')

    def pickNumber(self):
        return len(self.andb.lines)
            
    def giveMeObj(self,byOwners,data = None):
        pass

    def createUser(self,data = None):
        pass

            

r = RootOwner()