# from urlextract import URLExtract
import emoji
import pandas as pd
from collections import Counter

# extractor = URLExtract()

def fetch_stats(selected_user,df):

    if(selected_user != 'Overall'):
        df = df[df['Participants'] == selected_user]
        
    # nummber of messages
    num_messages = df.shape[0]

    # total number of words
    words = []
    for i in df['Messages']:
        words.extend(i.split())

    # media messages
    num_media_msgs = df[df['Messages'] == '<Media omitted>\n'].shape[0]

    # # links shared
    # links=[]
    # for message in df['Messages']:
    #     links.extend(extractor.find_urls(message))
    # all_links_df = links

    # user_links=[]
    # new_df = df[df['Participants'] == selected_user]['Messages']
    # for message in new_df:
    #     user_links.extend(extractor.find_urls(message))
    # links_df = user_links
    
    # emojis shared
    emoticon = []
    for message in df['Messages']:
        emoj = [c for c in message if c in emoji.EMOJI_DATA]
        emoticon.extend(emoj)

    # return num_messages,len(words), num_media_msgs, len(links), len(emoticon), links_df, all_links_df
    return num_messages,len(words), num_media_msgs, len(emoticon)

def most_busy_users(df):
    # most busy users 
    x = df['Participants'].value_counts().head()
    df = round((df['Participants'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'Participant','Participants':'Percent'})
    return x, df  

def most_common_word(selected_user, df):
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    if(selected_user != 'Overall'):
        df = df[df['Participants'] == selected_user]
    
    temp = df[df['Participants'] != 'Group notification'] 
    temp = temp[temp['Messages'] != '<Media omitted>']

    words = []

    for message in temp['Messages']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

# word finder
# def word_finder(df):
    # df[df.apply(lambda row: row.astype(str).str.contains(substring, case=False).any(), axis=1)]

def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['Participants'] == selected_user]
    
    emojis = []
    for message in df['Messages']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df


def monthly_timeline(selected_user,df):

    if(selected_user != 'Overall'):
        df = df[df['Participants'] == selected_user]

    timeline = df.groupby(['Year', 'month_num', 'Month']).count()['Messages'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['Month'][i] + "-" + str(timeline['Year'][i]))

    timeline['time'] = time
    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['Participants'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['Messages'].reset_index()
    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['Participants'] == selected_user]
    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['Participants'] == selected_user]
    return df['Month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['Participants'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='Messages', aggfunc='count').fillna(0)
    return user_heatmap
    
    





