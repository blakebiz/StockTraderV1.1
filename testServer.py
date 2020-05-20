import random
import Server, time, threading
import yahooInterface

server = Server.Server(refresh_rate=1, super_charged=True, auto_tune=True, inc=1)
stocks = ['aapl', 'msft', 'amzn', 'znga', 'tsla', 'qd', 'pfe', 'jblu', 'mac']
criteria = ['quote_table', 'history', 'live_price', 'analytics']
def get_results1():
    global server
    results = server.request(random.sample(stocks, random.randint(1, len(stocks)-1)),
                             random.sample(criteria, random.randint(1, len(criteria)-1)), histLength=1)
    # print(f'results: {results}')
def get_results2():
    global server
    results = yahooInterface.grabInfo(random.sample(stocks, random.randint(1, len(stocks) - 1)),
                             random.sample(criteria, random.randint(1, len(criteria) - 1)), histLength=1, superCharged=True)
    # print(f'results: {results}')

def test_func(func, count):
    start = time.time()
    threads = []
    for _ in range(count):
        thread = threading.Thread(target=func)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    # while any([thread.is_alive() for thread in threads]):
    #     print(f'still running: {time.time() - start}')
    #     time.sleep(5)
    print(f'run time: {time.time() - start}')
    print(f'grab count: {server.grab_count}')

test_func(get_results1, 25)
server.stop_updates()
test_func(get_results2, 250)

