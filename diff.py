# Importing necessary package

import pyttsx3 as satyamjarvis
engine = satyamjarvis.init()

# say method on the engine that passing input text to be spoken
engine.say(' this is satyam assistant jarvis now called tuesday... i am personal assistant of satyam, solving day-to-day activities ')

# run and wait method, it processes the voice commands.
engine.runAndWait()
