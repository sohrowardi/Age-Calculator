import speech_recognition as sr
import pyttsx3
from datetime import date
from dateutil import parser
import time

# Initialize speech recognition and text-to-speech engines
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Set the voice. You can change the voice based on the available voices on your system.
# Use the voices[0].id for the default voice, or experiment with other indices.
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Change the index as needed

def get_audio(prompt):
    with sr.Microphone() as source:
        print(prompt)
        engine.say(prompt)
        engine.runAndWait()
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            print("You said:", text)
            return text
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand your speech.")
        except sr.RequestError as e:
            print("An error occurred while accessing Google Speech Recognition:", str(e))

def calculate_age(birth_date):
    today = date.today()
    age = today - birth_date
    return age

while True:
    # Get the date of birth from the user through speech
    birth_date_str = get_audio("Please say your date of birth...")

    # Parse the birth date
    try:
        parsed_date = parser.parse(birth_date_str, fuzzy=True)
        birth_date = date(parsed_date.year, parsed_date.month, parsed_date.day)

        # Calculate the age
        age = calculate_age(birth_date)

        # Speak and print the age breakdown
        response = f"You were born on {birth_date:%B %d, %Y}. Your age is {age.days // 365} years, {age.days % 365 // 30} months, and {age.days % 30} days."
        print(response)
        engine.say(response)
        engine.runAndWait()

    except ValueError:
        print("Sorry, I couldn't determine your birth date from the speech input.")

    # Ask the user if they want to calculate again
    response = get_audio("Do you want to calculate age again? Say yes or no.")
    if response.lower() != "yes":
        break

# Exit the program
exit()
