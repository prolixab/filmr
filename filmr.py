import json
import os
from pathlib import Path, PurePath, PurePosixPath, PureWindowsPath
import ffmpegmaker as film
import ffmpeg
import speech
import script
import image
from prompts import system_prompt, image_style_prompt

# #topic_array = ["utbildning", "transport", "ai", "energiförsörjning", "projekt Planet B", "bostäder", "mat"]
topic_array = ["utbildning"]
#topia_array = ["dystopic", "utopic"]
topia_array = ["dystopic"]

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


def populate_filelists(audio_file_list, image_file_list, audio_file_length_list, topic, topia):
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


def create_film(topic, topia):
    audio_file_list = []
    image_file_list = []
    audio_file_length_list = []
    # Create the script
    # created_script = script.create_script(system_prompt, topic, topia)
    # script.save_script(created_script, base_script_path, topic, topia)
    # # Convert the script to JSON
    # data = json.loads(created_script)
    # sequences = data["sekvenser"]
    # # Create all images and audio for each sequence.
    # for i, sequence in enumerate(sequences):
    #     filename = f'{topic}-{topia}-{i}'
    #     speech.create_speech(sequence["beskrivning"], base_audio_path, filename)
    #     image.generate_DALLE_images(sequence["bild"], base_image_path, filename)

    populate_filelists(audio_file_list, image_file_list, audio_file_length_list, topic, topia)
    # Make short films
    video_list = film.make_short_films(image_file_list, audio_file_list, base_video_path, f'{topic}-{topia}')
    # Construct the demuxer file
    #textfile_path = os.path.join(base_demux_path, f'{topic}-{topia}.txt')
    #create_filelist(textfile_path, video_list)
    # Make final film
    output = film.summarize_film(video_list, base_video_path, f'{topic}-{topia}')
    return output


def create_multiple_films(topic_list, topia_list):
    for topic in topic_list:
        for topia in topia_list:
            create_film(topic, topia)


if __name__ == '__main__':
    create_multiple_films(topic_array, topia_array)

    # with open(textfile_path, "w") as f:
    #     for i, img in enumerate(image_file_list):
    #         f.write(f'file {img}\n')
    #         duration = math.ceil(float(audio_file_length_list[i]))
    #         f.write(f'duration {duration}\n')
