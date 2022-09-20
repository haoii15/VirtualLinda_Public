from itertools import count
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build

import pandas as pd
import dataframe_image as dfi
import df as dafr
import os
import pickle as pkl
import time

import discord

from kjellar.config import SPREADSHEETID, GPJSON, GPFILE, GPPATH, HUBS, READRANGES, ALFA, CHECKID, SEASON, SEASONS

def update():
    with open(GPFILE, "rb") as file:
        gp = pkl.load(file)

    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    creds = ServiceAccountCredentials.from_json_keyfile_name('skagesundvegen-gp-65093fbf62d5.json', scope)

    service = build("sheets", "v4", credentials = creds)

    ark = service.spreadsheets()

    result = ark.values().get(spreadsheetId = SPREADSHEETID, range=f"{gp}!I4:P500").execute()

    verdier = result.get("values", [])

    navn = []
    values = []
    laps = []

    troms = []
    tnavn = []
    jland = []
    jnavn = []
    aas = []
    anavn = []

    count = {}

    for row in verdier:
        if row[1] in count:
            count[row[1]] += 1
        else:
            count[row[1]] = 1
        
        

    max1 = max(count.values())
    max2 = 10

    for runder in count.values():
        if (runder > max2 and runder < max1):
            max2 = runder
    
    max2 += 10

    appended = {}
    
    for row in verdier:
        if row[1] in appended:
            appended[row[1]] += 1
        else:
            appended[row[1]] = 1
        
        if row[1] not in navn and row[6] == "1" and row[1] != "The Stig" and int(row[0]) <= max2:
            values.append([row[1],row[2],row[3],row[4],row[5]])
            navn.append(row[1])

        if row[1] not in tnavn and row[6] == "1" and row[1] != "The Stig" and int(row[0]) <= max2 and row[7] == "Tromsø":
            troms.append([row[1],row[2],row[3],row[4],row[5]])
            tnavn.append(row[1])

        if row[1] not in jnavn and row[6] == "1" and row[1] != "The Stig" and int(row[0]) <= max2 and row[7] == "Jørpeland":
            jland.append([row[1],row[2],row[3],row[4],row[5]])
            jnavn.append(row[1])

        if row[1] not in anavn and row[6] == "1" and row[1] != "The Stig" and int(row[0]) <= max2 and row[7] == "Ås":
            aas.append([row[1],row[2],row[3],row[4],row[5]])
            anavn.append(row[1])

    body = {
                    "values": values
    }

    tbody = {
                    "values": troms
    }

    jbody = {
                    "values": jland
    }
    
    abody = {
                    "values": aas
    }

    for key in count:
        if int(count[key]) <= max2:
            laps.append([key, count[key], 0])
        else:
            laps.append([key, max2, int(count[key]) - max2])

    laps = sorted(laps, key=lambda x: x[1], reverse=True)

    body1 = {
                    "values": laps
    }

    ark.values().update(
        spreadsheetId = SPREADSHEETID, 
        range=f"{gp}!B4", 
        valueInputOption="USER_ENTERED", 
        body=body
    ).execute()

    ark.values().update(
        spreadsheetId = SPREADSHEETID, 
        range=f"{gp}!B29", 
        valueInputOption="USER_ENTERED", 
        body=tbody
    ).execute()

    ark.values().update(
        spreadsheetId = SPREADSHEETID, 
        range=f"{gp}!B54", 
        valueInputOption="USER_ENTERED", 
        body=jbody
    ).execute()

    ark.values().update(
        spreadsheetId = SPREADSHEETID, 
        range=f"{gp}!B79", 
        valueInputOption="USER_ENTERED", 
        body=abody
    ).execute()

    ark.values().update(
        spreadsheetId = SPREADSHEETID, 
        range=f"{gp}!Q4", 
        valueInputOption="USER_ENTERED", 
        body=body1
    ).execute()

def gp_update():
    
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    creds = ServiceAccountCredentials.from_json_keyfile_name('skagesundvegen-gp-65093fbf62d5.json', scope)

    service = build("sheets", "v4", credentials = creds)

    ark = service.spreadsheets()

    if os.path.getsize(GPPATH) > 0:
        with open(GPPATH, "rb") as file:
            toprow = pkl.load(file)

    values = []
    toprow.insert(0, "Driver")
    toprow.append("Points")
    values.append(toprow)
    y=3

    for hub in HUBS:

        laps = {}
        scores = {}

        navn = []
        drivers = []

        for i in range(len(toprow)-2):
            if hub == "Tromsø" and i < 7:
                read = READRANGES["All"]
            else:
                read = READRANGES[hub]

            result = ark.values().get(spreadsheetId = SPREADSHEETID, range=f"{toprow[i+1]}!{read}").execute()

            med = []

            verdier = result.get("values", [])

            for row in verdier: 
                if row[0] == "":
                    break
                if row[0] in laps:
                    laps[row[0]].append(row[4])
                else:
                    navn.append(row[0])
                    lst = ["-"]*i
                    lst.append(row[4])
                    laps[row[0]] = lst

                if row[0] in scores:
                    scores[row[0]] += int(row[5])
                else:
                    scores[row[0]] = int(row[5])

                med.append(row[0])
            
            for dude in laps:
                if dude in med:
                    continue
                laps[dude].append("-")

        for driver in scores:
            lst = [driver]
            for i in range(len(laps[driver])):
                lst.append(laps[driver][i])
            lst.append(scores[driver])
            drivers.append(lst)

        drivers = sorted(drivers, key=lambda x: x[len(toprow)-1], reverse=True)
        
        drivers.insert(0, toprow)

        body = {
                        "values": drivers
        }

        ark.values().update(
            spreadsheetId = SPREADSHEETID, 
            range=f"Overall Ranking!B{y}", 
            valueInputOption="USER_ENTERED", 
            body=body
        ).execute()
        
        y+= 33
        time.sleep(60)


def season_update():
    
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    creds = ServiceAccountCredentials.from_json_keyfile_name('skagesundvegen-gp-65093fbf62d5.json', scope)

    service = build("sheets", "v4", credentials = creds)

    ark = service.spreadsheets()

    with open(GPPATH, "rb") as file:
        gps = pkl.load(file)

    with open(SEASONS, "rb") as file:
        seasons = pkl.load(file)
    
    y = 3

    for hub in HUBS:
        x = len(gps) + 4
        
        for season in seasons:
            g = 0
    
            values = []

            with open(f"../data/kjellar/gp/{season}.pkl", "rb") as source:
                toprow = pkl.load(source)

            toprow.insert(0, "Driver")
            toprow.append("Points")
            values.append(toprow)

            if (hub == "Jørpeland" or hub == "Ås") and season == "v22":
                x += len(toprow)
                continue

            laps = {}
            scores = {}

            navn = []
            drivers = []
            
            if hub == "Tromsø" and (season == "v22" or (season == "s22" and g < 7)):
                read = READRANGES["All"]
            else:
                read = READRANGES[hub]
            g+=1
            for i in range(len(toprow)-2):
                result = ark.values().get(spreadsheetId = SPREADSHEETID, range=f"{toprow[i+1]}!{read}").execute()

                med = []

                verdier = result.get("values", [])

                for row in verdier: 
                    if row[0] == "":
                        break
                    if row[0] in laps:
                        laps[row[0]].append(row[4])
                    else:
                        navn.append(row[0])
                        lst = ["-"]*i
                        lst.append(row[4])
                        laps[row[0]] = lst

                    if row[0] in scores:
                        scores[row[0]] += int(row[5])
                    else:
                        scores[row[0]] = int(row[5])

                    med.append(row[0])
                
                for dude in laps:
                    if dude in med:
                        continue
                    laps[dude].append("-")

            for driver in scores:
                lst = [driver]
                for i in range(len(laps[driver])):
                    lst.append(laps[driver][i])
                lst.append(scores[driver])
                drivers.append(lst)

            drivers = sorted(drivers, key=lambda x: x[len(toprow)-1], reverse=True)
            
            drivers.insert(0, toprow)

            body = {
                            "values": drivers
            }

            ark.values().update(
                spreadsheetId = SPREADSHEETID, 
                range=f"Overall Ranking!{ALFA[x]}{y}", 
                valueInputOption="USER_ENTERED", 
                body=body
            ).execute()
            x += len(toprow)
        y += 33
        time.sleep(60)

async def ranking(guild, msg):
    
    update()
    gp_update()

    split = msg.content.split(" ", 1)

    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    creds = ServiceAccountCredentials.from_json_keyfile_name(GPJSON, scope)

    service = build("sheets", "v4", credentials = creds)

    ark = service.spreadsheets()

    if os.path.getsize(GPPATH) > 0:
        with open(GPPATH, "rb") as file:
            gps = pkl.load(file)
    
    if len(split) == 1:

        result = ark.values().get(spreadsheetId = SPREADSHEETID, range="Overall Ranking!A4:Z25").execute()

        verdier = result.get("values", [])      

        rows =      []      
        driver =    []
        points =    []
        
        for row in verdier:

            if len(row) < 2:
                break

            rows.append(row[0])
            driver.append(row[1])
            points.append(row[2+len(gps)])

        data = {
            ""      : rows,
            "Driver": driver,
            "Points": points
        }

        df = pd.DataFrame(data = data, index = rows)

        dfi.export(dafr.styleDf(df), "gp.png")

        await msg.channel.send(file=discord.File("gp.png")) 
        return
    else:
        if split[1] in gps:

            gp = split[1]

            result = ark.values().get(spreadsheetId = SPREADSHEETID, range=f"{gp}!A4:F18").execute()

            verdier = result.get("values", [])      

            rows =       []      
            driver =     []
            sec1 =       []
            sec2 =       []
            sec3 =       []
            laptime =    []

            for row in verdier:
     
                if len(row) < 2:
                    break

                rows.append(row[0])
                driver.append(row[1])
                sec1.append(row[2])
                sec2.append(row[3])
                sec3.append(row[4])
                laptime.append(row[5])

            data = {
                ""        : rows,
                "Driver"  : driver,
                "Sector 1": sec1,
                "Sector 2": sec2,
                "Sector 3": sec3,
                "Lap Time": laptime
            }

            df = pd.DataFrame(data = data, index = rows)

            dfi.export(dafr.styleDf(df), f"{gp}.png")

            await msg.channel.send(file=discord.File(f"{gp}.png")) 

        else:
            await msg.channel.send(f"{split[1]} e isje et Grand Prix eg har hørt om.")

async def addGP(msg, gp):
    if os.path.getsize(GPPATH) > 0:
        with open(GPPATH, "rb") as file:
            gps = pkl.load(file)
    else:
        gps = ["Skagehrain GP", "Saudisund GP", "Simola GP", "Skaustralia GP", "Stakkelona GP", "Smonaco GP", "Stazerbadsjan GP", "Ska GP"]

    if gp not in gps:
        gps.append(gp)
        
        with open(GPPATH, "wb") as file:
            pkl.dump(gps, file)

        await msg.channel.send(f"La {gp} inn i systemet")
    else:
        await msg.channel.send("GP e allerede i systemet")
    
    with open(SEASON, "rb") as seas:
        season = pkl.load(seas)

        if os.path.getsize(f"../data/kjellar/gp/{season}.pkl") > 0:
            with open(f"../data/kjellar/gp/{season}.pkl", "rb") as file:    
                sgps = pkl.load(file)
        else:
            sgps = []

        if gp not in sgps:
            sgps.append(gp)

            with open(f"../data/kjellar/gp/{season}.pkl", "wb") as dest:
                pkl.dump(sgps, dest)
            await msg.channel.send(f"La te {gp} i tellende sesong")
        else:
            await msg.channel.send("GP allerede i tellende sesong")
            
        


async def removeGP(msg, gp):
    if os.path.getsize(GPPATH) > 0:
        with open(GPPATH, "rb") as file:
            gps = pkl.load(file)

    if gp in gps:
        gps.remove(gp)
        
        with open(GPPATH, "wb") as file:
            pkl.dump(gps, file)

        await msg.channel.send(f"Fjerna {gp} fra systemet")
        return 

    await msg.channel.send("GP e isje i systemet")

async def printGP(msg):
    if os.path.getsize(GPPATH) > 0:
        with open(GPPATH, "rb") as file:
            gps = pkl.load(file)

    with open(SEASON, "rb") as source:
        season = pkl.load(source)
        with open(f"../data/kjellar/gp/{season}.pkl", "rb") as file:
            seasongps = pkl.load(file)

    await msg.channel.send(f"all time: {gps}")
    await msg.channel.send(f"tellende sesong: {seasongps}")

async def setGP(msg, gp):
    if os.path.getsize(GPPATH) > 0:
        with open(GPPATH, "rb") as file:
            gps = pkl.load(file)

    if gp in gps:
        with open(GPFILE, "wb") as file:
            pkl.dump(gp, file)

        await msg.channel.send(f"{gp} e nå satt som GP")
    else:
        await msg.channel.send(f"{gp} e ingen GP i mitt system")

async def newSeason(msg, season):
    if os.path.getsize(SEASONS) > 0:
        with open(SEASONS, "rb") as source:
            seasons = pkl.load(source)
    else:
        seasons = ["v22", "h22", "s22"]

    if season in seasons:
        await msg.channel.send(f"{season} e allerde i systeme")
        return
    
    seasons.append(season)

    with open(SEASONS, "wb") as dest:
        pkl.dump(seasons, dest)

    with open(f"../data/kjellar/gp/{season}.pkl", "wb") as file:
        new = []
        pkl.dump(new, file)

    await msg.channel.send(f"{season} e oppretta som en sesong")
    await setSeason(msg, season)
    
async def setSeason(msg, season):
    with open(SEASON, "wb") as dest:
        pkl.dump(season, dest)

    await msg.channel.send(f"{season} e satt som tellende sesong")

async def removeGPseason(msg, gp):

    with open(SEASON, "rb") as file:
        season = pkl.load(file)
        with open(f"../data/kjellar/gp/{season}.pkl", "rb") as source:
            gps = pkl.load(source)

    if gp in gps:
        gps.remove(gp)
        
        with open(f"../data/kjellar/gp/{season}.pkl", "wb") as dest:
            pkl.dump(gps, dest)

        await msg.channel.send(f"Fjerna {gp} fra tellende sesong")
        return 

    await msg.channel.send("GP e isje i tellende sesong")
    

async def loadGP(guild, msg):
    update()
    await msg.channel.send("1/3")
    gp_update()
    await msg.channel.send("2/3")
    season_update()
    await msg.channel.send("3/3")
    await msg.add_reaction(await guild.fetch_emoji(CHECKID))

if __name__ == '__main__':
    update()
    gp_update()