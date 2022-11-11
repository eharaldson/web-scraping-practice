# Web scraping practice with Beautiful soup

## imdb.py
- Collects data on the actors/actresses of Pulp fiction and further goes into each persons imdb page to collect the movies they have done. All of this is collated into a dictionary with the structure:

```
actor_data = {
    'name': [],
    'link': [],
    'movies': [{'title': [], 'year': []}]
}
```

## zoopla.py
- Accesses the page of zoopla and collects important information on each house listed on the page in a function. The function returns the link to the next page aswell so that a series of pages can be scraped for house information.