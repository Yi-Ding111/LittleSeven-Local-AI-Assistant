from types import SimpleNamespace

cfg = SimpleNamespace(**{})

cfg.device='mps'

cfg.model_path='./model'
cfg.model_path_gguf='./model_gguf'
cfg.model_name='gpt2'
cfg.model_name_llama_gguf='TheBloke/Llama-2-7B-GGUF'
cfg.file_name_llama_gguf='llama-2-7b.Q4_K_S.gguf'


cfg.llm_gguf_model_path='../model_gguf/llama-2-7b.Q4_K_S.gguf'
cfg.llm_gguf_model_path_2='../model_gguf/llama-2-7b-chat.Q4_0.gguf'
cfg.llm_gguf_model_path_3='../model_gguf/Meta-Llama-3-8B.Q4_K_S.gguf'


# pyaudio parameters
cfg.audio_channels=1
cfg.sample_rate=44100
cfg.sample_rate_2=16000
cfg.frame_chunk=1024
cfg.voice_duration=5

# VAD parameters
cfg.frame_duration=10
cfg.vad_mode=1
cfg.silence_limit=100

# whisper parameters
cfg.whisper_model_name='medium'
cfg.whisper_model_name_2="openai/whisper-large"
cfg.whisper_model_path='./whisper_model'
cfg.whisper_model_path_2='./STT/whisper_model'

cfg.accelerator='mps'


# llama.cpp param
cfg.token_context_window=4096
cfg.n_gpu_layers=1
