import math
from collections import Counter
counts = Counter()

kScreenWidth=2000
kLedCount=37
kHeight = int(round(kScreenWidth/float(kLedCount)))
groupWidthCeil = math.ceil(kScreenWidth/float(kLedCount))
groupWidthFloor = math.floor(kScreenWidth/float(kLedCount))
remainder = kScreenWidth%kLedCount
# for (int i=0; i<kScreenWidth*kHeight; ++i) {
for i in range(0,kScreenWidth*kHeight):
  kPixelColumn = i%kScreenWidth
  borderBetweenDifferentGroupSizes = (remainder)*groupWidthCeil
  if kPixelColumn < borderBetweenDifferentGroupSizes:
    #Groups of size groupWidthCeil
    counts[int(kPixelColumn/groupWidthCeil)] += 1
  else:
    #Groups of size groupWidthFloor
    counts[int((kPixelColumn-remainder)/groupWidthFloor)] += 1

print(counts)