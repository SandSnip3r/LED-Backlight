from time import sleep
import serial


class Test:
  def __init__(self, x):
    self.x = x

t = Test(10)
print(t.x)
# with serial.Serial('COM4',9600) as seiralConnection:
#   sleep(2)
#   result = seiralConnection.write(str.encode('1'))
#   sleep(2)
  # bytesWritten = seiralConnection.write(bytes(b"Flashing lights, soon...\n"))
  # print("Wrote {}".format(bytesWritten))
  # print("Readable:{}".format(seiralConnection.readable()))
  # responseByte = seiralConnection.read()
  # print("Read  {}".format(responseByte))