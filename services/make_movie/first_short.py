from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip, AudioFileClip


def make(
    clip1,
    gif_clip,
):
    # GIFクリップを読み込む
    gif_clip = gif_clip.set_duration(
        clip1.duration).resize(height=500).set_pos(('center', 'bottom'))

    # テキストとGIFを動画に合成
    video = CompositeVideoClip([clip1, gif_clip])

    video.write_videofile("./services/outputs/first.mp4",
                          codec="libx264",
                          audio_codec="aac")
