from collections import Counter
from string import printable

def distribute(items, num_containers, hash_function=hash):
    return Counter([hash_function(item) % num_containers for item in items])

def plot(histogram):
    for key in sorted(histogram):
        count = histogram[key]
        padding = (max(histogram.values()) - count) * " "
        print(f"{key:3} {'■' * count}{padding} ({count})")

def main():
    plot(distribute(printable, num_containers=5, hash_function=hash))

if __name__ == "__main__":
    main()