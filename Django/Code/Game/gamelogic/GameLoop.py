from time import sleep

from pyasn1.type.univ import Boolean

from .GameObject import GameObject

import threading

class GameLoop(threading.Thread):
    def __init__(self):
        super(GameLoop, self).__init__()
        self.gameObject = GameObject()


    def acquire_locks(self) -> None:
        self.gameObject.ball.lock.acquire()
        self.gameObject.playerOne.lock.acquire()
        self.gameObject.playerTwo.lock.acquire()


    def release_locks(self) -> None:
        self.gameObject.ball.lock.release()
        self.gameObject.playerOne.lock.release()
        self.gameObject.playerTwo.lock.release()


    def run(self):

        while self.gameObject.running:
            if self.gameObject.playing:
                self.acquire_locks()
                self.gameObject.tick()
                self.release_locks()
            #this has to be done to not overload the CPU
            sleep(0.01)
