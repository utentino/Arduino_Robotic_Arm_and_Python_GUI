# Arduino controlled robotic arm with Python programmed GUI
Below is the screenshoot of the first window that will appear once the python script is started. Here we can configure serial communication between the computer (where the script is running) and the arduino to which a six-axis robotic arm equipped with servo motors is connected.

![alt text](https://github.com/utentino/Arduino_Robotic_Arm_and_Python_GUI/blob/main/configuration_window.png?raw=true)

Below, however, is the main interface screen where you can:
--> manage the movements of the six axes of the robotic arm; 
--> store its positions, the execution time of each arm movement from one position to another, and the waiting time between movements (note that these information are stored in arduino's EEPROM);
--> perform the stored actions, also continuously (note that the movements will be quite smooth and coordinated, which means that as the robotic arm changes position, each of the six servomotors will start and stop moving at the same time, regardless of the different amplitudes they have to travel, all of course very smoothly thanks to the "ServoEasing.h" library that you can see here: https://github.com/ArminJo/ServoEasing).

![alt text](https://github.com/utentino/Arduino_Robotic_Arm_and_Python_GUI/blob/main/main_window.png?raw=true)
