import json
import os
import mysql.connector

DB_HOST = "localhost"
DB_USER = "root"
DB_PW = ""
DB_SCHEMA_FILE = "db_schema.sql"
DIR_PATH = os.path.dirname(os.path.realpath(__file__))

# ============================================================================================================================================
# =======================================================          FONCTIONS              ====================================================
# ============================================================================================================================================

def get_json_data(json_filename):
  json_file = os.path.join(DIR_PATH, json_filename)
  with open(json_file) as json_data:
      return json.load(json_data)

def multi_insert(array, query, connect):
    print("Inserting data...")
    try:
      connect.cursor().executemany(query, array)
      connect.commit()
      print("Done!")
    except mysql.connector.Error as e:
      print('Error:', e)

# ============================================================================================================================================
# ======================================================               MYSQL                ==================================================
# ============================================================================================================================================

# connexion mysql
connect = mysql.connector.connect(
  host = DB_HOST,
  user = DB_USER,
  passwd = DB_PW
)
db_cursor = connect.cursor()

# création de la db
schema_file = os.path.join(DIR_PATH, DB_SCHEMA_FILE)
for line in open(schema_file).read().split(';\n'):
  if len(line) > 0: # ------------------------------------> À REVOIR 
    db_cursor.execute(line)

# ============================================================================================================================================
# ======================================================             INSERTION              ==================================================
# ============================================================================================================================================

seasons = []
episodes = []
subs = []

# création des listes avant insertion en db
for i in range(1,8):
  json_data = get_json_data(f"season{i}.json")
  for episode_str, subtitles_list in json_data.items():
    if len(subtitles_list) > 0:
      season_number = episode_str[17:19]
      if (season_number,) not in seasons:
        seasons.append((season_number,))
      episode_number = episode_str[20:22]
      episode_title = json.dumps(episode_str[23:].replace('.srt',''))
      episode = (episode_number, episode_title, season_number)
      episodes.append(episode)
      for subtitle_number, subtitle_content in subtitles_list.items():
        sub = (subtitle_number, subtitle_content, episode_number, season_number)
        subs.append(sub)

# insertion des saisons # ------------------------------------> À REVOIR (IGNORE IF EXISTS)
query = """INSERT INTO got.season (number) VALUES (%s)"""
multi_insert(seasons, query, connect)

# insertion des episodes # ------------------------------------> À REVOIR (IGNORE IF EXISTS)
query = """
  INSERT INTO 
    got.episode (number, title, season_id) 
  VALUES 
    (%s, %s, (SELECT s.id FROM got.season as s WHERE s.number = %s))
  """
multi_insert(episodes, query, connect)

# insertion des sous-titres # ------------------------------------> À REVOIR (IGNORE IF EXISTS)
query = """
  INSERT INTO 
    got.subtitle (number, content, episode_id) 
  VALUES 
    (%s, %s, (SELECT e.id FROM got.episode as e WHERE e.number = %s AND season_id = (
        SELECT s.id FROM got.season as s WHERE s.number = %s 
  )))
  """
multi_insert(subs, query, connect)

# fermeture du curseur
connect.cursor().close()
connect.close()







  #     ____                       
  #    /  __\                     ____                     
  #    \( oo                     (___ \                     
  #    _\_o/  Thx!                oo~)/
  #   / \|/ \      Cool db bruh! _\-_/_
  #  / / __\ \___               / \|/  \
  #  \ \|   |__/_)             / / .- \ \
  #   \/_)  |                  \ \ .  /_/
  #    ||___|                   \/___(_/
  #    | | |                     | |  |
  #    | | |                     | |  |
  #    |_|_|                     |_|__|
  #    [__)_)                   (_(___]