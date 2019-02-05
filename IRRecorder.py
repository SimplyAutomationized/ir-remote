import json
import serial
import time, os

debug = True


class IRRecorder:
		def __init__(self, serialport):
				self.serialPort = serialport
				self.connected = False
				self.port = serialport
				self.baud = 9600
				self.serial_port = serial.Serial(self.port, self.baud, timeout=1)
				self.runLoop = True
				self.keys = {}
				self.load_file()
				self.read_from_port()

		def load_file(self):
				if os.access("keys.json", os.R_OK):
						f = open('keys.json', 'r')
						self.keys = json.loads(f.readlines())
						f.close()
				else:
						self.keys = {}

		def write_to_file(self, key, data):
				self.keys[key] = data
				json_file = json.dumps(self.keys, sort_keys=True, indent=2)
				f = open('keys.json', 'w')
				f.write('{0}'.format(json_file))
				f.close()

		def read_from_port(self):
				print 'reading from port', self.port
				while not self.connected:
						self.connected = True
						while self.runLoop:
								# try:
								data = bytearray(self.serial_port.read(3))
								if len(list(data)) > 0 and len(list(data)) >= 3:
										print (list(data))
										key = raw_input('enter key: ')
										self.write_to_file(key, list(data))


if __name__ == '__main__':
		ir = IRRecorder('/dev/ttyS0')
