import sys
from redis import Redis

client = Redis()

"""This program is designed to take the data from Redis 
and perform the desired operation on them and send it to the database, for example.

"""

def watch_links_data(name):
    print(f"Worker {name} started")

    while True:
        link = client.blpop('links')
        print(link)



if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise KeyError("Worker name is required")
    watch_links_data(sys.argv[1])
