import json

from langchain_openai import ChatOpenAI
import os
from pathlib import Path, PurePath, PurePosixPath, PureWindowsPath
import ffmpegmaker as film
import ffmpeg
import speech
import script
import image

system_prompt = '''
Du är en futurist och en dokumentärskapare. Ditt jobb är att skriva ett manus till en dokumentär om hur världen kommer ser ut om 50 år. 
Manuset ska vara begränsad till ett visst område. 
Beroende på propmpten är du antingen utopikst eller dystopiskt. 
Ditt manus formatteras som en JSON fil. 
Du ger förslag till text men även till bilderna som ska vara med i doumentären. 
När du beskriver bilderna gör du det genom att skriver ett DALLE-E prompt som skulle genera den bilden. 
Bilden ska se verkligt ut. 
Manuset ska består ett antal sekvensker coh varje sekvens ska ha JSON keys "titel", "beskrivning" och "bild".  
Beskrivningen ska vara utförlig. 
Det ska även finnas en sekvens för introduktion och avslutning. 
ALla sekvenser placeras i en array som heter sekvenser.
'''

# #topic_array = ["utbildning", "transport", "ai", "energiförsörjning", "projekt Planet B", "bostäder", "mat"]
topic_array = ["utbildning"]
topia_array = ["dystopic", "utopic"]

#File paths
parent_dir = os.getcwd()
base_audio_path = os.path.join(parent_dir, "audio")
base_image_path = os.path.join(parent_dir, "image")
base_script_path = os.path.join(parent_dir, "script")
base_video_path = os.path.join(parent_dir, "video")
base_demux_path = os.path.join(parent_dir, "demux")


def create_filelist(textfile_path, video_list):
    with open(textfile_path, "w") as f:
        for i, img in enumerate(video_list):
            img_with_double = img.replace('\\', '\\\\')
            f.write(f'file {img_with_double}\n')


def populate_filelists(audio_file_list, image_file_list, audio_file_length_list):
    # Find all the newly created image files
    p = Path(base_image_path)
    for filepath in p.glob(f'{topic}-{topia}-*.png'):
        image_file_list.append(filepath)
    # Find all the newly created sound files
    p = Path(base_audio_path)
    for filepath in p.glob(f'{topic}-{topia}-*.mp3'):
        audio_file_list.append(filepath)
    # Store all the lengths of the newly created files
    for file in audio_file_list:
        duration = ffmpeg.probe(file)["format"]["duration"]
        audio_file_length_list.append(duration)


for topic in topic_array:
    for topia in topia_array:
        audio_file_list = []
        image_file_list = []
        audio_file_length_list = []
        # Create the script
        created_script = script.create_script(system_prompt, topic, topia)
        script.save_script(created_script, base_script_path, topic, topia)
        # Convert the script to JSON
        data = json.loads(created_script)
        sequences = data["sekvenser"]
        #Create all images and audio for each sequence.
        for i, sequence in enumerate(sequences):
            filename = f'{topic}-{topia}-{i}'
            speech.create_speech(sequence["beskrivning"], base_audio_path, filename)
            image.generate_DALLE_images(sequence["bild"], base_image_path, filename)

        populate_filelists(audio_file_list, image_file_list, audio_file_length_list)
        # Make short films
        video_list = film.make_short_films(image_file_list, audio_file_list, base_video_path, f'{topic}-{topia}')
        #Construct the demuxer file
        textfile_path = os.path.join(base_demux_path, f'{topic}-{topia}.txt')
        create_filelist(textfile_path, video_list)
        # Make final film
        film.summarize_film(textfile_path, base_video_path, f'{topic}-{topia}')

    # with open(textfile_path, "w") as f:
    #     for i, img in enumerate(image_file_list):
    #         f.write(f'file {img}\n')
    #         duration = math.ceil(float(audio_file_length_list[i]))
    #         f.write(f'duration {duration}\n')
