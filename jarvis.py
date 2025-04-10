import pyttsx3 
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import os.path
import pyjokes
import sys
import smtplib
import cv2
import random
import pywhatkit as kit
import pyautogui
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import requests
from requests import get
import time
import instadownloader
import PyPDF2
import operator
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTime, QDate, QTimer,Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from jarvisui import Ui_JarisUI 

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")
    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   
    else:
        speak("Good Evening!")  
    speak("I am Jarvis Sir. Please tell me, how may i help you ? ")       

def news():
    main_url='http://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=83263a48521a48a797182dbc3926e513'
    main_page= requests.get(main_url).json()
    articles = main_page["articles"]
    head=[]
    day=["first","second","third"]#,"fourth","fifth","sixth","seventh","eighth","ninth","tenth"]
    for article in articles:
        head.append(article["title"])
    for i in range(len(day)) :
        speak(f"today's {day[i]} news is : {head[i]}")
        print(f"today's {day[i]} news is : {head[i]}")

def pdf_reader(name):
    try:
        book = open(f'{name}.pdf','rb')
        pdfReader=PyPDF2.PdfReader(book)
        num_pages = len(pdfReader.pages)
        speak(f"Total pages in this book {name} are {num_pages}")
        print(f"Number of pages: {num_pages}")
        speak("sir please enter the page number you want to read")
        pg=int(input("Enter the page number: "))
        page = pdfReader.pages[pg-1]
        text = page.extract_text()
        speak(text)
        print(text)
    except FileNotFoundError:
        speak("Sorry, the file does not exist.")
        print("Sorry, the file does not exist.")

class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()
    
    def run(self):
        self.TaskExecution()
        
    def takeCommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source,timeout=5,phrase_time_limit=10)

        try:
            print("Recognizing...")    
            self.query = r.recognize_google(audio, language='en-in')
            print(f"User said: {self.query}\n")

        except Exception as e:   
            speak("Can you say that again please...")
            print("Can you say that again please...")  
            return "None"
        return self.query
    
    def TaskExecution(self):
        wishMe()
        while True:
            self.query = self.takeCommand().lower()
            if 'wikipedia' in self.query:
                speak('Searching Wikipedia...')
                self.query = self.query.replace("wikipedia", "")
                results = wikipedia.summary(self.query, sentences=2)
                speak("According to Wikipedia")
                speak(results)
                print(results)

            elif 'open command prompt' in self.query:
                os.system('start cmd')

            elif 'open youtube' in self.query:
                speak("Should i search on youtube on your behalf ?")
                ans1=self.takeCommand().lower()
                if'yes'in ans1:
                    speak("What should i search on youtube ?")
                    search1=self.takeCommand().lower()
                    kit.playonyt(search1)
                else:
                    webbrowser.open("youtube.com")

            elif 'open google' in self.query:
                speak("Sir, what would you like to search on google ?")
                cm = self.takeCommand().lower()
                webbrowser.open(f"{cm}")

            elif 'open stackoverflow' in self.query:
                webbrowser.open("stackoverflow.com")   

            elif 'play music' in self.query:
                music_dir = "C:\\Users\\DARSHAN\\Downloads\\krishna.mp3"  
                os.startfile(music_dir)

            elif 'open camera' in self.query:
                cap=cv2.VideoCapture(0)
                while True:
                    ret, img = cap.read()
                    cv2.imshow('webcam',img)
                    k = cv2.waitKey(50)
                    if k == 27:
                        break
                cap.release()
                cv2.destroyAllWindows()

            elif "the time" in self.query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")    
                speak(f"Sir, the time is {strTime}")
                print(f"Sir, the time is {strTime}")    

            elif 'open python' in self.query:
                codePath = "C:\\Users\\darshan\\AppData\\Local\\Programs"
                os.startfile(codePath)

            elif 'open a book' in self.query or 'open a pdf' in self.query:
                speak("Sure, do you also want me to read it for you ?")
                ans2=self.takeCommand().lower()
                if 'yes' in ans2:
                    speak("please enter the name of the file you want to read")
                    book_name=input("Enter file name here: ")
                    pdf_reader(book_name)
                else:
                    speak("please enter the name of the file you want to open")
                    book_name=input("Enter file name here: ")
                    bookpath = f"C:\\Users\\DARSHAN\\OneDrive - somaiya.edu\\Desktop\\bks\\{book_name}.pdf"
                    os.startfile(bookpath)
                    
            elif 'read a pdf' in self.query or 'read a book' in self.query:
                speak("Sir, please enter the name of the file you want me to read")
                name = input("Enter the name here: ")
                pdf_reader(name)

            elif 'whatsapp message' in self.query:
                speak("To whom should i send the message ?")
                contact= self.takeCommand().lower()
                if 'me' in contact:
                    number = "9313574729"
                    speak("What should i say ?")
                    message = self.takeCommand().lower()
                    h1=int(datetime.datetime.now().hour)
                    m1=int(datetime.datetime.now().minute) + 4
                    kit.sendwhatmsg("+91"+number, message, h1,m1)
                else:
                    number = "9313574729"
                    speak("What should i say ?")
                    message = self.takeCommand().lower()
                    h1=int(datetime.datetime.now().hour)
                    m1=int(datetime.datetime.now().minute) + 3
                    kit.sendwhatmsg("+91"+number, message, h1,m1)

            elif 'close yourself' in self.query or 'no thanks' in self.query:
                speak("Goodbye sir, have a nice day!")
                exit()

            elif 'send a mail' in self.query:
                email='jarvismypy@gmail.com'
                password='devsassistant'
                speak("Sir, please enter the recipient's email address")
                sendee_mail=input("Please enter the recipient's email address here: ")
                speak("should i attach a file to your mail ?")
                self.query=self.takeCommand().lower()
                if'yes' in self.query:
                    speak("Sir, what will be the subject of email ?")
                    self.query=self.takeCommand().lower()
                    subject=self.query
                    speak("Sir, what should i write in the email ?")
                    body=self.takeCommand().lower()
                    speak("Sir, please provide the file path")
                    file_path=input("Please provide the file path here: ")
                    speak("please wait sending the email")
                    msg = MIMEMultipart()
                    msg['From'] = email
                    msg['To'] = sendee_mail
                    msg['Subject'] = subject
                    msg.attach(MIMEText(body, 'plain'))
                    filename=os.path.basename(file_path)
                    attachment = open(file_path, "rb")
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', "attachment; filename= "+filename)
                    msg.attach(part)
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.ehlo()
                    server.starttls()
                    server.login(email, password)
                    text = msg.as_string()
                    server.sendmail(email, sendee_mail, text)
                    server.quit()
                    speak("Email has been sent!")   
                else:
                    message=self.query
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.ehlo()
                    server.starttls()
                    server.login(email, password)
                    server.sendmail(email,sendee_mail, message)
                    server.quit()
                    speak("Email has been sent!")  

            elif 'switch window' in self.query:
                pyautogui.keyDown("alt")
                pyautogui.press("tab")
                time.sleep(1)
                pyautogui.keyUp("alt")

            elif 'news'in self.query:
                speak("please wait Sir, The news is being fetched")
                news()

            elif 'where am i' in self.query or 'where are we' in self.query:
                speak('please wait sir let me check')
                try:
                    ipAdd = requests.get('https://api.ipify.org').text
                    print(ipAdd)
                    url = 'https://get.geojs.io/v1/ip/geo/'+ipAdd+'.json'
                    geo_req = requests.get(url)
                    geo_data = geo_req.json()
                    region = geo_data['city']
                    country = geo_data['country']
                    speak(f"Sir we are in {region} city of {country} country")
                    print(f"Sir we are in {region} city of {country} country")
                except Exception as e:
                    speak("Sorry sir, due to network issue i cannot find where we are.")

            elif 'instagram profile' in self.query or 'profile on insta' in self.query:
                speak("Sir, what is the name of the profile ?")
                name = input("Enter the username: ")
                webbrowser.open(f"https://www.instagram.com/{name}/")
                speak(f"sir here is the profile of {name}")
                time.sleep(5)
                speak("would you like to download the profile picture ?")
                res = self.takeCommand().lower()
                if 'yes' in res:
                    mod=instadownloader.InstaDownloader()
                    mod.download_profile(name, profile_pic_only=True)
                    speak(f"Sir, the profile picture of {name} has been downloaded successfully and saved in {os.getcwd()} folder.")

            elif 'take a screenshot' in self.query:
                speak("Sir, please tell me the name for this screenshot file ?")
                name = self.takeCommand().lower()
                speak(f"Taking screenshot in 5 seconds")
                time.sleep(5)
                img = pyautogui.screenshot()
                img.save(f"{name}.png")
                speak(f"Sir, the screenshot is saved in {os.getcwd()} folder.")
            elif 'do nothing' in self.query:
                speak("Ok sir")
                time.sleep(10)
            else:
                print("No self.query matched")
            speak("Sir do you have any other task for me ?")

startexecution =MainThread()
        
class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_JarisUI()
        self.ui.setupUi(self)
        self.ui.RUN.clicked.connect(self.startTask)
        self.ui.pushButton.clicked.connect(self.close)

    def startTask(self):
        self.ui.movie = QtGui.QMovie("../../../../Downloads/Jarvis pic/image_processing20210911-30861-12ai18g.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer=QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startexecution.start()
        
    def showTime(self):
        current_time = QTime.currentTime()
        current_date=QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)

app = QApplication(sys.argv)
jarvis = Main()
jarvis.show()
exit(app.exec_())