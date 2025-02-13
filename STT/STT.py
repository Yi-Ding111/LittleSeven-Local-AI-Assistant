import pyaudio
import webrtcvad
import numpy as np
import collections
import wave
import io
import whisper
import time
import librosa
import sys
import torch
from transformers import WhisperProcessor, WhisperForConditionalGeneration

sys.path.append("../littleSeven/")
from common.config import cfg

import os

print(os.getcwd())

# initilization WebRTC VAD
vad = webrtcvad.Vad(cfg.vad_mode)

# initilization PyAudio
p = pyaudio.PyAudio()

# open audio streaming
stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=cfg.sample_rate_2,
    input=True,
    frames_per_buffer=int(cfg.sample_rate_2 * cfg.frame_duration / 1000),
)

print("start recording...")

frames = collections.deque(maxlen=cfg.sample_rate_2 * 100)
no_speech_count = 0
start_time = time.time()

while True:
    audio_frame = stream.read(int(cfg.sample_rate_2 * cfg.frame_duration / 1000))
    frames.append(audio_frame)

    audio_data = np.frombuffer(audio_frame, dtype=np.int16)

    is_speech = vad.is_speech(audio_data.tobytes(), cfg.sample_rate_2)

    if is_speech:
        print("detect voice...")
        no_speech_count = 0
        start_time = time.time()
    else:
        print("with no voice...")
        no_speech_count += 1

    if no_speech_count >= cfg.silence_limit:
        print("end recording...")
        break

stream.stop_stream()
stream.close()
p.terminate()

audio_in_memory = io.BytesIO()
with wave.open(audio_in_memory, "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(cfg.sample_rate_2)
    wf.writeframes(b"".join(frames))

# save audio data into memory
audio_in_memory.seek(0)
with wave.open(audio_in_memory, "rb") as wf:
    audio_data = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16)

# convert int-typed audio data into float-type and do normalization to [-1,1]
audio_data_float = audio_data.astype(np.float32) / np.max(np.abs(audio_data))

# adjust the audio to 16000HZ sample rate
audio_data_resampled = librosa.resample(
    audio_data_float, orig_sr=cfg.sample_rate_2, target_sr=16000
)

# normalize the audio to [-1,1]
audio_data_resampled = audio_data_resampled / np.max(np.abs(audio_data_resampled))

# prepare data as a tensor
input_audio = torch.tensor(audio_data_resampled, dtype=torch.float32)


# load model and processor
processor = WhisperProcessor.from_pretrained(
    pretrained_model_name_or_path=cfg.whisper_model_name_2,
    cache_dir=cfg.whisper_model_path_2,
)

model = WhisperForConditionalGeneration.from_pretrained(
    pretrained_model_name_or_path=cfg.whisper_model_name_2,
    cache_dir=cfg.whisper_model_path_2,
)

model.config.forced_decoder_ids = None


input_features = processor(
    input_audio, sampling_rate=16000, return_tensors="pt"
).input_features


# acceleration
model = model.to(cfg.device)

input_features = input_features.to(cfg.device)

predicted_ids = model.generate(input_features)

transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)

print(transcription[0])
