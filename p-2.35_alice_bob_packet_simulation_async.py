"""
P-2.35: Write a set of Python classes that can simulate an Internet application in
which one party, Alice, is periodically creating a set of packets that she
wants to send to Bob. An Internet process is continually checking if Alice
has any packets to send, and if so, it delivers them to Bob's computer, and
Bob is periodically checking if his computer has a packet from Alice, and,
if so, he reads and deletes it.
"""

import asyncio
import logging

from random import randint
from typing import NamedTuple

# Set logging parameters
logger = logging.getLogger()
logger.setLevel(logging.INFO)
console = logging.StreamHandler()
logger.addHandler(console)

class Packet(NamedTuple):
    sender: str
    size: int

class Client:
    def __init__(self, name, speed, buffer: asyncio.Queue):
        self.name = name
        self.buffer = buffer
        self.speed = speed

    async def simulate_idle(self):
        delay = randint(1, 3)
        logging.info(f"{self.name} is idling for {delay} seconds.")
        await asyncio.sleep(delay)

    async def simulate_work(self):
        delay = randint(1, 1 + 15 // self.speed)
        logging.info(f"{self.name} is working.")
        for _ in range(100):
            await asyncio.sleep(delay / 100)

    async def send(self):
        while True:
            await self.simulate_work()
            packet = Packet(self.name, randint(4, 512))
            await self.buffer.put(packet)
            logging.info(f"{self.name} sent a packet of size {packet.size} bytes to the queue.")
            await self.simulate_idle()

    async def receive(self):
        while True:
            total_bytes = 0
            iter = 0
            await self.simulate_work()
            while not self.buffer.empty():
                packet = await self.buffer.get()
                total_bytes += packet.size
                iter += 1
                logging.info(f"{self.name} received {packet.size} bytes from {packet.sender}")
                self.buffer.task_done()   
            if total_bytes != 0 and iter != 1:
                logging.info(f"Total {total_bytes} bytes received.")
            await self.simulate_idle()

async def main():
    q = asyncio.Queue()
    a = Client("Alice", 1, q)
    b = Client("Bob", 0.5, q)

    # wrap class coroutines into asyncio Tasks
    t1 = asyncio.create_task(a.send())
    t2 = asyncio.create_task(b.receive())

    await asyncio.gather(t1, t2)

if __name__ == "__main__":
    asyncio.run(main())