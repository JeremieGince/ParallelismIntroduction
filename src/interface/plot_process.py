import multiprocessing as mp
import time

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np


class PlotProcess(mp.Process):
	"""
	TODO
	"""
	def __init__(self, sensors, lock, log_file, date, update_dt: float = 1.0):
		super().__init__()
		self._sensors = sensors
		self._lock = lock
		self._close_event = mp.Event()
		self._log_file = log_file
		self._date = date
		self.update_dt = update_dt
		self.sensor_to_ax = {}
		self.sensor_to_lines = {}

	def run(self):
		while not os.path.exists(self._log_file) and not self._close_event.is_set():
			time.sleep(self.update_dt)

		self.create_plot()
		plt.legend()
		plt.pause(self.update_dt)
		while not self._close_event.is_set():
			self.update_plot()
			plt.pause(self.update_dt)

	def create_plot(self):
		self.sensor_to_ax.clear()
		self.sensor_to_lines.clear()

		ncols = int(np.sqrt(len(self._sensors)))
		nrows = int(len(self._sensors) / ncols)
		figure, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10, 8))
		figure.canvas.manager.full_screen_toggle()
		if isinstance(axes, plt.Axes):
			axes = np.asarray([axes])
		else:
			axes = axes.flatten()
		with self._lock:
			df = pd.read_csv(self._log_file, index_col="Date")

		X = df.index.tolist()
		if self._date not in X:
			X.append(self._date)
		for i, sensor in enumerate(self._sensors):
			axes[i].set_title(sensor.name)
			axes[i].set_ylabel(sensor.units)
			low, high, avg = df[sensor.columns_names].to_numpy().transpose()
			if len(low) < len(X):
				low = list(low) + [0, ]
				high = list(high) + [0, ]
				avg = list(avg) + [0, ]
			low_line, = axes[i].plot(low, label='low', marker='o')
			high_line, = axes[i].plot(high, label='high', marker='o')
			avg_line, = axes[i].plot(avg, label='avg', marker='o')
			if (i+1) > ncols*(nrows-1):
				axes[i].set_xticks(range(len(X)), X, rotation=45)
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

	def update_plot(self):
		with self._lock:
			df = pd.read_csv(self._log_file, index_col="Date")
		for i, sensor in enumerate(self._sensors):
			low, high, avg = df.loc[self._date, sensor.columns_names]
			for line_name, new_y in zip(['low', 'high', 'avg'], [low, high, avg]):
				y = self.sensor_to_lines[sensor][line_name].get_ydata()
				y[-1] = new_y
				self.sensor_to_lines[sensor][line_name].set_ydata(y)
			self.sensor_to_ax[sensor].relim()
			self.sensor_to_ax[sensor].autoscale_view()
		plt.draw()

	def join(self, *args, **kwargs):
		self._close_event.set()
		super(PlotProcess, self).join(*args, **kwargs)






