import json
import os
import mysql.connector

DB_HOST = "localhost"
DB_USER = "root"
DB_PW = ""
DB_NAME = "got"
DB_TABLE = "subtitles"
JSON_FILES_COUNT = 7
QUERIES = {
  "insert" : "INSERT INTO " + DB_NAME + "." + DB_TABLE + " (SEASON_ID, EPISODE_ID, EPISODE_NAME, SUBTITLE_ID, SUBTITLE_CONTENT) VALUES (%s,%s,%s,%s,%s)",
  "create_db" : "CREATE DATABASE IF NOT EXISTS " + DB_NAME,
  "create_table": "CREATE TABLE IF NOT EXISTS " + DB_NAME + "." + DB_TABLE +
      """(
        ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
        SEASON_ID INT NOT NULL,
        EPISODE_ID INT NOT NULL,
        EPISODE_NAME VARCHAR(255),
        SUBTITLE_ID INT NOT NULL,
        SUBTITLE_CONTENT VARCHAR(255)
      )
      """
}

# ============================================================================================================================================
# =======================================================          FONCTIONS              ====================================================
# ============================================================================================================================================

def get_json_data(json_filename):
  dir_path = os.path.dirname(os.path.realpath(__file__))
  json_file = os.path.join(dir_path, json_filename)
  with open(json_file) as json_data:
      return json.load(json_data)

def insert_subtitles(subtitles, connect):
  print("Inserting subtitles... Please do not blink...")
  try:
    connect.cursor().executemany(QUERIES['insert'], subtitles)
    connect.commit()
    print("Woah! Already done?!")
  except mysql.connector.Error as e:
    print('Error:', e)
  finally:
    connect.cursor().close()
    connect.close()

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
db_cursor.execute(QUERIES['create_db'])

# création de la table
db_cursor.execute(QUERIES['create_table'])

# ============================================================================================================================================
# ======================================================             INSERTION              ==================================================
# ============================================================================================================================================

subs = []

# création d'une liste de sous-titres (tuples) à insérer 
for i in range(JSON_FILES_COUNT):
  json_data = get_json_data("season"+str(i+1)+".json")
  for episode_str, subtitles_list in json_data.items():
    if len(subtitles_list) > 0:
      season_id = episode_str[17:19]
      episode_id = episode_str[20:22]
      episode_name = json.dumps(episode_str[23:].replace('.srt',''))
      for subtitle_id, subtitle_content in subtitles_list.items():
        sub = (season_id, episode_id, episode_name, subtitle_id, subtitle_content)
        subs.append(sub)
      
# insertion en bdd
insert_subtitles(subs, connect)











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