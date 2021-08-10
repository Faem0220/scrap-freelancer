from bs4 import BeautifulSoup 
import requests
from datetime import date 
import json 

date = date.today().isoformat()
keywords = ['python','javascript']
pages = 2
ranking_keys = []

for key in keywords:
    page = 1
    jobs_list = []
    
    while page < pages:
        # Se extrae el html
        url = f'https://www.freelancer.com/jobs/{key}/{page}/?results=100'
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'lxml')
       # Se extrae la cantidad de trabajos y con esta la cantidad de páginas para el while
        jobs_amount = soup.find('div',class_='ProjectSearch-header-info').span.text.replace(',','')
        pages = int(jobs_amount.replace(',','')) // 100
        page += 1
        # Se seleccionan las cards de trabajos
        jobs = soup.find('div', class_= 'JobSearchCard-list')
        cards = jobs.find_all('div', class_='JobSearchCard-item')
        
        for card in cards:
            # Se extrae la información de cada card
            title = card.find('a', class_='JobSearchCard-primary-heading-link').text.strip()
            url = f'https://www.freelancer.com'+card.find('a')['href']
            pub_date = card.find('span', class_='JobSearchCard-primary-heading-days').text
            description = card.find('p', class_='JobSearchCard-primary-description').text.strip()
            payment_bids = card.find('div', class_='JobSearchCard-secondary').text.split()
            # Se filtran los valores inválidos
            if payment_bids[0].startswith('$'):
                payment = int(payment_bids[0].replace(',','').replace('$',''))
                bids = int(payment_bids[-4])
                # Se crea el diccionario con los valores extraidos
                Job = dict(Title=title,
                            Url=url,
                            Pub_date=pub_date,
                            Description=description,
                            Payment=payment,
                            Bids=bids)
                # Se agrega el diccionario a la lista
                jobs_list.append(Job)
                print(title)
    
    # Al cambiar de keyword se guarda la lista de diccionarios en archivo json            
    sorted_jobs_list = sorted(jobs_list, key=lambda k: k['Payment'],reverse=True)
    sorted_list = open(f'listas_freelancer/Trabajos en {key}: {date}.txt','w')
    json.dump(sorted_jobs_list, sorted_list)
    # Se crea el diccionario con la key y cantidad
    Key = dict(Name=key,
               Amount=int(jobs_amount))
    ranking_keys.append(Key)
# Se crea una lista con el ranking de keys
sorted_keys_list = sorted(ranking_keys, key=lambda k: k['Amount'],reverse=True)
ranking_list = open(f'listas_freelancer/Ranking Keys: {date}.txt','w')
json.dump(sorted_keys_list, ranking_list)
 