from harvesters.core import Harvester
import numpy as np
import cv2
import time
import faulthandler
faulthandler.enable()


h = Harvester()
h.add_file('C:\\Program Files\\JAI\\SDK\\bin\\JaiGevTL.cti')
h.update()
lis = h.device_info_list
print(lis)
ia = h.create(0)

tiem0 = ia.statistics.elapsed_time_s
fps0 = ia.statistics.fps

ia.start()
time.sleep(3)
tiem = ia.statistics.elapsed_time_s
fps = ia.statistics.fps
buffer = ia.fetch()
print(buffer)
image = buffer.payload.components[0].data

# Don't forget to queue the buffer.
buffer.queue()
print(tiem0, fps0, tiem, fps)
print(type(image))


ia.stop()

ia.destroy()
h.reset()


