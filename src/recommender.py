import csv
import heapq
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

# Stores points/max points to be gained for a particular attribute.
# Additionally, stores base sentence structure for reasoning.
attribute_points_and_reason_base: Dict = {
    "genre": (7, "genre match"),
    "mood": (5, "mood match"),
    "energy": (3, "energy is similar to preference"),
    "valence": (2, "valence is similar to preference"),
    "danceability": (1, "user prefers danceability "),
    "acousticness": (0.75, "user prefers acousticness "),
    "tempo_bpm": (0.5, "tempo bpm is similar to preference"),
}

class compare_attr_data_keys:
    key_name = 0
    song_value = 1
    user_pref_value = 2

class attribute_points_and_reason_base_keys:
    points = 0
    reason_base = 1

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the top k songs recommended for the given user."""
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a human-readable explanation for why a song was recommended to the user."""
        return "Explanation placeholder"

def _parse_value(value: str):
    """Converts a CSV string field to int/float when possible, else leaves it as a string."""
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        return value

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({key: _parse_value(value) for key, value in row.items()})
    return songs

def attr_score_str(data: tuple[str, str, str]) -> tuple:
    """Scores a string-valued attribute by whether the song's value matches the user's preference."""
    reward = attribute_points_and_reason_base[data[compare_attr_data_keys.key_name]]
    return data[compare_attr_data_keys.song_value] == data[compare_attr_data_keys.user_pref_value] and reward or (0,"")

def attr_score_float(data: tuple[str, float, float]) -> tuple:
    """Scores a numeric attribute by how close the song's value is to the user's preference."""
    attribute_name = data[compare_attr_data_keys.key_name]
    song_value = data[compare_attr_data_keys.song_value]
    user_pref_value = data[compare_attr_data_keys.user_pref_value]

    reward = attribute_points_and_reason_base[attribute_name]
    
    if attribute_name == "tempo_bpm": #tempo bpm is > 1 so:
        return (reward[attribute_points_and_reason_base_keys.points] * (min(song_value, user_pref_value) / max(song_value, user_pref_value)), reward[attribute_points_and_reason_base_keys.reason_base])
    else:
        return (reward[attribute_points_and_reason_base_keys.points]*(1 - abs(song_value - user_pref_value)), reward[attribute_points_and_reason_base_keys.reason_base])

def attr_score_bool(data: tuple[str, float, bool]) -> tuple:
    """Scores a boolean preference attribute based on the song's corresponding numeric value."""
    attribute_name = data[compare_attr_data_keys.key_name]
    song_value = data[compare_attr_data_keys.song_value]
    user_pref_value = data[compare_attr_data_keys.user_pref_value]
    
    reward = attribute_points_and_reason_base[attribute_name]
    if user_pref_value: # PREFERS
        return (reward[attribute_points_and_reason_base_keys.points] * song_value, reward[attribute_points_and_reason_base_keys.reason_base] + "more")
    else: # DOES NOT PREFER
        return (reward[attribute_points_and_reason_base_keys.points] * (1 - song_value), reward[attribute_points_and_reason_base_keys.reason_base] + "less")

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    attributes_dict: Dict = {}
    total_score = 0
    reasons: list[str] = []

    for key in user_prefs.keys():
        """
        compare_attr_data stores:
            * key_name | Song/UserProfile Attribute
            * song_value | Song Attribute Value
            * user_pref_value | User Profile Attribute value
        """
        compare_attr_data = (key, song[key], user_prefs[key])
        data_type = type(user_prefs[key]).__name__
        attributes_dict.setdefault(data_type, [])
        attributes_dict[data_type].append(compare_attr_data)

    for key, list_tuples in attributes_dict.items():
        for tuple_data in list_tuples:
            reward_data = None
            if key == "str":
                reward_data = attr_score_str(tuple_data)
            elif key in ("float", "int"):
                reward_data = attr_score_float(tuple_data)
            elif key == "bool":
                reward_data = attr_score_bool(tuple_data)
            else:
                raise Exception("score_song() FAILED | There is another data type in this set!")
            
            total_score += reward_data[attribute_points_and_reason_base_keys.points]
            if reward_data[attribute_points_and_reason_base_keys.points] > 0:
                reasons.append(f"(+{reward_data[attribute_points_and_reason_base_keys.points]:.3f}) - {reward_data[attribute_points_and_reason_base_keys.reason_base]}")

    # Expected return format: (score, reasons)
    return (total_score, reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, List[str]]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    # Expected return format: (song_dict, score, reasons)

    scored = (
        (song, score, reasons)
        for song in songs
        for score, reasons in (score_song(user_prefs, song),)
    )
    return heapq.nlargest(k, scored, key=lambda entry: entry[1])
