import speech_recognition as sr
from time import ctime
import time
from sys import exit
import webbrowser
import playsound
import os
import calendar
import datetime
from gtts import gTTS
import random
import wikipedia
import subprocess as sp


r = sr.Recognizer()

def record_audio(ask=False):
    with sr.Microphone() as source:
        if ask:
            speak(ask)
        audio = r.listen(source)
        voice_data = ""
        try:
            voice_data = r.recognize_google(audio)
        except sr.UnknownValueError:
            speak("Sorry, I couldn't get it")
        except sr.RequestError:
            speak("Sorry my speech service is dowm")
        return voice_data

def speak(audio_string):
    tts = gTTS(text=audio_string, lang='en')
    r = random.randint(1, 10000000)
    audio_file = 'audio-' + str(r) +'.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(audio_string)
    os.remove(audio_file)
    
def respond(voice_data):
    if 'what is your name' in voice_data.lower():
        speak('My name is Mini, what is your name?')
        name = record_audio()
        current_hour = time.strptime(time.ctime(time.time())).tm_hour
        if current_hour < 12 :
            speak("Good Morning, Nice to meet you "+name)
        elif current_hour == 12:
            speak("Good Noon, Nice to meet you "+name)
        elif current_hour > 12 and current_hour < 18:
            speak("Good Afternoon, Nice to meet you "+name)
        elif current_hour >= 18 and current_hour <21:
            speak("Good Noon, Nice to meet you "+name)
        else:
            speak("Good Night, Nice to meet you "+name)
        # speak("Nice to meet you "+name)
    elif 'tell me the time' in voice_data.lower():
        now = datetime.datetime.now()
        my_date = datetime.datetime.today()
        weekday = calendar.day_name[my_date.weekday()]
        monthNum = now.month
        dayNum = now.day
        month_names = ["January", "Febraury", "March", "April", "May", "June", "July", "August", "September", "Otober", "November", "December"]
        days = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th',
                '11th', '12th', '13th', '14th', '15th', '16th', '17th', '18th', '19th', '20th',
                '21st', '22nd', '23rd', '24th', '25th', '26th', '27th', '28th', '29th', '30th','31st']
        say = "Today is "+days[dayNum-1]+" "+month_names[monthNum-1]+ " a " +weekday
        speak(say)
    elif 'search' in voice_data.lower():
        search = record_audio('What do you want to search?')
        url = 'https://google.com/search?q=' +search
        webbrowser.get().open(url)
        speak("Here is what I found for "+search)
    elif 'location' in voice_data.lower():
        location = record_audio('Which location do you want to find?')
        url = 'https://google.nl/maps/place/' + location + '/&amp;'
        webbrowser.get().open(url)
        speak("Here is the location of "+location)
    elif 'wikipedia' in voice_data.lower():
        look = record_audio("What do you want to look in wikipedia?")
        print("You replied: "+str(look))
        form = record_audio("Please mention the format,page,content,title,summary,references")
        print("You replied: "+str(form))
        if "page" in form.lower():
            speak("Searching Wikipedia")
            wik = wikipedia.page(look)
            speak("Showing the results")
            print(wik)
        elif "content" in form.lower():
            speak("Searching Wikipedia")
            wik = wikipedia.page(look).content
            speak("Showing the results")
            print(wik)
        elif "title" in form.lower():
            speak("Searching Wikipedia")
            wik = wikipedia.page(look).title
            speak("Showing the results")
            print(wik)
        elif "references" in form.lower():
            speak("Searching Wikipedia")
            wik = wikipedia.page(look).references
            speak("Showing the results")
            print(wik)
        elif "summary" in form.lower():
            speak("Searching Wikipedia")
            wik = wikipedia.summary(look, sentences=2)
            speak("Showing the results")
            print(wik)
        else:
            speak("I could not understand your requested command")
            pass
    elif 'bye' in voice_data:
        speak("Bye, have a good time")
        exit()
    elif 'youtube' in voice_data.lower():
        speak("Looking into YouTube")
        webbrowser.get().open("https://www.youtube.com/")
        ans = record_audio("Do you want me to search for you?")
        print("You replied: "+str(ans))
        if "yes" in ans.lower():
            ask = record_audio("What do you want to search?")
            url = "https://www.youtube.com/results?search_query=" +ask
            webbrowser.get().open(url)
            speak("See what I have got for "+ask)
        elif "no" in ans.lower():
            speak("Ok, Let's move on")
        elif "maybe" in ans.lower():
            speak("Check on, maybe, sometime later!")
        else:
            print("I could not understand your requested command")
            pass
    elif 'browser' in voice_data.lower():
        speak("Opening Google")
        webbrowser.get().open("https://www.google.com/")
        ans = record_audio("Do you want me to search for you?")
        print("You replied: "+str(ans))
        if "yes" in ans.lower():
            ask = record_audio("What do you want to search?")
            url = "https://google.com/search?q=" +ask
            webbrowser.get().open(url)
            speak("See what I have got for "+ask)
        elif "no" in ans.lower():
            speak("Ok, Let's move on")
        elif "maybe" in ans.lower():
            speak("Check on, maybe, sometime later!")
        else:
            print("I could not understand your requested command")
            pass
    elif 'linkedin' in voice_data.lower():
        speak("Opening LinkedIn")
        webbrowser.get().open("https://www.linkedin.com/")
    elif 'text document' in voice_data.lower():
        speak("Opening Notepad")
        prog_name = "Notepad.exe"
        sp.Popen(prog_name)
    elif 'take note' in voice_data.lower():
        speak("What would you like me to write down?")
        text = record_audio().lower()
        date = datetime.datetime.now()
        file_name = str(date).replace(":", "-") + "-note.txt"
        with open(file_name, "w") as f:
            f.write(text)
            f.write("\n\nNote taken by Mini..")
        speak("See, I have taken a note of this!")    
        sp.Popen(["notepad.exe", file_name])
        time.sleep(10)
    else:
        speak("No such service available!")
        pass

# time.sleep(1)
# print("How can I help you? To stop the service say 'bye'")
# while 1:
#     voice_data = record_audio()
#     if str(voice_data) == "":
#         print("Nothing")
#     else:
#         print("You said: "+str(voice_data))
#     respond(voice_data)
 
chance = int(input("Enter the no. of chances: "))
#chance = 10     
while chance != 0:
    print("\nHow can I help you? You have {} chances, to exit say 'bye'".format(chance))
    voice_data = record_audio()
    print("You said: "+str(voice_data))
    respond(voice_data)
    chance -= 1
if chance == 0:
    speak("\nYour turn is over, bye!")