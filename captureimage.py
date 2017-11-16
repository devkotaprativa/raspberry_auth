
from PIL import Image
import select
import time
import v4l2capture
import VL53L0X

video = v4l2capture.Video_device("/dev/video0")

size_x, size_y = video.set_format(1280, 1024)

video.create_buffers(1)

video.start()

time.sleep(2)

video.queue_all_buffers()

select.select((video,), (), ())

image_data = video.read_and_queue()
video.close()
image = Image.frombytes("RGB", (size_x, size_y), image_data)
image.save("image.jpg")
print "Saved image.jpg (Size: " + str(size_x) + " x " + str(size_y) + ")"


tof = VL53L0X.VL53L0X()
tart ranging
tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

timing = tof.get_timing()
if (timing < 20000):
    timing = 20000
print ("Timing %d ms" % (timing/1000))
distance = tof.get_distance()
distance = distance/10
file = open('distance.txt', 'w')
file.write(distance)
file.close()
print distance
time.sleep(timing/1000000.00)

tof.stop_ranging()