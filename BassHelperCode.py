import threading
import time
from threading import Timer

def run_confirmation_loop(prompt, option_count):
    if option_count == 0:
        confirmation_loop = True
        while confirmation_loop:
            print('\n', prompt, end='', sep='')
            confirmation = input('(Y/N): ')
            if confirmation == 'Y' or confirmation == 'y':
                return True
            elif confirmation == 'N' or confirmation == 'n':
                return False
            else:
                print('\nPlease only input either "Y" or "N"!\n')
    if option_count == -1:
        confirmation_loop = True
        while confirmation_loop:
            print('\n', prompt, end='', sep='')
            confirmation = input(': ')
            try:
                int(confirmation)
            except ValueError:
                print('\nPlease only input an integer!\n')
            else:
                confirmation = int(confirmation)
                if confirmation < 0:
                    print('\nPlease only input a positive integer!\n')
                else:
                    return confirmation
    confirmation_loop = True
    while confirmation_loop:
        print('\n', prompt,end='',sep='')
        confirmation = input(': ')
        try:
            int(confirmation)
        except ValueError:
            print('Please only input integers!')
        else:
            if int(confirmation) in range(1, int(option_count) + 1):
                return int(confirmation)
            print('\nPlease only input one of the integers given!\n')

def check_in_file(fname):
    #Try reading in file return result
    try:
        open(fname, 'r')
    except FileNotFoundError:
        print('\nStorage file not found.\n')
        return True
    except:
        print('unknown error reading in file. Try again or try another file.')
        return True
    else:
        print('\nInput File Found!\n')
        return False

def check_out_file(fname):
    try:
        open(fname, 'r')
    except FileNotFoundError:
        return False
    else:
        return True

def ask_date(confirm):
    start_loop = True
    while start_loop:
        print('\nPlease input a ', confirm, ' ', sep = '', end = '')
        date = input('date (MM/DD/YY): ')
        if len(date) != 8:
            print('\n\nYour input is not properly formatted! Please enter date as MM/DD/YY!\n\n')
        else:
            try:
                int(date[0:2])
                int(date[3:5])
                int(date[6:])
            except ValueError:
                print('\nOnly input integers as dates!\n')
            else:
                if int(date[0:2]) > 12 or int(date[3:5]) > 31 or int(date[6:]) > 3000:
                    print('\nError with given date, double check values input!\n')
                elif date[2] != '/' or date[5] != '/':
                    print('\nError with given format, ensure data is given in MM/DD/YY format! Include slashes!')
                else:
                    if int(date[0:2]) > 12:
                        print('A month greater than 12? Try again!')
                    elif int(date[3:5]) >31:
                        print('A day greater than 31? Try Again!')
                    else:
                        date = '20' + date[6:] + '/' + date[:2] + '/' + date[3:5]
                        return date

def rec_strip(givenList):
    return_list = []
    for item in givenList:
        if isinstance(item, list):
            return_list.append(rec_strip(item))
        elif isinstance(item, str):
            return_list.append(item.strip())
        else:
            return_list.append(item)
    return return_list




class perpetualTimer():

   def __init__(self, t, hFunction, params):
      self.t=t
      self.hFunction = hFunction
      self.params = params
      self.thread = Timer(self.t, self.handle_function)

   def handle_function(self):
      if self.params == '':
         self.hFunction()
      else:
         self.hFunction(self.params)
      self.thread = Timer(self.t, self.handle_function)
      self.thread.start()

   def start(self):
      self.thread.start()

   def cancel(self):
      self.thread.cancel()


def main(time, func, params = ''):
    t = perpetualTimer(time, func, params)
    t.start()

def deComma(num):
    if not isinstance(num, str):
        return float(num)
    if ',' in num:
        num = num.split(',')
        levels = []
        for itr1 in range(len(num)):
            if itr1 == 0:
                levels.append(0)
            elif itr1 == 1:
                power = 3
                levels.append(power)
            else:
                power += 3
                levels.append(power)

        for itr1 in range(len(num)):
            if '.' not in num[(itr1 + 1) * -1]:
                num[(itr1 + 1) * -1] = int(num[(itr1 + 1) * -1]) * (10 ** levels[itr1])
            else:
                num[(itr1 + 1) * -1] = float(num[(itr1 + 1) * -1]) * (10 ** levels[itr1])
        return sum(num)
    else:
        return float(num)

def timer(f, store=None, index=None):
    def wrapper():
        rv = f()
        if store:
            store[index] = rv
        return rv
    return wrapper


def testFuncs(count, funcs, avg=False, limit=1):
    '''
    :param count:
    The amount of times each function is to be ran
    :param args:
    all of the functions to be ran
    :return:
    '''
    counter = 0
    rvs = []
    times = []
    for func in funcs:
        rvs.append([])
        for i in range(count):
            rvs[counter].append(-1)
            times.append(threading.Thread(target=timer(func, rvs[counter], i)))
        counter += 1
    limit_threads(limit, times)
    if avg:
        avgs = []
        for result in rvs:
            sum, count = 0, 0
            for time in result:
                sum += time
                count += 1
            avgs.append(sum/count)
        return avgs
    return rvs

def testFuncsGen(count, funcs, avg=False, limit=1):
    '''
    :param count:
    The amount of times each function is to be ran
    :param args:
    all of the functions to be ran
    :return:
    '''
    counter = 0
    rvs = []
    times = []
    choices = []
    for func in funcs:
        rvs.append([])
        for i in range(count):
            rvs[counter].append(-1)
            times.append(threading.Thread(target=timer(func[0], rvs[counter], i)))
        counter += 1
        choices.append(func[1])
    limit_threads(limit, times)
    if avg:
        avgs = []
        for result in rvs:
            sum, count = 0, 0
            for time in result:
                sum += time
                count += 1
            avgs.append(sum/count)
        return avgs, choices
    return rvs, choices


def limit_threads(limit, threads, reverse=True, interval=.1):
    '''
    :param limit:
    An int limit of how many threads max should run at a time
    :param threads:
    A list of threads that haven't been started
    :param reverse:
    By default for efficiency reasons the threads will be ran in reverse order of passed in but change this to False
    to run it in the order it was passed in.
    :param interval:
    How long the function sleeps for before checking to see if a thread dies to start a new one
    '''
    if not reverse:
        threads.reverse()
    running = []
    count = 0
    while threads:
        ind = 0
        for _ in range(len(running)):
            if not running[ind].is_alive():
                running.pop(ind)
            else:
                ind += 1
        if len(running) < limit:
            thread = threads.pop()
            thread.start()
            running.append(thread)
        if count >= limit:
            time.sleep(interval)
        count += 1
    for thrd in running:
        thrd.join()


def simulate_threads(threads, limit, reverse=True):
    if not reverse:
        threads.reverse()
    running = []
    timer = 0
    while threads:
        if len(running) < limit:
            running.append(threads.pop())
        else:
            low = min(running)
            ind = 0
            timer += low
            for _ in range(len(running)):
                if running[ind] == low:
                    running.pop(ind)
                else:
                    running[ind] -= low
                    ind += 1

    while running:
        low = min(running)
        ind = 0
        for _ in range(len(running)):
            if running[ind] == low:
                running.pop(ind)
            else:
                running[ind] -= low
                ind += 1
        timer += low
    return timer

class Gen:
    def __init__(self, n):
        self.n = n
        self.last = 0

    def __iter__(self):
        self.last = 0
        return self

    def __next__(self):
        return self.next()

    def next(self):
        if self.last == self.n:
            raise StopIteration()

        rv = self.last ** 2
        self.last += 1
        return rv