import requests
from bs4 import BeautifulSoup

r = requests.get('https://www.imdb.com/title/tt0110912/?ref_=nv_sr_srsg_0')
html = r.text
soup = BeautifulSoup(html, 'html.parser')

actors = soup.find_all(name='a', attrs={'data-testid': "title-cast-item__actor", 'class': "sc-bfec09a1-1 gfeYgX"})

links = ['https://www.imdb.com' + feature.attrs['href'] for feature in actors]
names = [feature.text for feature in actors]

actor_data = {'name': names, 'link': links}

movies_ls = []

# Loop through links to access movie/year data
for link in links:
    r = requests.get(link)
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')

    film_section = soup.find(name='div', attrs={'class': 'filmo-category-section'})
    years = film_section.find_all(name='span', attrs={'class': 'year_column'})
    year_ls = [feature.text[-5:-1] for feature in years]

    movies = film_section.find_all(name='b')
    movie_names = [feature.text for feature in movies]

    movies_ls.append({'title': movie_names, 'year': year_ls})

actor_data['movies'] = movies_ls

print(actor_data)
