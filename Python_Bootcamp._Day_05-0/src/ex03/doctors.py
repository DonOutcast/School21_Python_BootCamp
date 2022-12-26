import threading
import time


class Doctor(threading.Thread):
    running = True

    def __init__(self, index, screwdriverOnLeft, screwdriverOnRight):
        threading.Thread.__init__(self)
        self.index = index
        self.screwdriverOnLeft = screwdriverOnLeft
        self.screwdriverOnRight = screwdriverOnRight

    def run(self):
        while (self.running):
            time.sleep(1)
            self.dine()

    def dine(self):
        screwdriver1, screwdriver2 = self.screwdriverOnLeft, self.screwdriverOnRight
        while self.running:
            screwdriver1.acquire()
            locked = screwdriver2.acquire(False)
            if locked:
                break
            screwdriver1.release()
            screwdriver1, screwdriver2 = screwdriver2, screwdriver1
        else:
            return
        self.working()
        screwdriver2.release()
        screwdriver1.release()

    def working(self):
        time.sleep(1)
        print('Doctor %s: BLAST!' % self.index)


def main():
    screwdrivers = [threading.Semaphore() for n in range(9, 14)]
    doctors = [Doctor(i, screwdrivers[i % 5], screwdrivers[(i + 1) % 5])
               for i in range(9, 14)]

    Doctor.running = True
    for p in doctors:
        p.start()
    time.sleep(7)
    Doctor.running = False


if __name__ == "__main__":
    main()
