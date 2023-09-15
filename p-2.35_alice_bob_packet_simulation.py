"""
P-2.35: Write a set of Python classes that can simulate an Internet application in
which one party, Alice, is periodically creating a set of packets that she
wants to send to Bob. An Internet process is continually checking if Alice
has any packets to send, and if so, it delivers them to Bob's computer, and
Bob is periodically checking if his computer has a packet from Alice, and,
if so, he reads and deletes it.
"""

import threading
import logging

from queue import Queue
from time import sleep
from random import randint
from typing import NamedTuple

class Packet(NamedTuple):
    sender: str
    size: int

class Worker(threading.Thread):
    def __init__(self, user, buffer, speed):
        super().__init__(daemon=True)
        self.user = user
        self.working = False
        self.speed = speed
        self.buffer = buffer

    def __repr__(self):
        return self.user
    
    @property
    def state(self):
        if self.working:
            return f"{self} is working."
        return f"{self} is idling."

    def simulate_idle(self):
        self.working = False
        logging.info(self.state)
        sleep(randint(1, 3))
              
    def simulate_work(self):
        self.working = True
        logging.info(self.state)
        delay = randint(1, 1 + 15 // self.speed)
        for _ in range(100):
            sleep(delay / 100)

class Server(Worker):
    def run(self):
        logging.info(f"Thread: {self} is starting.")
        while True:
            self.simulate_work()
            self.send_packet()
            self.simulate_idle()

    def send_packet(self):
        """Generate a packet of some size bytes."""
        packet = Packet(self.user, randint(4, 512))
        logging.info(f"{self} sent a packet of {packet.size} bytes.")
        self.buffer.put(packet) # place packet into the queue

class Client(Worker):
    def run(self):
        logging.info(f"Thread: {self} is starting.")
        while True:
            self.process_queue()
            self.simulate_work()
            self.simulate_idle()

    def process_queue(self):
        """
        Check the queue if there is anything to retrieve
        """
        total_bytes = 0
        while not self.buffer.empty():
            packet = self.buffer.get()
            total_bytes += self.read(packet)
        
        if total_bytes != 0:
            logging.info(f"-- {self} received {total_bytes} bytes in total. --")
        
        logging.info("-- The queue is empty. --")
    
    def read(self, packet):
        if packet is not None:
            logging.info(f"{self} received {packet.size} bytes from {packet.sender}")
            self.buffer.task_done()
            return packet.size
        return 0

# Set logging parameters
logger = logging.getLogger()
logger.setLevel(logging.INFO)
console = logging.StreamHandler()
logger.addHandler(console)

shared_queue = Queue() # Unbounded First-in-First-Out

a = Server("Alice", shared_queue, 2)
b = Client("Bob", shared_queue, 0.5)

# start threads
a.start(), b.start()
# wait for all threads to finish
a.join(), b.join()