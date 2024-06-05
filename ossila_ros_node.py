import xtralien
import time
import rospy
from std_msgs.msg import Float64
from collections import deque
from statistics import mean



rospy.init_node('ossila', anonymous=True)


curr_pub = rospy.Publisher('/current', Float64)
ohm_pub = rospy.Publisher('/resistance', Float64)
# with xtralien.Device() as SMU:
#     SMU.reset()
SMU = xtralien.Device('/dev/ttyACM0')
# SMU.smu1.set.osr(0)

R_queue = deque(51*[0], maxlen=51)

# SMU.reset()
try:
    SMU.smu1.set.enabled(True, response=0)

    # print(SMU.smu1.set.filter(10))
    # print(SMU.smu1.get.filter())

    i = 0

    now = time.time()
    while True:
        i += 1
        v, c = SMU.smu1.oneshot(5)[0]
        # print(v, c*1e6, i)
        c_ohm = v/(c*1e3)
        R_queue.append(c_ohm)
        ohm = mean(R_queue)
        curr_pub.publish(Float64(c))
        ohm_pub.publish(Float64(ohm))


            # print((time.time() - now) / 100, i)
            # now = time.time()
except KeyboardInterrupt:
    SMU.smu1.set.voltage(0, response=0)
    SMU.smu1.set.enabled(False)

SMU.close()