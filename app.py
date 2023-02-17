import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_option_menu import option_menu

# col1,col2= st.columns(2)
# with col1:
#     st.write('')
# with col2:
#     # st.write(' ')
st.success("Whatsapp Chat Analyser")
# # with col3:
# #     st.write('')

st.sidebar.warning('Drop Whatsapp text file only')
st.sidebar.header('How to get whatsapp text file?')
st.sidebar.write('-> Open a chat\n\n-> Click on more\n\n-> Export chat\n\n-> Without media')
st.sidebar.write('')
# st.sidebar.write('-> Open a chat \n-> Click on more\n-> Export chat\n-> Without media')
uploaded_file = st.sidebar.file_uploader("Choose a txt file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    # converting byte stream to string
    data = bytes_data.decode('utf-8') 
    df = preprocessor.preprocess(data)

    # fetching participant names
    user_list = df['Participants'].unique().tolist()
    user_list.remove('Group notification')
    user_list.sort()
    user_list.insert(0,'Overall')

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)
    if st.sidebar.button("Show Analysis"):
        # num_messages, words, num_media_msgs, links, emoticon, links_df, all_links_df = helper.fetch_stats(selected_user,df)
        num_messages, words, num_media_msgs, emoticon= helper.fetch_stats(selected_user,df)
        
        if(selected_user == 'Overall'):
            st.title('Messages')
            st.dataframe(df)
        else:   
            user_df = df[df['Participants'] == selected_user]
            st.dataframe(user_df)

        col1, col2, col3, col4= st.columns(4)
        with col1:
            st.header('Total messages')
            st.title(num_messages)
        with col2:
            st.header('Total words')
            st.title(words) 
        with col3:
            st.header('Media Shared')
            st.title(num_media_msgs)
        # with col4:
        #     st.header('Links Shared')
        #     st.title(links)
        with col4:
            st.header('Emojis Shared')
            st.title(emoticon)
        
        # if selected_user is not 'Overall':
        #     st.subheader("Links shared by " + selected_user + ":")
        #     st.dataframe(links_df)
        # else:
        #     st.subheader("Links shared:")
        #     st.dataframe(all_links_df)

        # monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['Messages'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['Messages'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title('Activity Map')
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)


        # Group Analysis
        if(selected_user == 'Overall'):
            st.title("Most Busy Users")
            x,msg_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1,col2 = st.columns(2)
            
            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(msg_df)


        # emoji analysis
        st.title('Emoji Analysis')
        emoji_df = helper.emoji_helper(selected_user, df)

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

hide_st_style = """
            <style>
            # MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            # header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

stll = """
<h3 align="left">Made with ❤️ by Arunim</h3>
<p align="left">
<a href="https://www.linkedin.com/in/arunim-malviya-271ba5201/" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/linked-in-alt.svg" alt="arunim malviya" height="30" width="40" /></a>
<a href="https://instagram.com/arunimm_" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/instagram.svg" alt="arunim__" height="30" width="40" /></a>
<a href="https://github.com/Arunim313" target="blank"><img align="center" src="https://github.com/rahuldkjain/github-profile-readme-generator/blob/master/src/images/icons/Social/github.svg" alt=Arunim313 height="30" width="40" /></a>
</p>
"""

st.markdown(stll, unsafe_allow_html=True)
