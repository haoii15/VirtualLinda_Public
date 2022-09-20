import os
import pickle

from kjellar.config import KEKW, KEKWCHL, KEKWPATH
from config import GUILDID

async def find_kekw(msg, client):
    kekw = 0
    if os.path.getsize(KEKWPATH) > 0:
        with open(KEKWPATH, "rb") as file:
            kekw = pickle.load(file)

    a = kekw

    guild = client.get_guild(GUILDID)
    kekw += msg.content.count(KEKW)

    b = kekw
     
    if a == b:
        return

    kanal = guild.get_channel(KEKWCHL)     

    with open(KEKWPATH, "wb") as file:
        pickle.dump(kekw, file)

    await kanal.send(f"{kekw}{KEKW}")   