#!/usr/bin/env python
import math
import random
from .simple_goto import *
from dronekit import connect, VehicleMode, LocationGlobalRelative
from dronekit_sitl import SITL
import time

lat1 = 41715167
long1 = -86243146
lat2 = 41714350
long2 = -86243146
speed = 15
rate = speed/5 #pings per second
home_lat = 41.715446209367
home_long = -86.242847096132

#Coordinates
right = -86240335
left = -8624316
top = 41715167
bottom = 41714350

import argparse


def hide_black_box():
    vertical_range = top-bottom
    horizontal_range = left-right

    # Create latitude
    i=0
    rand_num = random.random()
    vertical_offset = rand_num * vertical_range
    new_latitude = bottom + vertical_offset
    new_latitude = new_latitude/1000000
    new_latitude = "%.6f" % new_latitude

    # Create longitude
    rand_num = random.random()
    horizontal_offset = rand_num * horizontal_range
    new_longitude = (left-horizontal_offset)/1000000
    new_longitude = "%.6f"%(new_longitude)
    print("Black box hidden")

    return (new_latitude, new_longitude, 0)

def calculate_path_array(start_lat, start_long):




def measure_distance_meters(lat_1, lon_1, lat_2, lon_2):
    R = 6378.137; #Radius of earth in KM
    dLat = lat_2 * math.pi / 180 - lat_1 * math.pi / 180;
    dLon = lon_2 * math.pi / 180 - lon_1 * math.pi / 180;
    a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.cos(lat_1 * math.pi / 180) * math.cos(lat_2 * math.pi / 180) * math.sin(dLon / 2) * math.sin(dLon / 2);
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a));
    d = R * c;
    return d * 1000;


def ping_distance(current_lat, current_long, goal_lat, goal_long):
    return measure_distance_meters(current_lat, current_long, goal_lat, goal_long)


def arm_and_takeoff(a_target_altitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(3)
        print("Arming motors")
        vehicle.mode = VehicleMode("GUIDED")
        vehicle.armed = True

    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Vehicle armed!")
    print("Taking off!")
    vehicle.simple_takeoff(a_target_altitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto
    #  (otherwise the command after Vehicle.simple_takeoff will execute
    #   immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= a_target_altitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
    parser.add_argument('--connect',
                        help="Vehicle connection target string. If not specified, SITL automatically started and used.")
    args = parser.parse_args()
    connection_string = args.connect
    sitl = None

    if not connection_string:
        sitl_defaults = '~/git/ardupilot/tools/autotest/default_params/copter.parm'
        sitl = SITL()
        sitl.download('copter', '3.3', verbose=True)
        sitl_args = ['-I0', '--model', 'quad', '--home=35.361350, 149.165210,0,180']
        sitl.launch(sitl_args, await_ready=True, restart=True)
        connection_string = 'tcp:127.0.0.1:5760'

    vehicle = connect(connection_string, wait_ready=True, baud=57600)

    print("Set default/target airspeed to 3")
    vehicle.airspeed = 3

    print("Going towards first point for 30 seconds ...")
    point1 = LocationGlobalRelative(41.715167, -86.243146, 50)
    vehicle.simple_goto(point1)
    black_box_location = hide_black_box()

    while vehicle.mode.name == "GUIDED":
        transition_count = 0
        current_location = vehicle.location.global_frame
        down = True
        up = False
        right = False

        if down:
            goal_location = LocationGlobalRelative(current_location[0] - (7.566222546e-4*5), current_location[1])
            vehicle.simple_goto(goal_location)
            time.sleep(2)
            if vehicle.location.global_frame[0] - goal_location <= 0.1:
                transition_count += 1
                #at bottom
                down = False
                right = True
                up = False
            else:
                down = True
                right = False
                up = False
        if right:
            goal_location = LocationGlobalRelative(current_location[0], current_location[1] + (3.76927067e-4 * 5))
            vehicle.simple_goto(goal_location)
            time.sleep(2)
            if vehicle.location.global_frame[1] - goal_location <- 0.1:
                transition_count += 1
                #gone right
                if transition_count % 2:
                    up = True
                    down = False
                    right = False
                else:
                    up = False
                    down = True
                    right = False
        if up:
            goal_location = LocationGlobalRelative(current_location[0] + (7.566222546e-4*5), current_location[1])
            vehicle.simple_goto(goal_location)
            time.sleep(2)
            if vehicle.location.global_frame[0] - goal_location <= 0.1:
                transition_count += 1
                right = True
                down = False
                up = False



