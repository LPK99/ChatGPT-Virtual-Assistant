import openai
import speech_recognition as sr
import pyttsx3
import time 


openai.api_key = "openai_api_key_here"
engine=pyttsx3.init()


def transcribe_audio_to_text(filename):
    recognizer=sr.Recognizer()
    with sr.AudioFile(filename)as source:
        audio=recognizer.record(source) 
    try:
        return recognizer.recognize_google(audio)
    except:
        print("skipping unkown error")

def generate_response(prompt):
    response= openai.completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response ["Choices"][0]["text"]
def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def main():
    while True:
        print("Say 'GPT' to start recording your question")
        with sr.Microphone() as source:
            recognizer=sr.Recognizer()
            audio=recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                if transcription.lower()=="gpt":
                    filename ="input.wav"
                    print("Start your question")
                    with sr.Microphone() as source:
                        recognizer=sr.recognize()
                        source.pause_threshold=1
                        audio=recognizer.listen(source,phrase_time_limit=None,timeout=None)
                        with open(filename,"wb")as f:
                            f.write(audio.get_wav_data())
                    text=transcribe_audio_to_text(filename)
                    if text:
                        print(f"you said {text}")
                        
                        response = generate_response(text)
                        print(f"chat gpt 3 say {response}")
                        
                        speak_text(response)
            except Exception as e:
                
                print("An error ocurred : {}".format(e))
if __name__=="__main__":
    main()