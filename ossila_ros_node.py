import xtralien
import time
import rospy
from std_msgs.msg import Float64


rospy.init_node('ossila', anonymous=True)


ohm_pub = rospy.Publisher('/piezo', Float64)
# with xtralien.Device() as SMU:
#     SMU.reset()
SMU = xtralien.Device('/dev/ttyACM0')
# SMU.smu1.set.osr(0)

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

        ohm_pub.publish(Float64(c))
        

            # print((time.time() - now) / 100, i)
            # now = time.time()
except KeyboardInterrupt:
    SMU.smu1.set.voltage(0, response=0)
    SMU.smu1.set.enabled(False)

SMU.close()