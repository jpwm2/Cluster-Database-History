from sympy import isprime

class DBServerBasic:
    data = {}
    def __init__(self):
        def getFile():
            with open('ANDBData','r') as f:
                self.data = eval(f.read())
        
        getFile()


    def saveFile(self):
        print(self.data)
        #with open('ANDBData','w') as f:
        #    f.write(str(self.data))

class DBServer(DBServerBasic):

    def checkObj(self,*obj):
        for o in obj:
            if o not in self.data.keys():
                self.data[o] = [None,[None,['8']],[],[]]
                self.giveCites(o,'8','9')
                return False
            else:
                return True

    def checkReservation(self,obj):
        if isprime(obj):
            return False
        else:
            return True

    def judgeYouOwners(self, obj, byOwners):
        def operatePasskeyOwner(obj,byOwners):
            return True if self.data.get(obj)[1][0] == byOwners.get(obj) else False
        def allowPasskeyOwner(ownerNumber, ownerCount):
            if ownerNumber == 0:
                return True
            else:
                if ownerCount == 0:
                    ownerCount = 0.1
                return True if ownerNumber / ownerCount < 2 else False
        
        if self.checkObj(obj):
            owners = self.data.get(obj)[1][1]
            ownerNumber = 0
            ownerCount = 0
            for o in owners:
                ownerNumber += 1
                ownerCount += 1 if self.judgeYouOwners(o,byOwners) else 0
            if allowPasskeyOwner(ownerNumber,ownerCount):
                if operatePasskeyOwner(obj,byOwners):
                    ownerCount += 1
            ownerNumber += 1
            if ownerCount == 0:
                ownerCount = 0.1
            return True if ownerNumber / ownerCount <= 2 else False
        else:
            return False

    def judgeAccess(self, fromObj, toObj):
        for to in toObj:
            fromObj = str(fromObj)
            to = str(to)
            print(to)
            print(self.data.get(to))
            rootsFO = []
            rootsTO = []
            for path in self.data.get(fromObj)[2]:
                rootsFO.append(path[0])
            for path in self.data.get(to)[2]:
                rootsTO.append(path[0])
            for rfo in rootsFO:
                for rto in rootsTO:
                    if rfo != rto:
                        return False
        return True

    def deleteCites(self, fromObj, toObj):
        self.data.get(fromObj)[2].remove(toObj)

    def giveCites(self, fromObj, toObj):
        
        def giveCiteTo(fromObj,toObj):
            toObjPathes = list(toObj)
            fromObjPathes = self.data.get(fromObj)[2]
            if toObjPathes not in fromObjPathes:
                self.data.get(fromObj)[2].append(toObjPathes)
        
        def giveCiteFrom(fromObj, toObj):
            for to in toObj:
                if fromObj not in self.data.get(to)[3]:
                    self.data.get(to)[3].append(fromObj)
        giveCiteTo(fromObj, toObj)
        giveCiteFrom(fromObj, toObj)
        self.saveFile()


    def changeData0(self, obj, data):
        data = str(data)
        self.data.get(obj)[0] = data
    

    def addOwners0(self, toObj, fromObj):
        if fromObj not in self.data.get(toObj)[1][1]:
            self.data.get(toObj)[1][1].append(fromObj)
            return True
        else:
            return False
    
    def notificateCiteFrom(self, fromObj,toObjs1, toObjs2):
        sameObjs = set(self.data.get(fromObj)[3]) & set(self.data.get(toObjs1[-1])[3])
        for so in sameObjs:
            for path in self.data.get(so)[2]:
                length = len(path)
                for i in range(length-1):
                    if path[i] == toObjs1[-1]:
                        if path[i + 1] == fromObj:
                            self.data.get(so)[2].remove(path)
                            for toObjs



    def deleteOwners0(self, toObj, fromObj):
        self.data.get(toObj)[1][1].remove(fromObj)

class ArrowNetworkDB(DBServer):
    def putAccessArrow(self, fromObj, byOwners, *toObj):
        self.checkObj(fromObj,toObj)
        if self.judgeYouOwners(fromObj, byOwners):
            if self.judgeAccess(fromObj, toObj):
                self.giveCites(fromObj, toObj)
                self.saveFile()

    def switchAccessArrow(self, fromObj, byOwners, toObjs1, toObjs2):
        self.checkObj(fromObj,toObjs1,toObjs2)
        if self.judgeYouOwners(fromObj, byOwners):
            self.deleteCites(fromObj, toObjs1)
            self.giveCites(fromObj, toObjs2)
            self.notificateCiteFrom(fromObj, toObjs1, toObjs2)
            self.saveFile()
                
    def changeData(self, obj, byOwners,data):
        self.checkObj(obj)
        if self.judgeYouOwners(obj, byOwners):
            self.changeData0(obj,data)
            self.saveFile()


    def addOwners(self, toObj, fromObj, byOwners):
        self.checkObj(fromObj,toObj)
        if self.judgeYouOwners(toObj, byOwners):
            self.addOwners0(toObj, fromObj)
            self.saveFile()
        else:
            return False

    
    def deleteOwner(self,toObj,fromObj,byOwners):
        self.checkObj(fromObj,toObj)
        if self.judgeYouOwners(fromObj,byOwners):
            self.deleteOwner0(toObj,fromObj)
            self.saveFile()

class RootOwner():
    iamtheOwner = {'8':'rootpasskey1234'}
    def __init__(self):
        self.andb = ArrowNetworkDB()
        
    def giveMeObj(self,toObj, fromObj, byOwners):
        self.andb.addOwners(toObj, fromObj, byOwners)
        self.andb.deleteOwner(toObj,'8',self.iamtheOwner)

class UserControl():
    def __init__(self,r):
        self.r = r
    def createObj(toObj,fromObj,byOwners):
        pass

r = RootOwner()
r.andb.putAccessArrow('10',r.iamtheOwner,'8')