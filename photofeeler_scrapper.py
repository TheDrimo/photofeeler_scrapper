# scrapper les données de photofeeler (provenant de mon compte)
# étape 1 : se connecter avec id et pw
# étape 2 : récupérer le lien vers toutes la page individuelle de toutes les photos
# ne pas oublier d'appuyer sur le bouton "show more" pour avoir toutes les photos
# étape 3 : récupérer les données de la photo en format json
# la récupération doit se faire en fonction de la structure html et non des titres de données
# car les catégories sont pas les mêmes en dating qu'en social
# et que les structures de données sont les mêmes pour chaque catégorie (smart, trust...)

import os
from dotenv import load_dotenv
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException



load_dotenv()  # Charge les variables d'environnement à partir du fichier .env

username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

print("initialisation du driver ...")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

print("chargement de la page de connexion ...")
driver.get('https://www.photofeeler.com/login')
WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.NAME, 'email')))

print("remplissage du formulaire de connexion ...")
username_input = driver.find_element(By.NAME, 'email')
password_input = driver.find_element(By.NAME, 'password')

username_input.send_keys(username)
password_input.send_keys(password)

password_input.send_keys(Keys.RETURN)

driver.get('https://www.photofeeler.com/my-tests#')

while True:  # Boucle pour cliquer tant que le bouton est présent
    try :
    	load_more_buttons = driver.find_elements(By.XPATH, "//div[contains(@class, 'btn btn-primary') and contains(text(), 'Load More')]")
    	load_more_buttons[0].click()
    	print("and one 'load more'")
    	time.sleep(10)
    except :
    	break


time.sleep(10)
page_html = driver.page_source

# Chemin du fichier où sauvegarder le HTML
file_path = 'photofeeler.html'  # Modifiez selon votre chemin

# Écrire le HTML dans un fichier
with open(file_path, 'w', encoding='utf-8') as file:
    file.write(page_html)

print("HTML saved to", file_path)

driver.quit()
