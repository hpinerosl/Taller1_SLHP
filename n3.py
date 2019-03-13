#!/usr/bin/python
import rospy

from geometry_msgs.msg import Twist
from std_msgs.msg import Float32
from std_msgs.msg import String
from std_msgs.msg import Bool
class Prueba():
	def __init__(self):
		self.rospy = rospy
		self.rospy.init_node('Nodo3', anonymous = True)
		self.initParameters()
		self.initSubscribers()
		self.initPublishers()
		self.main()
		return

	def initParameters(self):
		self.topic1 = "/lineal"
		self.topic2 = "/angular"
		self.vel_topic = "/cmd_vel"
		self.topic3 = "/aux_topic"
		self.mensaje_vel = Twist()
		self.mensaje1 = Float32()
		self.mensaje2 = Float32()
		self.mensaje3 = Bool()
		self.cambio1 = False
		self.cambio2 = False
		self.cambio3 = False
		self.rate = self.rospy.Rate(50)
		return

	def initSubscribers(self):
		self.sub1 = self.rospy.Subscriber(self.topic1, Float32, self.callback1)
		self.sub2 = self.rospy.Subscriber(self.topic2, Float32, self.callback2)
		self.sub3 = self.rospy.Subscriber(self.topic3, Bool, self.callback3)
		return

	def initPublishers(self):
		self.pub1 = self.rospy.Publisher(self.vel_topic, Twist, queue_size=10)
		return

	def callback1(self, msg):
		self.mensaje1 = msg.data
		self.cambio1 = True
		return

	def callback2(self, msg):
		self.mensaje2 = msg.data
		self.cambio2 = True
		return

	def callback3(self, msg):
		self.mensaje3 = msg.data
		if self.mensaje3:
			self.cambio3 = True
		return

	def main(self):
		print("Nodo OK")
		while not self.rospy.is_shutdown():
			if self.cambio3:
				self.mensaje_vel.linear.x = float(0)
				self.mensaje_vel.angular.z = float(0)
				self.pub1.publish(self.mensaje_vel)				
				self.cambio3 = False
			else:
				if self.cambio1 and self.cambio2:
					self.mensaje_vel.linear.x = float(self.mensaje1)
					self.mensaje_vel.angular.z = float(self.mensaje2)
					self.pub1.publish(self.mensaje_vel)				
					self.cambio1 = False
					self.cambio2 = False				
			self.rate.sleep()
		

if __name__ == "__main__":
	try:
		print("Iniciando Nodo")
		nodo = Prueba()
	except rospy.ROSInterruptException:
		print("Finalizando Nodo")
		pass


