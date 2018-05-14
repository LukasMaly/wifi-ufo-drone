import logging
import sys
import time

import pygame

from dronecontrol import DroneControl


def clamp(n, minn, maxn): return max(min(maxn, n), minn)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting keyboard control app")
    pygame.init()
    screen = pygame.display.set_mode((0, 0))

    drone = DroneControl()
    drone.connect()

    airborne = False  # flag denoting whether the drone is airborne

    speeds = [0.3, 0.6, 1]  # list of speeds to select from (0-1)
    speed_idx = 0  # selected speed

    r = 128  # roll
    p = 128  # pitch
    t = 128  # throttle
    y = 128  # yaw

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                key = event.key

                if event.type == pygame.KEYDOWN:
                    direction = 1
                else:
                    direction = -1

                if key == 27:  # ESC
                    logging.info("Exiting...")
                    drone.stop()
                    pygame.quit()

                elif key == 32 and event.type == pygame.KEYDOWN:  # spacebar
                    if airborne:
                        drone.land()
                        airborne = False
                    else:
                        drone.take_off()
                        airborne = True

                elif key == 9 and event.type == pygame.KEYDOWN:  # tab
                    speed_idx += 1
                    if speed_idx == len(speeds):
                        speed_idx = 0
                    print("speed: {0}".format(speeds[speed_idx]))
                
                elif key == 119:  # w
                    p += int(direction * 128 * speeds[speed_idx])  # pitch forward
                elif key == 115:  # s
                    p -= int(direction * 128 * speeds[speed_idx])  # pitch backward
                elif key == 97:  # a
                    r -= int(direction * 128 * speeds[speed_idx])  # roll left
                elif key == 100:  # d
                    r += int(direction * 128 * speeds[speed_idx])  # roll righ
                elif key == 273:  # up arrow
                    t += int(direction * 128 * speeds[speed_idx])  # throttle up
                elif key == 274:  # down arrow
                    t -= int(direction * 128 * speeds[speed_idx])  # throttle down
                elif key == 275:  # right arrow
                    y += direction * 128  # yaw right
                elif key == 276:  # left arrow
                    y -= direction * 128  # yaw left

                logging.debug("roll: {}, pitch: {}, throttle: {}, yaw: {}".format(r, p, t, y))

                r = clamp(r, 0, 255)
                p = clamp(p, 0, 255)
                t = clamp(t, 0, 255)
                y = clamp(y, 0, 255)

        drone.cmd(r, p, t, y)
