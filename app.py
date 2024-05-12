from main.s2t import speech_recognition 
from main.llm import Robot
from main.audio import AudioRecorder
from main.t2s.edge2txt import edge2s
from transformers import AutoModelForSpeechSeq2Seq, Wav2Vec2Processor
import sounddevice as sd
import numpy as np
import keyboard
import torch
import os

# Load the pre-trained model and processor
model_name = "biodatlab/whisper-th-small-combined"
processor = Wav2Vec2Processor.from_pretrained(model_name)
model = AutoModelForSpeechSeq2Seq.from_pretrained(model_name)
os.environ['GROQ_API_KEY']='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'

class AI_Robot_App:
    def __init__(self,model,processer):
        #self.memory = talking_log('log')
        self.robot = Robot()
        self.audio = AudioRecorder()
        self.s2t = speech_recognition()
        self.e2s = edge2s()
        self.model = model
        self.processor = processer

    def capture_audio(self,duration=7, sr=16000):
        print("* Recording")
        audio_data = sd.rec(int(duration * sr), samplerate=sr, channels=1, dtype="float32")
        sd.wait()
        print("* Finished recording")
        return audio_data.squeeze()

    # Function to perform speech-to-text conversion
    def speech_to_text(self,audio_data, sample_rate):
        input_values = self.processor(audio_data, sampling_rate=sample_rate, return_tensors="pt", padding=True)

        with torch.no_grad():
            logits = self.model(input_values.input_values).logits

        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = self.processor.batch_decode(predicted_ids)[0]
        
        return transcription

    def run(self):
        while True:
            data = self.audio.start_recording()
            text = self.s2t.get_text("human.wav")
            #text = speech_to_text(audio_data, sample_rate=16000)
            print("You said: ", text)
            response = self.robot.gorq(text) #Change to self.rotbot.ollama() if you want to use Ollama model
            bot_speak = response
            bot_speak = bot_speak.replace("*", "")
            print("Robot said: ", bot_speak)
            self.e2s.speak(bot_speak,gender="Female")
        print("finish run")

if __name__ == "__main__":
    app = AI_Robot_App(model,processor)
    app.run()
