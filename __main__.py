import src.sensors.thermometer as th
from src.app import App
import multiprocessing as mp

if __name__ == '__main__':
	app = App(
		sensors=[th.Thermometer(0), ],
		seconds_per_day=1,
	)
	app.run_single_day("2013-12-21")
