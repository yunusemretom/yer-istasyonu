from pymavlink import mavutil
import time
import pymavlink.mavutil as utility
import pymavlink.dialects.v20.all as dialect
import geopy.distance

class MavlinkController:
    def __init__(self):
        #self.master = mavutil.mavlink_connection('udpin:localhost:14551')
        self.TARGET_LOCATIONS = [
            {
                "latitude": -35.36130812,
                "longitude": 149.16114736,
                "altitude": 30
            },
            {
                "latitude": -35.36579988,
                "longitude": 149.16302080,
                "altitude": 40
            }
        ]
        # vehicle's current location
        self.current_location = {
            "latitude": 0.0,
            "longitude": 0.0
        }

        # vehicle's target location
        self.target_location = {
            "latitude": 0.0,
            "longitude": 0.0,
            "distance": 0.0
        }

        self.kanal_sayısı = 8
        self.zaman = time.time()

    def connection_port(self, port = 'udpin:localhost:14551'):
        #self.master = mavutil.mavlink_connection(port)
        try:
            self.master = mavutil.mavlink_connection("/dev/ttyACM0", baud=57600) # Bağlantı portu burada yazılmalı
        except:
            self.master = mavutil.mavlink_connection("/dev/ttyACM1", baud=57600) # Bazen bağlantı kopup yeniden geldiği zaman diğer porta geçiş yapabiliyor. Bunun için yedek port.


        self.kanal_sayısı = 8
        self.zaman = time.time()
        print("Waiting for heartbeat")
        self.master.wait_heartbeat()
        print("Hartbeat ok.")

    def wait_for_heartbeat(self):
        print("Waiting for heartbeat")
        self.master.wait_heartbeat()

    def arm(self):
        self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0, 1, 0, 0, 0, 0, 0, 0
        )
        print("Waiting for the vehicle to arm")
        self.master.motors_armed_wait()
        print('Armed!')

    def disarm(self):
        self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0, 0, 0, 0, 0, 0, 0, 0
        )
        print("Waiting for the vehicle to disarm")
        self.master.motors_disarmed_wait()
        print('Disarmed!')

    def set_rc_channel_pwm(self, channel_id, pwm=1500):
        if channel_id < 1 or channel_id > 18:
            print("Channel does not exist.")
            return

        rc_channel_values = [65535 for _ in range(self.kanal_sayısı + 1)]
        rc_channel_values[channel_id - 1] = pwm

        self.master.mav.rc_channels_override_send(
            self.master.target_system,
            self.master.target_component,
            *rc_channel_values
        )

    def set_servo_pwm(self, servo_n, microseconds):
        self.master.mav.command_long_send(
            self.master.target_system, self.master.target_component,
            mavutil.mavlink.MAV_CMD_DO_SET_SERVO,
            0, servo_n + 8, microseconds, 0, 0, 0, 0, 0
        )

    def takeoff(self, takeoff_altitude=20.0):
        self.arm()
        time.sleep(1)

        takeoff_msg = self.master.mav.command_long_encode(
            target_system=self.master.target_system,
            target_component=mavutil.mavlink.MAV_COMP_ID_AUTOPILOT1,
            command=mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
            confirmation=0,
            param1=0,
            param2=0,
            param3=0,
            param4=0,
            param5=0,
            param6=0,
            param7=takeoff_altitude
        )

        self.master.mav.send(takeoff_msg)
        time.sleep(5)

    def set_position_target(self, target_latitude, target_longitude, target_altitude, vx, vy, vz):
        msg = self.master.mav.set_position_target_global_int_encode(
            time_boot_ms=int(time.time() - self.zaman),
            target_system=1,
            target_component=mavutil.mavlink.MAV_COMP_ID_AUTOPILOT1,
            coordinate_frame=mavutil.mavlink.MAV_FRAME_GLOBAL_INT,
            type_mask=mavutil.mavlink.POSITION_TARGET_TYPEMASK_VX_IGNORE |
                      mavutil.mavlink.POSITION_TARGET_TYPEMASK_VY_IGNORE |
                      mavutil.mavlink.POSITION_TARGET_TYPEMASK_VZ_IGNORE |
                      mavutil.mavlink.POSITION_TARGET_TYPEMASK_AX_IGNORE |
                      mavutil.mavlink.POSITION_TARGET_TYPEMASK_AY_IGNORE |
                      mavutil.mavlink.POSITION_TARGET_TYPEMASK_AZ_IGNORE |
                      mavutil.mavlink.POSITION_TARGET_TYPEMASK_YAW_RATE_IGNORE,

            lat_int=int(target_latitude * 1e7),
            lon_int=int(target_longitude * 1e7),
            alt=target_altitude,
            vx=int(vx * 100),
            vy=int(vy * 100),
            vz=int(vz * 100),
            afx=0,
            afy=0,
            afz=0,
            yaw=0,
            yaw_rate=0
        )

        self.master.mav.send(msg)

    def go_waypoint(self):
        self.message = dialect.MAVLink_mission_item_int_message(
            target_system=self.master.target_system,
            target_component=self.master.target_component,
            seq=0,
            frame=dialect.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,
            command=dialect.MAV_CMD_NAV_WAYPOINT,
            current=2,
            autocontinue=0,
            param1=0,
            param2=0,
            param3=0,
            param4=0,
            x=int(self.TARGET_LOCATIONS[0]["latitude"] * 1e7),
            y=int(self.TARGET_LOCATIONS[0]["longitude"] * 1e7),
            z=self.TARGET_LOCATIONS[0]["altitude"]
        )
        self.master.mav.send(self.message)

    def distance(self):
        message = self.master.recv_match(type=[dialect.MAVLink_position_target_global_int_message.msgname,
                                       dialect.MAVLink_global_position_int_message.msgname],
                                 blocking=True)

        # convert the message to dictionary
        message = message.to_dict()

        # get vehicle's current location
        if message["mavpackettype"] == dialect.MAVLink_global_position_int_message.msgname:
            self.current_location["latitude"] = message["lat"] * 1e-7
            self.current_location["longitude"] = message["lon"] * 1e-7

            # debug message
            print("Vehicle current location",
                "Latitude:", self.current_location["latitude"],
                "Longitude:", self.current_location["longitude"])

        # get vehicle's target location
        if message["mavpackettype"] == dialect.MAVLink_position_target_global_int_message.msgname:
            self.target_location["latitude"] = message["lat_int"] * 1e-7
            self.target_location["longitude"] = message["lon_int"] * 1e-7

            # calculate target location distance
            distance = geopy.distance.GeodesicDistance((self.current_location["latitude"],
                                                        self.current_location["longitude"]),
                                                    (self.target_location["latitude"],
                                                        self.target_location["longitude"])).meters
            self.target_location["distance"] = distance

            # reached target location
            if distance < 1:
               self.land() 
               

            # debug message
            """
            print("Vehicle target location",
                "Latitude:", self.target_location["latitude"],
                "Longitude:", self.target_location["longitude"],
                "Distance:", self.target_location["distance"])
            """

            degerler = {"latitude": self.target_location["latitude"],
            "longitude":self.target_location["longitude"],
            "distance": self.target_location["distance"]}

            return degerler

    def land(self):
        land_command = dialect.MAVLink_command_long_message(
            target_system=self.master.target_system,
            target_component=self.master.target_component,
            command=dialect.MAV_CMD_NAV_LAND,
            confirmation=0,
            param1=0,
            param2=0,
            param3=0,
            param4=0,
            param5=0,
            param6=0,
            param7=0
        )
        self.master.mav.send(land_command)

    def change_mode(self,FLIGHT_MODE = "GUIDED"):
        flight_modes = self.master.mode_mapping()
        set_mode_message = dialect.MAVLink_command_long_message(
            target_system=self.master.target_system,
            target_component=self.master.target_component,
            command=dialect.MAV_CMD_DO_SET_MODE,
            confirmation=0,
            param1=dialect.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
            param2=flight_modes[FLIGHT_MODE],
            param3=0,
            param4=0,
            param5=0,
            param6=0,
            param7=0
        )

        self.master.mav.send(set_mode_message)

    def current_location_get(self):
        message = self.master.recv_match(type=[dialect.MAVLink_position_target_global_int_message.msgname,
                                       dialect.MAVLink_global_position_int_message.msgname])

        # convert the message to dictionary
        try:  
            message = message.to_dict()
            x,y=0,0
            if message["mavpackettype"] == dialect.MAVLink_global_position_int_message.msgname:
                x = message["lat"] * 1e-7
                y = message["lon"] * 1e-7

            return x,y
        except:
            pass


# Example usage:
#mav_controller = MavlinkController()
#print(mav_controller.TARGET_LOCATIONS[0])
#mav_controller.connection_port()
#mav_controller.wait_for_heartbeat()
#mav_controller.takeoff(20)
#mav_controller.go_waypoint()
#mav_controller.set_servo_pwm(1,1700)
#mav_controller.set_position_target(-35.3631816, 149.1652138, 10, 0.2, 0.2, 0.2)
#mav_controller.change_mode("STABILIZE")
