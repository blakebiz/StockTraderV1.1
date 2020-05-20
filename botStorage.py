import json,jsonpickle, random, TraderBot, BassHelperCode, MainGUI, threading

class Storage():
    def __init__(self, gui=True, load=True):
        '''
        ----------------------------------------------------------------------------------------------------------------
        set load to false to delete all bots from Storage, warning this is kind of permanent
        ----------------------------------------------------------------------------------------------------------------
        gui - if you don't want to use a gui you can set it to False
        ----------------------------------------------------------------------------------------------------------------
        '''
        self.load_bots(load)
        if gui:
            try:
                print(self.bots)
                thread = threading.Thread(target=MainGUI.main(testing=False))
                self.gui = MainGUI.IndicSelectWindow(self.bots)
            except Exception as e:
                print('error in botStorage:', e)
        else:
            self.gui = None

    def load_bots(self, load=True):
        try:
            if not load:
                raise Exception('forced error loading bots')
            # raise Exception()
            with open(r'Bots\botMainStorage.json', 'r') as file:
                bots = json.load(file)
                bots = jsonpickle.decode(bots)
            self.bots = dict()
            self.activeBots = dict()
            self.inactiveBots = dict()
            for bot in bots[1]:
                newBot = self.genBot(bots[1][bot])
                self.activeBots[bot] = newBot
                self.bots[bot] = newBot
            for bot in bots[2]:
                newBot = self.genBot(bots[2][bot])
                self.inactiveBots[bot] = newBot
                self.bots[bot] = newBot
            for bot in bots[0]:
                if bot not in self.bots:
                    self.bots[bot] = self.genBot(bots[0][bot])
        except Exception as e:
            print('error loading bots:', e)
            prompt = 'Would you like to create a new Storage' \
                     ' (beware if you have previous bots their data might be lost) '
            if BassHelperCode.run_confirmation_loop(prompt, 0):
                self.bots = dict()
                self.activeBots = dict()
                self.inactiveBots = dict()
            else:
                raise Exception('Error loading bots, user chose not to make a new Storage, please fix any loading issues then try again')

    def export_bots(self):
        with open(r'Bots\botMainStorage.json', 'w') as file:
            json.dump(jsonpickle.encode([self.bots, self.activeBots, self.inactiveBots]), file)

    def new_bot(self, bot):
        self.bots[bot.id] = bot

    def gen_id(self):
        while True:
            id = ''
            for itr1 in range(9):
                id += str(random.randint(0, 9))
            if id not in self.bots:
                return id

    def genBot(self, bot):
        class StoreClass:
            def __init__(self):
                pass
        exec('from {} import {}'.format(bot.classInfo[0], bot.classInfo[1]))
        sC = StoreClass()
        exec('sC.cls = {}'.format(bot.classInfo[1]))
        try:
            stratClassInst = sC.cls(bot.stratClassInit)
        except NameError:
            try:
                stratClassInst = sC.cls()
            except TypeError:
                raise TypeError("Error on loading bots, ")


        newBot = TraderBot.TradeBot(bot.stocks, stratClassInst, self, id=bot.id, startMoney=bot.bank, printStatus=bot.printStatus)
        newBot.timesRan = bot.timesRan
        newBot.bought = bot.bought
        return newBot

    def activate_bot(self, id):
        if id in self.inactiveBots:
            self.activeBots[id] = self.inactiveBots.pop(id)
        elif id in self.bots:
            self.activeBots[id] = self.bots[id]
        else:
            raise Exception('bot with given id does not exist in Storage!')

    def disable_bot(self, id):
        if id in self.activeBots:
            self.inactiveBots = self.activeBots.pop(id)
        else:
            raise Exception('bot with given id is not active!')

    def run_bots(self):
        from PyQt5 import QtWidgets
        import sys
        if self.gui != None:
            app = QtWidgets.QApplication(sys.argv)
            self.gui.show()
            sys.exit(app.exec_())
        for bot in self.bots.values():
            bot.run()
        # self.timer = funcTimer.main(30, self.export_bots)

    def cancel_bots(self):
        for bot in self.activeBots.values():
            bot.stop()
        self.timer.cancel()