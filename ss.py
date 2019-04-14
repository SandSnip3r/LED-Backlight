import mss
import math
import numpy
import serial

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
      self.groupColorDict[i]["blueSum"] = 0
      self.groupColorDict[i]["greenSum"] = 0
      self.groupColorDict[i]["redSum"] = 0
      self.groupColorDict[i]["count"] = 0

    for i in range(0, len(data), 4):
      groupIndex = translateIndex(i/4, kScreenWidth)
      self.groupColorDict[groupIndex]["blueSum"] += int.from_bytes(data[i], byteorder='little')
      self.groupColorDict[groupIndex]["greenSum"] += int.from_bytes(data[i+1], byteorder='little')
      self.groupColorDict[groupIndex]["redSum"] += int.from_bytes(data[i+2], byteorder='little')
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

def serializePixelsForArduino(pixelList):
  #  [Pixel] pixelList
  # <pixelCount:n>:r_1,g_1,b_1,...,r_n,g_n,b_n
  pixelString = str(len(pixelList)) + ','
  for pixel in pixelList:
    pixelString += str(pixel.red) + ','
    pixelString += str(pixel.green) + ','
    pixelString += str(pixel.blue) + ','
  return pixelString

def toHtmlFile(pixels):
  with open("colors.html", 'w') as htmlFile:
    kBoxWidth = 50
    htmlStr = '<!DOCTYPE html>'
    htmlStr += '<html>'
    htmlStr += '<body>'
    for pixel in pixels:
      htmlStr += '<svg width="'+str(kBoxWidth)+'" height="'+str(kBoxWidth)+'"><rect width="'+str(kBoxWidth)+'" height="'+str(kBoxWidth)+'" style="fill:rgb('+str(pixel.red)+','+str(pixel.green)+','+str(pixel.blue)+')" /></svg>'
    htmlStr += '</body>'
    htmlStr += '</html>'
    htmlFile.write(htmlStr)


with serial.Serial('COM4',9600) as seiralConnection:
  with mss.mss() as sct:
    monitor_number = 2
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
    while True:
      sct.cls_image = ScreenshotDataCollector
      ssData = sct.grab(monitor)
      averages = ssData.getAverages()
      # toHtmlFile(averages)
      serialStr = serializePixelsForArduino(averages)
      seiralConnection.write(serialStr.encode())
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