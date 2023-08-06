import asyncio
import asyncio_dgram
import logging
import socket
import time

from dataclasses import dataclass
from typing import AsyncGenerator, Dict, List, Optional, Tuple
from .cube import MaxCube

logger = logging.getLogger(__name__)

DISCOVERY_PORT = 23272
BIND_ADDRESS = ('', DISCOVERY_PORT)
BROADCAST_ADDRESS = ('<broadcast>', DISCOVERY_PORT)
BROADCAST_SERIAL = '*' * 10
DISCOVERY_MAGIC = b'eQ3Max'
DISCOVERY_HEADER = DISCOVERY_MAGIC + b'*\0'
DISCOVERY_CMD = b'I'
REBOOT_CMD = b'R'


@dataclass(frozen=True)
class DiscoveredCube:
    serial: str
    address: str
    rf_address: str
    version: str


@dataclass(frozen=True)
class Instance:
    cubes: Dict[str, DiscoveredCube]
    queue: asyncio.Queue[DiscoveredCube]
    loop: asyncio.AbstractEventLoop
    stream: object
    senderTask: asyncio.Task
    receiverTask: asyncio.Task
    
    def is_cross_loop(self):
        assert(self.loop is not None)
        return self.loop != asyncio.get_running_loop()
    
    async def async_stop(self):
        if self.is_cross_loop():
            await asyncio.run_coroutine_threadsafe(self.async_stop(), self.loop)
            return
        self.senderTask.cancel()
        self.receiverTask.cancel()
        asyncio.wait([self.senderTask, self.receiverTask])
        self.stream.close()

    async def async_next_update(self) -> DiscoveredCube:
        if self.is_cross_loop():
            return await asyncio.run_coroutine_threadsafe(self.async_next_update(), self)
        return await self.queue.get()

__INSTANCE = None


async def async_start(broadcast_period: float = 60.0):
    global __INSTANCE
    loop = asyncio.get_running_loop()
    assert(__INSTANCE is None and loop is not None)
    stream = await __open_stream(broadcast=True)
    try:
        senderTask = loop.create_task(__sender(stream, broadcast_period))
        receiverTask = loop.create_task(__receiver(stream))
        __INSTANCE = Instance({}, asyncio.Queue(), loop, stream, senderTask, receiverTask)
    except:
        stream.close()
        raise

async def async_stop():
    global __INSTANCE
    await __INSTANCE.async_stop()
    __INSTANCE = None

async def async_next_update(self) -> DiscoveredCube:
    return await __INSTANCE.async_stop()

def next_update(self, *, timeout=None) -> DiscoveredCube:
    assert(__is_cross_loop())
    return asyncio.run_coroutine_threadsafe(__INSTANCE.async_next_update(), __INSLOOP).result(timeout)

async def async_get_cube(self, serial: str) -> DiscoveredCube:
    if __is_cross_loop():
        return await asyncio.run_coroutine_threadsafe(self.async_get_cube(serial), __LOOP)
    return __INSTANCE.cubes.get(serial)

def get_cube(self, serial: str, *, timeout=None) -> DiscoveredCube:
    assert(__is_cross_loop())
    return asyncio.run_coroutine_threadsafe(self.async_get_cube(serial), __LOOP).result(timeout)

async def async_reboot_cube(self, serial: str):
    assert(serial != BROADCAST_SERIAL)
    if __is_cross_loop():
        await asyncio.run_coroutine_threadsafe(self.async_reboot_cube(serial), __LOOP)
        return
    msg = __cmd(REBOOT_CMD, to=serial)
    await self.stream.send(msg, (__INSTANCE.cubes[serial].address, DISCOVERY_PORT))

def reboot_cube(self, serial: str, *, timeout=None):
    assert(__is_cross_loop())
    asyncio.run_coroutine_threadsafe(self.async_reboot_cube(serial), __LOOP).result(timeout)

def __is_cross_loop():
    assert(__LOOP is not None)
    return __LOOP != asyncio.get_running_loop()

async def __open_stream(*, broadcast: bool = False):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    try:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1 if broadcast else 0)
        s.bind(BIND_ADDRESS)
        return await asyncio_dgram.from_socket(s)
    except:
        s.close()
        raise

def __cmd(cmd: bytes, to: str) -> bytes:
    return DISCOVERY_HEADER + to.encode('utf-8') + cmd

async def __sender(stream, broadcast_period: float):
    cmd = __cmd(DISCOVERY_CMD, to=BROADCAST_SERIAL)
    while True:
        await stream.send(cmd, BROADCAST_ADDRESS)
        await asyncio.sleep(broadcast_period)

def __process_reply(reply: bytes, addr: Tuple[str, int]) -> DiscoveredCube:
    if (len(reply) < 26
            or not reply.startswith(DISCOVERY_MAGIC)
            or reply[19:20] != DISCOVERY_CMD):
        return None

    serial = reply[8:18].decode('utf-8')
    rf_address = reply[21:24].hex()
    fw_version = "%d.%d.%d" % (int(reply[24]), int(reply[25] >> 4), int(reply[25] % 16))
    return DiscoveredCube(serial, addr[0], rf_address, fw_version)

async def __receiver(stream):
    while True:
        reply, addr = await stream.recv()
        print("Response from %s: %s\n" % (addr, reply.hex()))
        cube = __process_reply(reply, addr)
        if not cube:
            continue

        print("Cube detected: %s\n" % cube)
        if cube.serial not in __INSTANCE.cubes or cube != __INSTANCE.cubes[cube.serial]:
            __INSTANCE.cubes[cube.serial] = cube
            await __EVENT_QUEUE.put(cube)
