from moviepy.editor import *
import openai
from services import make_shortmovie
from services.open_ai import get_texts


def make(OPENAI_API_KEY, keyword, num):
    # apikeyの設定
    openai.api_key = OPENAI_API_KEY

    # ワードの生成
    japaneses, koreans, romanizations = get_texts.main(keyword, num,
                                                       OPENAI_API_KEY)

    # 動画の生成
    make_shortmovie.make(japaneses, koreans, romanizations)

    # 動画ファイルの結合
    result = VideoFileClip("./services/outputs/0.mp4")
    for i in range(len(japaneses) - 1):
        clip2 = VideoFileClip("./services/outputs/" + str((i + 1)) + ".mp4")
        result = concatenate_videoclips([result, clip2])

    # mp3ファイルのオーディオクリップを読み込む
    audio_clip = AudioFileClip("./services/audios/Lamp.mp3").subclip(
        0, result.duration)

    # 元の動画の音声を取得
    original_audio = result.audio

    # 元の音声と新しい音声を合成
    composite_audio = CompositeAudioClip([original_audio, audio_clip])

    # 動画に合成音声をセット
    result = result.set_audio(composite_audio)

    # 動画ファイルを出力
    result.write_videofile("./services/outputs/output.mp4",
                           codec="libx264",
                           audio_codec="aac")
