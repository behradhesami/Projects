from sample import creat_sample


class Handler:
    def run (self):
        print("Program runed...")

if __name__ == '__main__':
    creat_sample()
    handler = Handler()

    handler.run()