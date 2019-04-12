import mss
import math
import numpy

kLedCount = 37

class Pixel:
  def __init__(self,r,g,b):
    self.red = r
    self.green = g
    self.blue = b
  def __str__(self):
    return "("+str(self.red)+","+str(self.green)+","+str(self.blue)+")"
  def __repr__(self):
    return "("+str(self.red)+","+str(self.green)+","+str(self.blue)+")"

class ScreenshotDataCollector:
  def __init__(self, data, monitor, **kwargs):
    self.monitor = monitor
    kScreenWidth = self.monitor["width"]
    self.groupColorDict = dict()
    for i in range(0,kLedCount):
      self.groupColorDict[i] = dict()
      self.groupColorDict[i]["greenSum"] = 0
      self.groupColorDict[i]["redSum"] = 0
      self.groupColorDict[i]["blueSum"] = 0
      self.groupColorDict[i]["count"] = 0

    for i in range(0, len(data), 4):
      groupIndex = translateIndex(i/4, kScreenWidth)
      self.groupColorDict[groupIndex]["greenSum"] += data[i]
      self.groupColorDict[groupIndex]["redSum"] += data[i+1]
      self.groupColorDict[groupIndex]["blueSum"] += data[i+2]
      self.groupColorDict[groupIndex]["count"] += 1
  
  def getAverages(self):
    pixels = []
    for value in self.groupColorDict.values():
      pixels.append(Pixel(int(round(value["redSum"]/float(value["count"]))), int(round(value["greenSum"]/float(value["count"]))), int(round(value["blueSum"]/float(value["count"])))))
    return pixels


def translateIndex(index, kScreenWidth):
  groupWidthCeil = math.ceil(kScreenWidth/float(kLedCount))
  groupWidthFloor = math.floor(kScreenWidth/float(kLedCount))
  remainder = kScreenWidth%kLedCount
  kPixelColumn = index%kScreenWidth
  borderBetweenDifferentGroupSizes = (remainder)*groupWidthCeil
  if kPixelColumn < borderBetweenDifferentGroupSizes:
    #This lands in a group of size groupWidthCeil
    return int(kPixelColumn/groupWidthCeil)
  else:
    #This lands in a group of size groupWidthFloor
    return int((kPixelColumn-remainder)/groupWidthFloor)

with mss.mss() as sct:
  # Get information of monitor 2
  monitor_number = 1
  mon = sct.monitors[monitor_number]
  kHeight = int(round(mon["width"]/float(kLedCount)))
  print("Square: {}x{}".format(kHeight,kHeight))

  # The screen part to capture
  monitor = {
    "top": mon["top"],
    "left": mon["left"],
    "width": mon["width"],
    "height": kHeight,
    "mon": monitor_number,
  }
  for i in range(0,100):
    sct.cls_image = ScreenshotDataCollector
    ssData = sct.grab(monitor)
    print("{}".format(ssData.getAverages()))
  # ...


# groupCount = 2
# groupColorDict = dict()
# for i in range(0,groupCount):
#   groupColorDict[i] = dict()
#   groupColorDict[i]["greenSum"] = 0
#   groupColorDict[i]["redSum"] = 0
#   groupColorDict[i]["blueSum"] = 0
#   groupColorDict[i]["count"] = 0


# data = [2,2,2,0,18,18,18,0,4,4,4,0,4,4,4,0]
# greenArr = data[0::4]
# redArr = data[1::4]
# blueArr = data[2::4]
# alphaArr = data[3::4]
# for i in range(0, len(greenArr)):
#   groupIndex = translateIndex(i, len(greenArr), groupCount)
#   groupColorDict[groupIndex]["greenSum"] += greenArr[i]
#   groupColorDict[groupIndex]["redSum"] += redArr[i]
#   groupColorDict[groupIndex]["blueSum"] += blueArr[i]
#   groupColorDict[groupIndex]["count"] += 1

# print(data)
# for key,value in groupColorDict.items():
#   p = Pixel(int(round(value["redSum"]/float(value["count"]))), int(round(value["greenSum"]/float(value["count"]))), int(round(value["blueSum"]/float(value["count"]))))
#   print("{} {}".format(key,p))
# # print(groupColorDict)