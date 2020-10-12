#!/usr/bin/env python
# Execute as a python script
# Description: Set linear and angular values for the Turtle.
import rospy    
import math         # Needed to create a ROS node -Python client library
# Message type that Turtlesim accepts - usually via the topic cmd_vel
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose 
from std_srvs.srv import Empty


class Swim:
    def __init__(self):
        rospy.init_node('swim', anonymous=False)
        self.pose_sub =rospy.Subscriber('turtle1/pose', Pose, self.update_pose)    
        self.cmd_vel = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size=10)
        self.rate = rospy.Rate(10);
        self.pose = Pose()
        self.goal = Pose()


    def update_pose(self,data):
        self.pose = data
        self.pose.x = round(self.pose.x,4)
        self.pose.y = round(self.pose.y, 4)

    def set_linear(self, goal, constant=1.5):
        return constant * self.set_distance(self.goal)

    def set_angular(self, goal, constant=6):
        return constant * (self.set_angle(self.goal) - self.pose.theta)

    def set_angle(self, goal):
        return math.atan2(self.goal.y - self.pose.y, goal.x - self.pose.x)

    def set_distance(self, goal):
        return math.sqrt(pow((self.goal.x -self.pose.x), 2) + pow((self.goal.y - self.goal.y),2))

    def go_to_goal(self):

        self.goal = Pose()
        self.goal.x = float(raw_input("Enter an x goal: "))
        self.goal.y = float(raw_input("Enter an y goal: "))
        tolerance = input("Enter tolerance: ")
        move_cmd = Twist()

        while self.set_distance >= tolerance:
            move_cmd.linear.x = self.set_linear(self.goal)
            move_cmd.linear.y = 0
            move_cmd.linear.z = 0   
            move_cmd.angular.y = 0
            move_cmd.angular.x = 0
            move_cmd.angular.z =  self.set_angular(self.goal)
            self.cmd_vel.publish(move_cmd)
            self.rate.sleep()

        move_cmd.linear.x = 0
        move_cmd.angular.z = 0
        self.cmd_vel.publish(move_cmd)
        rospy.spin()

  


if __name__ == '__main__':
    try:
        z = Swim()
        z.go_to_goal()
    except rospy.ROSInterruptException:
        pass
    

    