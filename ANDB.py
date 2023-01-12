from sympy import isprime



class DBServerBasic:
    data = []
    location = {}
    def __init__(self):
        getFile()

        def getFile():
            with open('ANDBData','r') as f:
                self.data = eval(f.read())
            with open('ANBDLocation','r') as f:
                self.location = dict(f.read())

    def saveFile(self):
        with open('ANDBData','w') as f:
            f.write(str(self.data))
        with open('ANDBLocation','w') as f:
            f.write(str(self.location))

    def doDBHaveObj(self,obj):
        return True if obj in self.location.keys() else False

class DBServer(DBServerBasic):
    def areYouOwners(self, inObj, byOwners):
        if self.doDBHaveObj(inObj):
            owners = self.data[self.location.get(inObj)][1]
            ownerNumber = len(owners)
            count = 0
            for id in byOwners.keys():
                if id in owners.keys():
                    if byOwners.get(id) in owners.values():
                        count += 1
            return True if ownerNumber // 2 < count else False

    def doYouHaveOwners(self, toObj, fromObj, byOwners):
        if ownerId in self.data[self.location.get(obj)][1].keys():
            return True if ownerKey == self.data[self.location.get(obj)][1].get(ownerId) else False

    def judgeAccess(self, fromObj, toObj):
        fromObj = int(fromObj)
        toObj = int(toObj)
        rootsFO = []
        rootsTO = []
        for path in self.data[self.location.get(fromObj)][2]:
            rootsFO.append(path[0])
        for path in self.data[self.location.get(toObj)][2]:
            rootsTO.append(path[0])
        for rfo in rootsFO:
            for rto in rootsTO:
                if rfo == rto:
                    return True
        return False

    def giveCites(self, fromObj, toObj):
        fromObj = int(fromObj)
        toObj = int(toObj)
        giveCiteTo()
        giveCiteFrom()
        self.saveFile()

        def giveCiteTo():
            toObjPathes = self.data[self.location.get(toObj)][2]
            fromObjPathes = self.data[self.location.get(fromObj)][2]
            for top in toObjPathes:
                for fop in fromObjPathes:
                    if top != fop:
                        self.lines[fromObj][3].append(top)

        def giveCiteFrom():
            self.lines[toObj][3].append(str(fromObj))

    def changeData0(self, obj, data):
        data = str(data)
        if self.doDBHaveObj(obj):
            newLine = [data,{'8':'roootpassword'},[['8']],[]]
            length = len(self.data)
            self.data.append(newLine)
            self.location[obj] = length
        else:
            self.data[self.location.get(obj)][0] = data

    def addOwners0(self, toObj, fromObj):
        added = True
        for ownerId in self.data[self.location.get(fromObj)][1].keys():
            if ownerId not in self.data[self.location.get(toObj)][1].keys():
                self.data[self.location.get(toObj)][1][ownerId] = self.data[self.location.get(fromObj)][1].get(ownerId)
                added = False
        return added
        

    def deleteOwner0(self, obj, ownerId):
        del self.data[self.location.get(obj)][1][ownerId]

class ArrowNetworkDB(DBServer):
    def putAccessArrow(self, fromObj, byOwners, toObj):
        if self.areYouOwners(fromObj, byOwners):
            if self.judgeAccess(fromObj, toObj):
                self.giveCites(fromObj, toObj)

    def changeData(self, obj, byOwners,data):
        if self.areYouOwners(obj, byOwners):
            self.changeData0(obj,data)

    def addOwners(self, toObj, fromObj, byOwners):
        if self.areYouOwners(toObj, byOwners):
            return self.addOwners0(toObj, fromObj)

    def deleteOwner(self,toObj,fromObj,byOwners):
        if self.doYouHaveOwners(toObj,byOwners):
            self.deleteOwner0(toObj,fromObj)

class RootOwner():
    iamtheOwner = {'8':'rootpassword'}
    def __init__(self):
        self.andb = ArrowNetworkDB()

    def pickNumber(self):
        return len(self.andb.data)
            
    def giveMeObj(self,byOwners,toObj, fromObj):
        if isprime(self.length):
            self.andb.changeData(self.length,self.iamtheOwner,self.length)
            self.andb.putAccessArrow(self.length,self.iamtheOwner,'9')
            return False
        else:
            if self.andb.addOwners(toObj,fromObj,byOwners):
            else:
                self.andb.deleteOwner(toObj,)

    def createUser(self,data = None):
        pass




r = RootOwner()
r.giveMeObj({'8':'rootpassword'},'Way1')