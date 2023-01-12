from ast import literal_eval

class Step1():
    
    def __init__(self):
        self.getFile()

    def getFile(self, name = 'ANDBData'):
        with open(name,'r') as f:
            self.data = self.changeType(f.read(), 'd')

    def saveFile(self, name = 'ANDBData'):
        print(self.data, end = '\n\n')
        #with open('ANDBData','w') as f:
        #    f.write(self.changeData(self.data, 's'))
        pass

    def changeType(self, raw, toType):
        fromType = str(type(raw))

        match fromType:
            case "<class 'str'>":
                match toType:
                    case 'l':
                        data = [raw]
                    case 'se':
                        data = {raw,}
                    case 't':
                        data = (raw,)
                    case 'd':
                        data = eval(raw)
                    case 'f':
                        data = frozenset([raw])
                    case _:
                        data =raw
            case "<class 'list'>":
                match toType:
                    case 's':
                        data = str(raw)
                    case 'se':
                        data = set(raw)
                    case 't':
                        data = tuple(raw)
                    case 'l':
                        data = []
                        for element in raw:
                            data.append(self.changeType(element, 's'))
                    case 'f':
                        data = []
                        for element in raw:
                            data.append(self.changeType(element,'s'))
                        data = frozenset(data)
                    case _:
                        data = raw
            case "<class 'set'>":
                match toType:
                    case 's':
                        data = str(raw)
                    case 'f':
                        data = frozenset(raw)
                    case _:
                        data = raw
            case "<class 'dict_keys'>":
                match toType:
                    case 's':
                        data = str(raw)
                    case 'l':
                        data = list(raw)
                    case _:
                        data = raw
            case "<class 'dict'>":
                match toType:
                    case 's':
                        data = str(raw)
                    case 'd':
                        data = {}
                        for k,v in raw.items():
                            data[str(k)] = str(v)
                    case _:
                        data = raw
            case "<class 'int'>":
                raw = str(raw)
                match toType:
                    case 's':
                        data = raw
                    case 'l':
                        data = [raw]
                    case 'se':
                        data = set([raw])
                    case 'f':
                        data = frozenset([raw])
                    case _:
                        data = raw
            case _:
                data = raw
        return data

class Step2(Step1):

    def getObjs(self):
        return self.data.keys()
        
    def getData(self, obj):
        obj = self.changeType(obj, 's')
        return self.data.get(obj)[0]

    def getPasskey(self, obj):
        obj = self.changeType(obj, 's')
        return self.data.get(obj)[1][0]
    
    def getOwners(self, obj):
        obj = self.changeType(obj, 's')
        return self.data.get(obj)[1][1]
        
    def getBrotherObjs(self, obj):
        obj = self.changeType(obj, 's')
        return self.data.get(obj)[2]

    def getChildObjs(self, obj):
        obj = self.changeType(obj, 's')
        return self.data.get(obj)[3]

    def getParentClusters(self, obj):
        obj = self.changeType(obj, 's')
        return self.data.get(obj)[4]

    def addModel(self, obj):
        obj = self.changeType(obj, 's')
        self.data[obj] = [None, [None, set()], set(), {}, set()]

    def setData(self, obj, data):
        obj = self.changeType(obj,'s')
        data = self.changeType(data, 's')
        self.data.get(obj)[0] = data

    def setPasskey(self, obj, passkey):
        obj = self.changeType(obj, 's')
        passkey = self.changeType(passkey, 's')
        self.data.get(obj)[1][0] = passkey

    def addOwner(self, obj, addObj):
        obj = self.changeType(obj, 's')
        addObj = self.changeType(addObj,'s')
        self.data.get(obj)[1][1].add(addObj)

    def addBrotherObj(self, obj, addObj):
        obj = self.changeType(obj, 's')
        addObj = self.changeType(addObj, 's')
        self.data.get(obj)[2].add(addObj)

    def addChildObj(self, obj, cluster, addChildObj):
        obj = self.changeType(obj, 's')
        cluster = self.changeType(cluster,'f')
        addChildObj = self.changeType(addChildObj, 's')
        self.data.get(obj)[3][cluster].add(addChildObj)

    def addParentCluster(self, obj, addCluster):
        obj = self.changeType(obj, 's')
        addCluster = self.changeType(addCluster, 'f')
        self.data.get(obj)[4].add(addCluster)

    def deleteOwner(self, obj, deleteObj):
        obj = self.changeType(obj, 's')
        deleteObj = self.changeType(deleteObj, 's')
        self.data.get(obj)[1][1].discard(deleteObj)

    def deleteBrotherObj(self, obj, deleteObj):
        obj = self.changeType(obj, 's')
        deleteObj = self.changeType(deleteObj, 's')
        self.data.get(obj)[2].discard(deleteObj)

    def deleteChildObj(self, obj, cluster, deleteChildObj):
        obj = self.changeType(obj,'s')
        cluster = self.changeType(cluster, 'se')
        deleteChildObj = self.changeType(deleteChildObj, 's')
        childObjs = self.getChildObjs(obj).get(cluster)
        childObjs.discard(deleteChildObj)
        self.data.get(obj)[3][cluster].discard(deleteChildObj)

    def deleteParentCluster(self, obj, deleteCluster):
        obj = self.changeType(obj, 's')
        deleteCluster = self.changeType(deleteCluster, 'f')
        self.data.get(obj)[4].discard(deleteCluster)

class Step3(Step2):
    def judgeObjOwners(self, obj, owners):
        obj = self.changeType(obj, 's')
        owners = self.changeType(owners, 'd')
        
        def operatePasskeyOwner(obj, owners):
            return True if self.getPasskey(obj) == owners.get(obj) else False

        def allowPasskeyOwner(ownerNumber, ownerCount):
            if ownerNumber == 0:
                return True
            else:
                if ownerCount == 0:
                    ownerCount = 0.1
                return True if ownerNumber / ownerCount < 2 else False

        owners0 = self.getOwners(obj)
        ownerNumber = 0
        ownerCount = 0
        for o in owners0:
            ownerNumber += 1
            ownerCount += 1 if self.judgeObjOwners(o, owners) else 0
        if allowPasskeyOwner(ownerNumber, ownerCount):
            if operatePasskeyOwner(obj, owners):
                ownerCount += 1
        ownerNumber += 1
        if ownerCount == 0:
            ownerCount = 0.1
        return True if ownerNumber / ownerCount <= 2 else False

    def releaseObj(self, obj):
        obj = self.changeType(obj, 's')
        if obj not in self.getObjs():
            self.addModel(obj)
            self.addOwner(obj,'6')
            super().addParentCluster(obj, ['7'])
            self.addChildObj('7','7',obj)
        
class Step4(Step3):
    def setData(self, obj, data, owners):
        self.releaseObj(obj)
        if self.judgeObjOwners(obj, owners):
            super().setData(obj,data)
            self.saveFile()

    def setPasskey(self, obj, passkey, owners):
        self.releaseObj(obj)
        if self.judgeObjOwners(obj, owners):
            super().setPasskey(obj, passkey)
            self.saveFile()

    def addOwners(self,obj, addObjs, owners):
        addObjs = self.changeType(addObjs,'l')
        self.releaseObj(obj)
        if self.judgeObjOwners(obj, owners):
            for o in addObjs:
                self.releaseObj(o)
                super().addOwner(obj, o)
                self.saveFile()

    def addParentCluster(self, obj, addCluster, owners):
        self.releaseObj(obj)
        addCluster = self.changeType(addCluster,'se')
        for o in addCluster:
            self.releaseObj(o)
        if self.judgeObjOwners(obj, owners):
            super().addParentCluster(obj, addCluster)
            for o1 in addCluster:
                super().addChildObj(o1, addCluster, obj)
                for o2 in addCluster:
                    super().addBrotherObj(o1,o2)
                    self.saveFile()

    def deleteOwners(self, obj, deleteObjs, owners):
        self.releaseObj(obj)
        deleteObjs = self.changeType(deleteObjs, 'se')
        for o in deleteObjs:
            self.releaseObj(o)
            if self.judgeObjOwners(o, owners):
                super().deleteOwner(obj, o)
                self.saveFile()

    def deleteParentCluster(self, obj, deleteCluster, owners):
        self.releaseObj(obj)
        deleteCluster = self.changeType(deleteCluster,'se')
        for o in deleteCluster:
            self.releaseObj(o)
        if self.judgeObjOwners(obj, owners):
            super().deleteParentCluster(obj, deleteCluster)
            for o1 in deleteCluster:
                super().deleteChildObj(o1, deleteCluster, obj)
                for o2 in deleteCluster:
                    super().deleteBrotherObj(o1,o2)
                    self.saveFile()

class Step5(Step4):
    rootOwner = {'6':'rootpasskey1234'}
    owners = {}
    def login(self, userId, passkey):
        self.owners[userId] = passkey
        super().setPasskey(userId, passkey, self.rootOwner)
        super().deleteOwners(userId, 6, self.rootOwner)

    def logout(self, userId, passkey):
        if self.judgeObjOwners(userId, {userId:passkey}):
            del self.owners[userId]

    def changePasskey(self, userId, newPasskey):
        super().setPasskey(userId, newPasskey, self.owners)

    def createFile(self, fileId, data, cluster = {'7',}):
        super().addOwners(fileId, self.owners.keys(),self.rootOwner)
        super().deleteOwners(fileId, 6, self.rootOwner)
        super().addOwners(fileId, self.owners.keys(), self.rootOwner)
        super().setData(fileId, data, self.owners)
        super().addParentCluster(fileId, cluster, self.owners)
        
    def changeData(self, fileId, data):
        super().setData(fileId, data, self.owners)

    def addOwners(self, id,addId):
        super().addOwners(id, addId, self.owners)

    def deleteOwners(self, id):
        super().addOwners(id, 6,self.owners)
        super().deleteOwners(id, self.owners.keys(),self.owners)

    def addCluster(self, id, addCluster):
        super().addParentCluster(id, addCluster, self.owners)

    def deleteCluster(self, id, deleteCluster):
        super().deleteParentCluster(id, deleteCluster, self.owners)