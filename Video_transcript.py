import moviepy.editor as mp
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

# Replace with the name of your video file
video_path = 'example_video.mp4'

# Extract audio from the video file
clip = mp.VideoFileClip(video_path)
audio = clip.audio

# Save audio to a temporary file
temp_audio_file = 'temp_audio.wav'
audio.write_audiofile(temp_audio_file)

# Set up speech-to-text API client
client = speech.SpeechClient()

# Set up audio file for transcription
with open(temp_audio_file, 'rb') as audio_file:
    content = audio_file.read()
    audio = types.RecognitionAudio(content=content)

# Set up transcription request
config = types.RecognitionConfig(
    encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
    language_code='en-US')

# Perform transcription
response = client.recognize(config, audio)

# Write transcripts to text file
transcript_file = 'transcripts.txt'
with open(transcript_file, 'w') as f:
    for result in response.results:
        f.write(result.alternatives[0].transcript + '\n')

# Clean up temporary audio file
os.remove(temp_audio_file)
