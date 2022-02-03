import pandas as pd
from scipy.stats import truncnorm
import time

from .sensor import Sensor


class Thermometer(Sensor):
	def __init__(self, sensor_id: int, name="thermometer"):
		super(Thermometer, self).__init__(sensor_id, name=name)
		self.acquisition_time = 0.08

	@property
	def columns_names(self):
		return ["TempLowF", "TempHighF", "TempAvgF"]

	def read(self):
		time.sleep(self.acquisition_time)
		cols = self.columns_names
		data = pd.read_csv(Sensor.rawData, index_col="Date")
		low, high, avg = data.loc[self._date, cols]
		scale = max(high - avg, avg - low)
		val = truncnorm.rvs(low, high, loc=avg, size=1, scale=scale)
		return val







