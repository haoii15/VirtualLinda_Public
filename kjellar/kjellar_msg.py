from kjellar.member import getServer, setServer
from kjellar.customs import customs, reset_customs
from kjellar.gp import addGP, loadGP, removeGP, printGP, setGP, ranking, loadGP, newSeason, setSeason, removeGPseason
from kjellar.csvtopkl import * 

import kjellar.kekw as kekw

from config import GUILDID, BOTID, ADMINID
from kjellar.config import KLUBBHUS, NEWS, LUCKYID, MASTER, MASTERID, ELITE, ELITEID, tiers, rankupmsg

async def joined(member):
    for channel in member.guild.channels:
        if channel.id == KLUBBHUS:
            strng = f"{len(member.guild.members) - 1} + 1 = {len(member.guild.members)}"
            await channel.send(strng)
        if channel.id == NEWS:
            strng = f"{member.name}"
            await channel.send(strng)

async def newMessage(client, msg):

    guild = client.get_guild(GUILDID)

    if msg.author.id != BOTID and msg.guild == guild and msg.content.startswith("&") == False and msg.channel.name != "controller":
        await userMsg(guild, msg)

    if msg.author.id != BOTID:
        await kekw.find_kekw(msg, client)

    await commandCheck(guild, msg)
    

    
async def commandCheck(guild, msg):
    if msg.content.startswith("&"):
        try:
            await commands[msg.content.split(" ", 1)[0]](guild, msg)
        except:
            await msg.channel.send("Den commanden klare eg sje tolka, eller så e de noe som skjere seg.")


async def userMsg(guild, msg):
    server = getServer(guild)
    got = await server.newMsg(guild, msg)
    
    fetch = got[0]
    user = got[1]
    if type(fetch[0]) == list:
        if "lucky" in fetch[0]:
            await msg.add_reaction(await guild.fetch_emoji(LUCKYID))
    
    if "rank" in fetch:
        retMsg = f"Nå har du vært jævla god **{user.displayname}**!\n"
        retMsg += rankupmsg[user.rank]
        retMsg += f"\n\nDu tar nå steget fra **{tiers[user.rank-1]}** te **{tiers[user.rank]}**\nKos deg videre i **Kjellarstuå**!" 

        if user.rank == MASTER:
            await msg.author.add_roles(guild.get_role(MASTERID))
        elif user.rank == ELITE:
            await msg.author.add_roles(guild.get_role(ELITEID))

        await msg.channel.send(retMsg)
    
    setServer(server)

async def rank(guild, msg):
    server = getServer(guild)

    await msg.channel.send(server.ranks(guild, msg))

async def server(guild, msg): 
    dserver = getServer(guild)

    await msg.channel.send(dserver.stats(guild))

async def tlist(guild, msg):
    await getServer(guild).toplist(guild, msg)

async def luckylist(guild, msg):
    await getServer(guild).lucklist(guild, msg)
    

async def forklar(guild, msg):
    msgstr = f"Du e forveden på ka eg gjør ja, notert!\nDu vil kun få xp 1 gang i minutte, men fortvil isje. Eg telle alle meldingar, både di som gjer xp og di som isje gjer xp.\nNår du får xp, får du mellom 10 og 30 xp. E du i de heldiga hjørna og får mer enn 27xp vil eg merka meldingen din me ei stjerna. De e de eg kalle ein **heldige melding**, å ja, eg telle di og.\nHvis du bler forveden på koss du ligge an, kan du alltids bruka &rank for å sjekka status.\nHvis der ennå e någe mer du lure på, får du bare lura!"

    await msg.channel.send(msgstr)

async def rename(guild, msg):
    server = getServer(guild)
    await server.renameUser(msg)
    setServer(server)

async def remove(guild, msg):
    if msg.author.id != ADMINID:
        await msg.channel.send("Kun admin kan bruga denne funksjonen")
        return
    server = getServer(guild)
    await server.rmUser(msg, guild)
    setServer(server)

async def unremove(guild, msg):
    if msg.author.id != ADMINID:
        await msg.channel.send("Kun admin kan bruga denne funksjonen")
        return
    server = getServer(guild)
    await server.unrmUser(msg, guild)
    setServer(server)

async def addGrand(guild, msg):
    if msg.author.id != ADMINID:
        await msg.channel.send("Kun admin kan bruga denne funksjonen")
    gp = msg.content.split(" ", 1)[1]
    await addGP(msg, gp)

async def rmGP(guild, msg):
    if msg.author.id != ADMINID:
        await msg.channel.send("Kun admin kan bruga denne funksjonen")
    gp = msg.content.split(" ", 1)[1]
    await removeGP(msg, gp)

async def printGrand(guild, msg):
    await printGP(msg)

async def setGrand(guild, msg):
    if msg.author.id != ADMINID:
        await msg.channel.send("Kun admin kan bruga denne funksjonen")
    gp = msg.content.split(" ", 1)[1]
    await setGP(msg, gp)

async def newSea(guild, msg):
    if msg.author.id != ADMINID:
        await msg.channel.send("Kun admin kan bruga denne funksjonen")
    season = msg.content.split(" ", 1)[1]
    await newSeason(msg, season)

async def setSea(guild, msg):
    if msg.author.id != ADMINID:
        await msg.channel.send("Kun admin kan bruga denne funksjonen")
    season = msg.content.split(" ", 1)[1]
    await setSeason(msg, season)

async def rmgpsea(guild, msg):
    if msg.author.id != ADMINID:
        await msg.channel.send("Kun admin kan bruga denne funksjonen")
    gp = msg.content.split(" ", 1)[1]
    await removeGPseason(msg, gp)

async def csvC(guild, msg):
    if msg.author.id != ADMINID:
        await msg.channel.send("Kun admin kan bruga denne funksjonen")
    cfile = msg.content.split(" ", 1)[1]
    await csvToPkl(guild, msg, cfile)

commands = {
    "&rank" : rank,
    "&forklar" : forklar,
    "&listå" : tlist,
    "&server" : server,
    "&spams" : luckylist,
    "&customs" : customs,
    "&reset" : reset_customs,
    "&rename" : rename,
    "&rm" : remove,
    "&unrm" : unremove,
    "&addgp" : addGrand,
    "&rmgp" : rmGP,
    "&printgp" : printGrand,
    "&setgp" : setGrand,
    "&topgp" : ranking,
    "&upgp" : loadGP,
    "&news" : newSea,
    "&sets" : setSea,
    "&rmgps" : rmgpsea,
    "&csvtopkl" : csvC
}