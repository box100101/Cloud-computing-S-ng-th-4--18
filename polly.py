import boto3
import os

import tkinter as tk
from tkinter import *
from tkinter import ttk
from playsound import playsound 
import random
import string

#gọi session của user
aws = boto3.session.Session(profile_name="tuong")
#lấy service(polly)
polly = aws.client(service_name='polly', region_name="ap-southeast-1")


root = tk.Tk()  #root: phần giao diện
root.geometry("930x500")
root.title("Typing your text!!!")
mylabel = tk.Label(root, text="Input your text here:", font=("Arial", 15))
mylabel.pack()
def checkLang(choosen):
    langCode=""
    voiceId=""
    langCodeS=""
    text =choosen.get()
    print(text)
    if(text =="English"):
        langCode = "en-GB"
        langCodeS="en"
        voiceId  ="Brian"
    elif(text =="Japanese"):
        langCode = "ja-JP"
        langCodeS = "ja"
        voiceId  ="Takumi"
    elif(text =="Korean"):
        langCode = "ko-KR"
        langCodeS = "ko"
        voiceId  ="Seoyeon"
    elif(text =="Spanish"):
        langCode = "es-US"
        langCodeS = "es"
        voiceId  ="Miguel"
    elif(text =="Turkish"):
        langCode = "tr-TR"
        langCodeS = "tr"
        voiceId  ="Filiz"
    elif(text =="French"):
        langCode = "fr-FR"
        langCodeS = "fr"
        voiceId  ="Léa"
    elif(text =="Dutch"):
        langCode = "nl-NL"
        langCodeS = "nl"
        voiceId  ="Lotte"
    return langCode,langCodeS,voiceId
        
def playSrc():
    langCode,temp,voiceId = checkLang(choosen)
    text = textInput.get("1.0", "end")
    response = polly.synthesize_speech( LanguageCode=langCode , Text=text, VoiceId=voiceId, OutputFormat='mp3')
    body = response['AudioStream'].read()
    letters = string.ascii_lowercase
    file_name= ( ''.join(random.choice(letters) for i in range(10))+".mp3" )
    with open(file_name ,'wb') as file:
        file.write(body)
        file.close()
    playsound(file_name)
    os.remove(file_name)
        
def playTar():
    langCode,temp,voiceId = checkLang(choosenTar)
    text = textOutput.get("1.0", "end")
    response = polly.synthesize_speech( LanguageCode=langCode , Text=text, VoiceId=voiceId, OutputFormat='mp3')
    body = response['AudioStream'].read()
    letters = string.ascii_lowercase
    file_name= ( ''.join(random.choice(letters) for i in range(10))+".mp3" )
    with open(file_name ,'wb') as file:
        file.write(body)
        file.close()
    playsound(file_name)
    os.remove(file_name)
   

def translateFunc():
    translate = aws.client(service_name='translate', region_name="ap-southeast-1")
    textOutput.delete("1.0","end")
    text = textInput.get("1.0", "end")
    temp,codeSrc,temp1=checkLang(choosen)
    temp2,codeTar,temp3=checkLang(choosenTar)
    result = translate.translate_text(Text=text,
                                  SourceLanguageCode=codeSrc,
                                  TargetLanguageCode=codeTar)
    textOutput.insert(tk.END,result["TranslatedText"])


#drop down box cho source
n = tk.StringVar()
choosen = ttk.Combobox(root, width = 27, textvariable = n)
  
# Drop down box
choosen['values'] = ('English', 
                     'Japanese',
                     'Korean',
                     'Spanish',
                     'Turkish',
                     'French',
                     'Dutch',)
choosen.current(0)
choosen.pack()

textInput = tk.Text(root, height=10,)
textInput.pack()

btnSrc = tk.Button(root, height=1, width=10, text="Read it!", command=playSrc)
btnSrc.pack()


# Drop down box cho target
n1 = tk.StringVar()
choosenTar = ttk.Combobox(root, width = 27, textvariable = n1)
choosenTar['values'] = ('English', 
                     'Japanese',
                     'Korean',
                     'Spanish',
                     'Turkish',
                     'French',
                     'Dutch',)
choosenTar.current(0)
choosenTar.pack()

btnRead = tk.Button(root, height=1, width=10, text="Translate", command=translateFunc)
btnRead.pack()

textOutput = tk.Text(root, height=10,)
textOutput.pack()

btnTar = tk.Button(root, height=1, width=10, text="Read it!", command=playTar)
btnTar.pack()


root.mainloop()