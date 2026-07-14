# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

In order to recommend a song based on the knowledge of how real world recommendations for large-scale applications like YouTube and Spotify, scores are assigned to each song in a given data set based on the song's attributes similiarity to the user's preferences (content-based filtering) for which after scores are assigned, the songs with their scores are organized in a high score to low score manner, and we'll pull the top songs from the list; the number of songs we get starting from the top varies.
For the system, I would have a `Song` use the attributes already provided in `recommender.py` as provided: 
    - id: int
    - title: str
    - artist: str
    - genre: str
    - mood: str
    - energy: float
    - tempo_bpm: float
    - valence: float
    - danceability: float
    - acousticness: float
These store essential information that I would need for a song in general. Of these attributes for the `Song` class, I would use the following attributes to develop the recommender system and compute a similarity value: "genre", "mood", "energy", "tempo_bpm", "valence", "danceability", "acousticness". 

The information that `UserProfile` will store would be what `Song` stores except that it would store a target value for each `Song` attribute (basically getting a user's preference for genre, mood,  energy, tempo_bpm, valence, danceability, and acousticness). If there are missing variables that need to be added, it will be done so during system implementation. (likes_danceability, target_valence, target_tempo_bpm)

In order for `Recommender` to compute a score for each song, we'll use a basic mathematical error analysis between a `Song`'s attribute (values) and the `UserProfile`'s information. We may use the error formula (1 - |A - B|) as one example. If they are strings, we'll simply determine if the string itself matches with the user's preferences. Then we'll weigh each attribute being used to determine a song for recommendation. Once weighed, we'll add sub-scores to the final score for each considered attribute (and consider their weight towards the final score). This score will be then used to compute a list of songs sorted by top score to lowest score, and we'll pick out the first few top elements.

## Algorithm Recipe
1. Yield Song's Attributes and UserProfile's Attributes.
    - id: int      
    - title: str 
    - artist: str             
    - genre: str               favorite_genre: str
    - mood: str                favorite_mood: str
    - energy: float            target_energy: float
    - tempo_bpm: float         target_tempo_bpm: float
    - valence: float           target_valence: float
    - danceability: float      likes_danceability: bool
    - acousticness: float      likes_acoustic: bool
2. Create tuples to store pairs of values that are being compared.
    ex. (genre, favorite_genre)
3. Create a dictionary to determine which comparion operation to utilize to subscore the attribute (for which it will be added to the final score later). Keys will be of the data type respectively from the `UserProfile` attributes.
    ex.
    {
        "str": list[tuple[str,str]]
        "float": list[tuple[float,float]]
        "bool": list[tuple[float,bool]]
    }
4. For each key -> value map, use the corresponding scoring operation.
    "str": Compare whether the genre/mood of the song exactly matches with the user's preference genre/mood.
    "float": Use a basic mathematic formula to determine the error of value between the 2 float values.
        error = (| A - B |) IF AND ONLY IF A, B = [0, 1].
        such that A is the song's attribute value, and B is the user's attribute value.
    "bool": The following scenarios are to be considered:
        * If the user does NOT like the given attribute, then a lower value of the song's attribute will be scored higher.
        * If the user does LIKE the given attribute, then a higher value of the song's attribute will be scored higher.

    (!) THERE MAY BE A SPECIAL CASE WHERE WE'LL HAVE TO IMPLEMENT AN ALTERNATIVE COMPARISON SCORING METHOD FOR TEMPO_BPM.
5. To properly point-weigh each attribute of a song, we'll follow this general idea of how scoring should be weighed, from 1 being the highest and 7 being the lowest:
                1. Genre         5. Danceability
                2. Mood          6. Acousticness
                3. Energy        7. Tempo BPM
                4. Valence
Then, we'll provide numerical amounts for how much points should be awarded for a song's similarity to the user's preference.
    (*) Genre [IF EXACT MATCH] provides 7 points.
    (*) Mood [IF EXACT MATCH] provides 5 points.
    (*) Energy provides 3 * [NON-ERROR] points.
    (*) Valence provides 2 * [NON-ERROR] points.
    (*) Danceability provides 1 * [SCALE] points.
    (*) Acousticness provides 0.75 * [SCALE] points.
    (*) Tempo BPM provides 0.5 * [NON-ERROR] points.
6. After computing subscores for each comparable attribute, we will then sum the subscores to get one final official score of similarity between the `Song` and the `UserProfile`. This can then be added to a list of songs with their computed similarity scores.
7. Sort the list of computed similarity scores by highest score, and pull the first number of elements of our choosing, 5 is our default.

Some potential biases that may occur during this analysis:
    * Genre and Mood are both singular-matching cases; it may be too strict to "exactly" match the genre/mood to the user's preference because there are genres/moods that can be SIMILAR to the user's preference but not exact. Vice versa can be said.
        (!) Because they are strict and are singular-match only, for one of the attributes to fail, it could mean missing songs that are perfect for the user because of its other passing attribute.
    * Because we only determine whether the values are high enough or low enough for the attributes "acousticness" and "danceability" (through like_acoustic and like_danceability respectively), we only consider extreme values as "valuable" information even though we should be looking for a target value since a user could like acousticness, even though their target acoustic value might actually be like 0.6 than 1.0.
    
## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

Assuming the following:
user_prefs = {
    "genre": "pop",
    "mood": "happy",
    "energy":  0.90,
    "acousticness": False,
    "danceability": True,
    "tempo_bpm": 140,
    "valence": 0.7,
}

```
Loaded songs: 18

Top Recommendations
============================================================

1. Sunrise City - Score: 18.31
   Artist: Neon Echo
   Reasons:
     - (+7.000) - genre match
     - (+5.000) - mood match
     - (+2.760) - energy is similar to preference
     - (+1.720) - valence is similar to preference
     - (+0.615) - user prefers acousticness less
     - (+0.790) - user prefers danceability more
     - (+0.421) - tempo bpm is similar to preference

2. Gym Hero - Score: 13.83
   Artist: Max Pulse
   Reasons:
     - (+7.000) - genre match
     - (+2.910) - energy is similar to preference
     - (+1.860) - valence is similar to preference
     - (+0.712) - user prefers acousticness less
     - (+0.880) - user prefers danceability more
     - (+0.471) - tempo bpm is similar to preference

3. Rooftop Lights - Score: 11.11
   Artist: Indigo Parade
   Reasons:
     - (+5.000) - mood match
     - (+2.580) - energy is similar to preference
     - (+1.780) - valence is similar to preference
     - (+0.488) - user prefers acousticness less
     - (+0.820) - user prefers danceability more
     - (+0.443) - tempo bpm is similar to preference

4. Neon Pulse Rave - Score: 6.57
   Artist: DJ Fractal
   Reasons:
     - (+2.940) - energy is similar to preference
     - (+1.600) - valence is similar to preference
     - (+0.660) - user prefers acousticness less
     - (+0.910) - user prefers danceability more
     - (+0.457) - tempo bpm is similar to preference

5. Concrete Kingdom - Score: 6.54
   Artist: MC Ironside
   Reasons:
     - (+2.700) - energy is similar to preference
     - (+1.960) - valence is similar to preference
     - (+0.690) - user prefers acousticness less
     - (+0.850) - user prefers danceability more
     - (+0.339) - tempo bpm is similar to preference
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



