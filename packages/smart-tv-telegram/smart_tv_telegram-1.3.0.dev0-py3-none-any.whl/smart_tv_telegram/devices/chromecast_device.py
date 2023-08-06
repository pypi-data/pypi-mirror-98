import typing

import pychromecast

from . import Device, DeviceFinder, RoutersDefType, DevicePlayerFunction
from .. import Config
from ..tools import run_method_in_executor


__all__ = [
    "ChromecastDevice",
    "ChromecastDeviceFinder"
]


class ChromecastDevice(Device):
    _device: pychromecast.Chromecast

    def __init__(self, device: typing.Any):
        self._device = device
        self._device.wait()

    def get_device_name(self) -> str:
        return self._device.device.friendly_name

    async def stop(self):
        pass

    @run_method_in_executor
    def play(self, url: str, title: str):
        self._device.media_controller.play_media(url, "video/mp4", title=title)
        self._device.media_controller.block_until_active()

    def get_player_functions(self) -> typing.List[DevicePlayerFunction]:
        return []


class ChromecastDeviceFinder(DeviceFinder):
    @run_method_in_executor
    def find(self, config: Config) -> typing.List[Device]:
        return [
            ChromecastDevice(device)
            for device in pychromecast.get_chromecasts(
                timeout=config.chromecast_scan_timeout)[0]
        ]

    @staticmethod
    def is_enabled(config: Config) -> bool:
        return config.chromecast_enabled

    async def get_routers(self, config: Config) -> RoutersDefType:
        return []
