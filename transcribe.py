import openai
import config

openai.api_key =  config.OPENAI_API_KEY

media_file_path = 'recording_good.wav'
media_file = open(media_file_path, 'rb')


transcription = openai.audio.transcriptions.create(
    model="whisper-1",
    file=media_file,
)
# print(transcription.text)


response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    # Conversation as a list of messages.
    messages=[
        {"role": "system", "content": "You are a helpful first responder who is trying to see how \
                            much in need of attention.  Here are the questions we asked the patient: \
                            Are you having trouble breathing? Is there a lot of blood? \
                            Where is the blood? and Can you move your arms and legs? \
                            Summarize the conversation if you can, only use the responses."   },
        {
            "role": "user",
            "content": transcription.text,
        }
    ]
)

print(response.choices[0].message.content)

    