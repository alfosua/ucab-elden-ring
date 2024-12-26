import os
import json

SAVES_PATH = "saves"
SAVES_INDEX_JSON_PATH = f"{SAVES_PATH}/index.json"

def init():
    if not os.path.exists(SAVES_PATH):
        os.mkdir(SAVES_PATH)
    if not os.path.exists(SAVES_INDEX_JSON_PATH):
        saves_index = create_index_starter()
        with open(SAVES_INDEX_JSON_PATH, "w") as fp:
            json.dump(saves_index, fp, indent=2, ensure_ascii=True)

def load_index():
    with open(SAVES_INDEX_JSON_PATH, "r") as fp:
        return json.load(fp)

def create_index_starter() -> dict:
    return {
        "version": 1,
        "saves": []
    }
