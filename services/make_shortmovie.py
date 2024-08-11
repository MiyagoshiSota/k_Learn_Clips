from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip, AudioFileClip
from services.make_img import add_texts
from services.make_movie import first_short, marge_short
from services.open_ai import text_to_speech


def make(japaneses, koreans, romanizations):
    for i in range(len(japaneses)):
        japanese = japaneses[i]
        korean = koreans[i]
        romanization = romanizations[i]

        add_texts.make_jpg(japanese, "", "", "first")
        add_texts.make_jpg(japanese, korean, romanization, "second")

        # 動画クリップを読み込む
        clip1 = VideoFileClip("./services/imgs/first.jpg").set_duration(5)

        # GIFクリップを読み込む
        gif_clip = VideoFileClip("./services/imgs/count_down.gif",
                                 has_mask=True)

        # 最初の動画を作成
        first_short.make(clip1, gif_clip)

        # 音声の作成
        text_to_speech.get_mp3(korean)

        # 音声クリップを読み込む
        voice_clip = AudioFileClip("./services/audios/output.mp3")

        # 動画クリップを読み込む
        video1 = VideoFileClip("./services/outputs/first.mp4")
        video2 = VideoFileClip("./services/imgs/second.jpg").set_duration(
            voice_clip.duration)

        # 動画をマージする
        marge_short.marge(voice_clip, video1, video2, str(i))
