import sys
from time import sleep
import numpy as np
from scipy import interpolate
from beamngpy import BeamNGpy, Scenario, Road, Vehicle, setup_logging
import math
import time


SIZE = 1024

def main():
    setup_logging()

    beamng = BeamNGpy('localhost', 64256, home='D:/Programs/BeamNG/trunk')
    #scenario = Scenario('west_cost_usa', 'ai_sine')
    scenario = Scenario('smallgrid', 'ai_sine')

    vehicle = Vehicle('ego_vehicle', model='etk800', license='AI')

    #orig = (-769.1, 400.8, 142.8)
    orig = (-10, -1309,  0.215133)#smallgrid

    #scenario.add_vehicle(vehicle, pos=orig, rot=(0, 0, 180))
    scenario.add_vehicle(vehicle, pos=orig, rot=(1, 0, 0))#smallgrid
    scenario.make(beamng)

    #Run simulation without emg_processing_time to obtain target trajectory.
    bng = beamng.open(launch=True)
    count = 0
    index = 0
    vehicle_dynamics = []

    try:
        print('Running simulation with target trajectory.')
        bng.load_scenario(scenario)
        bng.start_scenario()
        #Set throttle to maintain speed near 7 km/h during turn.
        vehicle.control(throttle = 0.04)
        start_time = time.time()

        while True:
            bng.step(1)
                
            vehicle.update_vehicle()
            if vehicle.state['pos'][1] <= -1319 and count == 0:
                vehicle.control(steering = -1.0)
                count+= 1
            if vehicle.state['pos'][1] >= -1319 and count == 1:
                break
                
            #Store vehicle dynamics.                
            vehicle_dynamics.append(','.join(map(str,[index, time.time()-start_time,math.sqrt(vehicle.state['vel'][0]**2 + vehicle.state['vel'][1]**2), vehicle.state['pos'][0],vehicle.state['pos'][1]])))
            print('Time:' + str(time.time()-start_time) + 'Position: ' + str(vehicle.state['pos'][1]) + ' ' + 'Velocity: ' + str(math.sqrt(vehicle.state['vel'][0]**2 + vehicle.state['vel'][1]**2)))
            index+=1
    finally:
        bng.close()

    #Save target trajectory results.        
    heading = ['','time', 'speed', 'x_coordinate', 'y_coordinate']
    with open('sim_target_trajectory_left_uturn.txt', "w") as results:
        heading = map(str, heading)
        results.write(",".join(heading) + '\n' + "\n".join(str(element) for element in vehicle_dynamics))
    results.close()

    #Read total EMG signal processing time (seconds/feature) per trial from txt files.
    f = [line.rstrip('\n') for line in open('D:/Research Projects/sEMG_control_for_automobiles/putemg-downloader/putemg_examples/total_processing_time_wrist_flexion.txt')][1:]
    total_EMG_processing_time = []
    for line in f:
        total_EMG_processing_time.append(float(line))
    
    #Run simulations that delay steering initiation based based on EMG signal processing time from trials.
    for emg_processing_time in range(len(total_EMG_processing_time)):
    #for emg_processing_time in range(0,1):
        print('\n' + 'Running simulations with EMG signal processing time from trial '+str(emg_processing_time) +'.')
        bng = beamng.open(launch=True)
        count = 0
        index = 0
        vehicle_dynamics = []

        try:
            bng.load_scenario(scenario)
            bng.start_scenario()
            #Set throttle to maintain speed near 7 km/h during turn.
            vehicle.control(throttle = 0.04)
            start_time = time.time()

            while True:
                bng.step(1)
                
                vehicle.update_vehicle()
                if vehicle.state['pos'][1] <= -1319 and count == 0:
                    sleep(total_EMG_processing_time[emg_processing_time])
                    vehicle.control(steering = -1.0)
                    count+= 1
                if vehicle.state['pos'][1] >= -1319 and count == 1:
                    break
                
                #Store vehicle dynamics.                
                vehicle_dynamics.append(','.join(map(str,[index, time.time()-start_time,math.sqrt(vehicle.state['vel'][0]**2 + vehicle.state['vel'][1]**2), vehicle.state['pos'][0],vehicle.state['pos'][1]])))
                print('Time:' + str(time.time()-start_time) + 'Position: ' + str(vehicle.state['pos'][1]) + ' ' + 'Velocity: ' + str(math.sqrt(vehicle.state['vel'][0]**2 + vehicle.state['vel'][1]**2)))
                index+=1
        finally:
            bng.close()
            
        heading = ['','time', 'speed', 'x_coordinate', 'y_coordinate']
        with open('sim_results_trial_' + str(emg_processing_time) +'.txt', "w") as results:
            heading = map(str, heading)
            results.write(",".join(heading) + '\n' + "\n".join(str(element) for element in vehicle_dynamics))
        results.close()
        

if __name__ == '__main__':
    main()
