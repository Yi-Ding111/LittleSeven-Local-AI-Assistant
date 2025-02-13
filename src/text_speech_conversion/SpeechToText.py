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


sys.path.append("../littleSeven/src/")
from common.config import cfg


class STT(object):
    def __init__(self) -> None:
        # initilization WebRTC VAD
        self.vad = webrtcvad.Vad(cfg.vad_mode)

        # initilization PyAudio
        self.p = pyaudio.PyAudio()

        # load model and processor
        self.processor = WhisperProcessor.from_pretrained(
            pretrained_model_name_or_path=cfg.whisper_model_name_2,
            cache_dir=cfg.whisper_model_path_2,
        )

        self.model = WhisperForConditionalGeneration.from_pretrained(
            pretrained_model_name_or_path=cfg.whisper_model_name_2,
            cache_dir=cfg.whisper_model_path_2,
        )

        self.model.config.forced_decoder_ids = None

        # acceleration
        self.model = self.model.to(cfg.device)

    def record_audio(self):
        """
        Record voice, use VAD to do voice detection (Auto stop).

        Return: Float array: the speech audio file.
        """

        stream = self.p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=cfg.sample_rate_2,
            input=True,
            frames_per_buffer=int(cfg.sample_rate_2 * cfg.frame_duration / 1000),
        )

        # print("start recording...")

        frames = collections.deque(maxlen=cfg.sample_rate_2 * 100)
        no_speech_count = 0

        is_recording = False  # if already checked the voice
        while True:
            audio_frame = stream.read(
                int(cfg.sample_rate_2 * cfg.frame_duration / 1000)
            )
            frames.append(audio_frame)

            audio_data = np.frombuffer(audio_frame, dtype=np.int16)

            is_speech = self.vad.is_speech(audio_data.tobytes(), cfg.sample_rate_2)

            if is_speech:
                # only print the info at the first time
                if not is_recording:
                    print("detect voice...")
                    is_recording = True

                no_speech_count = 0

            else:
                # print("with no voice...")
                no_speech_count += 1

            if no_speech_count >= cfg.silence_limit:
                print("end recording...")
                break

        stream.stop_stream()
        stream.close()

        return self._process_audio(frames)

    def _process_audio(self, frames):
        """
        Process audio file. Transfer audio data into the format Whisper asked.
        Params:
            frames: audio frames.
        Return: Tensor: audio tensor
        """
        audio_in_memory = io.BytesIO()
        with wave.open(audio_in_memory, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
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
        audio_data_resampled = audio_data_resampled / np.max(
            np.abs(audio_data_resampled)
        )

        # prepare data as a tensor
        input_audio = torch.tensor(audio_data_resampled, dtype=torch.float32)

        return input_audio

    def transcribe_audio(self, input_audio):
        """
        Use Whisper to detect and transcribe audio data.
        Params:
            input_audio: Tensor: audio tensor
        Return: The plain text
        """
        input_features = self.processor(
            input_audio, sampling_rate=16000, return_tensors="pt"
        ).input_features

        input_features = input_features.to(cfg.device)

        predicted_ids = self.model.generate(input_features)

        transcription = self.processor.batch_decode(
            predicted_ids, skip_special_tokens=True
        )

        return transcription[0]

    def close(self):
        """
        close PyAudio resource
        """
        self.p.terminate()


# if __name__=="__main__":
#     stt=STT()
#     input_audio=stt.record_audio()
#     plain_text=stt.transcribe_audio(input_audio=input_audio)

#     print(plain_text)

#     stt.close()
