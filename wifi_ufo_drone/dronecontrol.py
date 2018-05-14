import logging
import random
import threading
import time

from scapy.all import *


UDP_HEARTBEAT_DATA = bytearray([0x63, 0x63, 0x01, 0x00, 0x00, 0x00, 0x00])

FLY_DRONE_DATA = bytearray([0x63, 0x63, 0x0a, 0x00, 0x00,
                            0x08, 0x00, 0x66, 0x80, 0x80, 0x80, 0x80, 0x00, 0x00, 0x99])

class DroneControl(object):
    """Base drone control class which handles connecting to the drone
    and sending commands for controlling the drone.
    """

    def __init__(self):
        self._src = '192.168.0.2'
        self._dst = '192.168.0.1'
        self._iface = 'en0'
        self._tcp_dport = 7060
        self._udp_dport = 40000
        self._udp_sport = random.randint(32768, 49152)

    def tcp_heartbeat_worker(self):
        """TCP hearbeat"""
        while True:
            time.sleep(0.05)
            sport = random.randint(32768, 49152)
            SYN = TCP(sport=sport, dport=self._tcp_dport, flags='S', seq=0)
            SYNACK = sr1(IP(src=self._src, dst=self._dst, ttl=63)/SYN, iface=self._iface, verbose=0)

    def udp_heartbeat_worker(self):
        """UDP heartbeat"""
        sport = random.randint(32768, 49152)
        packet = IP(src=self._src, dst=self._dst, id=random.randint(0, 65535), ttl=63) / UDP(sport=sport, dport=self._udp_dport) / raw(UDP_HEARTBEAT_DATA)
        while True:
            time.sleep(1)
            send(packet, iface=self._iface, verbose=0)

    def connect(self):
        """Initiates connection on the TCP and UDP ports. This must be run
        before attempting to send control commands to the quadcopter.
        """
        workers = [self.tcp_heartbeat_worker, self.udp_heartbeat_worker]
        for worker in workers:
            t = threading.Thread(target=worker)
            t.start()

    def checksum(self, data):
        """The flight data has to be passed through a checksum.

        Returns:
            the 8 bit xor checksum of the data
        """
        return_data = (data[0] ^ data[1] ^ data[2] ^ data[3] ^ data[4])
        return return_data

    def cmd(self, r=128, p=128, t=128, y=128, m=0):
        """Send the flight command controls.

        Args:
            r (int): 0-255 for the roll of the drone, 128 is the middle
            p (int): 0-255 for the pitch of the drone, 128 is the middle
            t (int): 0-255 for the throttle of the drone, 0 is no throttle
            y (int): 0-255 for the yaw of the drone, 128 is middle
            m (int): 0: do nothing, 1: take off, 2: land, 4: stop
        """
        droneCmd = FLY_DRONE_DATA[:]
        droneCmd[8] = r
        droneCmd[9] = p
        droneCmd[10] = t
        droneCmd[11] = y
        droneCmd[12] = m
        droneCmd[13] = self.checksum(droneCmd[8:13])
        packet = IP(src=self._src, dst=self._dst, id=random.randint(0, 65535), ttl=63) / UDP(sport=self._udp_sport, dport=self._udp_dport) / raw(droneCmd)
        send(packet, iface=self._iface, verbose=0)

    def take_off(self):
        """Send the takeoff command for the drone.
        """
        logging.info("Taking off...")
        begin_time = time.time()
        while time.time() - begin_time < 1:
            self.cmd(m=1)
        logging.info("Took off")

    def land(self):
        """Send the land command for the drone.
        """
        logging.info("Landing...")
        begin_time = time.time()
        while time.time() - begin_time < 1:
            self.cmd(m=2)
        logging.info("Landed")

    def stop(self):
        """Send the hard stop for the drone. If it is flying and this is called,
        it will fall down.
        """
        logging.info("Stopping...")
        begin_time = time.time()
        while time.time() - begin_time < 1:
            self.cmd(m=4)
        logging.info("Stopped")


if __name__ == "__main__":
    drone = DroneControl()
    drone.connect()

    time.sleep(1)

    drone.take_off()

    for i in range(20):
        drone.cmd()

    drone.land()
