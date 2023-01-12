from ast import literal_eval
import os

class DBServerBasic:
    """

    サーバーへのアクセスする機能、またはPythonの機能のメソッドをを有するクラス

    """
    data = {}
    def __init__(self):
        def getFile(num, data = {}):
            match num:
                case 0:
                    with open('ANDBData','r') as f:
                        self.data = self.changeType(f.read(),'d')
                case 1:
                    pass
        getFile(0)


    def saveFile(self,num,data1 = None,data2=None):
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
        data = str(data)
        match toType:
            case 's':
                data = str(data)
            case 'l':
                data = literal_eval(data)
                if str(type(data)) != "<class 'list'>":
                    data = [data]
            case 'd':
                evalData = literal_eval(data)
                data = dict(evalData)
            case 'se':
                data = literal_eval(data)
                data = set(data)
            case _:
                print('fucyoumen')
        return data

        
class DBServer(DBServerBasic):
    """

    サーバーの基本的な機能のメソッドを有するクラス

    """
    directryFroms = []
    directryTos = []

    def checkObj(self, obj):
        """

        オブジェクトがデータベースに存在するかどうか調べデータベースに無い場合はRootをオーナとして追加する
        
        parameters
        ----------
        obj : string
            対称のオブジェ
        
        """
        obj = self.changeType(obj,'s')
        if obj not in self.data.keys():
            self.data[obj] = [None,['rootpasskey1234',['8']],[],[]]
            self.addAccessTo0(obj,['8','9'])
            self.addAccessFrom0('8',obj)
            self.addAccessFrom0('9',obj)

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
            return True if self.data.get(obj)[1][0] == owners.get(obj) else False
        def allowPasskeyOwner(ownerNumber, ownerCount):
            if ownerNumber == 0:
                return True
            else:
                if ownerCount == 0:
                    ownerCount = 0.1
                return True if ownerNumber / ownerCount < 2 else False
        self.checkObj(obj)
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
        newSearchObjs = set()
        for path in self.data.get(fromObj)[2]:
            path = self.changeType(path, 'se')
            newSearchObjs |= path
        newSearchObjs |= self.changeType(self.data.get(fromObj)[3],'se')
        newSearchObjs -= searchedObjs
        if toObj in newSearchObjs:
            return True
        else:
            searchedObjs |= newSearchObjs
            for o in newSearchObjs:
                if self.judgeAccess(o, toObj, searchedObjs):
                    return True
            return False

    

    def addAccessTo0(self, obj, addObjPath):
        """
        
        オブジェにアクセス先パスを追加する
        
        parameters
        ----------
        obj : string
            対象のオブジェ
        addObjPath : list
            追加するパス
        
        """
        obj = self.changeType(obj,'s')
        addObjPath = self.changeType(addObjPath,'l')
        objPathes = self.data.get(obj)[2]
        if addObjPath not in objPathes:
            self.data.get(obj)[2].append(addObjPath)


    def addAccessFrom0(self, obj, addObj):
        """
        
        オブジェにアクセス元オブジェを追加する
        
        parameters
        ----------
        obj : string
            対象のオブジェ
        addObj : string
            追加するオブジェ
        
        """
        obj = self.changeType(obj,'s')
        addObj = self.changeType(addObj,'s')
        if addObj not in self.data.get(obj)[3]:
            self.data.get(obj)[3].append(addObj)
            

    def deleteAccessTo0(self, obj, deleteObjPath):
        """
        
        オブジェからアクセス先パスを削除する
        
        parameters
        ----------
        obj : string
            対象のオブジェ
        deleteObjPath : list
            削除するパス
        
        """
        obj = self.changeType(obj,'s')
        deleteObjPath = self.changeType(deleteObjPath,'l')
        if deleteObjPath in self.data.get(obj)[2]:
            self.data.get(obj)[2].remove(deleteObjPath)


    def deleteAccessFrom0(self, obj, deleteObj):
        """
        
        オブジェからアクセス元オブジェを削除する
        
        parameters
        ----------
        obj : string
            対象のオブジェ
        deleteObj : string
            削除するオブジェ
        
        """
        obj = self.changeType(obj,'s')
        deleteObj = self.changeType(deleteObj,'s')
        if deleteObj in self.data.get(obj)[3]:
            self.data.get(obj)[3].remove(deleteObj)


    def addOwner0(self, obj, addObj):
        """
        
        オブジェにオーナオブジェを追加する
        
        parameters
        ----------
        obj : string
            対象のオブジェ  
        addObj : string
            追加するオブジェ
            
        """
        obj = self.changeType(obj,'s')
        addObj = self.changeType(addObj,'s')
        if addObj not in self.data.get(obj)[1][1]:
            self.data.get(obj)[1][1].append(addObj)

            
    def deleteOwner0(self, obj, deleteObj):
        """
        
        オブジェからオーナオブジェを削除する
        
        parameters
        ----------
        obj : string
            対象のオブジェ  
        deleteObj : list
            削除するオブジェ
            
        """
        obj = self.changeType(obj,'s')
        deleteObj = self.changeType(deleteObj,'s')
        if deleteObj in self.data.get(obj)[1][1]:
            self.data.get(obj)[1][1].remove(deleteObj)


    def switchObjPasskey0(self, obj, newPasskey):
        """
        
        オブジェのパスキーを入れ替える
        
        parameters
        ----------
        obj : string
            対象のオブジェ  
        newPasskey : string
            入れ替え先のパスキー
            
        """
        newPasskey = self.changeType(newPasskey,'s')
        self.data.get(obj)[1][0] = newPasskey

    def switchData0(self, obj, data):
        """
        
        オブジェのデータを入れ替える
        
        parameters
        ----------
        obj : string
            対象のオブジェ  
        data : string
            入れ替え先のデータ
            
        """
        data = self.changeType(data,'s')
        self.data.get(obj)[0] = data

    def getData(self,obj):
        return self.data.get(obj)[0]

    def getAccessTo(self,obj):
        return self.data.get(obj)[2]

    def getOwners(self,obj):
        return self.data.get(obj)[1][0]
    
    def getAccessFrom(self, obj):
        return self.data.get(obj)[3] 

    def makeDirectryFroms(self, obj):
        pass


    def makeDirectry(self, obj = '8'):
        pass





class ArrowNetworkDB(DBServer):
    """
    
    アローネットワークデータベースの基本的なメソッドを有するクラス
    
    """
    
    def addAccessTo(self, owners, obj, addObjPath):
        owners = self.changeType(owners,'d')
        obj = self.changeType(obj,'s')
        addObjPath = self.changeType(addObjPath,'l')
        self.checkObj(obj)
        for o in addObjPath:
            self.checkObj(o)
        if self.judgeYouOwners(obj, owners):
            self.addAccessTo0(obj,addObjPath)
            self.saveFile(0)

    
    def addAccessFrom(self, owners, obj, addObj):
        owners = self.changeType(owners,'d')
        obj = self.changeType(obj,'s')
        addObj = self.changeType(addObj,'s')
        self.checkObj(obj)
        self.checkObj(addObj)
        if self.judgeYouOwners(obj,owners):
            self.addAccessFrom0(obj,addObj)
            self.saveFile(0)
    
            
    def deleteAccessTo(self, owners, obj, deleteObjPath):
        owners = self.changeType(owners,'d')
        obj = self.changeType(obj,'s')
        deleteObjPath = self.changeType(deleteObjPath,'l')
        self.checkObj(obj)
        for o in deleteObjPath:
            self.checkObj(o)
        if self.judgeYouOwners(obj, owners):
            self.deleteAccessTo0(obj,deleteObjPath)
            self.saveFile(0)
        
    
    def deleteAccessFrom(self, owners, obj, deleteObj):
        owners = self.changeType(owners,'d')
        obj = self.changeType(obj,'s')
        deleteObj = self.changeType(deleteObj,'s')
        self.checkObj(obj)
        self.checkObj(deleteObj)
        if self.judgeYouOwners(obj,owners):
            self.deleteAccessFrom0(obj,deleteObj)
            self.saveFile(0)


    def addOwner(self, owners, obj, addObj):
        owners = self.changeType(owners,'d')
        obj = self.changeType(obj,'s')
        addObj = self.changeType(addObj,'s')
        self.checkObj(obj)
        self.checkObj(addObj)
        if self.judgeYouOwners(obj, owners):
            self.addOwner0(obj,addObj)
            self.saveFile(0)


    def deleteOwner(self, owners, obj, deleteObj):
        owners = self.changeType(owners,'d')
        obj = self.changeType(obj,'s')
        deleteObj = self.changeType(deleteObj,'s')
        self.checkObj(obj)
        self.checkObj(deleteObj)
        if self.judgeYouOwners(deleteObj, owners):
            self.deleteOwner0(obj, deleteObj)   
            self.saveFile(0)


    def switchObjPasskey(self, owners, obj, newPasskey = None):
        owners = self.changeType(owners,'d')
        obj = self.changeType(obj,'s')
        newPasskey = self.changeType(newPasskey,'s')
        self.checkObj(obj)
        if self.judgeYouOwners(obj, owners):
            self.switchObjPasskey0(obj, newPasskey)
            self.saveFile(0)


    def switchData(self, owners, obj, data):
        owners = self.changeType(owners,'d')
        obj = self.changeType(obj,'s')
        data = self.changeType(data,'s')
        self.checkObj(obj)
        if self.judgeYouOwners(obj, owners):
            self.switchData0(obj, data)
            self.saveFile(0)

class Tasks(ArrowNetworkDB):
    """
    
    アローネットワークデータベースの機能を一般に必要な機能としてまとめたメソッドを有するクラス
    
    """
    iamRootOwner = {'8':'rootpasskey1234'}

    def createYou(self, obj, newObjPasskey):
        self.switchObjPasskey(self.iamRootOwner, obj, newObjPasskey)
        self.deleteOwner(self.iamRootOwner, obj, 8)

    def createObj(self, obj, ownerObjs, newOwners):
        ownerObjs = self.changeType(ownerObjs,'l')
        newOwners = self.changeType(newOwners,'d')
        for o in ownerObjs:
            self.addOwner(self.iamRootOwner|newOwners, obj, o)
        self.switchObjPasskey(self.iamRootOwner | newOwners, obj)

    def putData(self, obj, data, owners):
        self.switchData(owners, obj, data)

    def putAccessesTo(self, fromObj, toObjPathes, owners):
        toObjPathes = self.changeType(toObjPathes,'l')
        for path in toObjPathes:
            self.addAccessTo(owners, fromObj, path)

    def putAccessesFrom(self, fromObjs, toObj, owners):
        fromObjs = self.changeType(fromObjs,'l')
        for o in fromObjs:
            self.addAccessFrom(owners, toObj, o)

    def deleteAccessesTo(self, fromObj, toObjPathes, owners):
        toObjPathes = self.changeType(toObjPathes, 'l')
        for path in toObjPathes:
            self.deleteAccessTo(owners, fromObj, path)

    def deleteAccessesFrom(self, fromObj, toObjs, owners):
        toObjs = self.changeType(toObjs, 'l')
        for o in toObjs:
            self.deleteAccessFrom(owners, o, fromObj)

    def putOwners(self, obj, owners, newOwnerObjs, newOwners):
        newOwnerObjs = self.changeType(newOwnerObjs, 'l')
        owners = self.changeType(owners, 'd')
        newOwners = self.changeType(newOwners,'d')
        for o in newOwnerObjs:
            self.addOwner(owners|newOwners, obj, o)
        
    def deleteOwners(self, obj, owner, deleteObjs):
        deleteObjs = self.changeType(deleteObjs, 'l')
        for o in deleteObjs:
            self.deleteOwner(owner, obj, o)

class User(Tasks):
    def createYou(self, obj,newObjPasskey):
        self.createYou(obj, newObjPasskey)

    def createFile(self, obj, ownerObjs, newOwners, data, toObjPath = []):
        self.createObj(obj, ownerObjs, newOwners)
        self.putData(obj, data, newOwners)
        self.putAccessesTo(obj, toObjPath, newOwners)

    def switchData(self, obj, owners, data):
        self.switchData(obj,owners,data)

    def putACCessesToAndFrom(self,fromObj, toObjPathes, owners):
        self.putAccessesTo(fromObj, toObjPathes,owners)
        for path in toObjPathes:
            self.putAccessesFrom(path, fromObj,owners)

    def showDirectry(self):
        self.saveDirectry()


        
owner1 = {'8':'rootpasskey1234'}
owner2 = {'12':'userpasskey1234'}
owner3 = {'15':'userpasskey2345'}
u = User()
u.createFile(0,8,owner1,0,[['8','9']])
u.createFile(1,8,owner1,1,[['8','9']])