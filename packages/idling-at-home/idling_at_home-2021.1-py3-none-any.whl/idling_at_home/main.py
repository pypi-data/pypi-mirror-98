#!/usr/bin/env python3

import argparse
import asyncio
import logging
import os
import subprocess
import time

import psutil
from FoldingAtHomeControl import FoldingAtHomeController, PyOnMessageTypes

from .idle import get_idle_time


class IdleChecker:
    def __init__(
        self,
        check_battery=False,
        battery_low=35.0,
        battery_high=95.0,
        idle_time=60.0,
        afterburner_path="C:/Program Files (x86)/MSI Afterburner/MSIAfterburner.exe",
        folding_afterburner_profile=None,
        idling_afterburner_profile=None,
    ):
        self.check_battery = check_battery
        self.battery_low = battery_low
        self.battery_high = battery_high
        self.idle_time = idle_time
        self.afterburner_path = afterburner_path
        self.folding_afterburner_profile = folding_afterburner_profile
        self.idling_afterburner_profile = idling_afterburner_profile
        self.running = False

    async def stop(self, controller):
        if self.running:
            logging.info("Stopping")
            self.running = False
            await controller.pause_all_slots_async()
            if self.idling_afterburner_profile:
                self.apply_gpu_profile(self.idling_afterburner_profile)

    async def start(self, controller):
        if not self.running:
            logging.info("Starting")
            self.running = True
            if self.folding_afterburner_profile:
                self.apply_gpu_profile(self.folding_afterburner_profile)
            await controller.unpause_all_slots_async()

    def battery_is_high(self):
        if self.check_battery:
            battery = psutil.sensors_battery()
            return battery.percent >= self.battery_high
        return True

    def battery_is_low(self):
        if self.check_battery:
            battery = psutil.sensors_battery()
            return battery.percent < self.battery_low
        return False

    def is_idle(self):
        idle_time_ms = int(self.idle_time * 1000)
        elapsed = get_idle_time()
        return elapsed > idle_time_ms

    def apply_gpu_profile(self, profile):
        subprocess.run(
            [
                self.afterburner_path,
                "-profile{}".format(profile),
            ]
        )

    async def run(self):
        controller = FoldingAtHomeController("localhost")
        while True:
            await controller.try_connect_async(self.idle_time)
            if self.is_idle() and self.battery_is_high():
                await self.start(controller)
            elif not self.is_idle() or self.battery_is_low():
                await self.stop(controller)
            time.sleep(self.idle_time / 2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-m",
        "--min-battery",
        type=float,
        help="Stop folding when the battery percentage goes below this value. [0, 100]",
        default=30.0,
    )
    parser.add_argument(
        "-M",
        "--max-battery",
        type=float,
        help="Start folding when the battery percentage goes above this value. [0, 100]",
        default=95.0,
    )
    parser.add_argument(
        "-c",
        "--check-battery",
        action="store_true",
        help="Start/stop folding based on battery percentage.",
    )
    parser.add_argument(
        "-t",
        "--idle-time",
        type=float,
        help="The length of time in seconds that the machine must be idle before beginning to fold.",
        default=60.0,
    )
    parser.add_argument(
        "-a",
        "--afterburner-path",
        help="The path to the MSI Afterburner binary.",
        default="C:/Program Files (x86)/MSI Afterburner/MSIAfterburner.exe",
    )
    parser.add_argument(
        "-f",
        "--folding-gpu-profile",
        help="The Afterburner profile to apply when folding.",
    )
    parser.add_argument(
        "-i",
        "--idling-gpu-profile",
        help="The Afterburner profile to apply when idling.",
    )
    args = parser.parse_args()

    root = logging.getLogger()
    root.setLevel(logging.INFO)

    checker = IdleChecker(
        check_battery=args.check_battery,
        battery_low=args.min_battery,
        battery_high=args.max_battery,
        idle_time=args.idle_time,
        afterburner_path=args.afterburner_path,
        folding_afterburner_profile=args.folding_gpu_profile,
        idling_afterburner_profile=args.idling_gpu_profile,
    )

    while True:
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(checker.run())
        except Exception as e:
            logging.error(str(e))
        time.sleep(args.idle_time / 2)


if __name__ == "__main__":
    main()
