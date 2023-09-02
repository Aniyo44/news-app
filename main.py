from tkinter import *
from tkinter import ttk
import requests
from PIL import Image, ImageTk
import webbrowser

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def scrape_data():

    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    browser = webdriver.Chrome(options=options)
    browser.get("https://www.mosaiquefm.net/ar/actualites/%D8%AA%D9%88%D9%86%D8%B3-%D8%A3%D8%AE%D8%A8%D8%A7%D8%B1-%D9%88%D8%B7%D9%86%D9%8A%D8%A9/1")
    containers = browser.find_elements(By.XPATH, '//div[@class="col-xl-3 col-md-4 col-6 item"]')

    titles=[]
    images=[]
    links=[]
    dates=[]

    for container in containers:
      title= container.find_element(By.XPATH, './/div[@class="desc"]/h3/a').text
      link= container.find_element(By.XPATH,'.//div[@class="desc"]/h3/a').get_attribute("href")
      image = container.find_element(By.XPATH,'.//figure//img').get_attribute('srcset').split(',')[0].strip().split(' ')[0]
      date=container.find_element(By.XPATH, './/div[@class="desc"]//div[@class="dateShareBar"]//time').text
      dates.append(date)
      titles.append(title)
      images.append(image)
      links.append(link)
    return titles, images, links,dates

root = Tk()
root.title("News App")
root.config(bg='#333')

root.geometry("800x300+100+100")


titles, images, links, dates = scrape_data()
current_index = 0

def update_image():
    global current_index
    global titles, images, links, dates

    title_label.config(text=titles[current_index])
    date_label.config(text=dates[current_index])
    title_label.bind("<Button-1>", lambda e: webbrowser.open(links[current_index]))
    image = Image.open(requests.get(images[current_index], stream=True).raw)
    # image = image.resize((500, 500), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(image)
    image_label.config(image=image)
    image_label.image = image

def prev_image():
    global current_index
    current_index -= 1
    if current_index < 0:
        current_index = len(titles) - 1
    update_image()

def next_image():
    global current_index
    current_index += 1
    if current_index >= len(titles):
        current_index = 0
    update_image()
old_arrow= Image.open("arrow-left.png")
resized= old_arrow.resize((100, 100), Image.ANTIALIAS)
left_arrow= ImageTk.PhotoImage(resized)
old_arrow2= Image.open("arrow-right.png")
resized= old_arrow2.resize((100, 100), Image.ANTIALIAS)
right_arrow= ImageTk.PhotoImage(resized)


title_label = Label(root, text=titles[0], font=("TkDefaultFont", 24), bg='#333')
title_label.config(fg='#E927F9')
title_label.pack(side="top")

date_label = Label(root, text=dates[0], font=("TkDefaultFont", 16),  bg='#333')
date_label.config(fg='#F9B327')
date_label.pack(side="top")

image_label = Label(root)
image_label.pack()



prev_button = Button(root, image=left_arrow, command=prev_image )
prev_button.place(relx=0.1, rely=0.5, anchor='center')
next_button = Button(root, image=right_arrow, command=next_image)
next_button.place(relx=0.9, rely=0.5, anchor='center')


update_image()
root.mainloop()


