from sympy import isprime

class DBServerBasic:
    data = {}
    def __init__(self):
        def getFile():
            with open('ANDBData','r') as f:
                self.data = eval(f.read())
        
        getFile()


    def saveFile(self):
        with open('ANDBData','w') as f:
            f.write(str(self.data))


class DBServer(DBServerBasic):
    
    def checkAndCreateObj(self,obj,objKey,owner,citeTo,citeFrom,data):
        if obj not in self.data.keys():
            self.data[obj] = [data,[objKey,[owner]],citeTo,citeFrom]

    def createObj(self,obj,objKey,owner,citeTo,citeFrom,data):
        self.data[obj] = [data,[objKey,[owner]],citeTo,citeFrom]

    def judgeYouOwners(self,obj,byOwners):
        def operateOwner(self,obj,byOwners):
            return True if self.data.get(obj)[1][0] == byOwners.get(obj) else False
        if self.judgeDBHaveObj(obj):
            owners = self.data.get(obj)[1][1]
            ownerNumber = 1
            ownerCount = 0
            for o in owners:
                ownerNumber += 1
                ownerCount += 1 if self.judgeYouOwners(o,byOwners) else 0
            if operateOwner(obj,byOwners):
                ownerCount += 1
            return True if ownerNumber // 2 <= ownerCount else False
        else:
            return False

    def judgeYouRootOwner(self,rootKey):
        return True if rootKey == 'rootpasskey1234' else False

    def judgeAccess(self, fromObj, toObj):
        if self.judgeDBHaveObj(toObj):
            if self.judgeDBHaveObj(fromObj):
                fromObj = int(fromObj)
                toObj = int(toObj)
                rootsFO = []
                rootsTO = []
                for path in self.data.get(fromObj)[2]:
                    rootsFO.append(path[0])
                for path in self.data.get(toObj)[2]:
                    rootsTO.append(path[0])
                for rfo in rootsFO:
                    for rto in rootsTO:
                        if rfo == rto:
                            return True
                return False
        else:
            if self.judgeDBHaveObj(fromObj):


    def giveCites(self, fromObj, toObj):
        fromObj = int(fromObj)
        toObj = int(toObj)
        giveCiteTo()
        giveCiteFrom()
        self.saveFile()
        
        def giveCiteTo():
            toObjPathes = self.data.get(toObj)[2]
            fromObjPathes = self.data.get(fromObj)[2]
            for top in toObjPathes:
                for fop in fromObjPathes:
                    if top != fop:
                        self.data.get(fromObj)[2].append(top)
        
        def giveCiteFrom():
            self.data.get(toObj)[3].append(str(fromObj))

    def changeData0(self, obj, data):
        data = str(data)
        self.data.get(obj)[0] = data

    def addOwners0(self, toObj, fromObj):
        if fromObj not in self.data.get(toObj)[1][1]:
            self.data.get(toObj)[1][1].append(fromObj)
            return True
        else:
            return False
        
    def deleteOwners0(self, toObj, fromObj):
        self.data.get(toObj)[1][1].remove(fromObj)

class ArrowNetworkDB(DBServer):
    def putAccessArrow(self, fromObj, byOwners, toObj):
        if self.judgeYouOwners(fromObj, byOwners):
            if self.judgeAccess(fromObj, toObj):
                self.giveCites(fromObj, toObj)

                
    def changeData(self, obj, byOwners,data):
        if self.judgeYouOwners(obj, byOwners):
            self.changeData0(obj,data)


    def addOwners(self, toObj, fromObj, byOwners):
        if self.judgeYouOwners(toObj, byOwners):
            return self.addOwners0(toObj, fromObj)
        else:
            return False

    
    def deleteOwner(self,toObj,fromObj,byOwners):
        if self.judgeYouOwners(toObj,byOwners):
            self.deleteOwner0(toObj,fromObj)

class RootOwner():
    iamtheOwner = {'8':'rootpasskey1234'}
    def __init__(self):
        self.andb = ArrowNetworkDB()
        
    def giveMeObj(self, byOwners, toObj, fromObj):
        if isprime(toObj):
            self.andb.changeData(toObj,self.iamtheOwner,toObj)
            self.andb.putAccessArrow(toObj,self.iamtheOwner,'9')
            return False
        else:
            if self.andb.addOwners(toObj,fromObj,byOwners):
                self.andb.deleteOwner(toObj,'9',self.iamtheOwner)
                return True
            else:
                return False


r = RootOwner()
r.andb.