import random
from kjellar.member import getServer

from kjellar.config import MAGNAR, ODDNY, KJELLARST

custom_channels = [975148464239435817, 975148601737113661]

async def customs(guild, msg):
    author = msg.author
    voice_channel = author.voice 
    users = []

    if voice_channel != None:
        if author.voice.channel.name == "Generelt" or author.voice.channel.name == "sofakroken":
            for user in author.voice.channel.members:
                if user.bot == False:
                    users.append(user)

            if len(users) > 1:
                num_users = len(users) // 2
                random.shuffle(users)
                team1 = users[:num_users]
                team2 = users[num_users:]

                msgstr = "Lag 1:\n"
                for player in team1:
                    try:
                        msgstr += f"{getServer(guild).users[player.id].displayname}"
                    except:
                        msgstr += f"{player.name}\n"
                    await player.move_to(guild.get_channel(MAGNAR))
                msgstr += "\nLag 2:\n"
                for player in team2:
                    try:
                        msgstr += f"{getServer(guild).users[player.id].displayname}"
                    except:
                        msgstr += f"{player.name}\n"
                    await player.move_to(guild.get_channel(ODDNY))
                await msg.channel.send(msgstr)
            else:
                await msg.channel.send("Beklage, men du e ensom og aleina. Få me deg någen så ska eg gjerna laga lag te deg!")
        else:
          await msg.channel.send("Dette kan eg kun hjelpa deg me viss du sitte i kjellarstuå eller sofakroken.")
    else:
        await msg.channel.send("Du e ikkje kobla te ein voice channel. Gjør de, så ska eg fiksa lag eg!")

async def reset_customs(guild, msg):
    author = msg.author

    if author.voice != None:
        if author.voice.channel.id in custom_channels:
            magnar = guild.get_channel(MAGNAR)
            oddny = guild.get_channel(ODDNY)
            dest = guild.get_channel(KJELLARST)
            
            for player in magnar.members:
                await player.move_to(dest)
            for player in oddny.members:
                await player.move_to(dest)
        else:
          await msg.channel.send("Dette kan eg kun hjelpa deg me viss du sitte i team Magnar eller team Oddny.")
    else:
        await msg.channel.send("Du e ikkje kobla te ein voice channel. Gjør de, så ska eg fiksa lag eg!")
