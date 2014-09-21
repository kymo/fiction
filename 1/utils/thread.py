import threading

class BaseThread(threading.Thread):
    def __init__(self, actionFunc):
        self.act = actionFunc
        threading.Thread.__init__(self)

    def run(self):
        result = self.act()
