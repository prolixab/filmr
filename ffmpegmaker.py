import ffmpeg
import os
import moviepy
from moviepy.editor import VideoFileClip
from moviepy.video.compositing.concatenate import concatenate_videoclips


def make_film(filelist, path, filename):
    output_file = os.path.join(path, filename)
    ffmpeg.input(filename=filelist, f='concat', safe='0').output(output_file).run()


def make_short_film(path, img, audio, filename, i):
    output_file = os.path.join(path, filename)
    input_img = ffmpeg.input(img)
    input_audio = ffmpeg.input(audio)
    final_filename = f'{output_file}-{i}.avi'
    output = ffmpeg.concat(input_img, input_audio, v=1, a=1).output(final_filename).overwrite_output()
    ffmpeg.run(output)
    return final_filename


def make_short_films(image_file_list, audio_file_list, video_path, filename):
    video_list = []
    for i, img in enumerate(image_file_list):
        final_filename = make_short_film(video_path, img, audio_file_list[i], filename, i)
        video_list.append(final_filename)
    return video_list


def summarize_film(file_list, path, filename):
    output_file = f'{os.path.join(path, filename)}.mp4'
    video_clips=[]
    for s in file_list:
        video_clips.append(VideoFileClip(s))
    final = concatenate_videoclips(video_clips)

    # Write output to the file
    final.write_videofile(output_file)
    return output_file
    # (
    #     ffmpeg
    #     .concat(t)
    #     .output(f'output-video.mp4')
    #     .overwrite_output()
    #     .run()
    # )
