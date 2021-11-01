

# This file was *autogenerated* from the file lowDensity.sage
from sage.all_cmdline import *   # import sage library

_sage_const_2 = Integer(2); _sage_const_0p6463 = RealNumber('0.6463'); _sage_const_0 = Integer(0); _sage_const_0p6408 = RealNumber('0.6408'); _sage_const_0p9408 = RealNumber('0.9408'); _sage_const_1 = Integer(1)# Low density attack for 0/1 knapsack
# Language: sagemath
# Made by DongHyeon. Kim (2021-09-21 22:40~23:00)

from Crypto.Util.number import long_to_bytes

class LatticeHack:
    def __init__(self, pubKey, encryptedMessage):
        self.pubKey = pubKey
        self.keyLength = len(pubKey)    
        self.encryptedMessage = encryptedMessage

        d = self.keyLength / log(max(pubKey), _sage_const_2 )
        if d < _sage_const_0p6463 :
            self.attackElement = _sage_const_0 
        elif _sage_const_0p6408  <= d < _sage_const_0p9408 :
            self.attackElement = _sage_const_1 /_sage_const_2 
        else:
            print("Can't hack this cryptosystem with 'low density attack' :(")
    
    def makeLattice(self):
        M = [[_sage_const_0  for i in range(self.keyLength + _sage_const_1 )] for j in range(self.keyLength + _sage_const_1 )]
        for i in range(self.keyLength):
            M[i][i] = _sage_const_1 
            M[i][self.keyLength] = self.pubKey[i]
            M[self.keyLength][i] = -self.attackElement
        M[self.keyLength][self.keyLength] = -self.encryptedMessage

        return Matrix(M)

    def checkVector(self, row):
        for i in row:
            if not(-self.attackElement <= i <= self.attackElement):
                return False
        return True

    def encryption(self, row):
        p = _sage_const_0 
        for i in range(self.keyLength):
            p += (row[i] * self.pubKey[i])
        return p

    def hack(self):
        ML = self.makeLattice().LLL()
        for i in range(self.keyLength + _sage_const_1 ):
            if self.checkVector(ML[i][:-_sage_const_1 ]):
                message = [(j + self.attackElement) for j in ML[i][:-_sage_const_1 ]]
                if self.encryption(message) != self.encryptedMessage: continue
                
                message = '0b' + ''.join([str(j) for j in message])
                try:
                    message = long_to_bytes(int(message, _sage_const_2 )).decode()
                except:
                    message = '0b' + message[_sage_const_2 :][::-_sage_const_1 ]
                    message = long_to_bytes(int(message, _sage_const_2 )).decode()
                print(message)
                return

if __name__ == "__main__":
    # Modify it!
    # pubKey = 
    # encryptedMessage = 

    # Test
    with open('./output.txt', 'r') as f:
        pubKey = list(map(Integer, f.readline().replace("Public key: [", "").replace("]", "").split(", ")))
        encryptedMessage = Integer(f.readline().replace("Encrypted Flag: ", ""))

    attack = LatticeHack(pubKey, encryptedMessage)
    attack.hack()

