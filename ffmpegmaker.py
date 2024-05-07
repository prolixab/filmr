import ffmpeg
import os


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

def make_short_films(image_file_list, audio_file_list, video_path, filename ):
    video_list=[]
    for i, img in enumerate(image_file_list):
        final_filename = make_short_film(video_path, img, audio_file_list[i], filename, i)
        video_list.append(final_filename)
    return video_list

def summarize_film(textfile_path, path, filename):
    ffmpeg.input(textfile_path,
                 format='concat', safe=0).output(f'output-video.avi', c='copy').run()
    # (
    #     ffmpeg
    #     .concat(t)
    #     .output(f'output-video.mp4')
    #     .overwrite_output()
    #     .run()
    # )
