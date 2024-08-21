from PIL import Image, ImageDraw, ImageFont


def make_jpg(japanese, korean, romanization, savename):
    # テキスト情報
    texts = [
        {
            "japanese": japanese,
            "korean": korean,
            "romanization": romanization
        },
        # 他のテキスト情報を追加
    ]

    # japaneseフィールドを取り出す
    japanese_texts = [text["japanese"] for text in texts]
    korean_texts = [text["korean"] for text in texts]
    romanization_texts = [text["romanization"] for text in texts]

    # テンプレート画像の読み込み
    img = Image.open('./services/imgs/white_smp.jpg')
    jp_font = ImageFont.truetype('./fonts/ヒラギノ角ゴシック W3.ttc', 120)
    kr_font = ImageFont.truetype('./fonts/DoHyeon-Regular.ttf', 120)

    draw = ImageDraw.Draw(img)

    #TODO:以下ループ

    #描きたい文字のサイズを取得する
    jp_draw_text_width, jp_draw_text_height = draw.textbbox((0, 0),
                                                            japanese_texts[0],
                                                            font=jp_font)[2:]
    kr_draw_text_width, kr_draw_text_height = draw.textbbox((0, 0),
                                                            korean_texts[0],
                                                            font=kr_font)[2:]
    rz_raw_text_width, rz_draw_text_height = draw.textbbox(
        (0, 0), romanization_texts[0], font=jp_font)[2:]

    #描きたい文字のサイズと元画像のサイズを元に、描画開始ポイントの座標を決める
    jp_start_X_point = img.size[0] / 2 - jp_draw_text_width / 2
    jp_start_Y_point = img.size[1] / 3 - jp_draw_text_height / 2

    kr_start_X_point = img.size[0] / 2 - kr_draw_text_width / 2
    kr_start_Y_point = img.size[1] / 2 - kr_draw_text_height / 2

    rz_start_X_point = img.size[0] / 2 - rz_raw_text_width / 2
    rz_start_Y_point = img.size[1] / 1.5 - rz_draw_text_height / 2

    #描画する
    draw.text((jp_start_X_point, jp_start_Y_point),
              japanese_texts[0],
              '#000',
              font=jp_font,
              anchor='lb')

    draw.text((kr_start_X_point, kr_start_Y_point),
              korean_texts[0],
              '#000',
              font=kr_font,
              anchor='lb')

    draw.text((rz_start_X_point, rz_start_Y_point),
              romanization_texts[0],
              '#000',
              font=jp_font,
              anchor='lb')

    img.save("./services/imgs/" + savename + ".jpg")
