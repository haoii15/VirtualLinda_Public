import pandas as pd
from config import COLOR, FONT

def styleDf(df):

    styled = df.style.set_table_styles(
    [{'selector': 'th',
    'props': [('background', COLOR), 
                ('color', 'white'),
                ('font-family', FONT)]},
    
    {'selector': 'td',
    'props': [('font-family', FONT),
                ('color', 'white')]},

    {'selector': 'tr:nth-of-type(odd)',
    'props': [('background', COLOR)]}, 
    
    {'selector': 'tr:nth-of-type(even)',
    'props': [('background', COLOR)]},
    
    ]
    ).hide_index()

    return styled

def listToDf(list):
    df = pd.DataFrame(list, columns = ["rank", "navn", "level", "xp", "meldingar"])
    return df

def llistToDf(list):
    df = pd.DataFrame(list, columns = ["rank", "navn", "xp/msg", "lucky%"]).round(1)
    return df
