## LiDAR Sensor Data Processing with SICK TiM561-2050101 

This repository contains a Python script to interface and process data from the SICK TiM561-2050101 LiDAR sensor. The script connects to the sensor, captures and decodes the data, filters it based on distance and viewing angle, and makes it available for further usage. 

### Smart Sprayer System

The script in this repository was used in the development of an updated version of a smart sprayer system, as described in the paper by Partel, V., Costa, L., and Ampatzidis, Y. (2021) titled "Smart tree crop sprayer utilizing sensor fusion and artificial intelligence" published in Computers and Electronics in Agriculture.

This updated version uses an industrial lidar for reliability and later production and comercialization of the system.

The smart sprayer system is a groundbreaking innovation that uses sensor fusion and artificial intelligence (AI) to optimize the application of crop sprays in tree plantations. It collects data from a range of sensors including the SICK TiM561-2050101 LiDAR sensor, as well as a camera for real-time crop imaging. The AI analyzes this data to determine the presence and structure of the tree canopy, and then adjusts the operation of the sprayer in real time, enabling it to apply pesticides and fertilizers more efficiently.

By controlling the spray application based on actual tree presence and structure, the smart sprayer system minimizes overspray, reduces the amount of chemicals used, improves the accuracy of application, and can significantly reduce the environmental impact of tree crop farming.

A video showcasing the system in action can be found [here](https://www.youtube.com/watch?v=qRd4g44b2lk). This video demonstrates how the system effectively controls the sprayer operation based on the real-time sensor data, validating the value and effectiveness of sensor fusion and AI in precision agriculture.

### SICK TiM561-2050101 LiDAR Sensor

The [SICK TiM561-2050101](https://www.sick.com/us/en/lidar-sensors/2d-lidar-sensors/tim/tim561-2050101/p/p369446) is a robust and accurate 2D LiDAR sensor that offers a wide range of features, making it suitable for indoor and outdoor use in various applications like robotics, autonomous vehicles, security, and navigation. The sensor has a scanning range of 270 degrees and a maximum range of 10m (outdoors) or 20m (indoors).

### NVIDIA Jetson Xavier NX

This script was created for a sensor fusion embedded system on an [NVIDIA Jetson Xavier NX](https://developer.nvidia.com/embedded/jetson-xavier-nx-devkit). Jetson Xavier NX is a small, powerful computer designed for AI applications and edge computing. The system uses the data processed by this script in conjunction with other sensor data to understand and interact with its environment.

### Dependencies 

This script requires the following libraries to be installed:

- [socket](https://docs.python.org/3/library/socket.html) - for network communication with the sensor
- [numpy](https://numpy.org/) - for data processing and mathematical operations
- [threading](https://docs.python.org/3/library/threading.html) - for concurrent execution
- [collections](https://docs.python.org/3/library/collections.html) - for data handling
- [time](https://docs.python.org/3/library/time.html) - for controlling the timing and execution of code

The standard Python libraries (socket, threading, collections, and time) come preinstalled with Python.

### How to Use

1. Clone the repository:
```bash
git clone https://github.com/your_username/your_repository.git
```

2. Navigate to the repository:
```bash
cd your_repository
```

3. Run the script:
```bash
python lidar_script.py
```

This script is intended to be used as a module in a larger system. The 'get' method can be used to retrieve the latest LiDAR data, which is continually updated in the background.

Please note that you will need to adjust the IP address of your sensor in the script (default is set to "192.168.0.1").
