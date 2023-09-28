from typing import NamedTuple, Any

DELETED = object()

class Pair(NamedTuple):
    key: Any
    value: Any

class MyHashTable:
    """
    Core features:
    * Create a hash table
    * Insert a key-value pair
    * Delete a key-value pair
    * Find a value by key
    * Update the value associate with an existing key
    * Check if the hash table has a given key
    """
    def __init__(self, capacity):
        if capacity < 1:
            raise ValueError("Hash table capacity must be a positive integer value")
        self._slots = capacity * [None]
    
    def __len__(self):
        return len(self.pairs)

    def __str__(self):
        pairs = []
        for key, value in self.pairs:
            pairs.append(f"{key!r}: {value!r}")
        return "{" + ", ".join(pairs) + "}"
    
    def __contains__(self, key):
        try:
            self[key]
        except KeyError:
            return False
        else:
            return True
        
    def __iter__(self):
        yield from self.keys
    
    def __setitem__(self, key, value):
        """
        Magic method in Python that allows class instances to use the indexer operators i.e. self[key]
        Uses linear probing to resolve hash collisions
        """
        for index, pair in self._probe(key):
            if pair is DELETED: continue
            if pair is None or pair.key == key:
                self._slots[index] = Pair(key, value)
                break
        else:
            raise MemoryError("Not enough capacity")

    def __getitem__(self, key):
        """"
        Magic method in Python that allows class instances to use indexer operators i.e. self[key]
        """
        for _, pair in self._probe(key):
            if pair is None:
                raise KeyError(key)
            if pair is DELETED:
                continue
            if pair.key == key:
                return pair.value
        raise KeyError(key)
    
    def __delitem__(self, key):
        for index, pair in self._probe(key):
            if pair is None:
                raise KeyError(key)
            if pair is DELETED:
                continue
            if pair.key == key:
                self._slots[index] = DELETED
                break
            else:
                raise KeyError(key)
        
    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def set(self, key, value):
        self[key] = value

    @property
    def pairs(self):
        return {
            pair for pair in self._slots
            if pair not in (None, DELETED)
        }
    
    @property
    def keys(self):
        return {pair.key for pair in self.pairs}

    @property
    def values(self):
        return [pair.value for pair in self.pairs]
    
    @property
    def capacity(self):
        return len(self._slots)
    
    def _index(self, key):
        return hash(key) % len(self._slots)
    
    def _probe(self, key):
        index = self._index(key)
        for _ in range(self.capacity):
            yield index, self._slots[index]
            index = (index + 1) % self.capacity