"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Starter example profile
    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy":  0.90,
        "acousticness": False,
        "danceability": True,
        "tempo_bpm": 140,
        "valence": 0.7,
    }

    user_prefs_test_2 = {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.20,
        "acousticness": True,
        "danceability": False,
        "tempo_bpm": 70,
        "valence": 0.4,
    }

    user_prefs_test_3 = {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.95,
        "acousticness": False,
        "danceability": False,
        "tempo_bpm": 160,
        "valence": 0.2,
    }

    # Genre/mood point to a slow, low-energy song ("Winter's Requiem": energy 0.25,
    # tempo 66) but every numeric field asks for the opposite. Tests whether
    # genre+mood match still wins despite a bad numeric fit.
    user_prefs_conflict_genre_vs_tempo = {
        "genre": "classical",
        "mood": "melancholic",
        "energy": 0.90,
        "acousticness": False,
        "danceability": True,
        "tempo_bpm": 180,
        "valence": 0.9,
    }

    # Matches "Neon Pulse Rave" (house/euphoric) on every field except
    # acousticness is flipped. Tests whether one contradicting low-weight
    # attribute can knock an otherwise near-perfect match out of the top spot.
    user_prefs_conflict_impossible_combo = {
        "genre": "house",
        "mood": "euphoric",
        "energy": 0.88,
        "acousticness": True,
        "danceability": True,
        "tempo_bpm": 128,
        "valence": 0.90,
    }

    # Tuned almost exactly between "Midnight Coding" and "Library Rain", which
    # both match genre+mood equally. Tests whether ranking correctly favors
    # the numerically closer song rather than falling back on tie order.
    user_prefs_tiebreak_lofi_chill = {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.40,
        "acousticness": True,
        "danceability": True,
        "tempo_bpm": 79,
        "valence": 0.58,
    }

    test_profiles = [
        ("Starter example", user_prefs),
        ("Test 2 (lofi/chill)", user_prefs_test_2),
        ("Test 3 (rock/intense)", user_prefs_test_3),
        ("Conflict: genre vs tempo", user_prefs_conflict_genre_vs_tempo),
        ("Conflict: impossible combo", user_prefs_conflict_impossible_combo),
        ("Tie-break: lofi/chill", user_prefs_tiebreak_lofi_chill),
    ]

    print(f"\nLoaded songs: {len(songs)}")

    for label, prefs in test_profiles:
        recommendations = recommend_songs(prefs, songs, k=5)

        print(f"\n=== {label} ===")
        print("=" * 60)
        print("Selected preferences:")
        for key, value in prefs.items():
            print(f"   {key}: {value}")
        for rank, (song, score, reasons) in enumerate(recommendations, start=1):
            print(f"\n{rank}. {song['title']} - Score: {score:.2f}")
            print(f"   Artist: {song['artist']}")
            print("   Reasons:")
            for reason in reasons:
                if reason.endswith("- "):
                    continue  # zero-point, no explanatory text to show
                print(f"     - {reason}")
        print()


if __name__ == "__main__":
    main()
