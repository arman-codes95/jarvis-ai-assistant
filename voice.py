import speech_recognition as sr
import asyncio
import edge_tts
import tempfile
import os
import pygame
import threading
import requests
import random

VOICE = "en-GB-RyanNeural"

pygame.mixer.init()

speech_thread = None
stop_signal = False

def add_respect(text):
    if not text.lower().endswith(("sir.", "sir")):
        return text + ", Sir."
    return text
# ---------------------------
# SEND STATE TO FLASK SERVER
# ---------------------------
def update_state(state, energy=0):
    try:
        requests.post(
            "http://127.0.0.1:5000/update_state",
            json={"state": state, "energy": energy},
            timeout=0.3
        )
    except:
        pass# Do not crash if Flask is not reachable


# ---------------------------
# ASYNC TTS GENERATION
# ---------------------------
async def generate_speech(text, path):
    communicate = edge_tts.Communicate(text, VOICE, rate="+15%")
    await communicate.save(path)


# ---------------------------
# AUDIO PLAYBACK THREAD
# ---------------------------
def _play_audio(temp_path):
    global stop_signal

    try:
        pygame.mixer.music.load(temp_path)
        pygame.mixer.music.play()

        # 🔥 Start in speaking mode
        current_energy = 60

        while pygame.mixer.music.get_busy():
            if stop_signal:
                pygame.mixer.music.stop()
                break

            # Smooth cinematic energy variation
            variation = random.randint(-15, 15)
            current_energy = max(30, min(100, current_energy + variation))

            update_state("speaking", current_energy)

            pygame.time.wait(120)  # smooth refresh rate

        pygame.mixer.music.unload()

    except Exception as e:
        print("Audio playback error:", str(e))

    finally:
        # 🔥 Stop animation when done
        update_state("idle", 0)

        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass


# ---------------------------
# SPEAK FUNCTION
# ---------------------------
def speak(text):
    global speech_thread, stop_signal

    stop_signal = False
    text = add_respect(text)
    print("Jarvis:", text)

    update_state("speaking")  # 🔥 Start animation

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            temp_path = f.name

        try:
            asyncio.run(generate_speech(text, temp_path))
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(generate_speech(text, temp_path))
            loop.close()

        speech_thread = threading.Thread(
            target=_play_audio,
            args=(temp_path,),
            daemon=True
        )
        speech_thread.start()

    except Exception as e:
        print("TTS generation error:", str(e))
        update_state("idle")


# ---------------------------
# STOP SPEAKING
# ---------------------------
def stop_speaking():
    global stop_signal
    stop_signal = True
    pygame.mixer.music.stop()
    update_state("idle")


# ---------------------------
# LISTEN FUNCTION
# ---------------------------
def listen():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = recognizer.listen(source)

        command = recognizer.recognize_google(audio)
        print("You:", command)
        return command.lower()

    except sr.UnknownValueError:
        return None

    except sr.RequestError as e:
        print("Speech recognition service error:", str(e))
        return None

    except Exception as e:
        print("Microphone error:", str(e))
        return None