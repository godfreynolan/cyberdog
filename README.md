# Using ChatGPT to get a Xiaomi to speak 

1. record whatever questions you want the dog to say using record_questions.py 
- this requires an OpenAI API key in a config.py file
- copy recordings and dogAudio.sh using scp by connecting to the download port 
2. run video_audio_server.py to set up the RTSP feed. Video is /dev/video5
3. run app.py on your laptop, change the RTSP_URL to the right URL
4. run ./dogAudio.sh on the dog to ask questions and hopefully get someone to answer
5. run transcribe.py on the laptop to get a summary of all the Q&A/
