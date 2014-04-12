from elliptic import *
from finitefield.finitefield import FiniteField

import os


def generateSecretKey(numBits):
   return int.from_bytes(os.urandom(numBits // 8), byteorder='big')


def sign(message, basePoint, basePointOrder, secretKey):
   modR = FiniteField(basePointOrder, 1)
   oneTimeSecret = generateSecretKey(len(bin(basePointOrder)) - 3) # numbits(order) - 1

   auxiliaryPoint = oneTimeSecret * basePoint
   signature = modR(oneTimeSecret).inverse() * (modR(message) + modR(secretKey) * modR(auxiliaryPoint[0]))

   return (message, auxiliaryPoint, signature)


def authentic(signedMessage, basePoint, basePointOrder, publicKey):
   modR = FiniteField(basePointOrder, 1)
   (message, auxiliary, signature) = signedMessage

   sigInverse = modR(signature).inverse()
   c, d = sigInverse * modR(message), sigInverse * modR(auxiliary[0])
   auxiliaryChecker = int(c) * basePoint + int(d) * publicKey

   print("Checking if %s == %s" % (auxiliaryChecker, auxiliary))
   return auxiliaryChecker == auxiliary



if __name__ == "__main__":
   F = FiniteField(1061, 1)

   # Totally insecure curve: y^2 = x^3 + 3x + 181
   curve = EllipticCurve(a=F(3), b=F(181))
   basePoint = Point(curve, F(2), F(81))
   basePointOrder = 349
   secretKey = generateSecretKey(8) # 255 < 349, which is not quite uniform but good for demonstration purposes
   publicKey = secretKey * basePoint

   print(('Public information:\n\tfield: %s\n\tcurve: %s\n\tnumber of points on curve: %d x %d\n\t' +
         'base point: %s\n\tpublic key: %s') % (F.__name__, curve, basePointOrder, 3, basePoint, publicKey))

   message = 123
   signedMessage = sign(message, basePoint, basePointOrder, secretKey)
   print('Signed message: %s' % (signedMessage,))

   validationResult = authentic(signedMessage, basePoint, basePointOrder, publicKey)
   print(validationResult)



