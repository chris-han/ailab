import os
from itertools import cycle
from tqdm import tqdm

def prepare_videos(
    videos, extension, start, duration, kinect_mask=True, background_path="/", width=1920, height=1080
):

    video_start_secs = start % 60
    video_start_mins = start // 60
    print(f"Dumping frames and segmenting {len(videos)} input videos")
    for i, video in enumerate(videos):
        try:
            os.makedirs(video)
        except FileExistsError:
            continue

        print(f"Dumping frames from {video} ({i+1}/{len(videos)})...")
        ffmpeg_duration = ""
        if duration != "-1":
            ffmpeg_duration = f"-t {duration}"

        cmd=(
            f"ffmpeg -y -ss 00:{video_start_mins:02}:{video_start_secs:02}.000 "
            f"-vsync 0 "
            f"-i \"{video}{extension}\" -vf scale={width}:{height} "
            f"-map 0:0 {ffmpeg_duration} \"{video}/%04d_img.png\" -hide_banner"
            f" > bg_matting_logs.txt 2>&1"
            )

        code = os.system(
            cmd
        )
        if code != 0:
            exit(code)

        print(f"Segmenting frames...")
        if kinect_mask:
            cmd = (
                f"KinectMaskGenerator.exe \"{video}{extension}\" \"{video}\" {start} {duration}"
                f" > segmentation_logs_{i}.txt 2>&1"
            )
            code = os.system(
                cmd
            )
            if code != 0:
                exit(code)
        else:
            code = os.system(
                f"python segmentation_deeplab.py -i \"{video}\""
                f" > segmentation_logs_{i}.txt 2>&1"
            )
            if code != 0:
                exit(code)

        print(f"Extracting background...")
        code = os.system(
            f"ffmpeg -y -i \"{video}{extension}\" -vf scale={width}:{height} "
            f"-map 0:0 -ss 00:00:02.000 -vframes 1 \"{video}.png\" -hide_banner"
            " > bg_matting_logs.txt 2>&1"
        )
        if code != 0:
            exit(code)

#######################################
# prepare target background video frames
    backgrounds = [os.path.join(background_path, f[:-4]) for f in os.listdir(background_path) if f.endswith(".mp4")]
    print(f"Dumping frames for {background_path} background videos")
    for i, background in enumerate(tqdm(backgrounds)):
        #os.makedirs(background, exist_ok=True)
        try:
            os.makedirs(background)
        except FileExistsError:
            continue

        code = os.system(
            f"ffmpeg -i \"{background}.mp4\" \"{background}/%04d_img.png\" -hide_banner"
            f" > bg_image_logs.txt 2>&1"
        )
        if code != 0:
            exit(code)
        print(f"Dumped frames for {background} ({i+1}/{len(videos)})")

    print(f"Creating CSV")
    background_frames = []
    for background in backgrounds:
        background_frames.extend([os.path.join(background, f) for f in sorted(os.listdir(background))])
    background_stream = cycle(background_frames)

    output_csv = "Video_data_train.csv"
    #videoframes = [os.path.join(videos, f[:-4]) for f in os.listdir(videos) if f.endswith(".png")
    
    with open(output_csv, "w") as f:
        for i, video in enumerate(videos):
            videoframes = []
            for pngfile in os.listdir(video):
                if pngfile.endswith(".png"):
                    videoframes.append(pngfile) # filter out timestampfile.txt leave only png files

            n = len(videoframes)
            assert n % 2 == 0
            n //= 2
            for j in range(1, n + 1 - 80):
                img_name = video + "/%04d_img.png" % j
                captured_back = video + ".png"
                seg_name = video + "/%04d_masksDL.png" % j
                mc1 = video + "/%04d_img.png" % (j + 20)
                mc2 = video + "/%04d_img.png" % (j + 40)
                mc3 = video + "/%04d_img.png" % (j + 60)
                mc4 = video + "/%04d_img.png" % (j + 80)
                target_back = next(background_stream)
                csv_line = f"{img_name};{captured_back};{seg_name};{mc1};{mc2};{mc3};{mc4};{target_back}\n"
                f.write(csv_line)
    print(f"Done, written to {output_csv}")
#######################################