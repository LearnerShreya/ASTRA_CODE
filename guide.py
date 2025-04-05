import pyttsx3
import speech_recognition as sr
import google.generativeai as genai
from dotenv import load_dotenv
import os
import random

# Set up TTS (Text-to-Speech) with male voice
engine = pyttsx3.init()
engine.setProperty("rate", 160)
voices = engine.getProperty("voices")
for voice in voices:
    if "male" in voice.name.lower():
        engine.setProperty("voice", voice.id)
        break
else:
    engine.setProperty("voice", voices[0].id)  # fallback to first voice if no "male" found

# Load environment variables
load_dotenv()

# Gemini API setup
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Use .env instead of hardcoding key
genai.configure(api_key=GEMINI_API_KEY)

# Gemini model instance
model = genai.GenerativeModel("gemini-1.5-flash")

# Domain-specific context for Kedarnath
KEDARNATH_CONTEXT = """
You are a knowledgeable and polite Kedarnath travel guide. Only answer questions related to:
- Travel routes and transportation options
- Stay and accommodation details
- Helicopter bookings and trekking info
- Weather updates and safety precautions
- Local food, culture, and traditional festivals
- Mythology, religious significance, temples, and history
- Nearby attractions (like Bhairavnath Temple, Vasuki Tal, Triyuginarayan)
- Best time to visit and temple opening/closing schedule
- Packing suggestions and altitude health tips (e.g., AMS)
- Mobile network availability and connectivity info
- Mandatory registration procedures
- Environment-friendly travel and do’s & don’ts
- Emergency contact info and government advisories

Do not answer anything unrelated to Kedarnath or religious travel. Keep your responses short, helpful, and traveler-friendly.
"""

# Listening prompts
listening_responses = ["Go ahead!", "I'm ready.", "Yes?", "Listening...", "Tell me!"]

# Speak function
def speak(text):
    print("ASTRA:", text)
    engine.say(text)
    engine.runAndWait()

# Get user voice input
def get_voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            speak(random.choice(listening_responses))
            r.adjust_for_ambient_noise(source, duration=1)
            print("🎧 Listening...")
            audio = r.listen(source, timeout=10)
            text = r.recognize_google(audio)
            print("🗣️ You:", text)
            return text.lower()
        except sr.WaitTimeoutError:
            speak("I didn't hear anything.")
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand your words.")
        except sr.RequestError:
            speak("Sorry, my speech service is down.")
        return None

# Get Gemini-generated response
def get_kedarnath_reply(question):
    prompt = KEDARNATH_CONTEXT + f"\n\nUser: {question}\nGuide:"
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return "I'm facing trouble connecting to the internet or processing your question."

# Main loop
def main():
    speak("Namaste! I am ASTRA, your online Kedarnath guide.")
    stop_words = {"stop", "exit", "bye", "quit"}

    while True:
        user_input = get_voice_input()
        if user_input:
            if any(word in user_input for word in stop_words):
                speak("Goodbye! Har Har Mahadev!")
                break
            answer = get_kedarnath_reply(user_input)
            speak(answer)

# Entry point
if __name__ == "__main__":
    main()
