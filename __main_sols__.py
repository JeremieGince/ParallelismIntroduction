import solution.sensors.thermometer as th
import solution.sensors.dewpoint as dp
import solution.sensors.humidity as hm
import solution.sensors.seaPressure as sp
from solution.app import App

if __name__ == '__main__':
	app = App(
		sensors=[th.Thermometer(0), dp.DewPointSensor(1), hm.HumiditySensor(2), sp.SeaLevelPressure(3)],
		seconds_per_day=10,
	)
	app.run(n_day=5)