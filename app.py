from flask import Flask, render_template,redirect,url_for
import pyttsx3
import speech_recognition as sr
import webbrowser 
import datetime 
import wikipedia


app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')
silence_count=0
def takeCommand():
    global silence_count
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening')
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            print("Recognizing")
            Query = r.recognize_google(audio, language='en-in')
            print("the command is", Query) 
            silence_count=0   
        except Exception as e:
            if silence_count == 2:
                speak("looks like you want me to shut down ok signing off")
                return "close"
            else:
                print(e)
                speak("Say that again sir")
                silence_count+=1
                return "None"
        return Query
def speak(audio):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 150)
    engine.say(audio) 
    engine.runAndWait()
def tellDay():
    day = datetime.datetime.today().weekday() + 1
    Day_dict = {1: 'Monday', 2: 'Tuesday',
                3: 'Wednesday', 4: 'Thursday',
                5: 'Friday', 6: 'Saturday',
                7: 'Sunday'}
    if day in Day_dict.keys():
        day_of_the_week = Day_dict[day]
        print(day_of_the_week)
        speak("Today is " + day_of_the_week)
def tellTime():
    time = str(datetime.datetime.now())
    print(time)
    hour = time[11:13]
    min = time[14:16]
    speak( "The time is sir" + hour + "Hours and" + min + "Minutes")   
def Hello():
    speak("hello sir I am  cookie dharanishwar's virtual assistant , i will help you to know about him")
def Take_query():
    Hello()
    while(True):
        query = takeCommand().lower()
        if "about dharan ishwar" in query:
            speak("""Dharanishwar was born on 5th of march 2003 .He is an undergraduate student pursuing his Bachelor of Technology in Computer Science Engineering with Artificial Intelligence and Machine Learning from Vardhaman college of engineering.
                    He is a self-starter with strong interpersonal skills and confidence.He works efficiently both as an individual contributor as well as along with a team.
                    He is a good learner, innovative, has a very positive attitude and committment to his work.
                    """)     
        elif "open google" in query:
            speak("Opening Google ")
            webbrowser.open("www.google.com")         
        elif "which day it is" in query:
            tellDay()    
        elif "tell me the time" in query:
            tellTime()
        elif "see you" in query:
            speak("had enough fun see you after")
            return True     
        elif "from wikipedia" in query:
            speak("Checking the wikipedia ")
            query = query.replace("wikipedia", "")
            result = wikipedia.summary(query, sentences=4)
            speak("According to wikipedia")
            speak(result)
        elif "tell me your name" in query:
            speak("I am Cookie. Dharanishwar's personal assistant ")
        elif "who are you" in query:
            speak("I am Cookie. Dharanishwar's personal assistant ")
        elif "what are you" in query:
            speak("I am Cookie. Dharanishwar's personal assistant ")
        elif "how to stop you" in query:
            speak("say see you")
        elif "none" in query:
            speak("")
        elif "close" in query:
            return True
        else:
            speak("sorry! I am not familiar with that, please try another.")


@app.route('/take_command')
def take_command():
    redirect_flag = Take_query()
    if redirect_flag:
        return redirect(url_for('home'))
if __name__ == '__main__':
    app.run(debug=True)
