import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
from flask import Flask, request, jsonify
from flask_cors import CORS

load_dotenv()
NEO4J_URI = os.getenv('NEO4J_URI', 'bolt://localhost:7688')
NEO4J_USERNAME = os.getenv('NEO4J_USERNAME')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')

app = Flask(__name__)
CORS(app)

class Neo4jMusic:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def get_music_titles_by_genres(self, genres):
        with self._driver.session() as session:
            result = session.run("""
              MATCH (artist:Artist)-[:PRODUCED]->(track:Track)-[:OF_GENRE]->(genre:Genre) 
              WHERE toLower(genre.name) IN $genres
              RETURN track.name AS name, artist.name AS artist, genre.name AS genre
              ORDER BY name
              LIMIT 25 
            """, genres=genres)
            return [(record['name'], record['artist'], record['genre']) for record in result]
        
    def get_available_genres(self):
        with self._driver.session() as session:
            result = session.run("MATCH (genre:Genre) RETURN DISTINCT genre.name AS name")
            return [record["name"] for record in result]
        
@app.route("/genres", methods=['GET'])
def get_genres():
    try:
        neo4j = Neo4jMusic(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD)
        genres = neo4j.get_available_genres()
        neo4j.close()

        response = {'success': True, 'data': genres}
        return jsonify(response)

    except Exception as e:
        response = {'success': False, 'error': str(e)}
        return jsonify(response)
    
@app.route("/suggestions", methods=['GET'])
def get_tracks_by_genres():
    try:
        genres = request.args.get('genres')

        if not genres:
          return jsonify({"error": "Genres parameter missing"}), 400
    
        genres_list = list(map(lambda x: x.lower(), genres.split(',')))

        neo4j = Neo4jMusic(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD)
        tracks = neo4j.get_music_titles_by_genres(genres=genres_list)
        neo4j.close()

        result = [
            {'name': name, 'artist': artist, 'genre': genre}
            for name, artist, genre in tracks
        ]
        response = { 'success': True, 'data': result }
        return jsonify(response)

    except Exception as e:
        response = {'success': False, 'error': str(e)}
        return jsonify(response)


def add_tags_to_genres(self, genres, tags):
        with self._driver.session() as session:
            for genre, tag in zip(genres, tags):
                session.run("""
                MATCH (g:Genre {name: 'Rock'})
                MERGE (t1:Tag {name: '1: Rock'})-[:HAS_TAG]->(g)
                
                MATCH (g:Genre {name: 'Indie'})
                MERGE (t2:Tag {name: '2: Indie'})-[:HAS_TAG]->(g)
                
                MATCH (g:Genre {name: 'Alt'})
                MERGE (t3:Tag {name: '3: Alt'})-[:HAS_TAG]->(g)
                
                MATCH (g:Genre {name: 'Pop'})
                MERGE (t4:Tag {name: '4: Pop'})-[:HAS_TAG]->(g)
                
                MATCH (g:Genre {name: 'Metal'})
                MERGE (t5:Tag {name: '5: Metal'})-[:HAS_TAG]->(g)
                
                MATCH (g:Genre {name: 'HipHop'})
                MERGE (t6:Tag {name: '6: HipHop'})-[:HAS_TAG]->(g)
                
                MATCH (g:Genre {name: 'AltMusic'})
                MERGE (t7:Tag {name: '7: AltMusic'})-[:HAS_TAG]->(g)
                
                MATCH (g:Genre {name: 'Blues'})
                MERGE (t8:Tag {name: '8: Blues'})-[:HAS_TAG]->(g)
                
                MATCH (g:Genre {name: 'Acoustic/Folk'})
                MERGE (t9:Tag {name: '9: Acoustic/Folk'})-[:HAS_TAG]->(g)
                
                MATCH (g:Genre {name: 'Instumental'})
                MERGE (t10:Tag {name: '10: Instumental'})-[:HAS_TAG]->(g)
                
                MATCH (g:Genre {name: 'Country'})
                MERGE (t11:Tag {name: '11: Country'})-[:HAS_TAG]->(g)
                
                MATCH (g:Genre {name: 'Bollywood'})
                MERGE (t12:Tag {name: '12: Bollywood'})-[:HAS_TAG]->(g)
                """, genre=genre, tag=tag)


if __name__ == '__main__':
    app.run(debug=True)
        
