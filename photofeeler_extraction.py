from bs4 import BeautifulSoup
import json
import re


file_path = 'photofeeler.html'

with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()


def extract_data_from_block(html_block):
    soup = BeautifulSoup(html_block, 'html.parser')
    
    data = {
        "link": soup.a['href'],
        "photo": soup.find('img')['src'],
        "category": soup.find('div', class_='test-category').text.strip(),
        "votes": int(soup.find('div', class_='test-vote-count').contents[0].strip().split()[0]),
        "traits": {}
    }

    # Vérifier si la classe contient la chaîne de base
    traits = soup.find_all('div', class_=lambda value: value and "test-box-row test-rank-row clearfix" in value)

    for trait in traits:
        trait_name = trait.find('div', class_='test-trait-name').text.strip()
        trait_value = float(trait.find('div', class_='test-trait-value').text.strip())
        data["traits"][trait_name] = trait_value
    
    return data

def list_blocks_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    blocks = soup.find_all('div', class_='test-box col-md-3 col-sm-4 col-xs-6')
    
    results = []
    for block in blocks:
        block_html = str(block)  # Convert the block to a string to pass to extract_data_from_block
        extracted_data = extract_data_from_block(block_html)
        results.append(extracted_data)
    
    # Créer un dictionnaire global pour l'ensemble des résultats
    output_data = {
        "metadata": {
            "extraction_date": "2024-04-14",
            "total_entries": len(results)
        },
        "data": results
    }
    
    # Convertir le dictionnaire en chaîne JSON
    return json.dumps(output_data, indent=4)

#print(list_blocks_from_html(content))

#print(json.dumps(list_blocks_from_html(content)))

def save_data_to_json(data, filename):
    """Sauvegarde les données dans un fichier JSON.

    Args:
        data (list of dict): Données à sauvegarder.
        filename (str): Chemin du fichier où sauvegarder les données.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# Exemple d'utilisation
html_content = """<html>... Votre contenu HTML ...</html>"""
extracted_data = json.dumps(list_blocks_from_html(content))

# Spécifiez le chemin et le nom de votre fichier de sortie
output_filename = 'extracted_data.json'
save_data_to_json(extracted_data, output_filename)

print(f"Les données ont été sauvegardées dans le fichier {output_filename}.")