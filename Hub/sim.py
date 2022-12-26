#TODO some kind of heartbeat? and check download attachments from the mail and add them to the hub storage every x time?

from time import sleep
import newpi
import tools
a = newpi.Newpi()
b = tools.Tools()
a.joinnet("1.1.1.1")
b.rename(2, "beepbop")