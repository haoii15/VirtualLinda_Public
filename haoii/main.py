from config import BOTID, HAOIIID
from haoii.config import LUCKYID, ADMINID, PREFIX
from haoii.member import getServer, setServer



async def newMessage(client, msg):
    guild = client.get_guild(HAOIIID)

    if msg.author.id != BOTID and msg.guild == guild and msg.content.startswith(PREFIX) == False and msg.channel.name != "modchat":
        await userMessage(guild, msg)

    await commandCheck(guild, msg)

async def userMessage(guild, msg):
    server = getServer(guild)
    got = await server.newMsg(guild, msg)
    
    fetch = got[0]
    user = got[1]
    if type(fetch[0]) == list:
        if "lucky" in fetch[0]:
            await msg.add_reaction(await guild.fetch_emoji(LUCKYID))
    
    if "rank" in fetch:
        retMsg = f"Congrats **{user.displayname}**!\n"
        retMsg += f"*{msg.channel.name} + you = {user.rank}*!" 


        await msg.channel.send(retMsg)
    
    setServer(server)

async def commandCheck(guild, msg):
    if msg.content.startswith(PREFIX):
        try:
            await commands[msg.content.split(" ", 1)[0]](guild, msg)
        except:
            await msg.channel.send("That is not a command, or I failed handling it.")

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

async def rename(guild, msg):
    server = getServer(guild)
    await server.renameUser(msg)
    setServer(server)

async def remove(guild, msg):
    if msg.author.id != ADMINID:
        await msg.channel.send("Only the admins can use that function")
        return
    server = getServer(guild)
    await server.rmUser(msg, guild)
    setServer(server)

async def unremove(guild, msg):
    if msg.author.id != ADMINID:
        await msg.channel.send("Only the admins can use that function")
        return
    server = getServer(guild)
    await server.unrmUser(msg, guild)
    setServer(server)


commands = {
    "!rank" : rank,
    "!listå" : tlist,
    "!server" : server,
    "!spams" : luckylist,
    "!rename" : rename,
    "!rm" : remove,
    "!unrm" : unremove
}