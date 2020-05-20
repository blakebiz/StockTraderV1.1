import yahooInterface
import time
import threading

class Server:
    def __init__(self, refresh_rate=30, super_charged=False, start=True, auto_tune=False, inc=5):
        self.updated = time.time()
        self.refresh_rate, self.super_charged, self.auto_tune, self.inc = refresh_rate, super_charged, auto_tune, inc
        self.q = []
        self.results = dict()
        self.thread = None
        self.running = True
        self.updating = False
        self.storage = dict()
        self.grab_count = 0
        if start:
            self.start_updates()

    def request(self, stocks, criteria, histLength=1):
        rv = dict()
        wait = False
        waited = []
        for stock in stocks:
            if stock in self.storage:
                for info in self.storage[stock]:
                    if info[0][0] == criteria and info[0][1] == histLength:
                        rv[stock] = info[1]
                        break
                else:
                    self.queue(stock, criteria, histLength)
                    waited.append(stock)
                    wait = True
            else:
                self.queue(stock, criteria, histLength)
                waited.append(stock)
                wait = True
        if wait:
            updating = True
            while updating:
                try:
                    self.wait_update()
                except ServerWait:
                    wait_time = self.refresh_rate-(time.time()-self.updated)
                    if wait_time < 1: wait_time += 1
                    time.sleep(wait_time)
                else:
                    updating = False
            for stock in waited:
                if stock in self.results:
                    for info in self.results[stock]:
                        if info[0][1] == criteria and info[0][0] == histLength:
                            rv[stock] = info[1]
                            break
                    else:
                        print(self.results)
                        raise Exception('Error fetching stock data in Server.request() info was not grabbed for some reason')
                else:
                    print(self.results)
                    raise Exception('Error fetching stock data in Server.request() info was not grabbed for some reason')
        return rv


    def start_updates(self):
        threading.Thread(target=self._start_updates).start()

    def _start_updates(self):
        while self.running:
            while self.updating:
                if self.auto_tune:
                    self.refresh_rate += self.inc
                    time.sleep(self.inc)
                else:
                    raise Exception('Refresh rate too fast')
            self.thread = threading.Thread(target=self.update)
            self.thread.start()
            time.sleep(self.refresh_rate)

    def stop_updates(self):
        self.running = False
        time.sleep(10)


    def wait_update(self):
        if self.thread is None:
            raise ServerWait('Server.wait_update() called with no update running')
        if not self.thread.isAlive():
            time.sleep(1)
            self.wait_update()
        else:
            self.thread.join()


    def update(self):
        while self.updating:
            if self.auto_tune:
                self.refresh_rate += self.inc
                time.sleep(self.inc)
            else:
                raise Exception('Refresh rate too fast')
        if self.q:
            self.updating = True
            self.storage = dict()
            if self.super_charged:
                threads = []
            for search in self.q:
                if self.super_charged:
                    thread = threading.Thread(target=self.grab, args=[search])
                    thread.start()
                    threads.append(thread)
                else:
                    self.grab(search)
            if self.super_charged:
                for thread in threads:
                    thread.join()
            self.q = []
            self.results = self.storage
            self.storage = dict()
            self.updated = time.time()
            self.updating = False

    def grab(self, search):
        self.grab_count += 1
        info = yahooInterface.grabInfo(*search, superCharged=self.super_charged)
        for stock in info:
            if stock in self.storage:
                self.storage[stock].append([[search[2], search[1]], info[stock]])
            else:
                self.storage[stock] = [[[search[2], search[1]], info[stock]]]


    def queue(self, stock, criteria, histLength=1):
        for search in self.q:
            if search[1] == criteria and search[2] == histLength:
                search[0].add(stock)
                break
        else:
            self.q.append([{stock}, criteria, histLength])


class ServerWait(Exception):
    def __init__(self, msg):
        self.message = msg


