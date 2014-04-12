from elliptic import *
from fractions import Fraction as frac

from finitefield.finitefield import FiniteField

import itertools

# assume 'field' is Z/p
def findPointsModP(curve, field):
   print('Finding all points on %s over %s' % (curve, field.__name__))

   xs = [field(x) for x in range(field.p)]
   ys = [field(x) for x in range(field.p)]

   return [Point(curve, x, y) for x in xs for y in ys if curve.testPoint(x,y)] + [Ideal(curve)]


def slowOrder(point):
   Q = point
   i = 1
   while True:
      if type(Q) is Ideal:
         return i
      else:
         Q = Q + point
         i += 1


F = FiniteField(1061, 1)
curve = EllipticCurve(a=F(3), b=F(181))
points = findPointsModP(curve, F)

print(len(points))
for point in points:
   order = slowOrder(point)
   print(point, order)


