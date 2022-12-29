import tkinter as tk
import pickle
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
import time
import os
from datetime import datetime

codes=dict()
codesList = pickle.load(open("codes.pkl", "rb"))

for code, quantity in codesList.items():
        codes[code]=quantity

root = tk.Tk()
root.title("Gestione codici")
root.geometry("800x600")

def on_add_clicked():
    code = entry_code.get()
    quantity = float(entry_quantity.get())
    codes[code] = quantity
    pickle.dump(codes, open("codes.pkl", "wb")) 
    update_codes_text()

def on_remove_clicked():
    code = entry_code.get()

    if code in codes:
        del codes[code]
        pickle.dump(codes, open("codes.pkl", "wb")) 
        update_codes_text()
    else:
        label.config(text="Il codice inserito non esiste nell'elenco!")


def update_codes_text():
    text.delete("1.0", tk.END)
    codesListupdate = pickle.load(open("codes.pkl", "rb"))

    for code, quantity in codesListupdate.items():
        text.insert(tk.END, f"{code}: {quantity}\n")

def start_scraping(codice, quantita):
  simbolo= codice
  qty=quantita
  data=datetime.now()

  website='https://www.binance.com/it/markets'

  s = Service(os.path.join(os.getcwd(), "chromedriver"))
  driver = webdriver.Chrome(service=s)
  driver.set_window_position(-2000, 0)
  driver.get(website)

  barraRicerca=driver.find_element(By.XPATH, "/html/body/div[1]/div/div/main/div/div[2]/div/div/div[1]/div/div/div[2]/div/div/input")
  barraRicerca.send_keys(simbolo, Keys.RETURN)  
  time.sleep(1)

  try: 
      nome = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/main/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div[1]/div/a/div[3]/div").text
  except NoSuchElementException:
      nome = "No nome (errore)"

  try: 
      prezzo = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/main/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div[1]/div/div[1]/div").text
  except NoSuchElementException:
      prezzo = "0€"

  driver.quit()
  prezzotemp = prezzo.replace("€", "")
  prezzo2= float(prezzotemp.replace(",", ""))

  df = pd.read_excel('prezziCrypto.xlsx')
  new_row = [simbolo, nome, prezzo, qty, prezzo2*qty, data]
  new_df = pd.DataFrame([new_row], columns=df.columns)
  df = pd.concat([df, new_df])
  df.to_excel('prezziCrypto.xlsx', index=False)
      
def start_excel():
    for key, value in codes.items():
        print(f'{key},{value}')
        start_scraping(key, value)

    text.delete("1.0", tk.END)
    text.insert(tk.END, "File aggiornato")    


code_label = tk.Label(root, text="Inserire simbolo crypto (es.btc):", font=('Arial', '10', 'bold'))
code_label.pack(side=tk.TOP, pady=5)
entry_code = tk.Entry(root)
entry_code.pack()

qty_label = tk.Label(root, text="Inserire quantità:", font=('Arial', '10', 'bold'))
qty_label.pack(side=tk.TOP, pady=5)
entry_quantity = tk.Entry(root)
entry_quantity.pack()

add_button = tk.Button(root, text="Aggiungi", command=on_add_clicked)
add_button.pack()

remove_button = tk.Button(root, text="Rimuovi", command=on_remove_clicked)
remove_button.pack()

text = tk.Text(root)
text.pack()

update_codes_text()

add_button = tk.Button(root, text="Crea file Excel", command=start_excel)
add_button.pack()

label = tk.Label(root)
label.pack()

root.mainloop()