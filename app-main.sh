#!/bin/bash

while true
do
    current_hour=$(date +'%H')
    if [ "$current_hour" -ge 0 ] && [ "$current_hour" -lt 3 ]; then
        python3 camera_main.py
        sleep 0.1
        python3 classification.py
        #python3 ./Environment_sensor_for_jetson_nano/Code_Using_EnvironmentSensor_for_JetsonNano_.py
        #python3 ./UPS-Power-Module/UPS-Power-Module_Code/ups_display/Final_Code_Using_UPS_Power_Modules.py
	sleep 11
	#sudo rtcwake -m mem -s 10
        
        #echo "Jetson Nano is back!"
    else
	#sudo systemctl suspend
        echo "Jetson Nano is sleeping..."

    fi
done

