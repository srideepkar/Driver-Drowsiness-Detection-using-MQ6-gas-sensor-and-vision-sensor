import time, signal, sys
import Adafruit_ADS1x15

#########################
# Globals
#########################

voltVector = [] # Vector of read voltages

#########################
# Classes and Methods
#########################


#########################
# Functions
#########################

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
#print 'Press Ctrl+C to exit'

#########################
# Main
#########################

ADS1115 = 0x01 # 16-bit ADC

# Select the gain
# gain = 6144 # +/- 6.144V
gain = 1 # +/- 4.096V
# gain = 2048 # +/- 2.048V
# gain = 1024 # +/- 1.024V
# gain = 512 # +/- 0.512V
# gain = 256 # +/- 0.256V

# Select the sample rate
# sps = 8 # 8 samples per second
# sps = 16 # 16 samples per second
# sps = 32 # 32 samples per second
# sps = 64 # 64 samples per second
# sps = 128 # 128 samples per second
sps = 250 # 250 samples per second
# sps = 475 # 475 samples per second
# sps = 860 # 860 samples per second

# Initialise the ADCs using the default mode (use appropriate I2C address)
adc = Adafruit_ADS1x15.ADS1115()

while (True):
    voltVector = []    
    volts = adc.read_adc(0, gain, sps) / 1000
    # print "MQ-6 %.6fv" % (volts)
    voltVector.append(volts)
    print(voltVector)