"""
This script establishes a connection with a SICK TiM561-2050101 LiDAR sensor, then collects and processes the incoming data.
The LiDAR sensor is interfaced over a network socket. The data received from the sensor is in the form of datagrams which are
then decoded into a usable form.

The script uses threading to handle data collection and processing concurrently. The main thread of execution connects to 
the LiDAR sensor and starts a secondary thread that is responsible for continuously processing the incoming data.

Processing of data involves cleaning the raw data based on distance and viewing angle. The 'clean_datagram_by_distance' 
function filters out data points that are outside of a certain range of distances from the sensor. This is done to focus on 
objects that are within a specific range and eliminate potential noise from the data.

The 'clean_datagram_by_angle' function, on the other hand, filters out data points that are outside of a specific viewing 
angle from the sensor. This function allows the script to focus on objects that are in front of the sensor, effectively 
limiting the field of view.

Once the data is cleaned, it is stored in a variable, and can be retrieved by calling the 'get' function. This way, other 
parts of a larger system could access the LiDAR data while it is being continuously updated in the background.

The main loop in the script continuously retrieves and prints the cleaned LiDAR data. The secondary thread can be stopped 
by calling the 'kill' function which sets a flag to stop the loop in the 'run' method.

This script is intended to be used as a module in a larger system, such as a robotic or an autonomous vehicle system where 
LiDAR sensors are used for object detection or navigation purposes.
"""

import socket
import numpy as np
from threading import Thread
import time
import collections

# The SICK TiM561-2050101 sensor has the following IP. 
SENSOR_IP = "192.168.0.1"

# Defines a named tuple that can hold datagram information from a SICK TiM561-2050101 Lidar device.
Sick561Datagram = collections.namedtuple("sick561_datagram", ["TypeOfCommand", "Command", "VersionNumber",
                                                               "DeviceNumber", "SerialNumber", "DeviceStatus1",
                                                               "DeviceStatus2", "TelegramCounter", "ScanCounter",
                                                               "TimeSinceStartup", "TimeOfTransmission", 
                                                               "InputStatus1", "InputStatus2", "OutputStatus1",
                                                               "OutputStatus2", "ScanningFrequency", 
                                                               "MeasurementFrequency", "NumberOfEncoders",
                                                               "NumberOf16bitChannels", "MeasuredDataContents",
                                                               "ScalingFactor", "ScalingOffset", "StartingAngle",
                                                               "AngularStepWidth", "NumberOfData", "Data"])
                                                              
# Helper function to read bytes from a socket one at a time.
def bytes_from_socket(socket):
    while True:
        data = socket.recv(256)
        for byte in data:
            yield bytes([byte])

# Helper function to read datagrams from a socket. Datagrams are defined as byte sequences starting with STX and ending with ETX.
def datagrams_from_socket(socket):
    STX = b'\x02'
    ETX = b'\x03'

    byte_generator = bytes_from_socket(socket)

    while True:
        datagram = b''
        # Consume bytes until STX
        for byte in byte_generator:
            if byte == STX:
                break

        # Consume bytes until ETX, storing them in datagram
        for byte in byte_generator:
            if byte == ETX:
                break
            datagram += byte
        yield datagram

# Helper function to parse numbers in datagrams. Numbers can be either decimal (with a leading +/- sign) or hexadecimal.
def parse_number(nbr_str):
    if b'+' in nbr_str or b'-' in nbr_str:
        return int(nbr_str)
    else:
        return int(nbr_str, 16)

# Function to decode a datagram into its constituent parts.
def decode_datagram(datagram):
    items = datagram.split(b' ')
    header = {}
    header['TypeOfCommand'] = items[0].decode('ascii')
    header['Command'] = items[1].decode('ascii')
    header['VersionNumber'] = parse_number(items[2])
    header['DeviceNumber'] = parse_number(items[3])
    header['SerialNumber'] = items[4].decode('ascii')
    header['DeviceStatus1'] = parse_number(items[5])
    header['DeviceStatus2'] = parse_number(items[6])
    header['TelegramCounter'] = parse_number(items[7])
    header['TimeSinceStartup'] = parse_number(items[9])
    header['TimeOfTransmission'] = parse_number(items[10])
    header['AngularStepWidth'] = parse_number(items[24])
    header['NumberOfData'] = parse_number(items[25])
    header['Data'] = [parse_number(x) / 1000 for x in items[26:26+header['NumberOfData']]]

    # Only process datagrams that contain Lidar scan data and where the device status is OK.
    if header['TypeOfCommand'] != 'sSN' or header['Command'] != 'LMDscandata' or header['DeviceStatus1'] != 0 or header['DeviceStatus2'] != 0:
        return None

    return header

# Helper function to convert degrees to radians
def degrees_to_radians(degrees):
    return np.radians(degrees)

# The main Lidar class that encapsulates the functionality of a Lidar device.
class lidar(Thread):
    def __init__(self, IP=SENSOR_IP):
        # Call the Thread class's init function
        Thread.__init__(self)

        self.IP = IP
        self.condition = False
        self.stop = False
        
        self.ds = None # data from lidar, start as none

        # Setup the Lidar device parameters
        self.min_distance = 0.1    #min distance for lidar in meters
        self.max_distance = 3       # max distance for lidar in meters
        
        self.datagram_size = 811 # resolution of the lidar sensor
        self.sensor_angle = 270 # angle covered by the lidar sensor in degrees

        ang_start = degrees_to_radians(-45) # the SICK TiM lidar has 270 degrees of view, from -45 to 225
        ang_stop = degrees_to_radians(225)
        self.angles = np.linspace(ang_start, ang_stop, num=self.datagram_size, endpoint=True)


    # Connects to the Lidar device over a network socket.
    def connect(self):
        self.lidar = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lidar.settimeout(10)   #in seconds
        try:
            self.lidar.connect((self.IP, 2112))
        except socket.timeout:
            print("Cannot connect to lidar due to timeout")
        except OSError:
            print("Cannot connect to lidar due to network")
        else:
            self.lidar.settimeout(None)   #close timeout after so not break the connection
            # activate stream
            self.lidar.send(b'\x02sEN LMDscandata 1\x03\0')

            self.datagrams_generator = datagrams_from_socket(self.lidar)

            self.condition = True

            print("Lidar connected")

    # Returns the current Lidar scan data.
    def get(self):
        return self.ds
    
    # Stops the Lidar thread.
    def kill(self):
        self.condition = False
        self.stop = True          
        
    # Cleans the Lidar scan data based on a distance threshold.
    def clean_datagram_by_distance(self, ds):
        ds = np.where(ds > self.min_distance, ds, -1)
        ds = np.where(ds < self.max_distance, ds, -1)
        return ds

    
    # Cleans the Lidar scan data to only include a specific field of view around the center
    def clean_datagram_by_angle(self, ds, viewAngle = 30):
        #viewAngle in degrees
        cleanArraySize = int((self.datagram_size/self.sensor_angle)*(viewAngle/2))
        midpoint = len(ds) // 2
        
        # If the subarray size is even, start from one index earlier
        start = midpoint - (cleanArraySize // 2)
        if cleanArraySize % 2 == 0:
            start -= 1
            
        end = start + cleanArraySize
        
        # Return the cleaned data
        return ds[start:end]
    
    # The main loop that constantly processes Lidar scans
    def run(self):
        time.sleep(3) #wait for sensor to start
        print("Lidar started")
        while True:
            # Stop if the condition is met
            if self.stop:
                break
            
            # Retrieve the next datagram from the Lidar device
            datagram = next(self.datagrams_generator)
            
            # Decode the datagram into usable data
            decoded = decode_datagram(datagram)
            
            # If the decoded data is valid
            if decoded is not None:
                # Create an array from the decoded data
                ds = np.array(decoded['Data'])
                
                # Clean the data based on the distance constraints
                ds = self.clean_datagram_by_distance(ds)
                
                # Clean the data based on the viewing angle constraints
                self.ds = self.clean_datagram_by_angle(viewAngle=180)


if __name__ == "__main__":

    # Instantiate the Lidar object
    lidarsensor = lidar()

    # Connect to the Lidar device
    lidarsensor.connect()

    # Start the Lidar thread
    lidarsensor.start()

    # Continuously retrieve and print the Lidar data
    while True:
        time.sleep(0.5)
        print(lidarsensor.get())
    
    # Kill the Lidar thread when done
    lidarsensor.kill()