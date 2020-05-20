import testClass

def main():
    inst = testClass.myClass()
    classInfo = str(type(inst)).split()[1].split("'")[1].split('.')
    print(classInfo)
    class StoreClass:
        def __init__(self):
            pass
    exec('from {} import {}'.format(classInfo[0], classInfo[1]))
    sC = StoreClass()
    exec('sC.cls = {}'.format(classInfo[1]))
    print(sC.cls)
    newInst = sC.cls()
    newInst.print2()
if __name__ == '__main__':
    main()