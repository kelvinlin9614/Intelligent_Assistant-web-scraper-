# Group Project: Web Scraper
# Zewen Lin
import os
import textwrap
import time
from tkinter import *
import tkinter as tk
import urllib
import webbrowser
import nltk
from PIL import Image, ImageTk
from lxml.html.builder import FONT
from newspaper import Article
from selenium import webdriver as wd
import web_scraper
import price_tracker
import instock_alert
import tkHyperlinkManager
from gtts import gTTS
import dictionary
import word
from tkinter import ttk
from word import word, InvalidWordError
from datetime import datetime, timedelta

HEIGHT = 600
WIDTH = 800


# remove the main page(containing 4 buttons)
def forget_main_frame(button_1, button_2, button_3, button_4, button_5, button_6, display_job_frame):
    button_1.grid_remove()
    button_2.grid_remove()
    button_3.grid_remove()
    button_4.grid_remove()
    button_5.grid_remove()
    button_6.grid_remove()
    if display_job_frame:
        display_job_frame.grid_remove()


# display the main page
def back_main_frame():
    button_1.grid()
    button_2.grid()
    button_3.grid()
    button_4.grid()
    button_5.grid()
    button_6.grid()


def destroy_all_widget(frame):
    for widget in frame.winfo_children():
        widget.destroy()


# text to speech function.
# parameters are strings
def text_to_speech(text):
    language = 'en'
    speech = gTTS(text=text, lang=language, slow=False)
    speech.save("text.mp3")
    os.system("afplay text.mp3 -t 10")


# -------------------------------------ARTICLE STUFF----------------------------------------------------------#
def download_article(button_1, button_2, button_3, button_4, button_5, button_6, display_job_frame):
    forget_main_frame(button_1, button_2, button_3, button_4, button_5, button_6, display_job_frame)
    default_url = "https://www.cnn.com/2022/04/26/investing/markets-plunge-tech-down/index.html"

    search_box_frame = tk.Frame(root)
    search_box_frame.place(relx=0.5, rely=0.2, relwidth=0.8, relheight=0.5, anchor='n')

    # display website url label
    url_label = tk.Label(search_box_frame, text="ENTER URL: ", font=('Helvetica', 18))
    url_label.place(relx=0.1, rely=0.3, relwidth=0.2, relheight=0.2)

    # display website url input box
    url_box = tk.Entry(search_box_frame, font=(FONT, 18))
    url_box.insert(-1, default_url)
    url_box.place(relx=0.3, rely=0.3, relwidth=0.6, relheight=0.2)

    # display search button
    button_search = tk.Button(search_box_frame, text="Search", font=(FONT, 18),
                              highlightbackground="#20bebe", fg="black",
                              command=lambda: [url_label.place_forget(), url_box.place_forget(),
                                               button_search.place_forget(), search_box_frame.place_forget(),
                                               display_article(url_box.get())])
    button_search.place(relx=0.38, rely=0.75, relheight=0.2, relwidth=0.2)


def display_article(url):
    article = Article(url)
    # Do some NLP
    article.download()  # Downloads the link’s HTML content
    article.parse()  # Parse the article
    nltk.download('punkt')  # 1 time download of the sentence tokenizer
    article.nlp()  # Keyword extraction wrapper

    display_job_frame = tk.Frame(root)
    display_job_frame.place(relx=0.2, rely=0.05, relwidth=0.9, relheight=0.9)

    # information scraped from the article
    authors = ",".join(article.authors)
    date = article.publish_date
    text = article.text
    title = article.title
    # summ = article.summary.replace('\n', ' ').replace(u'\u2019', "\'")
    summ = textwrap.dedent(article.summary).strip()
    meta = article.meta_description
    image = article.top_image
    multi_images = article.images

    # information scarped from the article turned into a text block
    summary_text = "Author(s): " + str(authors) + "\nDate Published: " + str(date) + "\nArticle Name: " + str(title) + \
                   "\nArticle sypnosis: " + str(meta) + "\nArticle summary: " + str(summ)

    S = tk.Scrollbar(display_job_frame, orient=VERTICAL)
    T = tk.Text(display_job_frame, height=40, width=80, yscrollcommand=S.set, font=("Helvetica", 20), wrap=WORD)
    S.pack(side=tk.RIGHT, fill=tk.Y)
    T.pack(side=tk.LEFT, fill=tk.Y)
    S.config(command=T.yview)
    T.config(yscrollcommand=S.set)
    T.insert(tk.END, "Author(s): \n")
    T.insert(tk.END, authors)
    T.insert(tk.END, "\n\nDate Published: \n")
    T.insert(tk.END, date)
    T.insert(tk.END, "\n\nArticle Name: \n")
    T.insert(tk.END, title)
    T.insert(tk.END, "\n\nArticle sypnosis:\n")
    T.insert(tk.END, meta)
    T.insert(tk.END, "\n\nArticle summary:\n")
    T.insert(tk.END, summ)

    file_path = download_image(image)  # downloads all images found in article

    # ========title frame===========#
    bg_color = "#323a45"
    text_area_bg = "#e1f3f8"
    basic_font_color = "#ffffff"  # "#ccc4c4"

    display_buttons = tk.Frame(root)
    display_buttons.place(relx=0.0, rely=0.05, relwidth=0.2, relheight=0.9)

    F1 = LabelFrame(display_buttons, text="Category", font=(
        "helvetica", 20, "bold"), bg=bg_color, fg=basic_font_color, bd=10, relief=GROOVE)
    F1.place(x=0, y=0, width=380, relheight=1)

    # button to read summary
    text_talk = tk.StringVar()
    text_talk.set("PLAY SUMMARY")
    b1 = tk.Button(F1, textvariable=text_talk, font=('Helvetica', 18), width=17, bd=7,
                   highlightbackground="#20bebe", fg="black", command=lambda: text_to_speech(summ))
    b1.grid(row=1, column=0, padx=10, pady=5)

    # button to read article
    article_talk = tk.StringVar()
    article_talk.set("PLAY ARTICLE")
    b2 = tk.Button(F1, textvariable=article_talk, font=('Helvetica', 18), width=17, bd=7,
                   highlightbackground="#20bebe", fg="black", command=lambda: text_to_speech(text))
    b2.grid(row=2, column=0, padx=10, pady=5)

    # button to show top image
    image_button = tk.StringVar()
    image_button.set("SHOW IMAGE")
    b3 = tk.Button(F1, textvariable=image_button, font=('Helvetica', 18), width=17, bd=7,
                   highlightbackground="#20bebe", fg="black", command=lambda: [display_job_frame.destroy(),
                                                                               display_image(file_path)])
    b3.grid(row=3, column=0, padx=10, pady=5)

    # button to read summary
    summary_button = tk.StringVar()
    summary_button.set("SUMMARY")
    b0 = tk.Button(F1, textvariable=summary_button, font=('Helvetica', 18), width=17, bd=7,
                   highlightbackground="#20bebe", fg="black", command=lambda: [display_job_frame.destroy(),
                                                                               display_summary(authors, date, title,
                                                                                               meta, summ)])
    b0.grid(row=0, column=0, padx=10, pady=5)

    # button to return to main page
    back_button = tk.StringVar()
    back_button.set("BACK TO MAIN")
    bb = tk.Button(F1, textvariable=back_button, font=('Helvetica', 18), width=17, bd=7,
                   highlightbackground="#20bebe", fg="black",
                   command=lambda: return_main(root))
    bb.grid(row=6, column=0, padx=10, pady=5)


def display_image(image_file):
    display_job_frame = tk.Frame(root)
    display_job_frame.place(relx=0.2, rely=0.05, relwidth=0.9, relheight=0.9)

    load = Image.open(image_file)
    S = tk.Scrollbar(display_job_frame, orient=VERTICAL)
    render = ImageTk.PhotoImage(load)
    img = Label(image=render)
    img.image = render
    img.place(relx=0.2, rely=0.05, relwidth=0.9, relheight=0.9)


def display_summary(authors, date, title, meta, summ):
    display_job_frame = tk.Frame(root)
    display_job_frame.place(relx=0.2, rely=0.05, relwidth=0.9, relheight=0.9)
    S = tk.Scrollbar(display_job_frame, orient=VERTICAL)
    T = tk.Text(display_job_frame, height=40, width=80, yscrollcommand=S.set, font=("Helvetica", 20), wrap=WORD)
    S.pack(side=tk.RIGHT, fill=tk.Y)
    T.pack(side=tk.LEFT, fill=tk.Y)
    S.config(command=T.yview)
    T.config(yscrollcommand=S.set)
    T.insert(tk.END, "Author(s): \n")
    T.insert(tk.END, authors)
    T.insert(tk.END, "\n\nDate Published: \n")
    T.insert(tk.END, date)
    T.insert(tk.END, "\n\nArticle Name: \n")
    T.insert(tk.END, title)
    T.insert(tk.END, "\n\nArticle sypnosis:\n")
    T.insert(tk.END, meta)
    T.insert(tk.END, "\n\nArticle summary:\n")
    T.insert(tk.END, summ)


def download_image(images):
    # creates new folder for temp use
    newpath = r'temp'
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    cnt = 1  # keeps image names unique

    # changes directory to temp folder
    os.chdir(newpath)

    saved_filename = "0000000" + str(cnt) + ".jpg"
    urllib.request.urlretrieve(images, saved_filename)

    return saved_filename


# function to show images on screen
def show_image(path):
    im = Image.open(path)
    im.show()


# function to delete image
def delete_file(file_path):
    # deletes image
    os.remove(file_path)


# ---------------------------------------------------END ARTICLE-----------------------------------------#


# ---------------------------------------------------In Stock Alert-------------- -----------------------#
def in_stock_alert(button_1, button_2, button_3, button_4, button_5, button_6, display_job_frame):
    forget_main_frame(button_1, button_2, button_3, button_4, button_5, button_6, display_job_frame)
    default_url = "https://www.amazon.com/s?k=rtx+3080&sprefix=rtx+%2Caps%2C173&ref=nb_sb_ss_ts-doa-p_1_4"
    in_stock_alert_frame = tk.Frame(root)
    in_stock_alert_frame.grid(row=1, column=1)

    # display website url label
    url_label = tk.Label(in_stock_alert_frame, text="URL:  ", font=('Railway', 16))
    url_label.grid(row=1, column=1, sticky="NE", pady=20, padx=20)

    # display website url input box
    url_box = tk.Entry(in_stock_alert_frame, font=('Railway', 18), width=22)
    url_box.insert(-1, default_url)
    url_box.grid(row=1, column=2, sticky="NW", pady=20, padx=20)

    # display zipcode label
    zipcode_label = tk.Label(in_stock_alert_frame, text="ZipCode:  ", font=('Railway', 16))
    zipcode_label.grid(row=2, column=1, sticky="NE", pady=20, padx=20)

    # display zipcode input box
    zipcode_box = tk.Entry(in_stock_alert_frame, font=('Railway', 18), width=22)
    zipcode_box.grid(row=2, column=2, sticky="NW", pady=20, padx=20)

    # display maxprice label
    maxprice_label = tk.Label(in_stock_alert_frame, text="MaxPrice:  ", font=('Railway', 16))
    maxprice_label.grid(row=3, column=1, sticky="NE", pady=20, padx=20)

    # display maxprice input box
    maxprice_box = tk.Entry(in_stock_alert_frame, font=('Railway', 18), width=22)
    maxprice_box.grid(row=3, column=2, sticky="NW", pady=20, padx=20)

    # display keyword label
    keyword_label = tk.Label(in_stock_alert_frame, text="Keyword:  ", font=('Railway', 16))
    keyword_label.grid(row=4, column=1, sticky="NE", pady=20, padx=20)

    # display phoneNumber input box
    keyword_box = tk.Entry(in_stock_alert_frame, font=('Railway', 18), width=22)
    keyword_box.grid(row=4, column=2, sticky="NW", pady=20, padx=20)

    # display phoneNumber label
    phoneNum_label = tk.Label(in_stock_alert_frame, text="PhoneNo:  ", font=('Railway', 16))
    phoneNum_label.grid(row=5, column=1, sticky="NE", pady=20, padx=20)

    # display phoneNumber input box
    phoneNum_box = tk.Entry(in_stock_alert_frame, font=('Railway', 18), width=22)
    phoneNum_box.grid(row=5, column=2, sticky="NW", pady=20, padx=20)

    start_text = tk.StringVar()
    # display start button
    button_start = tk.Button(in_stock_alert_frame, textvariable=start_text, font=('Railway', 16), height=3, width=14,
                             highlightbackground="#20bebe", fg="black",
                             command=lambda: [in_stock_alert_frame.grid_remove(),
                                              start_instock_alert(zipcode_box.get(), maxprice_box.get(),
                                                                  wd, phoneNum_box.get(), keyword_box.get(),
                                                                  url_box.get())])
    start_text.set("Start")
    button_start.grid(row=6, column=2, sticky="NW", pady=20, padx=20)
    back_button_pic = PhotoImage(file="pic/back.png").subsample(5, 5)
    label_back = Label(image=back_button_pic)
    label_back.image = back_button_pic  # keep a reference

    button_back = tk.Button(in_stock_alert_frame, highlightthickness=0, bd=0, borderwidth=0,
                            image=back_button_pic,
                            command=lambda: [in_stock_alert_frame.destroy(), back_main_frame()])
    button_back.grid(row=6, column=2, sticky="NE", pady=20, padx=20)


def start_instock_alert(zipcode, maxPrice, webdriver, phoneNum, keyword, item_url):
    alert_system_frame = tk.Frame(root)
    alert_system_frame.grid(row=1, column=1)
    searching_label = tk.Label(alert_system_frame, text="Searching....", font=('Railway', 30))
    searching_label.grid(row=1, column=2, sticky="NE", pady=5)
    time.sleep(3)
    alert_system = instock_alert.InStockAlert(zipcode, float(maxPrice), webdriver, str(phoneNum), keyword, item_url)
    alert_system.run()


# ---------------------------------------------------END In Stock Alert----------------------------------#


# ---------------------------------------------------Job Search--------------------------------- --------#
def search_job(button_1, button_2, button_3, button_4, button_5, button_6, display_job_frame):
    forget_main_frame(button_1, button_2, button_3, button_4, button_5, button_6, display_job_frame)
    default_url = "https://www.timesjobs.com/"

    for i in range(5):
        root.rowconfigure(i, weight=1)

    # display website url label
    url_label = tk.Label(root, text="URL:  ", font=('Railway', 16))
    url_label.grid(row=1, column=1, sticky="NE", pady=5)

    # display website url input box
    url_box = tk.Entry(root, font=('Railway', 18), width=22)
    url_box.insert(-1, default_url)
    url_box.grid(row=1, column=2, sticky="NW")

    # display category label
    category_label = tk.Label(root, text="Category:  ", font=('Railway', 16))
    category_label.grid(row=2, column=1, sticky="NE", pady=5)

    # display category input box
    category_box = tk.Entry(root, font=('Railway', 18), width=22)
    category_box.grid(row=2, column=2, sticky="NW")

    # display location label
    location_label = tk.Label(root, text="Location:  ", font=('Railway', 16))
    location_label.grid(row=3, column=1, sticky="NE", pady=5)

    # display location input box
    location_box = tk.Entry(root, font=('Railway', 18), width=22)
    location_box.grid(row=3, column=2, sticky="NW")

    search_text = tk.StringVar()
    # display search button
    button_search = tk.Button(root, textvariable=search_text, font=('Railway', 16), height=3, width=14,
                              highlightbackground="#20bebe", fg="black",
                              command=lambda: [url_label.grid_forget(), url_box.grid_forget(),
                                               category_label.grid_forget(), category_box.grid_forget(),
                                               button_search.grid_forget(), location_label.grid_forget(),
                                               location_box.grid_forget(), button_back.grid_remove(),
                                               display_job(url_box.get(), category_box.get(), location_box.get())])
    search_text.set("Search")
    button_search.grid(row=4, column=2, sticky="NW")

    back_button_pic = PhotoImage(file="pic/back.png").subsample(5, 5)
    label_back = Label(image=back_button_pic)
    label_back.image = back_button_pic  # keep a reference
    button_back = tk.Button(root, highlightthickness=0, bd=0, borderwidth=0,
                            image=back_button_pic,
                            command=lambda: [url_label.grid_remove(), url_box.grid_remove(),
                                             category_label.grid_remove(), category_box.grid_remove(),
                                             button_search.grid_remove(), location_label.grid_remove(),
                                             location_box.grid_remove(), button_back.grid_remove(), back_main_frame()])
    button_back.grid(row=4, column=2, sticky="NE")


def callback(url):
    webbrowser.open_new(url)


def display_job(url, category, location):
    ws = web_scraper.WebScraper(url, category, location)
    company_name, skills, job_link, years, locations = ws.run()
    display_job_frame = tk.Frame(root)
    display_job_frame.grid(row=1, column=1)

    S = tk.Scrollbar(display_job_frame)
    T = tk.Text(display_job_frame, height=40, width=80, font=("Railway", 16), bd=0, highlightthickness=0)
    hyperlink = tkHyperlinkManager.HyperlinkManager(T)
    S.pack(side=tk.RIGHT, fill=tk.Y)
    T.pack(side=tk.LEFT, fill=tk.Y)
    S.config(command=T.yview)
    T.config(yscrollcommand=S.set)

    for i in range(len(company_name)):
        full_text = ""
        full_text += "Company: "
        full_text += company_name[i]
        full_text += "\n"
        full_text += "Skills: "
        full_text += skills[i]
        full_text += "\n"
        full_text += "Experience: "
        full_text += years[i][0]
        full_text += "\n"
        full_text += "Location: "
        full_text += locations[i]
        full_text += "\n"
        T.insert(tk.END, full_text)
        T.insert(tk.END, "Job Details", hyperlink.add(lambda: callback(job_link[i])))
        T.insert(tk.END, "\n")

    back_button_pic = PhotoImage(file="pic/back.png").subsample(5, 5)
    label_back = Label(image=back_button_pic)
    label_back.image = back_button_pic  # keep a reference
    button_back = tk.Button(root, bd=0, highlightthickness=0, borderwidth=0,
                            image=back_button_pic,
                            command=lambda: [display_job_frame.grid_forget(),
                                             button_back.grid_remove(), back_main_frame()])
    button_back.grid(row=1, column=4)


# ---------------------------------------------------END Job Search-----------------------------------------#


# ---------------------------------------------------Price Tracker-----------------------------------------#
def show_price(item_title, index):
    price_track = price_tracker.PriceTracker(item_title)
    bestbuy, ebay = price_track.run()
    bestbuy_text = "BESTBUY: " + bestbuy[0] + ": " + bestbuy[1]
    eaby_text = "\nEABY:        " + ebay[0] + ": " + ebay[1]
    total_text = bestbuy_text + eaby_text

    bt = tk.Text(root, font=("Railway", 16), bd=0, highlightthickness=0)
    bt.insert(tk.END, total_text)
    if index == 0:
        bt.place(relx=0.3, rely=0.1, relheight=0.15, relwidth=0.7)
    elif index == 1:
        bt.place(relx=0.3, rely=0.25, relheight=0.15, relwidth=0.7)
    elif index == 2:
        bt.place(relx=0.3, rely=0.42, relheight=0.15, relwidth=0.7)
    elif index == 3:
        bt.place(relx=0.3, rely=0.6, relheight=0.15, relwidth=0.7)


def price_tracker_gui(button_1, button_2, button_3, button_4, button_5, button_6, display_job_frame):
    forget_main_frame(button_1, button_2, button_3, button_4, button_5, button_6, display_job_frame)
    for i in range(10):
        root.columnconfigure(i, weight=1)
        root.rowconfigure(i, weight=1)

    text_1 = tk.StringVar()
    text_1.set("Nikon Z5")
    button_tracker_1 = tk.Button(root, textvariable=text_1, font=('Railway', 18), height=3, width=17,
                                 highlightbackground="#20bebe",
                                 fg="black", command=lambda: show_price(text_1.get(), 0))
    button_tracker_1.grid(row=1, column=0)

    text_2 = tk.StringVar()
    text_2.set("Xbox Series S(512GB)")
    button_tracker_2 = tk.Button(root, textvariable=text_2, font=('Railway', 18), height=3, width=17,
                                 highlightbackground="#20bebe",
                                 fg="black", command=lambda: show_price(text_2.get(), 1))
    button_tracker_2.grid(row=2, column=0)

    text_3 = tk.StringVar()
    text_3.set("Ipad pro 11-inch")
    button_tracker_3 = tk.Button(root, textvariable=text_3, font=('Railway', 18), height=3, width=17,
                                 highlightbackground="#20bebe",
                                 fg="black", command=lambda: show_price(text_3.get(), 2))
    button_tracker_3.grid(row=3, column=0)

    text_4 = tk.StringVar()
    text_4.set("AirPods(3rd gen)")
    button_tracker_4 = tk.Button(root, textvariable=text_4, font=('Railway', 18), height=3, width=17,
                                 highlightbackground="#20bebe",
                                 fg="black", command=lambda: show_price(text_4.get(), 3))
    button_tracker_4.grid(row=4, column=0)


# ---------------------------------------------------END Price Tracker-----------------------------------------#

# --------------- Super Awesome Richard Dictionary Function ------------- #


def getWordOTD():
    now = datetime.now()
    today = datetime.strftime(now, "%Y-%m-%d")
    return word.getDailyWord(today)


def getLastWordOTD():
    now = datetime.now()
    yesterday = now - timedelta(1)
    yesterday = datetime.strftime(yesterday, "%Y-%m-%d")
    return word.getDailyWord(yesterday)


def definition(myWord):
    try:
        defin = word.getWord(myWord)
        return defin
    except InvalidWordError:
        return [myWord, "Invalid word.", ""]


def setCurrentWord(myWord, wordL):
    wordL.config(text=myWord)


def setDefinition(definition, meanM):
    if definition == "Invalid word.":
        meanM.config(text=definition)
    else:
        definition = "1. " + definition
        meanM.config(text=definition)


def setAltDefinition(myAlt, altM):
    if myAlt == "":
        altM.config(text="")
    else:
        myAlt = "2. " + myAlt
        altM.config(text=myAlt)


def setNote(myNote, noteM):
    if myNote == "":
        noteM.config(text="")
    else:
        myNote = "Fun Fact: " + myNote
        noteM.config(text=myNote)


def prevWordButton(wordL, defM, noteM, altM):
    wordInfo = dictionary.getLastWordOTD()
    setCurrentWord(wordInfo[0], wordL)
    setDefinition(wordInfo[1], defM)
    setNote(wordInfo[2], noteM)
    setAltDefinition(wordInfo[3], altM)


def setCurrentWordOTD(wordL, defM, noteM, altM):
    wordInfo = getWordOTD()
    setCurrentWord(wordInfo[0], wordL)
    setDefinition(wordInfo[1], defM)
    setNote(wordInfo[2], noteM)
    setAltDefinition(wordInfo[3], altM)


def defineButton(myWord, wordL, defM, noteM, altM):
    wordInfo = definition(myWord)
    setCurrentWord(wordInfo[0], wordL)
    setDefinition(wordInfo[1], defM)
    setNote("", noteM)
    setAltDefinition(wordInfo[2], altM)


def dictionary_gui(button_1, button_2, button_3, button_4, button_5, button_6, display_job_frame):
    forget_main_frame(button_1, button_2, button_3, button_4, button_5, button_6, display_job_frame)

    # set frame

    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    wordL = ttk.Label(mainframe, width=25, text="", font=('Railway', 36))
    wordL.grid(column=1, row=1, sticky=W)

    wordDefinition = Message(mainframe, width=800, text="", font=('Railway', 22))
    wordDefinition.grid(column=1, row=2, sticky=W)

    wordAlt = Message(mainframe, width=800, text="", font=('Railway', 22))
    wordAlt.grid(column=1, row=3, sticky=W)

    wordNote = Message(mainframe, width=800, text="", font=('Railway', 22))
    wordNote.grid(column=1, row=4, sticky=W)

    # configure buttons, creating a style for them
    wordBox = Text(mainframe, padx=0, pady=0, height=1, width=25, font=('Railway', 22), bg="white", borderwidth=2)
    wordBox.grid(column=1, row=6, sticky=W)
    wordBox.insert("1.0", "Search new word")

    lastWordOTD = ttk.Button(mainframe, text="Get Yesterday's Word of the Day",
                             command=lambda: prevWordButton(wordL, wordDefinition, wordNote, wordAlt))
    lastWordOTD.grid(column=1, row=8, sticky=W)

    button_define = ttk.Button(mainframe, text="Find Definition",
                               command=lambda: defineButton(wordBox.get("1.0", "end-1c"), wordL, wordDefinition,
                                                            wordNote, wordAlt))
    button_define.grid(column=1, row=7, sticky=W)

    style = ttk.Style()
    style.configure('TButton', font=('Railway', 22))

    # by default, the frame has the current word of the day

    setCurrentWordOTD(wordL, wordDefinition, wordNote, wordAlt)


# ----------- End Super Awesome Richard Dictionary Function -------------- #


# ------------------------------------------ MAIN PAGE AGAIN FOR BACK BUTTON-----------------------------------------#
def return_main(root):
    display_job_frame = tk.Frame(root)
    display_job_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    for i in range(4):
        root.columnconfigure(i, weight=1)
        root.rowconfigure(i, weight=1)

    text_1 = tk.StringVar()
    button_1 = tk.Button(root, textvariable=text_1, font=('Railway', 22), height=6, width=20, highlightbackground="red",
                         fg="white", command=lambda: download_article(button_1, button_2, button_3, button_4, button_5,
                                                                      button_6, display_job_frame))
    text_1.set("Article")
    button_1.grid(row=1, column=1)

    text_2 = tk.StringVar()
    button_2 = tk.Button(root, textvariable=text_2, font=('Railway', 22), height=6, width=20,
                         highlightbackground="purple",
                         fg="white", command=lambda: in_stock_alert(button_1, button_2, button_3, button_4, button_5,
                                                                    button_6, display_job_frame))
    text_2.set("In Stock Alert")
    button_2.grid(row=1, column=2)

    text_3 = tk.StringVar()
    button_3 = tk.Button(root, textvariable=text_3, font=('Railway', 22), height=6, width=20,
                         highlightbackground="blue",
                         fg="white", command=lambda: price_tracker_gui(button_1, button_2, button_3, button_4, button_5,
                                                                       button_6, display_job_frame))
    text_3.set("Price Tracker")
    button_3.grid(row=2, column=1)

    text_4 = tk.StringVar()
    button_4 = tk.Button(root, textvariable=text_4, font=('Railway', 22), height=6, width=20,
                         highlightbackground="orange",
                         fg="white", command=lambda: search_job(button_1, button_2, button_3, button_4, button_5,
                                                                button_6, display_job_frame))
    text_4.set("Search Job")
    button_4.grid(row=2, column=2)

    text_5 = tk.StringVar()
    button_5 = tk.Button(root, textvariable=text_5, font=('Railway', 22), height=6, width=20,
                         highlightbackground="green",
                         fg="white", command=lambda: dictionary_gui(button_1, button_2, button_3, button_4, button_5,
                                                                    button_6, display_job_frame))
    text_5.set("For Richard")
    button_5.grid(row=3, column=1)

    text_6 = tk.StringVar()
    button_6 = tk.Button(root, textvariable=text_6, font=('Railway', 22), height=6, width=20,
                         highlightbackground="Magenta",
                         fg="white")
    text_6.set("Leave Blank")
    button_6.grid(row=3, column=2)

    root.mainloop()


# ---------------------------------- END MAIN PAGE AGAIN FOR BACK BUTTON-----------------------------------------#


root = tk.Tk()
root.title("Web Scraper Tool Box")
root.geometry("800x600")

for i in range(4):
    root.columnconfigure(i, weight=1)
    root.rowconfigure(i, weight=1)

display_null = tk.Frame(root)

text_1 = tk.StringVar()
button_1 = tk.Button(root, textvariable=text_1, font=('Railway', 22), height=6, width=20, highlightbackground="red",
                     fg="white", command=lambda: download_article(button_1, button_2, button_3, button_4, button_5,
                                                                  button_6, display_null))
text_1.set("Article")
button_1.grid(row=1, column=1)

text_2 = tk.StringVar()
button_2 = tk.Button(root, textvariable=text_2, font=('Railway', 22), height=6, width=20, highlightbackground="purple",
                     fg="white", command=lambda: in_stock_alert(button_1, button_2, button_3, button_4, button_5,
                                                                button_6, display_null))
text_2.set("Amazon Price Alert")
button_2.grid(row=1, column=2)

text_3 = tk.StringVar()
button_3 = tk.Button(root, textvariable=text_3, font=('Railway', 22), height=6, width=20, highlightbackground="blue",
                     fg="white", command=lambda: price_tracker_gui(button_1, button_2, button_3, button_4, button_5,
                                                                   button_6, display_null))
text_3.set("Price Tracker")
button_3.grid(row=2, column=1)

text_4 = tk.StringVar()
button_4 = tk.Button(root, textvariable=text_4, font=('Railway', 22), height=6, width=20, highlightbackground="orange",
                     fg="white", command=lambda: search_job(button_1, button_2, button_3, button_4, button_5,
                                                            button_6, display_null))
text_4.set("Search Job")
button_4.grid(row=2, column=2)

text_5 = tk.StringVar()
button_5 = tk.Button(root, textvariable=text_5, font=('Railway', 22), height=6, width=20, highlightbackground="green",
                     fg="white", command=lambda: dictionary_gui(button_1, button_2, button_3, button_4, button_5,
                                                                button_6, display_null))
text_5.set("Online Dictionary")
button_5.grid(row=3, column=1)

text_6 = tk.StringVar()
button_6 = tk.Button(root, textvariable=text_6, font=('Railway', 22), height=6, width=20, highlightbackground="Magenta",
                     fg="white")
text_6.set("Leave Blank")
button_6.grid(row=3, column=2)

root.mainloop()
