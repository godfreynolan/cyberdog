import openai
import config

openai.api_key =  config.OPENAI_API_KEY

speech_file = "recording1.wav"

with openai.audio.speech.with_streaming_response.create(
	model="tts-1",
	voice="alloy",
	input="Are you having trouble breathing?"
) as response:
	response.stream_to_file(speech_file)


	