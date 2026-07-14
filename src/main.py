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

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print(f"\nLoaded songs: {len(songs)}")
    print("\nTop Recommendations")
    print("=" * 60)
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
