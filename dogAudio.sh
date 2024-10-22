#!/bin/bash

wav_files=(
    "recording1.wav"
    "recording2.wav"
    "recording2a.wav"
    "recording3.wav"
    "recording4.wav"
)

play_audio() {
    local file_path="$1"
    echo "Playing: $file_path"
    aplay "$file_path"
}

play_audio "${wav_files[0]}"
sleep 10

play_audio "${wav_files[1]}"
sleep 10

play_audio "${wav_files[2]}"
sleep 10

play_audio "${wav_files[3]}"
sleep 10

play_audio "${wav_files[4]}"
sleep 10

echo "Script finished."
