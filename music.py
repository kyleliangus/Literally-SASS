from watson_developer_cloud import SpeechToTextV1, ToneAnalyzerV3
import json

from flask import Flask, request, redirect, g, render_template, url_for
import requests
import base64
import urllib

import os

# turn .wav file to text
def IBMAPI_Calls(f):
    
    stt = SpeechToTextV1(username="a3e9a6ce-11f9-43d5-9a0f-05cf198e3359", password="OeGWjpdyhATb")

    audio_file = open("test1.wav", "rb")

    x = json.dumps(stt.recognize(audio_file, content_type="audio/wav"), indent=2)
    parsed_json = json.loads(x)
    #print parsed_json
    p = parsed_json['results'][0]['alternatives'][0]
    confidence = p['confidence']
    transcript = p['transcript']
    print confidence
    print transcript

    #transcript = "I hate gross scary jubilant crying planners that are certain #that they are unsure of sharing caring popular agreements anger."


    tone_analyzer = ToneAnalyzerV3(
        username='18fe4961-f3ca-443c-981e-98cfa020e723',
        password='wA1ikph1pFiT',
        version='2016-05-19')
    tone_values = json.dumps(tone_analyzer.tone(text=transcript), indent=2)

    print tone_values

    parsed_tone_values = json.loads(tone_values)
    parsed = parsed_tone_values['document_tone']['tone_categories']
    emotion, language, social = parsed[0], parsed[1], parsed[2]
    anger, disgust, fear, joy, sadness = emotion['tones'][0]['score'], emotion['tones'][1]['score'], emotion['tones'][2]['score'], emotion['tones'][3]['score'], emotion['tones'][4]['score']
    analytical, confident, tentative = language['tones'][0]['score'], language['tones'][1]['score'], language['tones'][2]['score']
    openness, conscientiousness, extraversion, agreeableness, emotional_range = social['tones'][0]['score'], social['tones'][1]['score'], social['tones'][2]['score'], social['tones'][3]['score'], social['tones'][4]['score']

    print "Anger: " + str( anger )
    print "Disgust: " + str( disgust )
    print "Fear: " + str( fear )
    print "Joy: " + str( joy )
    print "Sadness: " + str( sadness )
    print "Analytical: " + str( analytical )
    print "Confident: " + str( confident )
    print "Tentative: " + str( tentative )
    print "Openness: " + str( openness )
    print "Conscientiousness: " + str( conscientiousness )
    print "Extraversion: " + str( extraversion )
    print "Agreeableness: " + str( agreeableness )
    print "Emotional Range: " + str( emotional_range )

    acousticness = max((openness + tentative - analytical) / 2, 0)
    danceability = (extraversion + joy + confident + openness) / 4
    energy = max((extraversion + joy + emotional_range - tentative )/3, 0)
    instrumentalness = (sadness + tentative) / 2
    liveness = (confident + disgust + extraversion) / 3
    loudness = (1 - (anger + fear) / 2) * (-1) * 60.0

    if((sadness + tentative + conscientiousness / 3) > (joy + confident) / 2):
        mode = 0;
    else:
        mode = 1;

    popularity = (extraversion + agreeableness) / 2
    speechiness = max((extraversion + openness - sadness) / 2, 0)
    #tempo = (anger + fear) / 2
    valence = max((joy + confident + extraversion - anger - sadness) / 3, 0)
	
    authorization_query = {'target_acousticness': acousticness, 'target_liveness': liveness, 'target_loudness': loudness, 'target_speechiness': speechiness, 'target_instrumentalness': instrumentalness, 'target_valence': valence, 'target_popularity': popularity, 'target_energy': energy, 'target_danceability': danceability, 'target_mode': mode }
    return
	

# call spotify API and start server

UPLOAD_FOLDER = '\uploads'
ALLOWED_EXTENSIONS = set(['m4a', 'wav', 'ogg', 'mp3'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Client Keys
CLIENT_ID = "70dc78caa32648ac80b0c4b28694a522"
CLIENT_SECRET = "0ca785fef2ca4031b1558cebb465bec4"

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

# Server-side Parameters
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 8081
REDIRECT_URI = "{}:{}/callback/q".format(CLIENT_SIDE_URL, PORT)
SCOPE = "playlist-modify-public playlist-modify-private"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

authorization_query = {'target_acousticness': 0.5, 'target_liveness': 0.5, 'target_loudness': -30, 'target_speechiness': 0.5, 'target_instrumentalness': 0.5, 'target_valence': 0.5, 'target_popularity': 50, 'target_energy': 0.5, 'target_danceability': 0.5, 'target_mode': 1 }

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    # "state": STATE,
    # "show_dialog": SHOW_DIALOG_str,
    "client_id": CLIENT_ID
}

@app.route("/")
def index():
    # Auth Step 1: Authorization
    url_args = "&".join(["{}={}".format(key,urllib.quote(val)) for key,val in auth_query_parameters.iteritems()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    #print auth_url
    return redirect(auth_url)

	
@app.route("/start", methods=['POST'])
def receive():
    print "I heard something"
    error = None
    f = request.files['speech']
    if( f ):
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        x = filename.split(".")
        os.system(".\ffmpeg.exe -i " + filename + " " + x + ".wav"  )
		
        IBMAPI_Calls( f )
        index()
    else:
        error = 'No audio file detected'
        return render_template('index.html', error=error)
	
    
@app.route("/callback/q")
def callback():
    # Auth Step 4: Requests refresh and access tokens
    # authorization_query = request.args.get('speech')
	
    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI
    }
    base64encoded = base64.b64encode("{}:{}".format(CLIENT_ID, CLIENT_SECRET))
    headers = {"Authorization": "Basic {}".format(base64encoded)}
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)

    # Auth Step 5: Tokens are Returned to Application
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]
    token_type = response_data["token_type"]
    expires_in = response_data["expires_in"]

    # Auth Step 6: Use the access token to access Spotify API
    authorization_header = {"Authorization":"Bearer {}".format(access_token)}
	
    genres = {'rap': 0, 'rock': 0, 'pop': 0, 'kpop': 0, 'r&b': 0, 'country': 0, 'latin': 0, 'dance': 0, 'classical': 0, 'jazz': 0}
	# pick a subset on 4 criteria
	
    popularity = authorization_query['target_popularity']
    # Based off of Popularity:
    genres['r&b'] += popularity / 100 *       .75
    genres['rock'] += popularity / 100 *      .75
    genres['rap'] += popularity / 100 *       .75
    genres['pop'] += popularity / 100 *       .75
    genres['country'] += popularity / 100 *   .75
    genres['latin'] += popularity / 100 *     .25
    genres['dance'] += popularity / 100 *     .25
    genres['kpop'] += popularity / 100 *      .25
    genres['classical'] += popularity / 100 * .25
    genres['jazz'] += popularity / 100 *      .25

    speechiness = authorization_query['target_speechiness']
    # Based off of Speechiness:
    genres['rap'] += speechiness *       .75
    genres['rock'] += speechiness *      .75
    genres['pop'] += speechiness *       .75
    genres['kpop'] += speechiness *      .75
    genres['country'] += speechiness *   .75
    genres['latin'] += speechiness *     .25
    genres['dance'] += speechiness *     .25
    genres['r&b'] += speechiness *       .25
    genres['classical'] += speechiness * .25
    genres['jazz'] += speechiness *      .25

    energy = authorization_query['target_energy']
    # Based off of Energy:
    genres['pop'] += energy *       .75
    genres['latin'] += energy *     .75
    genres['kpop'] += energy *      .75
    genres['dance'] += energy *     .75
    genres['rap'] += energy *       .75
    genres['rock'] += energy *      .25
    genres['classical'] += energy * .25
    genres['r&b'] += energy *       .25
    genres['country'] += energy *   .25
    genres['jazz'] += energy *      .25

    acousticness = authorization_query['target_acousticness']
    # Based off of Acoustic:
    genres['pop'] += acousticness *       .25
    genres['latin'] += acousticness *     .25
    genres['kpop'] += acousticness *      .25
    genres['dance'] += acousticness *     .25
    genres['rap'] += acousticness *       .25
    genres['rock'] += acousticness *      .75
    genres['classical'] += acousticness * .75
    genres['r&b'] += acousticness *       .75
    genres['country'] += acousticness *   .75
    genres['jazz'] += acousticness *      .75

    seed_genres = sorted(genres, key = genres.__getitem__)[:-4:-1]
    
    query = authorization_query.copy()
    query['seed_genres'] = seed_genres
    query['limit'] = 1;
    print query
	
    recommendations_endpoint = "{}/recommendations".format(SPOTIFY_API_URL)
    recommendations_response = requests.get(recommendations_endpoint, params=query, headers=authorization_header)
    recommendations_data = json.loads(recommendations_response.text)
    print recommendations_data
	
    
    # Combine profile and playlist data to display
    display_arr = recommendations_data
    return render_template("index.html",sorted_array=display_arr)

if __name__ == "__main__":
    app.run(debug=True,port=PORT)

