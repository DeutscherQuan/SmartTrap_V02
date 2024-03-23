#!/usr/bin/env python

import device_patches       # Device specific patches for Jetson Nano (needs to be before importing cv2)
import time
import datetime
import cv2
import os
import sys
import numpy as np
import pyrebase
import signal
import glob
import socket
import psutil

from edge_impulse_linux.image import ImageImpulseRunner


runner = None

today = datetime.datetime.now()
config = {
  "apiKey": "AIzaSyDQzoT9FMh9wVGVLrF6oT8PUIaX8gOsMlQ",
  "authDomain": "test-5b0a6.firebaseapp.com",
  "databaseURL": "https://test-5b0a6-default-rtdb.firebaseio.com",
  "projectId": "test-5b0a6",
  "storageBucket": "test-5b0a6.appspot.com",
  "messagingSenderId": "408527207975",
  "appId": "1:408527207975:web:4b51fe74fe1c82192a1802",
  "measurementId": "G-BDW2J9WDZB"
 }


firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
database = firebase.database()

ESP32_IP = '172.20.10.2'	# ESP32 IP
ESP32_PORT = 1234   		# ESP32 Port          

# Create socket TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def print_mem_usage():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_usage = memory_info.rss
    memory_usage_mb = memory_usage / (1024*1024)
    print(f"Mem: {memory_usage_mb:.2f} MB")

def main():
    model = './AutoEntangleModel.eim'
    image_directory = '/home/autoentangle2023/AutoEntangle2023/Realtime_Data'
    detection_result_directory = '/home/autoentangle2023/AutoEntangle2023/Detection_Result'
    dir_path = os.path.dirname(os.path.realpath(__file__))
    modelfile = os.path.join(dir_path, model)
    

    with ImageImpulseRunner(modelfile) as runner:
        try:
            model_info = runner.init()
            print()
            print("**************************Savvy Mindful Trap**************************")
            print("--------------------------------------------")
            print("CLASSIFICATION PROCESS BEGIN...")
            print("--------------------------------------------")
            

            labels = model_info['model_parameters']['labels']

            image_files = glob.glob(os.path.join(image_directory, '*.jpg'))
            image_files.extend(glob.glob(os.path.join(image_directory, '*.png')))
            if not image_files:
                print('No image files found in', image_directory)
                exit(1)

            image_files.sort(key=os.path.getmtime)
            newest_image = image_files[-1]
            input_image = newest_image
            img = cv2.imread(input_image)
            if img is None:
                print('Failed to load image', input_image)
                exit(1)
           

            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            #print_mem_usage()

            features, cropped = runner.get_features_from_image(img)
            
           
            res = runner.classify(features)
            
            

            if "classification" in res["result"].keys():
                print('Result (%d ms.) ' % (res['timing']['dsp'] + res['timing']['classification']), end='')
                for label in labels:
                    score = res['result']['classification'][label]
                    print('%s: %.2f\t' % (label, score), end='')
                print('', flush=True)
		
		# Print results
            elif "bounding_boxes" in res["result"].keys():
                yellow_flies_quantity = len(res["result"]["bounding_boxes"])
                dsp_time = res['timing']['dsp']
                classification_time = res['timing']['classification']
                total_time = dsp_time + classification_time
                #print_mem_usage()
                print("DONE!")
                print('Yellow flies quantity: %d' % yellow_flies_quantity)
                print('Time: {} ms'.format(total_time))
		
		# Declare image variables
		# Detect and send the newest image in the Folder
                for bb in res["result"]["bounding_boxes"]:
                    cropped = cv2.rectangle(cropped, (bb['x'], bb['y']), (bb['x'] + bb['width'], bb['y'] + bb['height']), (255, 0, 0), 1)
                    
                      

################################################################################################
                    output_file_name = os.path.splitext(os.path.basename(newest_image))[0]
                    output_file_extension = os.path.splitext(os.path.basename(newest_image))[1]
                    output_file = os.path.join(detection_result_directory, output_file_name + '-result' + output_file_extension)
                    cv2.imwrite(output_file, cv2.cvtColor(cropped, cv2.COLOR_RGB2BGR))

                try:
                    signal.alarm(60)
                    print("--------------------------------------------")
                    print("SENDING DATA TO USER DASHBOARD...")
                    database.child("Yellow Flies Quantity").push(yellow_flies_quantity)
                    time.sleep(0.2)
                    storage.child(os.path.basename(newest_image)).put(newest_image)
                    #print("Sent", os.path.basename(newest_image), "to User Dashboard!")
                    print("--------------------------------------------")
                    print("Sent data to User Dashboard!")
                    print("DONE!")
                    time.sleep(1)
                    signal.alarm(0)
                except Exception as e:
                    signal.alarm(0)
                    print(e)
                    print("Reconnecting...")
                    time.sleep(10)
                    print("Failed to send data to User Dashboard")
                    pass

                if yellow_flies_quantity == 0:
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                    try:
                        signal.alarm(10)
                    # TCP Connection with ESP32 establishment
                        client_socket.connect((ESP32_IP, ESP32_PORT))
                        print("--------------------------------------------")
                        print("REPLACING STICKY PLATE...")
                        print("--------------------------------------------")

                        # Send "1" to ESP32
                        signal_val = '1'
                        client_socket.sendall(signal_val.encode())
                        print("DONE!")
                        print("STICKY PLATE REPLACED!")
                        signal.alarm(0)
                    except Exception as exc:
                        signal.alarm(0)
                        print ("Failed to connect to ESP32!")
                        print(exc)
                        pass

                    finally:
                        # Close connection and socket
                        client_socket.close()

        except Exception as e:
            print(e)
        finally:
            print("FINISH!")
            if runner:
                runner.stop()

if __name__ == "__main__":
    main()


