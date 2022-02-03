import pandas as pd


class CleanAustinWeather:

	def __init__(self, path: str = "austin_weather.csv"):
		self.path = path

	def clean(self, output: str = None):
		data = pd.read_csv(self.path)
		data = data.replace("T", 0.0)
		data = data.replace("-", 0.0)
		# data = data.drop([data.columns[0], data.columns[1]], axis=1)
		if output is None:
			output = self.path
		data.to_csv(output)


if __name__ == '__main__':
	c = CleanAustinWeather()
	c.clean()
