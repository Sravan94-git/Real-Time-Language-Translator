import os
import pygame
from gtts import gTTS
import streamlit as st
import speech_recognition as sr
from googletrans import LANGUAGES, Translator

class LanguageTranslator:
    def __init__(self):
        self.translator = Translator()
        pygame.mixer.init()
        self.language_mapping = {name: code for code, name in LANGUAGES.items()}
        self.is_translate_on = False
        
    def get_language_code(self, language_name):
        return self.language_mapping.get(language_name, language_name)
    
    def translator_function(self, spoken_text, from_language, to_language):
        return self.translator.translate(spoken_text, src=from_language, dest=to_language)
    
    def text_to_voice(self, text_data, to_language):
        try:
            myobj = gTTS(text=text_data, lang=to_language, slow=False)
            myobj.save("cache_file.mp3")
            audio = pygame.mixer.Sound("cache_file.mp3")
            audio.play()
            pygame.time.wait(int(audio.get_length() * 1000))  # Wait for audio to finish
            os.remove("cache_file.mp3")
        except Exception as e:
            st.error(f"Text-to-Speech Error: {e}")
    
    def main_process(self, from_language, to_language):
        rec = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("Listening... Speak now.")
            rec.pause_threshold = 1
            audio = rec.listen(source, phrase_time_limit=10)
        
        try:
            st.info("Processing...")
            spoken_text = rec.recognize_google(audio, language=from_language)
            
            # Display the spoken text
            st.success(f"Input (Spoken): {spoken_text}")
            
            st.info("Translating...")
            translated_text = self.translator_function(spoken_text, from_language, to_language)
            
            # Display the translated text
            st.success(f"Output (Translated): {translated_text.text}")
            
            # Play the translated text as audio
            self.text_to_voice(translated_text.text, to_language)
        
        except sr.UnknownValueError:
            st.warning("Sorry, could not understand the audio.")
        except sr.RequestError:
            st.error("Could not request results from speech recognition service.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

def main():
    # Set page configuration
    st.set_page_config(
        page_title="Language Translator",
        page_icon="🌐",
        layout="wide"
    )
    
    # Title and description
    st.title("🌍 Real-Time Speech Translation App")
    st.markdown("""
    ### How to Use
    1. Select your source and target languages
    2. Click "Start Translation"
    3. Speak into your microphone
    4. See and hear the translation
    """)
    
    # Create translator instance
    translator = LanguageTranslator()
    
    # Sidebar for language selection
    st.sidebar.header("Translation Settings")
    
    # Language selection dropdowns
    from_language_name = st.sidebar.selectbox(
        "Source Language", 
        list(LANGUAGES.values()), 
        index=list(LANGUAGES.values()).index('english')
    )
    to_language_name = st.sidebar.selectbox(
        "Target Language", 
        list(LANGUAGES.values()), 
        index=list(LANGUAGES.values()).index('spanish')
    )
    
    # Convert language names to language codes
    from_language = translator.get_language_code(from_language_name)
    to_language = translator.get_language_code(to_language_name)
    
    # Translation control
    if st.sidebar.button("🎙️ Start Translation", type="primary"):
        # Disable other buttons during translation
        st.sidebar.warning("Translation in progress. Speak now!")
        
        try:
            # Perform translation
            translator.main_process(from_language, to_language)
        except Exception as e:
            st.error(f"Translation error: {e}")
    
    # Additional information
    st.sidebar.info(
        "Note: Ensure you have a working microphone. "
        "Internet connection is required for translation."
    )

if __name__ == "__main__":
    main()