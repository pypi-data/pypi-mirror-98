from .dobotedu import DobotEDU
from tkinter import ttk
from scipy.io.wavfile import write
from DobotRPC import loggers
import asyncio
import sys

def sleep(time):
    loop.run_until_complete(asyncio.sleep(time))


loggers.set_use_console(False)
loggers.set_use_file(True)
loggers.set_level(loggers.DEBUG)

loop = asyncio.get_event_loop()
dobot_edu = DobotEDU()
dobotEdu = dobot_edu
magicbox = dobot_edu.magicbox
m_lite = dobot_edu.m_lite
dobot_magician = dobot_edu.magician
go = dobot_edu.magiciango
ocr = dobot_edu.ocr
nlp = dobot_edu.nlp
ai = dobot_edu.pyimageom
beta_go = dobot_edu.beta_go
speech = dobot_edu.speech
robot = dobot_edu.robot
util = dobot_edu.util
face = dobot_edu.face
tmt = dobot_edu.tmt

argv = sys.argv
if len(argv) == 4:
    dobot_edu.set_portname(argv[1])
    dobot_edu.token = (argv[2])
    dobot_edu.url = (argv[3])


# __all__ = ("DobotEDU")
