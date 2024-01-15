import argparse
import os
import speech_recognition as sr
from pydub import AudioSegment

def convert_mp3_to_wav(mp3_file_path):
    # Load MP3 file
    audio = AudioSegment.from_mp3(mp3_file_path)

    # Create a temporary WAV file
    wav_file_path = os.path.splitext(mp3_file_path)[0] + '.wav'
    audio.export(wav_file_path, format='wav')

    return wav_file_path

def transcribe_audio(audio_file_path):
    # Convert MP3 to WAV if needed
    if audio_file_path.lower().endswith('.mp3'):
        audio_file_path = convert_mp3_to_wav(audio_file_path)

    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Load the audio file
    with sr.AudioFile(audio_file_path) as audio_file:
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(audio_file)

        # Record the audio
        audio = recognizer.record(audio_file)

        try:
            # Use Google Web Speech API for transcription
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            print(f"Google Web Speech API could not understand the audio: {audio_file_path}")
        except sr.RequestError as e:
            print(f"Could not request results from Google Web Speech API; {e}")

    return None

def transcribe_and_save(input_file_path):
    # Transcribe audio and get text
    transcribed_text = transcribe_audio(input_file_path)

    if transcribed_text:
        # Create corresponding text file
        output_file_path = os.path.splitext(input_file_path)[0] + '.txt'
        
        # Save transcribed text to the text file
        with open(output_file_path, 'w') as text_file:
            text_file.write(transcribed_text)

        print(f"Transcription saved to: {output_file_path}")
    else:
        print("Transcription failed.")

    # Delete temporary WAV file if created
    if input_file_path.lower().endswith('.mp3'):
        os.remove(input_file_path)

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Transcribe audio files to text.')
    parser.add_argument('-i', '--input', nargs='+', help='Input audio file(s)', required=True)
    parser.add_argument('-d', '--directory', help='Directory path for input audio files')
    args = parser.parse_args()

    # Process each input file
    for input_file in args.input:
        # Check if a directory is provided
        if args.directory:
            input_file = os.path.join(args.directory, input_file)

        transcribe_and_save(input_file)
