import src.sensors.thermometer as th
import src.sensors.dewpoint as dp
import src.sensors.humidity as hm
import src.sensors.seaPressure as sp
from src.app import App
import multiprocessing as mp

if __name__ == '__main__':
	app = App(
		sensors=[th.Thermometer(0), dp.DewPointSensor(1), hm.HumiditySensor(2), sp.SeaLevelPressure(3)],
		seconds_per_day=10,
	)
	app.run_single_day("2013-12-21")
