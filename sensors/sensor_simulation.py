import paho.mqtt.client as mqtt
import random
import time

# Работа датчиков
smart_sensors = True
# Стартовое значение параметров на датчиках
start_value = 1000

# Соединение с нашим брокером
client = mqtt.Client()
client.connect('localhost', 1883)


# Класс датчика
class Sensor:
    def __init__(self, id_sensor, state, value):
        self.id_sensor = id_sensor
        self.state = state
        self.value = value

    def set_value(self):
        # Свободно
        if self.state:
            self.value = random.randint(start_value - 25, start_value + 25)
        # Занято
        else:
            self.value = random.randint(start_value * 3 - 25, start_value * 3 + 25)

    def get_value(self):
        return self.value

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state


# Инициализация обьектов датчиков
sensors = {
    'sensor_1': Sensor(1, True, start_value),
    'sensor_2': Sensor(2, True, start_value),
    'sensor_3': Sensor(3, True, start_value),
    'sensor_4': Sensor(4, True, start_value),
    'sensor_5': Sensor(5, True, start_value),
}

# Симуляция реальной парковки
while True:
    print('---------------------------')

    print('Свободные парковочные места: ')
    for i in sensors:
        x = sensors.get(i)
        if x.state:
            print('Парковочное место №', x.id_sensor)
            x.set_value()
    print('---------------------------')

    print('Занятые парковочные места: ')
    for i in sensors:
        x = sensors.get(i)
        if not x.state:
            print('Парковочное место №', x.id_sensor)
            x.set_value()
    print('---------------------------')

    x = input('Вы хотите занять место? 1 - да, 2 - нет, 3 - сброс ')
    if x == '1':
        print('---------------------------')
        y = int(input('Какое место вы хотите занять? Введите номер свободного места: '))
        if 1 <= y <= 5:
            for i in sensors:
                x = sensors.get(i)
                if y == x.id_sensor and x.state:
                    print('Вы заняли место!')
                    x.set_state(False)
                    x.set_value()
                    client.publish(f"sensors/sensor_{x.id_sensor}", x.get_value())
                else:
                    print('Это место занято! Выберите другое место')
                    break
                break
        else:
            print('Вы ввели неверное значение, нужно вводить число от 1 до 5')
            break

    elif x == '2':
        print('---------------------------')
        for i in sensors:
            x = sensors.get(i)
            client.publish(f"sensors/sensor_{x.id_sensor}", x.get_value())
        print('Вы не стали парковаться')

    elif x == '3':
        print('---------------------------')
        for i in sensors:
            x = sensors.get(i)
            x.set_state(True)
            x.set_value()
            client.publish(f"sensors/sensor_{x.id_sensor}", x.get_value())
        print('Датчики приведены в изначальное состояние и данные отправлены на брокер!')

    else:
        print('Вы ввели неверное значение')
        pass
