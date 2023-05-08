from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv
load_dotenv()

# -----------------------------------
BASE_URL = str(os.getenv('URL'))
use_saved_page = False
# ------------------------------------

def get_scrape_results(query, home_page):
    if home_page:
        URL = BASE_URL
    else:
        URL = BASE_URL + f"/video/search?search={(query).replace(' ', '+')}"

    response_html = ''

    if not use_saved_page:
        print(f'Requesting {URL}')
        response_html = requests.get(URL).text
        with open('response_html.html', 'w', encoding='utf-8') as file_response_html:
            file_response_html.write(response_html)
    else:
        with open('response_html.html', 'r', encoding='utf-8') as file_response_html:
            response_html = file_response_html.read()

    if not home_page:
        soup = BeautifulSoup(response_html, features='html.parser').find_all(
            'ul', attrs={"id": "videoSearchResult"})[0]
    else:
        soup = BeautifulSoup(response_html, features='html.parser').find_all(
            'ul', attrs={"id": "singleFeedSection"})[0]

    anchor_tags = soup.find_all('a', href=True)

    data = []
    hrefs = []
    for anchor_tag in anchor_tags:
        try:
            if '/view_video.php?viewkey=' in anchor_tag.attrs['href']:
                url = BASE_URL + anchor_tag.attrs['href']
                title = anchor_tag.attrs['title']
                div_that_has_length = anchor_tag.find(
                    'div', {'class': 'marker-overlays js-noFade'})
                var_that_has_length = div_that_has_length.find('var')
                if url not in hrefs:

                    data.append({
                        'title': title,
                        'url': url,
                        'length': var_that_has_length.text
                    })
                hrefs.append(url)
        except Exception as e:
            pass


    if not home_page:
        videos_details = soup.find_all('div', {
            'class': 'videoDetailsBlock'
        })
    else:
        videos_details = soup.find_all('div', {
            'class': 'videoDetailBlock'
        })

    if (len(data) == len(videos_details)):
        print(f'Showing {len(videos_details)} Results:')
        for index, video_detail in enumerate(videos_details):
            # Scrapping Views
            try:
                if not home_page:
                    views = video_detail.find('div').find(
                        'span', {'class': 'views'}).find('var').text
                else:
                    views = video_detail.find(
                        'span', {'class': 'views'}).find('var').text
            except:
                views = '[Unable to Fetch]'

            # Scapping Date Added
            try:
                date_added = video_detail.find('var', {'class': 'added'}).text
            except:
                date_added = '[Unable to Fetch]'

            # Scapping Rating
            try:
                if not home_page:
                    rating = video_detail.find('div').find(
                        'div', {'class': 'rating-container neutral'}).find('div', {'class': 'value'}).text
                else:
                    rating = video_detail.find(
                        'div', {'class': 'rating-container neutral'}).find('div', {'class': 'value'}).text
            except:
                rating = '[Unable to Fetch]'

            data[index].update({
                'views': views,
                'date_added': date_added,
                'rating': rating
            })
    else:
        print('Unable to fetch Video Details.')
        print(f'Scraped Videos: {len(data)}')
        print(f'Scraped Video Details: {len(videos_details)}')
        print(f'Showing {len(data)} Results:')
        
    return data
