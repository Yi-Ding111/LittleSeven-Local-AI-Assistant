#!/bin/bash
set -e


if ! command -v conda &> /dev/null; then
    echo "[ERROR] Conda is not installed. Please install Miniconda or Anaconda first."
    exit 1
fi


if ! command -v ffmpeg &> /dev/null; then
    echo "[INFO] Installing ffmpeg via Homebrew..."
    brew install ffmpeg
else
    echo "[INFO] ffmpeg is already installed. Skipping installation."
fi



echo "[INFO] Activating Conda environment 'littleSeven'..."
conda env create -f ./environment.yml
conda activate littleSeven


# install llama-cpp-python for GPU specefic
# if dont use GPU could only run pip install llama-cpp-python
# I use m2 max chip, I could use Metal to run the llm
CMAKE_ARGS="-DLLAMA_METAL_EMBED_LIBRARY=ON -DLLAMA_METAL=on" pip install llama-cpp-python --no-cache-dir


echo "[INFO] Starting LittleSeven AI Assistant..."
exec python ./src/main/LittleSeven-AI-Assistant.py