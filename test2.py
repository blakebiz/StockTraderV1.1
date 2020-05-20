def wrap(x):
    def wrapper(*args):
        print('hi')
        x(*args)
    return wrapper

@wrap
def func(x):
    print(x)

func(6)