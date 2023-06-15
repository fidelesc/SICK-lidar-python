## LiDAR Sensor Data Processing with SICK TiM561-2050101 

This repository contains a Python script to interface and process data from the SICK TiM561-2050101 LiDAR sensor. The script connects to the sensor, captures and decodes the data, filters it based on distance and viewing angle, and makes it available for further usage. 

### Smart Sprayer System

This repository contains a script essential in the creation of an advanced smart sprayer system. This system, outlined in detail in Partel, V., Costa, L., and Ampatzidis, Y.'s 2021 paper ["Smart tree crop sprayer utilizing sensor fusion and artificial intelligence"](https://doi.org/10.1016/j.compag.2021.106556), leverages sensor fusion and AI to optimize pesticide and fertilizer applications in tree crop farming.

With the help of the SICK TiM561-2050101 LiDAR sensor and a real-time crop imaging camera, the smart sprayer analyzes the structure of tree canopies, adjusting its operations as needed. This improved system utilizes an industrial LiDAR sensor, enhancing its reliability and potential for future commercialization.

By reducing overspray and chemical usage, the smart sprayer enhances application accuracy and minimizes the environmental footprint of tree crop farming.

For a practical demonstration of the system, watch this [video](https://www.youtube.com/watch?v=qRd4g44b2lk). Further information on the project can be found in the aforementioned paper.

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

This script is intended to be used as a module in a larger system. The 'get' method can be used to retrieve the latest LiDAR data, which is continually updated in the background.

Please note that you will need to adjust the IP address of your sensor in the script (default is set to "192.168.0.1").
