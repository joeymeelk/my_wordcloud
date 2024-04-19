from tkinter import *
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
from wordcloud import WordCloud
from collections import Counter
from kiwipiepy import Kiwi, utils

# Tkinter 윈도우 생성
root = Tk()
root.title('WordCloudMaker - DDUALAB')
root.geometry("1200x1000+100+100")
root.resizable(False, False)

# 파일 선택 함수
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
            txt.delete("1.0", "end")
            txt.insert("1.0", file_content)

# WordCloud 생성 함수
def create_wordcloud():
    nouns = []
    max_words = int(maxes.get())
    font_size = int(size.get())
    min_length = int(length.get())
    
    wordcloud = WordCloud(font_path="malgun",
                          max_words=max_words,
                          max_font_size=font_size,
                          background_color="white",
                          width=1000, height=500)

    text_content = txt.get("1.0", "end").strip()

    kiwi = Kiwi()
    stopwords = utils.Stopwords()
    tokens = kiwi.tokenize(text_content, stopwords=stopwords)

    for token, pos, _, _ in tokens:
        if pos.startswith('N') or pos.startswith('SL'):
            if len(token) >= min_length:
                nouns.append(token)

    word_freq = Counter(nouns)
    most_common_words = word_freq.most_common(max_words)

    wordcloud.generate_from_frequencies(dict(most_common_words))

    # 워드클라우드 이미지를 PIL Image 객체로 변환
    global wordcloud_image
    wordcloud_image = wordcloud.to_image()

    # PIL Image를 Tkinter PhotoImage로 변환하여 표시
    global wordcloud_image_tk
    wordcloud_image_tk = ImageTk.PhotoImage(wordcloud_image)
    label_wordcloud.config(image=wordcloud_image_tk)

def save_wordcloud():
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if file_path:
        wordcloud_image.save(file_path)
        messagebox.showinfo("저장 완료", "워드클라우드 이미지가 성공적으로 저장되었습니다.")

# 초기화 함수
def clear():
    txt.delete("1.0", "end")
    label_wordcloud.config(image='')

# GUI 레이아웃 구성
frame_top = Frame(root)
frame_top.pack(pady=20)

lbl_file = Label(frame_top, text="파일 선택:")
lbl_file.pack(side=LEFT, padx=10)

btn_file = Button(frame_top, text="파일 선택", command=select_file)
btn_file.pack(side=LEFT, padx=10)

frame_middle = Frame(root)
frame_middle.pack(pady=20)

lbl_txt = Label(frame_middle, text="불러온 파일 내용 또는 직접 입력:")
lbl_txt.pack(pady=10)

# 텍스트 스크롤바와 텍스트 입력창
scrollbar = Scrollbar(frame_middle, orient=VERTICAL)
scrollbar.pack(side=RIGHT, fill=Y)

txt = Text(frame_middle, height=15, width=100, yscrollcommand=scrollbar.set)
txt.pack(pady=10)
scrollbar.config(command=txt.yview)

frame_bottom = Frame(root)
frame_bottom.pack(pady=20)

max_text = Label(frame_bottom, text='최대 단어 개수:')
max_text.pack(side=LEFT, padx=10)

maxes = Entry(frame_bottom, width=10)
maxes.insert(0, 70)
maxes.pack(side=LEFT)

size_text = Label(frame_bottom, text='단어 크기 설정:')
size_text.pack(side=LEFT, padx=10)

size = Entry(frame_bottom, width=10)
size.insert(0, 150)
size.pack(side=LEFT)

len_text = Label(frame_bottom, text='최소 단어 길이:')
len_text.pack(side=LEFT, padx=10)

length = Entry(frame_bottom, width=10)
length.insert(0, 1)
length.pack(side=LEFT)

# 워드클라우드 생성 및 초기화 버튼
btn_make = Button(frame_bottom, text="워드클라우드 생성", command=create_wordcloud)
btn_make.pack(side=LEFT, padx=20)

btn_save = Button(frame_bottom, text="워드클라우드 저장", command=save_wordcloud)
btn_save.pack(side=LEFT)

btn_clear = Button(frame_bottom, text="초기화", command=clear)
btn_clear.pack(side=LEFT)

# 워드클라우드 이미지 표시를 위한 Label
label_wordcloud = Label(root)
label_wordcloud.pack(pady=20)

root.mainloop()
