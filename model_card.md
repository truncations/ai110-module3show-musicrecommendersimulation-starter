# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

**MusicFitRecommender 1.0**

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

Some limitations of my systems that create bias are that genres and moods must be exactly matching, even though some genres and moods can be similar but not exact to the user's preference. (TLDR; hybrid genres are highly penalized) Mood is heavily fragmented as most of the dataset have their own unique moods, and so it leads to genre+mood being relied on rather than actual music taste. Additionally, for the acousticness/danceability attributes of a song, they are strictly based on whether a user likes acousticness or likes danceability, where if they do "like" acousticness/danceability that higher values reward more, and vice versa rather than actually finding the target acousticness/danceability value that someone would prefer which creates bias; for example, some users may like acousticness but not heavy acoustic.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

I checked whether the recommender behaved as expected by testing user profiles. As shown in main.py, I tested for user profiles such as "lofi-chill", "classical-melancholic", and "rock-intense". For each profile and their recommended songs, I analyzed the top 5 recommended song's attributes and manually determined similarities based on knowledge of music as well as numbers given (from data/songs.csv)--I took the recommended song's name, found it in the dataset and observed comparisons and differences from the user's profile. For example, on "lofi-chill", I made sure that the top songs were also similar by having the same genre or mood. What surprised me the most was when I tested "rock-intense" profile where it seemingly preferred the music "Gym Hero" over "Iron Descent" even though "Iron Descent" is clearly more similar (Metal-aggressive) than "Gym Hero" (pop-intense). This bias occurred since we only do exact-matching moods/genres. Additionally, another surprise was that my scoring system focused on label matching rather than genuine musical similarity, which made it hard to observe other behavior. However, one I noticed was that "rock-intense" profile preferred songs with lower acousticness-danceability and higher energy, while "lofi-chill" focused on lower energy with higher acousticness.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
