import csv
from kjellar.member import Member, getServer, setServer

async def csvToPkl(guild, msg, file):
    csvf = open(file, "rt")
    reader = csv.reader(csvf)

    server = getServer(guild)
    nr = 1    
    for line in reader:
        if line[0] == "name":
            continue

        for user in guild.members:
            print(line[0])
            print(user.name)
            if line[0] == user.name:
                uid = user.id
                break

        server.users[uid] = Member(guild, uid, line[0], int(line[2]), int(line[1]), int(line[3]), int(line[6]), int(line[4]))
        await msg.channel.send(f"added {line[0]} to the database.")
        nr += 1
    
    setServer(server)