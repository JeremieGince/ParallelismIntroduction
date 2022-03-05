import multiprocessing as mp
import time
from typing import List, Union

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

from src.sensors.sensor import Sensor


class PlotProcess(mp.Process):
	"""
	TODO: Objet héritant de mp.Processus servant à afficher les données de SensorLogger.get_data_filename() en
			temps réel.

			Tips: Utilisez mp.Lock afin de s'assurer de ne pas corrompe le fichier en l'ouvrant/le manipulant en
			même temps qu'un autre processus.
	"""
	def __init__(
			self,
			sensors: List[Sensor],
			lock: Union[mp.Lock, mp.RLock],
			log_file: str,
			date: str,
			update_dt: float = 1.0
	):
		"""
		Constructeur de PlotProcess.

		:param sensors: Liste des senseurs.
		:param lock: La serrure utilisée par les autres processus.
		:param log_file: Le nom/path du fichier contenant les données des senseurs courants.
		:param date: La date courante.
		:param update_dt: Le temps entre deux mises à jour du graphique.
		"""
		super(PlotProcess, self).__init__()
		self._sensors = sensors
		self._lock = lock
		self._close_event = mp.Event()
		self._log_file = log_file
		self._date = date
		self.update_dt = update_dt
		self.sensor_to_ax = {}
		self.sensor_to_lines = {}
		self._dates = None

	def run(self):
		"""
		TODO:
		Crée le graphique.
		Lance la boucle de mises à jour du graphique.
		:return: None
		"""
		can_plot = False
		while not can_plot and not self._close_event.is_set():
			if os.path.exists(self._log_file):
				try:
					pd.read_csv(self._log_file, index_col="Date")
					can_plot = True
				except Exception:
					time.sleep(self.update_dt)

		self.create_plot()
		plt.legend()
		plt.pause(self.update_dt)
		while not self._close_event.is_set():
			self.update_plot()
			plt.pause(self.update_dt)

	def create_plot(self):
		"""
		Crée le graphique contenant k subplots où k est le nombre de senseurs.
		:return: la figure
		"""
		self.sensor_to_ax.clear()
		self.sensor_to_lines.clear()

		ncols = int(np.sqrt(len(self._sensors)))
		nrows = int(len(self._sensors) / ncols)
		figure, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10, 8))
		figure.canvas.manager.full_screen_toggle()
		axes = np.ravel(axes)
		with self._lock:
			df = pd.read_csv(self._log_file, index_col="Date")

		self._dates = df.index.tolist()
		if self._date not in self._dates:
			self._dates.append(self._date)

		for i, sensor in enumerate(self._sensors):
			axes[i].set_title(sensor.name)
			axes[i].set_ylabel(sensor.units)
			low, high, avg = df[sensor.columns_names].to_numpy().transpose()
			if len(low) < len(self._dates):
				low = list(low) + [0, ]
				high = list(high) + [0, ]
				avg = list(avg) + [0, ]
			low_line, = axes[i].plot(low, label='low', marker='o')
			high_line, = axes[i].plot(high, label='high', marker='o')
			avg_line, = axes[i].plot(avg, label='avg', marker='o')
			if (i+1) > ncols*(nrows-1):
				axes[i].set_xticks(range(len(self._dates)), self._dates, rotation=45)
			else:
				axes[i].tick_params(
					axis='x',  # changes apply to the x-axis
					which='both',  # both major and minor ticks are affected
					bottom=False,  # ticks along the bottom edge are off
					top=False,  # ticks along the top edge are off
					labelbottom=False,  # labels along the bottom edge are off
				)
			self.sensor_to_ax[sensor] = axes[i]
			self.sensor_to_lines[sensor] = dict(low=low_line, high=high_line, avg=avg_line)
		for i in range(len(self._sensors), len(axes)):
			axes[i].axis('off')
		return figure

	def update_plot(self):
		"""
		Met à jour le graphique contenant les données des senseurs.
		:return: None
		"""
		with self._lock:
			df = pd.read_csv(self._log_file, index_col="Date")
		for i, sensor in enumerate(self._sensors):
			low, high, avg = df.loc[self._date, sensor.columns_names]
			for line_name, new_y in zip(['low', 'high', 'avg'], [low, high, avg]):
				y = self.sensor_to_lines[sensor][line_name].get_ydata()
				y[self._dates.index(self._date)] = new_y
				self.sensor_to_lines[sensor][line_name].set_ydata(y)
			self.sensor_to_ax[sensor].relim()
			self.sensor_to_ax[sensor].autoscale_view()
		plt.draw()

	def join(self, *args, **kwargs):
		"""
		Set le close event.
		Join le processus courant.
		"""
		self._close_event.set()
		return super(PlotProcess, self).join(*args, **kwargs)

