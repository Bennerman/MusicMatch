import pandas

# This class is just a note file for now... it manually matches results of FindHoroscope.py

# For more detailed stuff on this data:
# https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/
# https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4971092/

#https://developer.spotify.com/documentation/web-api/reference/library/get-users-saved-tracks/




# Here are the parameters we might use for selecting songs
# duration_ms (int in milliseconds) - I don't think we should have songs over 4-5 minutes for a playlist 
# mode (int, major = 1, minor = 0) - Some moods may be clearly major/minor 
# time_signature (int) - could experiment with dancy 3/4, 6/8 type stuff 
# acousticness (float, 0.0-1.0) - not so sure about this one... maybe
# danceability (float, 0.0-1.0) - combination of tempo, rhythm stability (positive correlation), beat strength
# energy (float, 0.0-1.0) - fast, loud, noisy
# valence (float, 0.0-1.0) - positivity of the track
# tempo (float, BPM) - mostly in range of 70-160 bpm 

# global: duration_ms < 300,000

# energy, danceability, acousticness, valence

'''
Depressed - Funeral - Phoebe Bridgers Bubble Gum - Clairo
energy: 0.15
danceability: 0.5
acousticness: 0.85
valence: 0.2

Prideful -- Suge - Dababy, Clique - Kanye, Money Machine
energy: 0.65
danceability: 0.7
acousticness: 0.2
valence: 0.75


'''


pd = 

