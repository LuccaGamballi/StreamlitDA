import streamlit as st
import datetime
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re


client_id = 'insert_spotify_dev_credentials'
client_secret = 'insert_spotify_dev_credentials'
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


df_original = pd.read_csv('C:\\Users\\lucca\\Desktop\\StreamlitDA\\hot-100-current _Filtered.csv')  

df = pd.read_csv('music_with_spotify_links.csv')

day =  None
month = None
year = None

st.set_page_config(
    page_title="Billboard Hits",
    page_icon=":musical_note:"
)

st.markdown("## Quais músicas eram populares quando eu nasci?")

st.markdown("Escolha o mês e o ano para ouvir as músicas que estavam no top 3 da Billboard naquele mês.")
st.markdown("Músicas disponíveis a partir de Agosto de 1958.")

col1, col2 = st.columns(2)

with col1:
    month = st.selectbox('Mês', 
                        options=range(1, 13),
                        format_func=lambda x: datetime.date(2000, x, 1).strftime('%B'))

with col2:
    year = st.selectbox('Ano',
                        options=range(1958, 2025))

if month != None and year != None:
    df["chart_week"] = pd.to_datetime(df["chart_week"])
    df_filtered = df[(df["chart_week"].dt.year == year) & 
                     (df["chart_week"].dt.month == month)]
    
    # Remove duplicates based on title, keeping the first occurrence (highest position)
    df_filtered = df_filtered.drop_duplicates(subset=['title'])
    
    # Sort by current_week and take top 3
    df_filtered = df_filtered.sort_values('current_week').head(3)
    
    # Display the results in a more readable format
    if not df_filtered.empty:
        st.write(f"Top 3 songs for {month}/{year}:")
        for i, (_, row) in enumerate(df_filtered.iterrows()):
            st.write(f"#{i+1}: {row['title']} - {row['performer']}")
            # Convert spotify link to embed format
            if pd.notna(row['spotify_link']):
                spotify_id = row['spotify_link'].split('/')[-1]
                spotify_embed = f'<iframe style="border-radius:16px" src="https://open.spotify.com/embed/track/{spotify_id}" width="100%" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>'
                st.markdown(spotify_embed, unsafe_allow_html=True)
            else:
                # Clean up the song title
                # Remove features, special characters, and parentheses content
                clean_title = re.sub(r'\(feat.*?\)|\(ft.*?\)|\(with.*?\)|\([^)]*\)', '', row['title'])
                clean_title = re.sub(r'[^\w\s]', '', clean_title).strip()
                
                # Search for the song on Spotify using only the title
                search_query = f"track:{clean_title}"
                results = sp.search(q=search_query, type='track', limit=1)
                
                if results['tracks']['items']:
                    spotify_id = results['tracks']['items'][0]['id']
                    spotify_embed = f'<iframe style="border-radius:16px" src="https://open.spotify.com/embed/track/{spotify_id}" width="100%" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>'
                    st.markdown(spotify_embed, unsafe_allow_html=True)
                else:
                    st.write("No Spotify link available for this song")
    else:
        st.write("No songs found for this period.")



