"""
P-2.36: Write a Python program to simulate an ecosystem containing two types
of creatures, bears and fish. The ecosystem consists of a river, which is
modeled as a relatively large list. Each element of the list should be a
Bear object, a Fish object, or None. In each time step, based on a random
process, each animal either attempts to move into an adjacent list location
or stay where it is. If two animals of the same type are about to collide in
the same cell, then they stay where they are, but they create a new instance
of that type of animal, which is placed in a random empty (i.e., previously
None) location in the list. If a bear and a fish collide, however, then the
fish dies (i.e., it disappears).
"""
from typing import NamedTuple
from random import choices, choice, randint
from os import system
from sys import platform

class Point(NamedTuple):
    x: int
    y: int

"""
List of all possible orthogonal directions in a 2D space
e.g. Northwest, North, Northeast, West, East, Southwest, South and Southeast
"""
offsets = [
        Point(-1, -1), 
        Point(0, -1),
        Point(1, -1),
        Point(-1, 0),
        Point(0, 1),
        Point(1, 1)
    ]

class Animal:
    def __init__(self, x, y, char='A'):
        self.x = x
        self.y = y
        self.char = char
        self.is_alive = True

    def __repr__(self):
        return f"{self.name()} (x: {self.x}, y:{self.y})"
    
    def __str__(self):
        return self.char
    
    def __eq__(self, other):
        return self.type() == other.type()

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    @property
    def name(self):
        return self.__class__.__name__
    
    def type(self):
        return self.__class__
    
class Fish(Animal):
    def __init__(self, x, y):
        super().__init__(x, y, 'f')

class Bear(Animal):
    def __init__(self, x, y):
        super().__init__(x, y, 'b')

class Ecosystem:
    def __init__(self, biome_type, width, height):
        self.biome_type = biome_type
        self.__map = [None] * (width * height)
        self.width = width
        self.height = height
        self.entities = self.populate_random()
        self.animal_count = dict()
    
    def __len__(self):
        return len(self.__map)

    def get(self, x, y):
        return self.__map[y * self.width + x]
    
    def set(self, x, y, val):
        if self.is_in_bounds(x, y):
            self.__map[y * self.width + x] = val

    def populate_random(self):
        """
        We visit each cell at each 2D coordinate and determine if we spawn an Animal at that location
        """
        entities = []
        for y in range(self.height):
            for x in range(self.width):
                # We determine if we will spawn a Bear, a Fish or leave the cell alone
                result = self.determine_animal()
                if result is not None:
                    animal = result(x, y)
                    self.set(x, y, animal) # update the cell with the animal
                    entities.append(animal) # update running list of animals
        return entities

    def determine_animal(self):
        return choices([Bear, Fish, None], weights=[2, 3, 5])[0]

    def is_in_bounds(self, x, y):
        return x >= 0 and x < self.width and y >= 0 and y < self.height
    
    def render(self):
        self.clear()
        for y in range(self.height):
            for x in range(self.width):
                current_cell = self.get(x, y)
                if current_cell is not None:
                    print(str(current_cell), end="")
                else:
                    print("~", end="")
            print(end="\n")
        for k, v in self.animal_count.items():
            print(f"{k}: {v}")

    def clear(self):
        if "linux" in platform:
            system('clear')
        elif "win32" in platform:
            system('cls')
        else:
            system('clear')

    def update(self):
        for animal in (entity for entity in self.entities if entity.is_alive):
            self.determine_actions(animal)
            self.update_counters()

    def determine_actions(self, entity):
        # check if the animal wishes to move or not
        is_moving = choices([True, False], weights=[7.5, 2.5])[0] # 75% vs 25% probability respectively
        direction = choice(offsets) # pick a random direction
        if is_moving and self.is_in_bounds(entity.x + direction.x, entity.y + direction.y): # check if this animal is planning to move and if it is a valid move, if it's not valid should we choose another direction?
            other_entity = self.get(entity.x + direction.x, entity.y + direction.y) # peek at what is at the new location
            if other_entity is not None:
                if entity != other_entity:
                    if isinstance(entity, Fish):
                        self.set(entity.x, entity.y, None)
                        entity.is_alive = False
                    elif isinstance(other_entity, Fish):
                        self.set(other_entity.x, other_entity.y, None)
                        other_entity.is_alive = False
                else: # making a new entity
                    x = randint(0, self.width - 1)
                    y = randint(0, self.height - 1)
                    if not any(entity.x == x and entity.y == y for entity in self.entities if entity.is_alive):
                        new_animal = type(entity)(x, y)
                        self.set(new_animal.x, new_animal.y, new_animal)
                        self.entities.append(new_animal)
            else:
                previous_xy = entity.x, entity.y
                self.set(*previous_xy, None)
                entity.move(direction.x, direction.y)
                self.set(entity.x, entity.y, entity)

    def update_counters(self):
        self.reset_counter()
        for entity in self.entities:
            if entity.is_alive:
                self.animal_count[entity.name] = self.animal_count.get(entity.name, 0) + 1

    def reset_counter(self):
        self.animal_count = self.animal_count.fromkeys(self.animal_count, 0)

    def step(self):
        self.update()
        self.render()

import time
previous_time = None
target_framerate = 0.5 # frames
frametime = 1_000 / target_framerate # every 5 seconds is 1 frame update
curr_iter = 0
max_iter = 1000

e = Ecosystem("river", width=25, height=25)
while curr_iter < max_iter:
    current_time = time.time() * 1_000
    if previous_time is None or current_time - previous_time >= frametime:
        e.step()
        previous_time = current_time # update previous time
        curr_iter += 1