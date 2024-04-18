import sqlite3
from photofeeler_scrapper_object import *

class database_photofeeler:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.initialize_db()

    def data_harvesting(self):
        scraper = PhotoFeelerScraper()
        scraper.login()
        scraper.load_full_page()
        links = scraper.list_photo_links()
        print("{} liens récupérés".format(len(links)))
        links_not_working = []
        
        photo_counter = 0
        for link in links:
            #scraper.save_html() #en cas de souci c'est utile de voir la page où ça bloque
            try :
                photo_data_result = scraper.scrape_photo_page_result(link)
                photo_data_data = scraper.scrape_photo_page_data(link)
                self.insert_photo_data(link, photo_data_result, photo_data_data)
                #scraper.main_page()
                photo_counter += 1
            except :
                links_not_working.append(link)

        print("{} photos scrapés".format(photo_counter))
        if len(links_not_working) > 0:
            print("liste des liens manquants :")
            for link in links_not_working:
                print(link)
        scraper.close()

    def initialize_db(self):
        cursor = self.conn.cursor()
        
        # Créer ou mettre à jour la table Photos
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Photos (
            photo_id TEXT PRIMARY KEY,
            categorie TEXT,
            votes TEXT,
            quality TEXT,
            voters_type TEXT,
            subject_info TEXT
        )
        ''')

        # Créer ou mettre à jour la table Scores
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Scores (
            score_id INTEGER PRIMARY KEY AUTOINCREMENT,
            photo_id INTEGER,
            critere TEXT,
            score_value TEXT,
            FOREIGN KEY (photo_id) REFERENCES Photos (photo_id)
        )
        ''')

        # Créer ou mettre à jour la table Votes
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Votes (
            vote_id INTEGER PRIMARY KEY AUTOINCREMENT,
            score_id INTEGER,
            no INTEGER,
            somewhat INTEGER,
            yes INTEGER,
            very INTEGER,
            FOREIGN KEY (score_id) REFERENCES Scores (score_id)
        )
        ''')

        self.conn.commit()

    def insert_photo_data(self, photo_id, results, vote_data):
        general_data, scores_data = self.split_results_data(results)

        cursor = self.conn.cursor()
        
        # Insérer les données générales dans Photos
        cursor.execute('''
        INSERT INTO Photos (photo_id,categorie,  votes, quality, voters_type, subject_info)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(photo_id) DO UPDATE SET
        votes=excluded.votes, quality=excluded.quality
        ''', (photo_id, 
              general_data['categorie'], 
              general_data['votes'], 
              general_data['quality'], 
              general_data['voters_type'], 
              general_data['subject_info']))

        # Insérer les scores et adapter les insertions pour Votes
        for critere, score in scores_data.items():
            cursor.execute('''
            INSERT INTO Scores (photo_id, critere, score_value)
            VALUES (?, ?, ?)
            ''', (photo_id, critere, score))
            score_id = cursor.lastrowid
            
            # Insertion adaptée pour la nouvelle structure de Votes
            cursor.execute('''
            INSERT INTO Votes (score_id, no, somewhat, yes, very)
            VALUES (?, ?, ?, ?, ?)
            ''', (score_id, 
                  vote_data[critere]['NO'], 
                  vote_data[critere]['SOMEWHAT'], 
                  vote_data[critere]['YES'], 
                  vote_data[critere]['VERY']))

        self.conn.commit()

    def close(self):
        self.conn.close()

    def split_results_data(self, results):
        general_keys = ['categorie', 'votes', 'quality', 'voters_type', 'subject_info']
        score_keys = results['scores_data'].keys()

        general_data = {key: results[key] for key in general_keys}
        scores_data = {key: results['scores_data'][key] for key in score_keys if key in results['scores_data']}

        return general_data, scores_data



lien_photo = "https://www.photofeeler.com/my-tests#view/tsnuo17esy2o926v"
results = {'categorie': 'DATING',
           'votes': '10', 
           'quality': 'ROUGH', 
           'voters_type': 'ALL', 
           'subject_info': '27 / MALE', 
           'scores_data': {'Smart': '6.7', 'Trustworthy': '5.0', 'Attractive': '5.7'}}
data = {'Smart': {'NO': '1', 'SOMEWHAT': '5', 'YES': '4', 'VERY': '0'}, 
        'Trustworthy': {'NO': '3', 'SOMEWHAT': '6', 'YES': '1', 'VERY': '0'}, 
        'Attractive': {'NO': '2', 'SOMEWHAT': '7', 'YES': '1', 'VERY': '0'}}


if __name__ == "__main__":
    db = database_photofeeler('dynamic_photofeeler.db')
    db.data_harvesting()
    db.close()


