from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip, AudioFileClip


def marge(voice_clip, video1, video2, savefile):
    # 音声を動画に追加
    # video1 = video1.set_audio(audio_clip)
    video2 = video2.set_audio(voice_clip)

    # 動画を結合
    final_clip = concatenate_videoclips([video1, video2])

    # 出力ファイルに書き込む
    final_clip.write_videofile("./services/outputs/" + savefile + ".mp4",
                               codec="libx264",
                               audio_codec="aac")
