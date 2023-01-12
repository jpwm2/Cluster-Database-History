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

    def changeType(self, raw, toType):
        raw = literal_eval(raw)
        fromType = type(raw)

        match fromType:
            case "<class 'str'>":
                match toType:
                    case 'l':
                        data = [raw]
                    case 'se':
                        data = {raw,}
                    case 't':
                        data = (raw,)
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
                    case _:
                        data = raw
            case _:
                data = raw
        return data

    def getObjs(self):
        return self.data.keys()
        
    def getData(self, obj):
        return self.data.get(obj)[0]

    def getPasskey(self, obj):
        return self.data.get(obj)[1][0]
    
    def getOwners(self, obj):
        return self.data.get(obj)[1][1]

    def getRootObjs(self, obj):
        return self.data.get(obj)[2]

    def getChainsAccess(self, obj):
        return self.data.get(obj)[3]

    def getObjsAccess(self, obj):
        return self.data.get(obj)[5]
    
class Step2(Step1):

    def addModel(self, obj):
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
        addObj = self.changeType(addObj, 's')
        self.data.get(obj)[1][1].add(addObj)

    def addRootObj(self, obj, addObj):
        obj = self.changeType(obj, 's')
        addObj = self.changeType(addObj, 's')
        self.data.get(obj)[2].add(addObj)

    def addChainAccess(self, obj, addPath, addEndObj):
        obj = self.changeType(obj, 's')
        addPath = self.changeType(addPath, 'se')
        addEndObj = self.changeType(addEndObj,'s')
        pathSet = self.getObjsAccess(obj).values()
        endObjs = [k for k, v in pathSet.items() if v == addPath]
        if addEndObj not in endObjs:
            newEndObjs = frozenset(self.changeType(endObjs,'se').add(addEndObj))
            self.data.get(obj)[3].add({newEndObjs:addPath})
            del self.data.get(obj)[3][endObjs]

    def addObjAccess(self, obj, addObj):
        obj = self.changeType(obj,'s')
        addObj = self.changeType(addObj,'s')
        self.data.get(obj)[4].add(addObj)

    def deleteOwner(self,obj,deleteObj):
        obj = self.changeType(obj, 's')
        deleteObj = self.changeType(deleteObj, 's')
        self.data.get(obj)[1][1].remove(deleteObj)

    def deleteRootObj(self, obj, deleteObj):
        obj = self.changeType(obj,'s')
        deleteObj = self.changeType(deleteObj, 's')
        self.data.get(obj)[2].remove(deleteObj)

    def deleteChainAccess(self, obj, deletePath, deleteEndObj):
        obj = self.changeType(obj, 's')
        addPath = self.changeType(addPath, 'se')
        addEndObj = self.changeType(addEndObj,'s')
        pathSet = self.getObjsAccess(obj).values()
        endObjs = [k for k, v in pathSet.items() if v == addPath]
        if addEndObj in endObjs:
            newEndObjs = frozenset(self.changeType(endObjs,'se').remove(addEndObj))
            self.data.get(obj)[3].add({newEndObjs:addPath})
            del self.data.get(obj)[3][endObjs]

    def deleteObjAccess(self, obj, deleteObj):
        obj = self.changeType(obj, 's')
        deleteObj = self.changeType(deleteObj,'s')
        self.data.get(obj)[5].remove(deleteObj)

class Step3(Step2):
    def judgeObjOwners(self, obj, owners):
        obj = self.changeType(obj, 's')
        owners = self.changeType(owners,'d')

        def operatePasskeyOwner(obj,owners):
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
            ownerCount += 1 if self.judgeYouOwners(o,owners) else 0
        if allowPasskeyOwner(ownerNumber,ownerCount):
            if operatePasskeyOwner(obj,owners):
                ownerCount += 1
        ownerNumber += 1
        if ownerCount == 0:
            ownerCount = 0.1
        return True if ownerNumber / ownerCount <= 2 else False
        
    def releaseObj(self, obj):
        obj = self.changeType(obj,'s')
        if obj not in self.getObjs():
            self.addModel(obj)
            self.addOwner(obj, '8')
            self.addRootObj(obj, '9')
            self.addObjAccess(obj, '8')
            self.addObjAccess(obj, '9')

class Step4(Step3):
    def judgeChainOwners(self, chain, owners):
        for obj in chain:
            if not self.judgeObjOwners(obj, owners):
                return False
        return True

class Step5(Step4):

    def setData(self, obj, data, owners):
        self.releaseObj(obj)
        if self.judgeObjOwners(obj, owners):
            super().setData(obj, data)

    def setPasskey(self, obj, passkey, owners):
        self.releaseObj(obj)
        if self.judgeObjOwners(obj, owners):
            super().setPasskey(obj, passkey)

    def addAccesses(self, chain, owners):
        self.changeType(chain,'l')
        if self.judgeChainOwners(chain, owners):
            super().addChainAccess(chain[0], chain[1:-1], chain[-1])
