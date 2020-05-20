from threading import Timer

class perpetualTimer():

   def __init__(self, t, hFunction, params):
      self.t=t
      self.hFunction = hFunction
      self.params = params
      self.thread = Timer(self.t, self.handle_function)

   def handle_function(self):
      if self.params == None:
         self.hFunction()
      else:
         self.hFunction(self.params)
      self.thread = Timer(self.t, self.handle_function)
      self.thread.start()

   def start(self):
      self.thread.start()

   def cancel(self):
      self.thread.cancel()


def main(time, func, params = None):
    t = perpetualTimer(time, func, params)
    t.start()
    return t