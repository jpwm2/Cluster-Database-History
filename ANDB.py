from sympy import prime

class ArrowNetworkDB:
    def __init__(self):
        getFile()

        def getFile(self):
            with open('ArrowNetworkDB', 'r') as f:
                self.lines = f.readlines()

    def areYouOwner(self,inObj,byOwner):
        owners = self.returnOwners(self.lines[inObj])
        ownerNumber = len(owners)
        count = 0
        for id in byOwner.keys():
            if id in owners:
                if byOwner.get(id) in owners.values():
                    count += 1
        return True if ownerNumber // 2 < count else False

    def putAccessArrow(self,fromObj, byOwner, toObj):
        if self.areYouOwner(fromObj, byOwner):
            pathesTO = self.returnDeeper(self.lines[toObj])
            pathesFO = self.returnDeeper(self.lines[fromObj])
            rootsTO, rootsFO = []
            for pto in pathesTO:
                rootsTO.add(pto[0])
            for pfo in pathesFO:
                rootsFO.add(pfo[0])
            for rfo in rootsFO:
                if rfo in rootsTO:
                    self.lines[fromObj][3] += pathesTO
                    break
            return True
        else:
            return False
            
    def deleteAccessArrow(self, fromObj, byOwner, toObj):
        if self.areYouOwner(fromObj, byOwner):
            
                

    def runAccessAuthority(self):
        pass

    def returnData(line):
        return line[0]

    def returnOwners(line):
        return line[1]

    def returnDeeper(line):
        return line[2]

    def returnShallower(line):
        return line[3]

class RootOwner:
    def __init__(self):
        self.andb = ArrowNetworkDB()
        self.length = len(self.andb.lines)
        if prime.isprime(self.length):
            pass

    def passMeInitialObj(self, OwnerPassword,data = None):
        pass

    def passMeObj(self, OwnerObjId, OwnerPassword, accessId, data = None):
        pass






ro = RootOwner()




#5 - 3 → 5 + (-3) → 1101 + 0101 → 10010 → 2

#784 - 638 = 1100010000 - 1001111110 = 1100010000 + 110000010 = 10010010010 = 146

#784 - 638 = 784 + 362 = 1146