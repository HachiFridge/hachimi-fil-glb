import json
import os
import sqlite3

master_db = sqlite3.connect(os.environ["MASTER_MDB_LOC"])
master_db.row_factory = sqlite3.Row
character_system_text = json.load(open('localized_data/character_system_text_dict.json'))


character_system_text_translated = {}
character_system_text_total = {}

def get_character_name(id_: int) -> str:
    return master_db.execute('SELECT "text" FROM text_data WHERE category = 6 AND "index" = ?', (id_,)).fetchone()["text"]

for x in master_db.execute(
    'SELECT character_id, character_id, voice_id FROM character_system_text'
).fetchall():
    _character_id = x["character_id"]
    _voice_id = x["voice_id"]

    if _character_id not in character_system_text_translated:
        character_system_text_total[_character_id] = 0
        character_system_text_translated[_character_id] = 0

    character_system_text_total[_character_id] += 1

    if str(_character_id) in character_system_text:
        if str(_voice_id) in character_system_text[str(_character_id)]:
            character_system_text_translated[_character_id] += 1

result = """
| Character | Strings Translated | Total Strings | % |
| --- | --- | --- | --- |
"""


for x in character_system_text_total:
    result += f"| {get_character_name(x)} | {character_system_text_translated[x]} | {character_system_text_total[x]} | {character_system_text_translated[x] / character_system_text_total[x]:.2%} |\n"

print(result)



