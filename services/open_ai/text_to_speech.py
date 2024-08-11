from pathlib import Path
import openai
from pydub import AudioSegment


def get_mp3(text):
    volume = 5
    speech_file_path = Path(__file__).parent / "../audios/speech.mp3"

    # 音声生成
    response = openai.audio.speech.create(model="tts-1",
                                          voice="alloy",
                                          input=text)
    response.stream_to_file(speech_file_path)

    # 音量を増加させた音声の読み込みと無音の追加
    sound = AudioSegment.from_mp3(speech_file_path) + volume
    one_second_silence = AudioSegment.silent(duration=1000)

    # 音声の前後に無音を追加
    padded_sound = one_second_silence + sound + one_second_silence + sound + one_second_silence

    # 出力ファイルの保存
    padded_sound.export("./services/audios/output.mp3", format="mp3")
