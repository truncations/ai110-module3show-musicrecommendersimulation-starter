# 7/7/2026
## Data Types involved in both collaborative and content-based filtering
Collaborative Filtering:
- Songs played
- Songs skipped
- Likes/dislikes
- Playlists
- Watch time (YouTube)
- Replays
- Search history
- Time of day
- Device used
Content-Based Filtering:
- Tempo of song
- Any vocals in song?
- Energy of song
- Moods

## Schema
Plan according to content-based filtering as instructed:
"Attach songs.csv and ask your AI coding assistant to analyze the available data and suggest which features would be most effective for a simple content-based recommender." (Codepath, Project: Music Recommender Simulation)

Claude Suggests the following features for determining "musical vibe" and content-based recommendations:
- Genre
- Mood
- Energy
- valence
- Danceability
- Acousticness
- Tempo_bpm

To officialize, my "algorithm recipe" or how I will score my songs will be of the order:
1. Genre 
2. Mood
3. Energy
4. Valence
5. Danceability
6. Acousticness
7. Tempo BPM
Other than Genre and Mood, they are scored numerically which means we can mathematically match towards a user's preference based on what they listen to.

Prompt a mathematical based scoring rule:
    "How can I design a mathematically-based 'Scoring Rule' for my simple content-based recommender system where I calculate the score for a song's similarity to a user's preference based on the song's attributes of the following order (for weighting; left is most weight, right is least weight generally): Genre, Mood, Energy, Valence, Danceability, Acousticness, and Tempo BPM.
    
    I understand that mathematically, we need to calculate the error and use that error to determine a score for the song's similarity, and that we'll use a Ranking Rule to determine which songs should be recommended to the user.
    
    For genre and mood matching, because they both are string-based and not actually numerical-based, how could I compute a value of error between the song's genre/mood to the user's preference? There are genres out in music that can be closely similar and I would like to know how I could handle these situations.
    
    Lastly, given the context of the recommender file that contains the classes to be used for this project, how would I determine features that the classes 'Song', 'UserProfile' would use? Does features under this context of developing a song recommender system mean what attributes from those classes would I use or methods to create for it? (Or would it be both?)"

## 7/14/2026
Define specific "taste profile":

taste_profile = {
    "favorite_genre": "pop"
    "favorite_mood": "intense"
    "target_energy": "0.90"
    "likes_acoustic": False
    "likes_danceability": True
    "target_tempo_bpm": "140"
    "target_valence": "0.7"
}