import src.sensor_loggers as sl
import src.sensors.thermometer as th

if __name__ == '__main__':
    t = th.Thermometer(12)
    s_l = sl.SensorLogger.new(t)
    print(type(s_l))