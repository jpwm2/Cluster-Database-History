from ast import literal_eval
import os

class DBServerBasic:
    """

    サーバーへのアクセスする機能、またはPythonの機能のメソッドをを有するクラス

    """
    data = {}
    def __init__(self):
        def getFile(num=0, data = {}):
            match num:
                case 0:
                    with open('ANDBData','r') as f:
                        self.data = self.changeType(f.read(),'d')
                case 1:
                    pass
        getFile()


    def saveFile(self,num = 0,data1 = None,data2=None):
        print(self.data,end='\n\n')
        match num:
            case 0:
                #with open('ANDBData','w') as f:
                #    f.write(self.changeData(self.data,'s'))
                pass
            case 1:
                os.mkdir(data1)
                pass
            case 2:
                with open(data1,'w') as f:
                    f.write(data2)

    def changeType(self,data, toType = 's'):
        match toType:
            case 's':
                data = str(data)
            case 'l':
                if str(type(data)) == "<class 'dict_keys'>":
                    data = list(data)
                data = str(data)
                data = literal_eval(data)
                match str(type(data)):
                    case "<class 'int'>":
                        data = [data]
                    case _:
                        data = list(data)
                tempData = data
                for i in range(len(tempData)):
                    data[i] = str(tempData[i])
            case 'd':
                data = str(data)
                evalData = literal_eval(data)
                tempData = dict(evalData)
                data = {}
                for k in tempData.keys():
                    if str(type(tempData.get(k))) == "<class 'int'>":
                        data[str(k)] = str(tempData.get(k))
                    else:
                        data[str(k)] = tempData.get(k)
            case 'se':
                data = str(data)
                data = literal_eval(data)
                data = set(data)
            case 't':
                data = str(data)
                data = literal_eval(data)
                data = tuple(data)
            case 'i':
                data = int(data)
            case _:
                pass
        return data

    def getKeys(self):
        return self.data.keys()

    def getData(self,obj):
        return self.data.get(obj)[0]

    def getPasskey(self, obj):
        return self.data.get(obj)[1][0]

    def getOwners(self, obj):
        return self.data.get(obj)[1][1]

    def getObjsAccessTo(self, obj):
        return self.data.get(obj)[2]

    def getChainsAccessTo(self, obj):
        return self.data.get(obj)[3]

    def getObjsAccessFrom(self,obj):
        return self.data.get(obj)[4]

    def getChainsAccessFrom(self, obj):
        return self.data.get(obj)[5]

    def addModel(self,obj):
        self.data[obj] = [None,[None,set()],set(),set(),set(),set()]

    def setData(self,obj, data):
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

    def addObjAccessTo(self, obj, addObj):
        obj = self.changeType(obj, 's')
        addObj = self.changeType(addObj, 's')
        self.data.get(obj)[2].add(addObj)

    def addChainAccessTo(self, obj, addPath):
        obj = self.changeType(obj, 's')
        addPath = self.changeType(addPath, 't')
        self.data.get(obj)[3].add(addPath)

    def addObjAccessFrom(self, obj, addObj):
        obj = self.changeType(obj, 's')
        addObj = self.changeType(addObj, 's')
        self.data.get(obj)[4].add(addObj)

    def addChainAccessFrom(self, obj, addPath):
        obj = self.changeType(obj, 's')
        addPath = self.changeType(addPath, 't')
        self.data.get(obj)[5].add(addPath)

    def deleteOwner(self,obj,deleteObj):
        obj = self.changeType(obj, 's')
        deleteObj = self.changeType(deleteObj, 's')
        self.data.get(obj)[1][1].remove(deleteObj)
    
    def deleteObjAccessTo(self, obj, deleteObj):
        obj = self.changeType(obj, 's')
        deleteObj = self.changeType(deleteObj, 's')
        self.data.get(obj)[2].remove(deleteObj)

    def deleteChainAccessTo(self, obj, deletePath):
        obj = self.changeType(obj, 's')
        deletePath = self.changeType(deletePath, 't')
        self.data.get(obj)[3].remove(deletePath)

    def deleteObjAccessFrom(self, obj, deleteObj):
        obj = self.changeType(obj, 's')
        deleteObj = self.changeType(deleteObj, 's')
        self.data.get(obj)[4].remove(deleteObj)

    def deleteChainAccessFrom(self, obj, deletePath):
        obj = self.changeType(obj, 's')
        deletePath = self.changeType(deletePath, 't')
        self.data.get(obj)[5].remove(deletePath)



class DBServer(DBServerBasic):
    """

    サーバーの基本的な機能のメソッドを有するクラス

    """

    def setPasskey(self,obj, passkey):
        obj = self.changeType(obj, 's')
        passkey = self.changeType(passkey, 's')
        super().setPasskey(obj, passkey)
        self.saveFile()

    def addOwner(self, obj, addObj):
        obj = self.changeType(obj, 's')
        addObj = self.changeType(addObj, 's')
        super().addOwner(obj, addObj)
        self.saveFile()

    def deleteOwner(self,obj, deleteObj):
        obj = self.changeType(obj, 's')
        deleteObj = self.changeType(deleteObj, 's')
        if deleteObj in super().getOwners(obj):
            super().deleteOwner(obj, deleteObj)
            self.saveFile()

    def setData(self, obj, data):
        obj = self.changeType(obj, 's')
        data = self.changeType(data, 's')
        super().setData(obj, data)
        self.saveFile()

    def addChainAccessTo(self,objIndexInPath, addPath):
        objIndexInPath = self.changeType(objIndexInPath, 'i')
        addPath = self.changeType(addPath, 't')
        leftChain = []
        for iLeft in range(objIndexInPath):
            leftChain.append(addPath[iLeft])
        super().addChainAccessTo(addPath[objIndexInPath], leftChain)
        for obj in leftChain:
            self.addObjAccessTo(addPath[objIndexInPath],obj)
        self.saveFile()
                    
    def addChainAccessFrom(self,objIndexInPath, addPath):
        objIndexInPath = self.changeType(objIndexInPath, 'i')
        addPath = self.changeType(addPath, 't')
        rightChain = []
        for iRight in range(objIndexInPath,len(addPath)):
            rightChain.append(addPath[iRight])
        super().addChainAccessFrom(addPath[objIndexInPath], rightChain)
        for obj in rightChain:
            self.addObjAccessFrom(addPath[objIndexInPath],obj)
        self.saveFile()

    def deleteChainAccessTo(self, objIndexInPath, deletePath):
        objIndexInPath = self.changeType(objIndexInPath,'i')
        deletePath = self.changeType(deletePath,'t')
        leftChain = []
        for iLeft in range(objIndexInPath):
            leftChain.append(deletePath[iLeft])
        if self.changeType(self.changeType(leftChain,'t')) in self.changeType(self.getChainAccessTo(deletePath[objIndexInPath]),'l'):
            super().deleteChainAccessTo(deletePath[objIndexInPath],leftChain)
        for obj in deletePath:
            if obj in self.getObjsAccessTo(deletePath[objIndexInPath]):
                self.deleteObjAccessTo(deletePath[objIndexInPath],obj)
        self.saveFile()

    def deleteChainAccessFrom(self, objIndexInPath, deletePath):
        objIndexInPath = self.changeType(objIndexInPath,'i')
        deletePath = self.changeType(deletePath,'t')
        rightChain = []
        for iRight in range(objIndexInPath, len(deletePath)):
            rightChain.append(deletePath[iRight])
        if self.changeType(self.changeType(rightChain, 't')) in self.changeType(self.getChainAccessFrom(deletePath[objIndexInPath]),'l'):
            super().deleteChainAccessFrom(deletePath[objIndexInPath],rightChain)
        for obj in deletePath:
            if obj in self.getObjsAccessFrom(deletePath[objIndexInPath]):
                self.deleteObjAccessFrom(deletePath[objIndexInPath],obj)
        self.saveFile()


    def checkObj(self, obj):
        """

        オブジェクトがデータベースに存在するかどうか調べデータベースに無い場合はRootをオーナとして追加する
        
        parameters
        ----------
        obj : string
            対称のオブジェ
        
        """
        obj = self.changeType(obj,'s')
        if obj not in self.getKeys():
            self.addModel(obj)
            self.addOwner(obj, '8')
            self.addChainAccessTo(2,['8','9',obj])
            self.addChainAccessTo(1,['8','9',obj])
            self.addChainAccessFrom(2,['8','9',obj])
            self.addChainAccessFrom(1,['8','9',obj])
            self.addChainAccessFrom(0,['8','9',obj])
            self.saveFile()

    def judgeYouOwners(self, obj, owners):
        """
        
        オブジェのオーナがメソッド実行者かどうか調べる
        
        
        parameters
        ----------
        obj : string
            対象のオブジェ
        owners : list
            オブジェのオーナ
            
        """
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
        self.checkObj(obj)
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

        
            

    def judgeAccess(self, fromObj, toObj, searchedObjs = set()):
        """
        
        オブジェからオブジェにアクセスできるかどうか調べる
        
        
        parameters
        ----------
        fromObj : string
            アクセス元オブジェ
        toObj : string
            アクセス先オブジェ
        searchedOjs : set
            走査済みオブジェ
            
        """
        fromObj = self.changeType(fromObj,'s')
        toObj = self.changeType(toObj,'s')
        newSearchObjs = self.getObjsAccessTo(fromObj)
        newSearchObjs |= self.getObjsAccessFrom(fromObj)
        newSearchObjs -= searchedObjs
        if toObj in newSearchObjs:
            return True
        else:
            searchedObjs |= newSearchObjs
            for o in self.changeType(newSearchObjs,'l'):
                if self.judgeAccess(o, toObj, searchedObjs):
                    return True
            return False


class ArrowNetworkDB():
    def __init__(self):
        self.d = DBServer()

    def addChainsAccessTo(self,path,owners):
        
        for iCenter in range(1, len(path)):
            self.d.checkObj(path[iCenter])
            if self.d.judgeYouOwners(path[iCenter],owners):
                self.d.addChainAccessTo(iCenter,path)

    def addChainsAccessFrom(self,path, owners):
        for iCenter in range(len(path)):
            self.d.checkObj(path[iCenter])
            if self.d.judgeYouOwners(path[iCenter], owners):
                self.d.addChainAccessFrom(iCenter, path)

    def deleteChainsAccessTo(self, path, owners):
        for iCenter in range(1, len(path)):
            self.d.checkObj(path[iCenter])
            if self.d.judgeYouOwners(path[iCenter],owners):
                self.d.deleteChainAccessTo(iCenter, path)
                self.d.deleteChainAccessFrom(iCenter,path)

    def deleteChainsAccessFrom(self, path, owners):
        for iCenter in range(len(path)):
            self.d.checkObj(path[iCenter])
            if self.d.judgeYouOwners(path[iCenter],owners):
                self.d.deleteChainAccessTo(iCenter, path)

    def addOwners(self, obj, addObjs, owners):
        addObjs = self.d.changeType(addObjs,'l')
        self.d.checkObj(obj)
        for o in addObjs:
            self.d.checkObj(o)
            if self.d.judgeYouOwners(obj, owners):
                self.d.addOwner(obj, o)

    def deleteOwners(self, obj, deleteObjs, owners):
        deleteObjs = self.d.changeType(deleteObjs,'l')
        self.d.checkObj(obj)
        for o in deleteObjs:
            self.d.checkObj(o)
            if o in self.d.getKeys():
                if self.d.judgeYouOwners(o, owners):
                    self.d.deleteOwner(obj, o)

    def setPasskey(self, obj, newPasskey, owners):
        obj = self.d.changeType(obj, 's')
        newPasskey = self.d.changeType(newPasskey, 's')
        owners = self.d.changeType(owners,'d')
        self.d.checkObj(obj)
        if self.d.judgeYouOwners(obj, owners):
            self.d.setPasskey(obj, newPasskey)


    def setData(self,obj, data, owners):
        self.d.checkObj(obj)
        if self.d.judgeYouOwners(obj, owners):
            self.d.setData(obj, data)


class User(ArrowNetworkDB):
    rootOwner = {'8':'rootpasskey1234'}
    owners = {}


    def login(self,userId,passkey):
        self.owners[userId] = passkey
        self.setPasskey(userId,passkey,self.rootOwner)
        super().deleteOwners(userId,8,self.rootOwner)

    def changePasskey(self, userId, newPasskey):
        self.setPasskey(userId,newPasskey,self.owners)


    def logout(self, userId, passkey):
        if self.d.judgeYouOwners(userId,{self.d.changeType(userId,'s'):self.d.changeType(passkey,'s')}):
            del self.owners[userId]

    def createFile(self,fileId, data, accessPath = []):
        super().addOwners(fileId, self.owners.keys(),self.rootOwner)
        super().deleteOwners(fileId,8,self.rootOwner)
        super().addOwners(fileId, self.owners.keys(),self.rootOwner)
        super().setData(fileId, data, self.owners)
        super().addChainsAccessTo(accessPath,self.owners)
        super().addChainsAccessFrom(accessPath,self.owners)

    def changeData(self, fileId, data):
        super().setData(fileId, data, self.owners)

    def addOwners(self,id):
        super().addOwners(id, self.owners.keys(),self.owners)
        super().deleteOwners(id,8,self.rootOwner)

    def deleteOwners(self, id):
        super().addOwners(id, 8,self.owners)
        super().deleteOwners(id, self.owners.keys(),self.owners)

    def addPath(self,path):
        super().addChainsAccessTo(path, self.rootOwner|self.owners)
        super().addChainsAccessFrom(path, self.rootOwner|self.owners)

    def deletePath(self,path):
        super().deleteChainsAccessTo(path, self.rootOwner|self.owners)
        super().deleteChainsAccessFrom(path, self.rootOwner|self.owners)

    def searchObj(self,root):
        pass

    def showTree(self,center):
        deepLevel = 0
        leftTree = {}
        rightTree = {center:{}}
        center = self.d.changeType(center,'l')
        createLeft()
        createRight()
        print(leftTree)
        print(rightTree)
        def createLeft(obj = center):
            for path in self.d.getChainsAccessTo(obj):
                leftTree = dict(leftTree, path)
            
            def mkDict(tree,path,index = 0):
                if path[index] not in tree.getKeys():
                    tree[path[index]] = {}
                if index < len(path)-1:
                    tree[path[index]] = mkDict(tree,path,index+1)
                    return tree
                else:
                    return tree


                    
                
        def createRight(path = center):
            tree = rightTree
            for obj in self.d.getChainAccessFrom(path[-1]):
                for o in path:
                    tree = tree.get(o)
                tree[obj] = {}
                rightTree[path[-1]] = tree
                path.append(obj)
                path = createRight(path)
            path[:-1]
            return path
    