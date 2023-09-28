class MyArray:
    def __init__(self):
        self.length = 0
        self.data = {}

    def __str__(self):
        return str(self.__dict__)

    def __getItem__(self, index):
        return self.data.get(index)

    def get(self, index):
        self[index]
    
    def push(self, value):
        self.length += 1
        self.data[self.length - 1] = value
        return self.length

    def pop(self):
        last_item = self.data[self.length-1]
        del self.data[self.length - 1]
        self.length -= 1
        return last_item
    
    def delete(self, index):
        deleted_item = self.data[index]
        self.shift_items(index)
        return deleted_item

    def shift_items(self, index):
        for i in range(index, self.length - 1):
            self.data[i] = self.data[i+1]
        del self.data[self.length - 1] # Remove last item that we don't need anymore
        self.length -= 1