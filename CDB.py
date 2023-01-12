from ast import literal_eval
from copy import copy
from math import log2

class Step1():
    
    def __init__(self):
        self.getFile()

    def getFile(self, name = 'CDBData'):
        with open(name,'r') as f:
            self.data = self.changeType(f.read(), 'd')

    def saveFile(self, name = 'CDBData'):
        for k,v in self.data.items():
            print(str(k) + ': ' + str(v))
            pass
        print('')
        with open(name,'w') as f:
            data = self.changeType(self.data,'s')
            f.write(data)
        pass

    def changeType(self, raw, toType):
        fromType = str(type(raw))
        match fromType:
            case "<class 'str'>":
                match toType:
                    case 'i':
                        data = int(raw)
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
                        data = self.changeType(raw,'s')
                    case 'se':
                        data = set()
                        for element in raw:
                            data.add(self.changeType(element, 's'))
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
                        print('HI2')
                        if len(raw) == 1:
                            data = str(next(iter(raw)))
                        data = str(raw)
                    case 'l':
                        data = list(raw)
                    case 'f':
                        data = set()
                        for element in raw:
                            data.add(self.changeType(element, 's'))
                        data = frozenset(data)
                    case 'se':
                        data = set()
                        for element in raw:
                            data.add(self.changeType(element, 's'))
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
        print(obj)
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
        self.saveFile()

    def setData(self, obj, data):
        obj = self.changeType(obj,'s')
        data = self.changeType(data, 's')
        self.data.get(obj)[0] = data
        self.saveFile()

    def setPasskey(self, obj, passkey):
        obj = self.changeType(obj, 's')
        passkey = self.changeType(passkey, 's')
        self.data.get(obj)[1][0] = passkey
        self.saveFile()

    def addOwner(self, obj, addObj):
        obj = self.changeType(obj, 's')
        addObj = self.changeType(addObj,'s')
        self.data.get(obj)[1][1].add(addObj)
        self.saveFile()

    def addBrotherObj(self, obj, addObj):
        obj = self.changeType(obj, 's')
        addObj = self.changeType(addObj, 's')
        self.data.get(obj)[2].add(addObj)
        self.saveFile()

    def addChildObj(self, obj, cluster, addChildObj):
        obj = self.changeType(obj, 's')
        cluster = self.changeType(cluster,'f')
        addChildObj = self.changeType(addChildObj, 's')
        if cluster in self.getChildObjs(obj).keys():
            self.data.get(obj)[3][cluster].add(addChildObj)
        else:
            self.data.get(obj)[3][cluster] = self.changeType(addChildObj, 'se')
        self.saveFile()

    def addParentCluster(self, obj, addCluster):
        obj = self.changeType(obj, 's')
        addCluster = self.changeType(addCluster, 'f')
        self.data.get(obj)[4].add(addCluster)
        self.saveFile()

    def deleteOwner(self, obj, deleteObj):
        obj = self.changeType(obj, 's')
        deleteObj = self.changeType(deleteObj, 's')
        self.data.get(obj)[1][1].discard(deleteObj)
        self.saveFile()

    def deleteBrotherObj(self, obj, deleteObj):
        obj = self.changeType(obj, 's')
        deleteObj = self.changeType(deleteObj, 's')
        self.data.get(obj)[2].discard(deleteObj)
        self.saveFile()

    def deleteChildObj(self, obj, cluster, deleteChildObj):
        obj = self.changeType(obj,'s')
        cluster = self.changeType(cluster, 'f')
        deleteChildObj = self.changeType(deleteChildObj, 's')
        childObjs = self.getChildObjs(obj).get(cluster)
        childObjs.discard(deleteChildObj)
        self.data.get(obj)[3][cluster].discard(deleteChildObj)
        self.saveFile()

    def deleteParentCluster(self, obj, deleteCluster):
        obj = self.changeType(obj, 's')
        deleteCluster = self.changeType(deleteCluster, 'f')
        self.data.get(obj)[4].discard(deleteCluster)
        self.saveFile()

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

    def searchObj(self, obj, cluster):
        obj = self.changeType(obj, 's')
        cluster = self.changeType(cluster, 'l')
        childObjs = self.getChildObjs(obj).get(cluster)
        return childObjs

        
class Step4(Step3):
    def setData(self, obj, data, owners):
        if self.judgeObjOwners(obj, owners):
            super().setData(obj,data)

    def setPasskey(self, obj, passkey, owners):
        if self.judgeObjOwners(obj, owners):
            super().setPasskey(obj, passkey)

    def addOwners(self,obj, addObjs, owners):
        addObjs = self.changeType(addObjs,'l')
        if self.judgeObjOwners(obj, owners):
            for o in addObjs:
                self.releaseObj(o)
                super().addOwner(obj, o)

    def addParentCluster(self, obj, addCluster, owners):
        addCluster = self.changeType(addCluster,'se')
        addCluster.add(obj)
        addCluster = self.changeType(addCluster,'l')
        initCluster = copy(addCluster)
        for i in range(len(addCluster)):
            obj = addCluster.pop(i)
            if self.judgeObjOwners(obj,owners):
                super().addParentCluster(obj, addCluster)
                for o1 in addCluster:
                    super().addChildObj(o1, addCluster, obj)
                    for o2 in addCluster:
                        super().addBrotherObj(o1, o2)
            addCluster = copy(initCluster)

    def deleteOwners(self, obj, deleteObjs, owners):
        deleteObjs = self.changeType(deleteObjs, 'se')
        for o in deleteObjs:
            self.releaseObj(o)
            if self.judgeObjOwners(o, owners):
                super().deleteOwner(obj, o)

    def deleteParentCluster(self, obj, deleteCluster, owners):
        deleteCluster = self.changeType(deleteCluster,'se')
        deleteCluster.add(obj)
        deleteCluster = self.changeType(deleteCluster, 'l')
        initCluster = copy(deleteCluster)
        for i in range(len(deleteCluster)):
            obj = deleteCluster.pop(i)
            if self.judgeObjOwners(obj, owners):
                super().deleteParentCluster(obj, deleteCluster)
                for o1 in deleteCluster:
                    super().deleteChildObj(o1, deleteCluster, obj)
                    for o2 in deleteCluster:
                        super().deleteBrotherObj(o1,o2)
            deleteCluster = copy(initCluster)

    def releaseObj(self, obj):
        allObjs = self.getObjs()
        obj = self.changeType(obj, 's')
        if obj not in allObjs:
            titleObj = self.changeType(obj, 'i') + 1
            while True:
                if self.changeType(titleObj, 's') in allObjs:
                    titleObj += 1
                else:
                    if log2(titleObj) % 1 == 0:
                        titleObj += 1
                    else:
                        if self.changeType(titleObj, 's') in allObjs:
                            titleObj += 1
                        else:
                            titleObj = self.changeType(titleObj,'s')
                            break
            self.addModel(obj)
            self.addModel(titleObj)
            self.addParentCluster(obj, {titleObj, '18'}, {'12':'rootpasskey1234'})
            self.addParentCluster(obj, [titleObj],{'12':'rootpasskey1234'})
            return titleObj, True
        else: 
            return 0, False
        

class Step5(Step4):
    rootOwner = {'12':'rootpasskey1234'}
    owners = {}
    def login(self, userId, passkey):
        self.owners[userId] = passkey
        super().releaseObj(userId)
        super().setPasskey(userId, passkey, self.rootOwner)
        super().deleteOwners(userId, 12, self.rootOwner)

    def logout(self, userId, passkey):
        super().releaseObj(userId)
        if self.judgeObjOwners(userId, {userId:passkey}):
            del self.owners[userId]

    def changePasskey(self, userId, newPasskey):
        super().releaseObj(userId)
        super().setPasskey(userId, newPasskey, self.owners)

    def createFile(self, fileId, data, cluster = {'14',}):
        
        if log2(fileId) % 1 == 0:
            data = fileId
        
        
        titleId, nothing = super().releaseObj(fileId)
        for obj in cluster:
            super().releaseObj(obj)
        if nothing:
            super().addOwners(fileId, self.owners.keys(),self.rootOwner)
            super().addOwners(titleId, self.owners.keys(), self.rootOwner)
            super().deleteOwners(fileId, 12, self.rootOwner)
            super().addOwners(fileId, self.owners.keys(), self.rootOwner)
            super().addParentCluster(fileId, cluster, self.owners|self.rootOwner)
            super().addParentCluster(fileId, cluster, self.owners|self.rootOwner)
            super().addParentCluster(titleId, {'14',}, self.owners|self.rootOwner)
            super().setData(titleId, data, self.owners)
        
        
    def changeData(self, fileId, data):
        super().releaseObj(fileId)
        super().setData(fileId, data, self.owners)

    def addOwners(self, id,addId):
        super().addOwners(id, addId, self.owners)

    def deleteOwners(self, id):
        super().addOwners(id, 12,self.owners)
        super().deleteOwners(id, self.owners.keys(),self.owners)

    def addCluster(self, id, addCluster):
        super().addParentCluster(id, addCluster, self.owners)
        for obj in addCluster:
            super().addParentCluster(obj, id, self.owners|self.rootOwner)

    def deleteCluster(self, id, deleteCluster):
        super().deleteParentCluster(id, deleteCluster, self.owners)

    def searchObj(self, rootObj = '12'):
        c = CUIComponent(self,rootObj)
        c.showComponent()


class CUIComponent:

    cluster = set()
    selectedCluster = set()

    def __init__(self, s, obj):
        self.a = s
        self.selectedCluster.add(obj)

    def showComponent(self):
        visualCluster = {}
        visualSelectedCluster = {}
        for obj1 in self.selectedCluster:
            self.cluster = self.searchChildObj(obj1)
            for obj2 in self.cluster:
                print('HI')
                print(type(self.getObjWith(obj2,'18')))
                visualCluster[obj] = self.a.getData(self.getObjWith(obj2,'18'))
        for obj in self.cluster:
            visualCluster[obj] = self.a.getData(self.getObjWith(obj, '18'))
        print('Cluster:' + visualCluster)
        print('Selected Cluster:' + visualSelectedCluster)

    def addSelectedObj(self, obj):
        self.selectedCluster.add(obj)

    def deleteSelectedObj(self, obj):
        self.selectedCluster.remove(obj)
    
    def clearSelectedObj(self):
        self.selectedCluster = set()

    def getObjWith(self, obj, withObj):
        obj = self.a.changeType(obj, 's')
        withObj = self.a.changeType(withObj, 's')
        return self.searchChildObj(frozenset({obj, withObj}))

    def searchChildObj(self, parentCluster = frozenset({'12',})):
        parentCluster = self.a.changeType(parentCluster, 'f')
        cluster = set()
        for obj in parentCluster:
            childObjs = self.a.getChildObjs(obj)
            for k, v in childObjs.items():
                if k >= parentCluster:
                    cluster |= v
        return cluster
    