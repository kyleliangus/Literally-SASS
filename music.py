from watson_developer_cloud import SpeechToTextV1, ToneAnalyzerV3
import json
import re

# turn .wav file to text

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

'''
transcript = "I hate gross scary jubilant crying planners that are certain that they are unsure of sharing caring popular agreements anger."
'''
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


'''
print "Emotion: "
print emotion
print "Language: " 
print language
print "Social: " 
print social
'''

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

accoustic = max((openness + tentative - analytical) / 2, 0)
danceability = (extraversion + joy + confident + openness) / 4
energy = max((extraversion + joy + emotional_range - tentative )/3, 0)
instrumentalness = (sadness + tentative) / 2
liveness = (confident + disgust + extraversion) / 3
loudness = (anger + fear) / 2

if((sadness + tentative + conscientiousness / 3) > (joy + confident) / 2):
	mode = 0;
else:
	mode = 1;

popularity = (extraversion + agreeableness) / 2
speechiness = max((extraversion + openness - sadness) / 2, 0)
tempo = (anger + fear) / 2
valence = max((joy + confident + extraversion - anger - sadness) / 3, 0)

# call spotify API

