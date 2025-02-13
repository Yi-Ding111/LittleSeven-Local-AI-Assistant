from types import SimpleNamespace

cfg = SimpleNamespace(**{})

# local device setup
cfg.device = "mps"


# VAD parameters
cfg.frame_duration = 10
cfg.vad_mode = 1
cfg.silence_limit = 100


# pyaudio parameters
cfg.audio_channels = 1
cfg.sample_rate = 44100
cfg.sample_rate_2 = 16000
cfg.frame_chunk = 1024
cfg.voice_duration = 5


# whisper parameters
cfg.whisper_model_name_2 = "openai/whisper-large"
cfg.whisper_model_path_2 = "./STT/whisper_model"


# langchain RAG DB
cfg.fire_dir_origin = "../../../NOTES/papers/inprogress/attentionisallyouneed.pdf"
cfg.fire_dir_with_notes = "/Users/yiding/personal_projects/NOTES/papers/inprogress/Attention-is-all-you-need.pdf"
cfg.embedding_model_name = "text-embedding-3-small"
cfg.chunk_overlap = 100
cfg.chunk_size = 1000
cfg.rag_db_retriever_search_type = "similarity"
cfg.rag_db_retriever_K = 1


# langchain variables
cfg.LLM_model = "gpt-4o"
cfg.history_placeholder_variable = "history"
cfg.memory_file_path = "./src/memory.json"
