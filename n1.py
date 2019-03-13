#!/usr/bin/python
import rospy

from geometry_msgs.msg import Twist
from std_msgs.msg import Float32

import serial
import time



class Prueba():
	def __init__(self):
		self.rospy = rospy
		self.rospy.init_node('Nodo1', anonymous = True)
		self.initParameters()
		self.initPublishers()
		self.main()
		return

	def initParameters(self):
		self.topiclin = "/lineal"
		self.topicang = "/angular"
		self.mensaje1 = Float32()
		self.mensaje2 = Float32()
		self.rate = self.rospy.Rate(50)
		self.arduino = serial.Serial('/dev/ttyACM0', 9600)
		time.sleep(2)
		return


	def initPublishers(self):
		self.pub1 = self.rospy.Publisher(self.topiclin, Float32, queue_size=10)
		self.pub2 = self.rospy.Publisher(self.topicang, Float32, queue_size=10)
		return

	def separar_datos(self, rawString):
		try:
			self.a, self.b = rawString.strip().split(',')
		except:
			self.a, self.b = 0, 0
		self.a =  float(self.a)*2.0/5
		self.b =  float(self.b)*2.0/5
		return

	def main(self):
		print("Nodo OK")
		while not self.rospy.is_shutdown():
			rawString = self.arduino.readline()
			self.separar_datos(rawString)
			self.pub1.publish(float(self.a))
			self.pub2.publish(float(self.b))
		self.arduino.close()

if __name__ == "__main__":
	try:
		print("Iniciando Nodo")
		nodo = Prueba()
	except rospy.ROSInterruptException:
		print("Finalizando Nodo")
		pass
