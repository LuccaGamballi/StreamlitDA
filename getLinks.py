import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


client_id = 'insert_spotify_dev_credentials'
client_secret = 'insert_spotify_dev_credentials'
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


df = pd.read_csv('C:\\Users\\lucca\\Desktop\\StreamlitDA\\hot-100-current _Filtered.csv')  

def get_spotify_link(track_name, artist_name=None):
    try:
        # Create search query
        query = track_name
        if artist_name:
            query += f' artist:{artist_name}'
            
        # Search for the track
        results = sp.search(q=query, type='track', limit=1)
        
        # Get the first result's URL
        if results['tracks']['items']:
            return results['tracks']['items'][0]['external_urls']['spotify']
        return None
    except Exception as e:
        print(f"Error searching for {track_name}: {str(e)}")
        return None

# Add Spotify links to the dataframe
def add_spotify_links(df):
    spotify_links = []
    for index, row in df.iterrows():
        # Adjust these column names based on your CSV structure
        track_name = row['title']  # Replace with your track name column
        artist_name = row.get('performer', None)  # Replace with your artist column if available
        
        link = get_spotify_link(track_name, artist_name)
        spotify_links.append(link)
        print(index, row, link)
    df['spotify_link'] = spotify_links
    return df

# Process the dataframe and save results
df = add_spotify_links(df)
df.to_csv('music_with_spotify_links.csv', index=False)
