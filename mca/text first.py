import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton
import openai
import pyttsx3
import speech_recognition as sr
from PyQt5.QtGui import QFont

# Set up OpenAI API key
openai.api_key = "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"

# Initialize pyttsx3
engine = pyttsx3.init()

# Create the main window
class ChatbotWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JIMIN YOUR PERSONAL ASSISTANT")
        self.setGeometry(100, 100, 500, 400)

        # Create a central widget and set the layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Create a text box for displaying the conversation
        self.conversation_text = QTextEdit(self)
        self.conversation_text.setFont(QFont("Times New Roman", 12))  # Set font size and style
        self.layout.addWidget(self.conversation_text)

        # Create a line edit for user input
        self.input_line = QLineEdit(self)
        self.layout.addWidget(self.input_line)

        # Create a button for submitting user input
        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.handle_user_input)
        self.layout.addWidget(self.submit_button)

        # Create a button for voice input
        self.voice_button = QPushButton("Voice Input", self)
        self.voice_button.clicked.connect(self.handle_voice_input)
        self.layout.addWidget(self.voice_button)

        # Initialize the conversation
        self.messages = [
            {"role": "system", "content": "Hi JIMIN, You are a helpful assistant!"}
        ]

        # Disable the voice input button initially
        self.voice_button.setEnabled(False)

    # Function to handle user input
    def handle_user_input(self):
        user_input = self.input_line.text()

        # Process user input and generate response
        if user_input:
            self.conversation_text.append("User: " + user_input)

            self.messages.append({"role": "user", "content": user_input})
            chat_completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=self.messages
            )
            reply = chat_completion["choices"][0]["message"]["content"]

            # Display the assistant's reply text
            self.conversation_text.append("Chatbot: " + reply)
            
            QApplication.processEvents()  # Ensure that the reply text is displayed immediately

            # Convert assistant's reply to speech
            engine.say(reply)
            engine.runAndWait()

            self.input_line.clear()

            # Enable the voice input button
            self.voice_button.setEnabled(True)

    # Function to handle voice input
    def handle_voice_input(self):
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            self.conversation_text.append("Listening...")

            audio = recognizer.listen(source)

        try:
            user_input = recognizer.recognize_google(audio)
            self.conversation_text.append("User (Voice): " + user_input)

            # Display the voice input in the text box
            self.input_line.setText(user_input)

            self.handle_user_input()

        except sr.UnknownValueError:
            self.conversation_text.append("Chatbot: Sorry, I couldn't understand that.")
        except sr.UnknownValueError:
                self.conversation_text.append(
                    "Chatbot: Sorry, there was an issue with the speech recognition service: " + str(e)
                )

# Create the application and the window
app = QApplication(sys.argv)
window = ChatbotWindow()

window.show()

# Start the application event loop
sys.exit(app.exec_())

