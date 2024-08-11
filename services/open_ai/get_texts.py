import os
import openai


# ワードを取得する関数
def words(keyword, num, apikey):
    stream = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role":
            "system",
            "content":
            "Provide responses in Japanese. Output should be in the format: 'number,Japanese,Korean,Korean pronunciation'. For example: '1,猫,고양이,goyangi'"
        }, {
            "role":
            "user",
            "content":
            f"Provide {num} words related to {keyword} in the specified format."
        }],
        stream=True,
    )

    return stream


# streamから配列に格納する関数
def extract_words_from_stream(stream):
    word_list = []
    current_word = []

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            current_word.append(content)
            if content.endswith('\n'):
                word_list.append(''.join(current_word).strip())
                current_word = []

    # 最後の単語が残っている場合に追加
    if current_word:
        word_list.append(''.join(current_word).strip())

    return word_list


# 配列を分ける関数
def divide_word_list(word_list):
    jp_word_list = []
    kr_word_list = []
    pr_word_list = []
    tmp = []
    for str in word_list:
        tmp = str.split(",")
        jp_word_list.append(tmp[1])
        kr_word_list.append(tmp[2])
        pr_word_list.append(tmp[3])
    return jp_word_list, kr_word_list, pr_word_list


def main(keyword, num, apikey):
    st = words(keyword, num, apikey)
    word_list = extract_words_from_stream(st)
    jp_word_list, kr_word_list, pr_word_list = divide_word_list(word_list)
    return jp_word_list, kr_word_list, pr_word_list
