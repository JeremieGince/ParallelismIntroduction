import multiprocessing as mp
import time
import typing

from .sensor_loggers import SensorLogger
from .sensors.sensor import Sensor
from src.weather_predictor.weather_predictor import WeatherPredictor


class App:
	def __init__(self, sensors: typing.List[Sensor], seconds_per_day: int = 100_000):
		self.manager = mp.Manager()
		self.sensors = sensors
		self.sensors_lock = mp.RLock()
		self.sensor_loggers = mp.Manager().list()
		self.weather_predictor = WeatherPredictor(self.sensors_lock)
		self.seconds_per_day = seconds_per_day
		self.done_date = list()
		self.sensors_process_id = None
		self.sensors_process = None
		self.weather_predictor_process_id = None

	def __getstate__(self):
		# capture what is normally pickled
		state = self.__dict__.copy()

		# remove unpicklable/problematic variables
		state['sensors_process'] = None
		state['weather_predictor_process'] = None
		state['manager'] = None
		return state

	def run(self, n_day='all'):
		raise NotImplementedError()

	def run_single_day(self, date):
		print(f"Start day - {date}")
		self.start_day(date)
		time.sleep(self.seconds_per_day)
		print(f"Stop day - {date}")
		self.stop_day(date)

	def start_day(self, date):
		"""
		run start_sensors and start_predictor in multiprocessing
		:param date:
		:return:
		"""
		self.sensors_process = mp.Process(target=self.start_sensors, args=(date, self.sensor_loggers))
		#self.weather_predictor_process = mp.Process(target=self.start_predictor, args=(date,))

		self.sensors_process.start()
		self.sensors_process_id = self.sensors_process.pid
		# self.weather_predictor_process.start()
		# mp.Process(target=self.run, args=(date,)).start()

	def start_sensors(self, date, sensor_loggers):
		"""
		#TODO:
		- start one thread for each sensor
		- In each thread do:
			# - call set_day(day)
			- do
				- read the sensor
				- save the data
				- save stats (mean, min, max) of the data in a file named [sensor.name]-[day].npy
				- concat all stats together in a file named [day].npy

		:param date:
		:return:
		"""
		sensor_loggers.extend([SensorLogger(sensor, self.sensors_lock) for sensor in self.sensors])
		for logger in self.sensor_loggers:
			logger.set_date(date)
			logger.start()

	def stop_day(self, date):
		self.done_date.append(date)
		self.stop_sensors()
		self.stop_processes()

	def stop_sensors(self):
		for logger in self.sensor_loggers:
			logger.stop()
			logger.join()

	def stop_processes(self):
		self.sensors_process.join()
		self.sensors_process.kill()
		self.sensors_process.close()

	def start_predictor(self, date):
		"""
		#TODO:
		- read and add the data of the previous day to the training set.
		- re-train the model.
		-

		:param date:
		:return:
		"""
		# self.weather_predictor.set_date(date)
		# self.weather_predictor.set_done_date(self.done_date)
		# self.weather_predictor.run()
		pass

	def log_sensor_data(self, sensor):
		pass
