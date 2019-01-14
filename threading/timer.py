from threading import Timer
import time
import os

class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

def read_number(link, number):
    try:
        read_file = open(link, "r")
    except IOError as e:
        with open(link, "w") as read_file:
            read_file.write(str(number))
    else:
        with read_file:
            number = int(read_file.read())
     
    return number

def write_number(link, number):
    with open(link, 'w') as outfile:
        outfile.write(str(number))

    return number
  
def notify(link, num):
    res = read_number(link, num)
    print(res)
    write_number(link, (lambda n: n + 1)(res))

myfile='input.txt'

if os.path.isfile(myfile):
    os.remove(myfile)
else:
    print("Error: %s file not found" % myfile)

try:
    number = int(input('Write number: '))
    updater = RepeatTimer(1, notify, args=(myfile, number,))
    updater.start()
except ValueError as e:
    print('Not number')
    time.sleep(3)

    

