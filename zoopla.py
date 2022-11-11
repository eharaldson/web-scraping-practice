import requests
from bs4 import BeautifulSoup

def scrape_homes(link):

    r = requests.get(link)
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')

    houses = soup.find(name='div', attrs={'data-testid': "regular-listings"})

    prices = houses.find_all(name='p', attrs={'data-testid': 'listing-price', 'class': "c-bTssUX"})
    price_ls = [feature.text for feature in prices]

    address = houses.find_all(name='h3', attrs={'class': "c-eFZDwI"})
    address_ls = [feature.text for feature in address]

    list_date = houses.find_all(name='li', attrs={'class': "c-eUGvCx"})
    list_date_ls = [feature.text[10:] for feature in list_date]

    bedroom_ls = []
    bathroom_ls = []
    livingroom_ls = []

    for house in houses:

        stats = house.find_all(name='span', attrs={'class': "c-PJLV"})
        stats_ls = [feature.text for feature in stats]
        bedroom_ls.append(int(stats_ls[0]))

        if len(stats_ls) >= 2:
            bathroom_ls.append(int(stats_ls[1]))
            if len(stats_ls) == 3:
                livingroom_ls.append(int(stats_ls[2]))
            else:
                livingroom_ls.append(0)
        else:
            bathroom_ls.append(0)
            livingroom_ls.append(0)

    house_data = {'price': price_ls, 'address': address_ls, 'date_listed': list_date_ls, 'bedrooms': bedroom_ls, 'bathrooms': bathroom_ls, 'livingrooms': livingroom_ls}

    next_link = 'https://www.zoopla.co.uk' + soup.find(name='li', attrs={'class': 'css-qhg1xn-PaginationItemPreviousAndNext-PaginationItemNext eaoxhri2'}).find(name='a').attrs['href']
    
    return house_data, next_link

main_link = 'https://www.zoopla.co.uk/new-homes/property/london/?q=London&results_sort=newest_listings&search_source=new-homes&page_size=25&pn=1&view_type=list'

house_data, next_link = scrape_homes(main_link)
all_house_data = [house_data]

for _ in range(4):

    house_data, next_link = scrape_homes(next_link)
    all_house_data.append(house_data)

print(all_house_data)