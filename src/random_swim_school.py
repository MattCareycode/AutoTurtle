#!/usr/bin/env python
# Execute as a python script
# Description: Set linear and angular values for the Turtle.
import rospy    
import math  
import random       # Needed to create a ROS node -Python client library
# Message type that Turtlesim accepts - usually via the topic cmd_vel
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose 
from std_srvs.srv import Empty
from turtlesim.srv import TeleportAbsolute

pose = Pose()


def update_pose(data):
    global pose
    pose = data

rospy.Subscriber('turtle1/pose', Pose, update_pose)    

def main():
    global pose, pose1
    rospy.init_node('swim', anonymous=False)
    #rospy.on_shutdown(shutdown)
        # Message to screen
        # Twist message on topic /turtle1/cmd_vel. lets do that below-
   
    teleport = rospy.ServiceProxy('turtle1/teleport_absolute', TeleportAbsolute)
    cmd_vel = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size=10)
        # Here we are creating a handle to publish messages to a topic using
        # the rospy.Publisher class.
        # The most common usage for this is to provide the name of the topic
        # and the message class/type of the topic.
        # You can then call publish() on that handle to publish a message.
        # General usage:
        # pub = rospy.Publisher('topic_name', message class, queue_size=10)

        # Turtlesim will receive our messages 10 times per second.
    rate = rospy.Rate(10);
        # Do not confuse this 10 with the queue_size = 10 above.
        # 10 Hz is fine as long as the processing does not exceed
        #   1/10 second.

        # We may want the user to specify the rate rather than echo a fixed rate.

        # Twist is geometry_msgs for linear and angular velocity
        # create an object of the class Twist.
    move_cmd = Twist()

        # Linear speed in x in units/second: positive values imply forward,
        # negative values == backwards
    move_cmd.linear.x = random.randint(1,8) # Modify this value to change the Turtle's speed

        # Turn at 0 radians/s
    move_cmd.angular.z = random.randint(1,8)

    #pose = rospy.wait_for_message('turtle1/teleport_absolute', timeout=None)
        # Modify this value to cause rotation rad/s

        # Loop until you type CTRL+c
    #while True:

             # publish Twist values to the Turtlesim node /cmd_vel
             # handle.publish(message class instance)
    teleport(pose.x, pose.y, pose.theta)

    cmd_vel.publish(move_cmd)
    prev = rospy.get_time()

   # print(pose)


    while True:
        curr = rospy.get_time()
        #check if turtle has traveled a full circle
        if abs(move_cmd.angular.z) * (curr - prev) >= 2*math.pi:
            print("Center Position x: ", pose.x)
            print("Center Position y: ", pose.y)

            #teleport(pose.x, pose.y, pose.theta)
            move_cmd.angular.z *=-1
            prev = curr


        cmd_vel.publish(move_cmd)


                # wait for 0.1 seconds (10 HZ) and publish again
        rate.sleep()




if __name__ == '__main__':
    main()
    # Try and Except.
    # If an error is encountered, a try block code execution is stopped and
    # transferred down to the except block.

    