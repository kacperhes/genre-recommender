import os
import pandas as pd
from dotenv import load_dotenv
from neo4j import GraphDatabase

# Env variables
load_dotenv()

NEO4J_URI = os.getenv('NEO4J_URI', 'bolt://localhost:7688')
NEO4J_USERNAME = os.getenv('NEO4J_USERNAME')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')

# Neo4j authentication
class Neo4jRecommendations:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    # def write_uniqueness_constaints(self):
    #     with self._driver.session() as session:
    #         session.run("CREATE CONSTRAINT ON (track:Track) ASSERT track.id IS UNIQUE")
    #         session.run("CREATE CONSTRAINT ON (tag:Tag) ASSERT tag.name IS UNIQUE")
    #         print("Database constaints added successfully!")

    def write_genres(self, genres):
      with self._driver.session() as session:
          query = """
            UNWIND $genres as genre
            MERGE (g:Genre {name: genre})
          """
          session.run(query, genres=genres)
          print("Genres added successfully!")

    def write_artists(self, artists):
        with self._driver.session() as session:
            query = """
                UNWIND $artists as artist
                MERGE (a:Artist {name: artist})
            """
            session.run(query, artists=artists)
            print("Artists added successfully")

    def write_track(self, track):
        with self._driver.session() as session:
            query  = """
                MERGE (t:Track {name: $track.name})
                WITH t
                MATCH (genre:Genre)
                MATCH (artist:Artist)
                WHERE genre.name = $track.genre AND artist.name = $track.artist
                MERGE (artist)-[:PRODUCED]->(t)-[:OF_GENRE]->(genre)
            """
            session.run(query, track=track)
            print(f"Track {track['name']} added sucessfully")

    def rollback(self):
        with self._driver.session() as session:
            # session.run("DROP CONSTRAINT ON (track:Track) ASSERT track.id IS UNIQUE")
            # session.run("DROP CONSTRAINT ON (tag:Tag) ASSERT tag.name IS UNIQUE")
            session.run("MATCH (genre:Genre) DETACH DELETE genre")
            session.run("MATCH (artist:Artist) DETACH DELETE artist")
            session.run("MATCH (track:Track) DETACH DELETE track")
            print("Rollback run successfully!")

def map_music_gernes(music_id):
    genres_map = {
        1: 'Rock',
        2: 'Indie',
        3: 'Alt',
        4: 'Pop',
        5: 'Metal',
        6: 'HipHop',
        7: 'AltMusic',
        8: 'Blues',
        9: 'Acoustic/Folk',
        10: 'Instumental',
        11: 'Country',
        12: 'Bollywood'
    }
    genre = genres_map.get(music_id, 'Unknown')
    return genre

# data preprocessing
df = pd.read_csv('../data/songs.csv')
df.rename(
    columns={
        'Class': 'genre',
        'Artist Name': 'artist',
        'Track Name': 'name',
        'Popularity': 'popularity'
    }, 
    inplace=True
)
df['genre'] = df['genre'].map(map_music_gernes)

unique_artists = df['artist'].unique()
unique_genres = df['genre'].unique()

neo4j = Neo4jRecommendations(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD)

if __name__ == '__main__':
    try:
        neo4j.write_artists(artists=unique_artists)
        neo4j.write_genres(genres=unique_genres)

        for index, row in df.iterrows():
            neo4j.write_track(track=row.to_dict())

        print("Database seeded successfully")
    except Exception as e:
        print(f"An error occured: {str(e)}")
        neo4j.rollback()
    finally:
        neo4j.close()