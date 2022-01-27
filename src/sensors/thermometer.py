from sensor import Sensor
import numpy as np
import pandas as pd
import os


class Thermometer(Sensor):
	def __init__(self, sensor_id: int, name="thermometer"):
		super(Thermometer, self).__init__(sensor_id, name=name)

	def read(self):
		# TODO: add a time.sleep to simulate a acquisition time
		return 0







