import pandas as pd
import re

def preprocess(data): 
    
    # Assuming time format is in 24hr format not in AM PM
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern,data)

    df = pd.DataFrame({'user_message':messages, 'message_date':dates})
    # converting message_date format
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %H:%M - ')
    df.rename(columns={'message_date':'Date'}, inplace=True)

    participants = []
    messages = []
    for message in df['user_message']:
        user = re.split('([\W\w]+?):\s',message)
        if(user[1:]):
            participants.append(user[1])   # participant name
            messages.append(user[2])   # message
        else:
            participants.append('Group notification')
            messages.append(user[0])

    df['Participants'] = participants
    df['Messages'] = messages
    df.drop(columns = ['user_message'], inplace=True)

    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month_name() 
    df['Day'] = df['Date'].dt.day
    df['Hour'] = df['Date'].dt.hour
    df['Minute'] = df['Date'].dt.minute
    df['day_name'] = df['Date'].dt.day_name()
    df['only_date'] = df['Date'].dt.date
    df['month_num'] = df['Date'].dt.month

    period = []
    for hour in df[['day_name', 'Hour']]['Hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df



