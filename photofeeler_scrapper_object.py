"""
objet : photofeeler_scrapper
methodes :
- connexion avec mdp et id
- chargement de toute la page (en appuyant sur le bouton "load more")
- lister toutes les liens vers les pages individuelles des photos
- changer de page
- récupérer les données de la page si on est sur une page de photo
"""

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

class PhotoFeelerScraper:
    def __init__(self):
        load_dotenv()  # Charge les variables d'environnement à partir du fichier .env
        self.username = os.getenv('USERNAME')
        self.password = os.getenv('PASSWORD')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.base_url = 'https://www.photofeeler.com'

    def login(self):
        print("Chargement de la page de connexion...")
        self.driver.get(f'{self.base_url}/login')
        WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.NAME, 'email')))
        
        print("Remplissage du formulaire de connexion...")
        username_input = self.driver.find_element(By.NAME, 'email')
        password_input = self.driver.find_element(By.NAME, 'password')
        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.RETURN)

    def load_full_page(self):
        print("Chargement complet de la page...")
        self.driver.get(f'{self.base_url}/my-tests#')
        while True:
            try:
                load_more_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'btn btn-primary') and contains(text(), 'Load More')]"))
                )
                load_more_button.click()
                print("Un bouton 'Load More', click")
                time.sleep(2)
            except TimeoutException:
                print("Aucun autre bouton 'Load More' à cliquer.")
                break

    def list_photo_links(self):
        print("Listage de tous les liens vers les pages des photos...")
        selector = ".test-box.col-md-3.col-sm-4.col-xs-6 a.unstyled"
        links = self.driver.find_elements(By.CSS_SELECTOR, selector)
        return [link.get_attribute('href') for link in links]

    def scrape_photo_page_result(self, url):
	    #print(f"Navigation vers {url}...")
	    self.driver.get(url+ "/results")
	    time.sleep(1)
	    #print("Récupération des données de la page photo...")

	    # Extraction du nombre de votes
	    votes_element = self.driver.find_element(By.CSS_SELECTOR, ".test-info-box.vote-count .info-box-value")
	    votes = votes_element.text.strip()  # Enlève les espaces superflus

	    # Extraction de la qualité de l'échantillon
	    quality_element = self.driver.find_element(By.CSS_SELECTOR, ".test-info-box.sample-size-description .quality-value-label")
	    quality = quality_element.text.strip()

		# Extraction de la catégorie de l'échantillon
	    category_element = self.driver.find_element(By.CSS_SELECTOR, ".category-bar")
	    category_type = category_element.text.strip()  # Enlève les espaces superflus

	    # les photos business et social n'ont pas de contexte sur les voters ou le sujet
	    try:	
		    # Extraction du context (type de voters et infos sur le sujet)
		    context_element = self.driver.find_element(By.CSS_SELECTOR, ".context-demo-box")
		    context_element = context_element.text.strip().split()
		    voters_type = context_element[-1]
		    subject_info = " ".join(context_element[2:5])
	    except:
		    voters_type = "none"
		    subject_info = "none"

	    #print("Récupération des données des boîtes de score...")
		# Sélectionner toutes les boîtes de score
	    score_boxes = self.driver.find_elements(By.CSS_SELECTOR, ".score-boxes .score-box")
	    scores_data = {}
	    for box in score_boxes:
		    # Récupérer le nom du trait
		    trait_name = box.find_element(By.CSS_SELECTOR, ".trait-name").text.strip()
		    # Récupérer la valeur numérique du trait
		    trait_value = box.find_element(By.CSS_SELECTOR, ".trait-value").text.strip()
		    # Ajouter les données au dictionnaire
		    scores_data[trait_name] = trait_value

		# Retourner les données extraites
	    return {
	    	'categorie': category_type,
			'votes': votes,
			'quality': quality,
			'voters_type': voters_type,
			'subject_info': subject_info,
			'scores_data':scores_data
		}

    def scrape_photo_page_data(self, url):
	    #new_url = url.replace('/results', '/data')
	    new_url = url + "/data"
	    #print(f"Navigation vers {new_url}...")
	    self.driver.get(new_url)
	    time.sleep(1)

	    #print("Récupération des données des boîtes de score...")
    
	    # Sélectionner toutes les boîtes de score
	    score_boxes = self.driver.find_elements(By.CSS_SELECTOR, ".score-box")
	    
	    results = {}

	    for box in score_boxes:
	        # Récupérer le nom du critère
	        trait_name = box.find_element(By.CSS_SELECTOR, ".trait-name").text.strip()
	        results[trait_name] = {}
	        
	        # Récupérer tous les barres de scores pour chaque catégorie
	        score_bars = box.find_elements(By.CSS_SELECTOR, ".score-count-bar")
	        for bar in score_bars:
	            # Description de la catégorie (No, Somewhat, Yes, Very)
	            description = bar.find_element(By.CSS_SELECTOR, ".score-description").text.strip().split()[2]
	            # Compte des votes pour la catégorie
	            vote_count = bar.find_element(By.CSS_SELECTOR, ".score-vote-count-value").text.strip()
	            results[trait_name][description] = vote_count

	    return results

    def main_page(self):
		# Retour à la page principale (optionnel selon le besoin de navigation)
	    self.driver.get(f'{self.base_url}/my-tests#')

    def save_html(self, file_path='photofeeler.html'):
        page_html = self.driver.page_source
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(page_html)
        #print(f"HTML saved to {file_path}")

    def close(self):
        self.driver.quit()


if __name__ == "__main__":
	scraper = PhotoFeelerScraper()
	scraper.login()
	scraper.load_full_page()
	scraper.save_html()
	links = scraper.list_photo_links()
	
	photo_data_result = scraper.scrape_photo_page_result(links[0])
	photo_data_data = scraper.scrape_photo_page_data(links[0])

	print("lien :", links[0])
	print("result", photo_data_result)
	print("data", photo_data_data)
	scraper.close()