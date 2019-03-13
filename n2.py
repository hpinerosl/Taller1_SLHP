#!/usr/bin/python
import rospy
import math
import numpy
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool
from sensor_msgs.msg import LaserScan
from std_msgs.msg  import Float32


class Prueba():
	def __init__(self):
		self.rospy = rospy
		self.rospy.init_node('Nodo2', anonymous = True)
		self.initParameters()
		self.initSubscribers()
		self.initPublishers()
		self.main()
		return

	def initParameters(self):
		self.topic1 = "/scan"
		self.topic2 = "/aux_topic"
		self.msg_scan = LaserScan()
		self.msg_aux=	Bool()
		self.distancia = Float32()
		self.disper = Float32()
		self.cambio1 = False
		self.obstaculo = False
		self.rate = self.rospy.Rate(50)
		return

	def initSubscribers(self):
		self.sub1 = self.rospy.Subscriber(self.topic1, LaserScan, self.funci)
		return

	def initPublishers(self):
		self.pub1 = self.rospy.Publisher(self.topic2, Bool, queue_size=10)
		return

	def funci(self, msg):
		self.msg_scan = msg.header
		self.msg_scan = msg.angle_min
		self.msg_scan = msg.angle_max
		self.msg_scan = msg.range_min
		self.msg_scan = msg.range_max
		self.msg_scan = msg.ranges
		self.msg_scan = msg.angle_increment
		grupos = []
		distanciax=[]
		distanciay=[]
		conti=0
		datos = list(msg.ranges) 
		angle = msg.angle_min
		i=1
		x=0
		a=False
		for i in range(len(msg.ranges)):
			if datos[i] == numpy.inf:
				datos[i]=0 
			k = datos[i]*math.sin(angle)
			if k > 0 and k <= 1:	
				distanciay.append(datos[i]*math.sin(angle))	
				distanciax.append(datos[i]*math.cos(angle))
				if x > 0:
					disper = math.sqrt(((distanciax[x]-distanciax[x-1])**2)+((distanciay[x]-distanciay[x-1])**2))
					if disper <= 0.1 :
						conti=conti+1
					else:				
						grupos.append(conti) 
						conti=0
						a=True
				x=x+1
			angle += msg.angle_increment
		print(grupos)
		if not a:
			grupos.append(conti)
		for i in range(len(grupos)):		
			if grupos[i] >5: 
				self.obstaculo=True
		self.cambio1 = True
		return

	def main(self):
		print("Nodo OK")
		while not self.rospy.is_shutdown():
			if self.cambio1: 
				self.msg_aux.data = self.obstaculo
				self.pub1.publish(self.msg_aux)	
				self.cambio1 = False
				self.obstaculo = False
			self.rate.sleep()
		return

if __name__ == "__main__":
	try:
		print("Iniciando Nodo")
		nodo = Prueba()
	except rospy.ROSInterruptException:
		print("Finalizando Nodo")
		pass
