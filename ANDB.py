from sympy import isprime

class DBServerBasic:
    data = {}
    def __init__(self):
        def getFile():
            with open('ANDBData','r') as f:
                self.data = eval(f.read())
        
        getFile()


    def saveFile(self):
        print(self.data,end='\n\n')
        #with open('ANDBData','w') as f:
        #    f.write(str(self.data))
        pass
        
class DBServer(DBServerBasic):

    def checkObj(self, obj):
        for o in obj:
            if o not in self.data.keys():
                self.data[o] = [None,[None,['8']],[],[]]
                self.addAccessTo0(o,['8','9'])
                self.addAccessFrom0('8',o)
                self.addAccessFrom0('9',o)
                return False
            else:
                return True

    def judgeYouOwners(self, obj, owners):
        def operatePasskeyOwner(obj,owners):
            return True if self.data.get(obj)[1][0] == owners.get(obj) else False
        def allowPasskeyOwner(ownerNumber, ownerCount):
            if ownerNumber == 0:
                return True
            else:
                if ownerCount == 0:
                    ownerCount = 0.1
                return True if ownerNumber / ownerCount < 2 else False
        if self.checkObj({obj}):
            owners0 = self.data.get(obj)[1][1]
            ownerNumber = 0
            ownerCount = 0
            for o in owners0:
                ownerNumber += 1
                ownerCount += 1 if self.judgeYouOwners(o,owners) else 0
            if allowPasskeyOwner(ownerNumber,ownerCount):
                if operatePasskeyOwner(obj,owners):
                    ownerCount += 1
            ownerNumber += 1
            if ownerCount == 0:
                ownerCount = 0.1
            return True if ownerNumber / ownerCount <= 2 else False
        else:
            return False
            

    def judgeAccess(self, fromObj, toObj, objs = None):
        newSearchObjNum = len(self.data.get(fromObj)[2] - objs)
        if newSearchObjNum == 0:
            return False
        for path in self.data.get(fromObj)[2]:
            objs = objs | set(path)
        objs = objs & set(self.data.get(toObj)[3])
        if toObj in objs:
            return True
        else:
            for o in objs:
                if self.judgeAccess(o, toObj, objs):
                    return True
            return False

    def addAccessTo0(self, obj, addObjPath):
        objPathes = self.data.get(obj)[2]
        if addObjPath not in objPathes:
            self.data.get(obj)[2].append(addObjPath)

    def addAccessFrom0(self, obj, addObj):
        print(obj)
        print(addObj)
        print(type(self.data.get(obj)))
        if addObj not in self.data.get(obj)[3]:
            self.data.get(obj)[3].append(addObj)

    def deleteAccessTo0(self, obj, deleteObjPath):
        self.data.get(obj)[2].remove(deleteObjPath)

    def deleteAccessFrom0(self, obj, deleteObj):
        self.data.get(obj)[3].remove(deleteObj)


    def addOwners0(self, obj, addObj):
        if addObj not in self.data.get(obj)[1][1]:
            self.data.get(obj)[1][1].append(addObj)
            return True
        else:
            return False

            
    def deleteOwner0(self, obj, deleteObj):
        self.data.get(obj)[1][1].remove(deleteObj)

    def switchObjPasskey0(self, obj, newPasskey):
        self.data.get(obj)[1][0] = newPasskey

    def switchData0(self, obj, data):
        data = str(data)
        self.data.get(obj)[0] = data


class ArrowNetworkDB(DBServer):
    def addAccessTo(self, owners, obj, addObjPath):
        self.checkObj(set([obj] + addObjPath))

        if self.judgeYouOwners(obj, owners):
            self.addAccessTo0(obj,addObjPath)
        self.saveFile()

    def addAccessFrom(self, owners, objs, addObj):
        self.checkObj(set(list(objs) + [addObj]))
        for o in objs:
            if self.judgeYouOwners(o,owners):
                self.addAccessFrom0(o,addObj)
        self.saveFile()
            
    def deleteAccessTo(self, owners, obj, deleteObjPath):
        self.checkObj(set([obj] + deleteObjPath))
        if self.judgeYouOwners(obj, owners):
            self.deleteAccessTo0(obj,deleteObjPath)
        self.saveFile()

    def deleteAccessFrom(self, owners, objs, deleteObj):
        self.checkObj(set(objs + [deleteObj]))
        for o in objs:
            if self.judgeYouOwners(o,owners):
                self.deleteAccessFrom0(o,deleteObj)
        self.saveFile()

    def addOwners(self, owners, obj, addObj):
        self.checkObj({obj,addObj})
        if self.judgeYouOwners(obj, owners):
            self.addOwners0(obj,addObj)
        self.saveFile()

    def deleteOwner(self, owners, obj, deleteObj):
        self.checkObj({obj, deleteObj})
        if self.judgeYouOwners(deleteObj, owners):
            self.deleteOwner0(obj, deleteObj)   
        self.saveFile()

    def switchObjPasskey(self, owners, obj, newPasskey):
        self.checkObj({obj})
        if self.judgeYouOwners(obj, owners):
            self.switchObjPasskey0(obj, newPasskey)
        self.saveFile()


    def switchData(self, owners, obj, data):
        self.checkObj({obj})
        if self.judgeYouOwners(obj, owners):
            self.switchData0(obj, data)
        self.saveFile()

class RootTask(ArrowNetworkDB):
    iamRootOwner = {'8':'rootpasskey1234'}
    def putData(self,obj,data,*objPathes):
        obj = str(obj)
        data = str(data)
        objs = set()
        for op in objPathes:
            self.addAccessTo(self.iamRootOwner, obj, op)
            objs = objs | set(op)
        self.addAccessFrom(self.iamRootOwner,list(objs),obj)
        self.switchData(self.iamRootOwner, obj, data)

    def giveMeObj(self,obj1, objOrKey1, objOrKey2):
        if objOrKey1:
            self.switchObjPasskey(self.iamRootOwner, obj1, objOrKey2)
        else:
            self.addOwners(self.iamRootOwner, obj1, objOrKey2)
        self.deleteOwner(self.iamRootOwner,obj1, '8')

    def notificateMeAccessObj(self, objs, addObj):
        self.addAccessFrom(self.iamRootOwner, objs, addObj)

class User(ArrowNetworkDB):
    def __init__(self, r):
        self.r = r

    def createYou(self, obj, newObjPasskey):
        r.giveMeObj(obj, True, newObjPasskey)

    def putData(self, data, obj, objPathes, ownerObj, owners):
        obj = str(obj)
        ownerObj = str(ownerObj)
        data = str(data)
        self.r.giveMeObj(obj, False, ownerObj)
        objs = set()
        for op in objPathes:
            self.addAccessTo(owners, obj, op)
            objs = objs | set(op)
        self.r.notificateMeAccessObj(objs, obj)
        self.switchData(owners, obj, data)


r = RootTask()
me = {'12':'passkey0987'}
u = User(r)
u.createYou('12', me.get('12'))
u.putData("I don't wanna be afraid to fail", 13, [['8','9']], 12, me)