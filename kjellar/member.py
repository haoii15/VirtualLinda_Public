import os
import pickle
import df
import discord

import dataframe_image as dfi

from datetime import datetime
from time import perf_counter
from random import randint

from config import ranks
from kjellar.config import MINXP, MAXXP, SERVERPATH, LUCKY, LOGPATH, tiers


class Server():
    def __init__(self, guild, msgs=0, xpmsgs=0, lmsgs=0):
        self.msgs = msgs
        self.xpmsgs = xpmsgs
        self.lmsgs = lmsgs
        self.numUsers = len(guild.members)
        
        self.users = {}
        self.rm = []

    async def newMsg(self, guild, msg):
        self.msgs += 1
        author = msg.author

        if author.id not in self.users.keys():
            self.users[author.id] = Member(guild, author.id, author.name)
            string = f"Hei på deg {self.users[author.id].displayname}, eg e Linda!\nVelkommen som **Førstereis i Kjellarstuå**!\n\nNyd **Kjellarstuå**!"
            await msg.channel.send(string)
            user = self.users[author.id]
        else:
            user = self.getUser(msg)

        result = user.newMsg()
        if type(result[0]) == list:
            if "lucky" in result[0]:
                self.lmsgs += 1
            if "xp" in result[0][0]:
                self.xpmsgs += 1

        self.setUser(msg, user)

        return [result, user]
    
    def ranks(self, guild, msg):
        split = msg.content.split(" ", 1)

        if len(split) == 1:
            user = self.getUser(msg)
        else:
            id = getID(guild, split[1])
            try:
                user = self.users[id]
            except:
                return f"{split[1]} e ingen bruker i mitt system."

        if user.id in self.rm:
            return f"{user.name} e ingen bruker i mitt system."

        return user.getRank()

    def stats(self, guild):
        
        return f"*medlemmer*: **{len(guild.members)}**\n*meldingar*: **{self.msgs}**\n*xp meldingar*: **{self.xpmsgs}**\n*heldige messages*: **{self.lmsgs}**\n"
    
    async def toplist(self, guild, msg):
        split = msg.content.split(" ", 1)
        listlist = []
        do = 0

        if len(split) == 1:
            data = self.users.values()
            do = 1
        else:
            for role in guild.roles:
                if role.name == split[1]:
                    do = 1
                    data = role.members
            
        if do == 0:
            msgstr = f"{split[1]} e ingen rolle i mitt system."
            await msg.channel.send(msgstr)
            return

        for user in data:
            if user.id in self.rm:
                continue
            listlist.append([user.displayname, user.rank, user.xp, user.msgs])

        slist = sorted(listlist, key=lambda x: x[2], reverse=True)

        place = 1
        for list in slist:
            list.insert(0, place)
            place += 1

        dfr = df.listToDf(slist)
        dfr = df.styleDf(dfr)

        dfi.export(dfr, "listå.png")

        await msg.channel.send(file=discord.File("listå.png"))

    async def lucklist(self, guild, msg):
        split = msg.content.split(" ", 1)
        listlist = []
        do = 0

        if len(split) == 1:
            data = self.users.values()
            do = 1
        else:
            for role in guild.roles:
                if role.name == split[1]:
                    do = 1
                    data = role.members
            
        if do == 0:
            msgstr = f"{split[1]} e ingen rolle i mitt system."
            await msg.channel.send(msgstr)
            return

        for user in data:
            if user.id in self.rm:
                continue
            xpmsg = round(user.xp / user.msgs, 2)
            luckies = round(user.lmsgs / user.msgs, 2) * 100
            listlist.append([user.displayname, xpmsg, luckies])

        slist = sorted(listlist, key=lambda x: x[1])

        place = 1
        for list in slist:
            list.insert(0, place)
            place += 1

        dfr = df.llistToDf(slist)
        dfr = df.styleDf(dfr)

        dfi.export(dfr, "lucky.png")

        await msg.channel.send(file=discord.File("lucky.png")) 

    async def renameUser(self, msg):
        user = self.getUser(msg)
        user.rename(msg)
        self.setUser(msg, user)
    
    async def rmUser(self, msg, guild):
        name = msg.content.split(" ", 1)[1]

        id = getID(guild, name)

        if id == 0:
            await msg.channel.send(f"{name} brukeren finnes ikke i mitt system.")
            return

        if id not in self.rm:
            self.rm.append(id)
            await msg.channel.send(f"Fine, der va {name} ute av systemet.")
        else:
            await msg.channel.send(f"{name} e allerede på svartelistå.")

        logs = f"removed {name}"
        log(logs)

    async def unrmUser(self, msg, guild):
        name = msg.content.split(" ", 1)[1]

        id = getID(guild, name)

        if id == 0:
            await msg.channel.send(f"{name} brukeren finnes ikke i mitt system.")
            return

        if id in self.rm:
            self.rm.remove(id)
            await msg.channel.send(f"Der e {name} tebage i det gode selskap.")
        else:
            await msg.channel.send(f"{name} e isje på svartelistå.")

        logs = f"unremoved {name}"
        log(logs)

    def getUser(self, msg):
        author = msg.author
        
        return self.users[author.id]

    def setUser(self, msg, user):        
        author = msg.author

        self.users[author.id] = user

class Member(Server):
    def __init__(self, guild, id, name, xp = 0, rank = 0, msgs = 0, xpmsgs = 0, lmsgs = 0):
        super().__init__(guild)
        self.id = id
        self.name = name
        self.displayname = name
        self.xp = xp
        self.rank = rank
        self.msgs = msgs
        self.xpmsgs = xpmsgs
        self.lmsgs = lmsgs
        self.timer = perf_counter()

    def newMsg(self):
        returns = []
        self.msgs += 1
        returns.append(self.xpCheck())
        returns.append(self.rankCheck())
        return returns
    
    def xpCheck(self):
        if perf_counter() - self.timer > 60 or self.timer > perf_counter():
            xp = randint(MINXP, MAXXP)
            self.xp += xp
            self.xpmsgs += 1
            returning = ["xp"]
            self.timer = perf_counter()

            if xp > LUCKY:
                self.lmsgs += 1
                returning.append("lucky")

            logs = f"{self.xp}xp->{self.displayname}({self.id})"
            log(logs)
            return returning

    def rankCheck(self):
        if self.xp > ranks[self.rank]:
            self.rank += 1
            
            logs = f"{self.displayname}({self.id})->{self.rank}->{tiers[self.rank]}"
            log(logs)

            return "rank"
    
    def getRank(self):
        value = f"*navn*: **{self.displayname}**\n*tier*: **{tiers[self.rank]}**\n*level*: **{self.rank}**\n*alle meldingar*: **{self.msgs}**\n*xp meldingar*: **{self.xpmsgs}**\n*heldige meldingar*: **{self.lmsgs}**\n*xp*: **{self.xp}**\n*xp te neste level*: **{ranks[self.rank] - self.xp}**"
        return value

    def rename(self, msg):
        split = msg.content.split(" ", 1)

        self.displayname = split[1]
        self.name = split[1]

def log(logs):
    time = datetime.now().strftime("%H:%M %d-%m-%Y")
    logstr = f"{time} \t" + logs + "\n"
    file =  open(LOGPATH, "a")
    file.write(logstr)
    file.close()

def getServer(guild):
    if os.path.getsize(SERVERPATH) > 0:
        with open(SERVERPATH, "rb") as file:
            server = pickle.load(file)
    else:
        server = Server(guild)
    return server

def setServer(server):
    with open(SERVERPATH, "wb") as file:
        pickle.dump(server, file)

def getID(guild, name):
    server = getServer(guild)

    for user in server.users.values():
        if name == user.name:
            return user.id
    
    return 0