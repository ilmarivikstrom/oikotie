'''
Fetch and save listing URLs for a given city.
'''

import datetime
import sys
from argparse import ArgumentParser
from os.path import basename

from bs4 import BeautifulSoup
from requests_html import HTMLSession
from tqdm import trange


def save_oikotie_urls(location_string):
    city = 'Unknown'
    if len(location_string.split('%22')) == 3:
        city = location_string.split('%22')[1]

    base_url = 'https://asunnot.oikotie.fi/myytavat-asunnot?locations={}&cardType=100&pagination='.format(location_string)
    urls = get_urls(base_url)

    finish_time = str(datetime.datetime.now()).replace('-', '').replace(':', '').replace(' ', '_').split('.')[0]

    write_url_file(urls, city, finish_time)
    write_log_file(city, len(urls), finish_time)


def write_url_file(urls, city, finish_time):
    with open('output/{}_urls_{}.txt'.format(finish_time, city), 'w') as url_file:
        string = '\n'.join(urls)
        url_file.write(string)
        print('URL file written.')


def write_log_file(city, number_of_urls, finish_time):
    with open('output/history.log', 'a') as log_file:
        log_file.write('Wrote {} URLs at {} for {} area.\n'.format(str(number_of_urls), finish_time, city))
        print('Log file written.')


def get_urls(base_url):
    urls = []
    session = HTMLSession()
    number_of_pages = get_number_of_pages(base_url)

    for i in trange(1, number_of_pages + 1):
        page = session.get(base_url + str(i))
        page.html.render()
        urls_from_cards = get_urls_from_cards(page)
        for url in urls_from_cards:
            urls.append(url)
    return urls


def get_number_of_pages(base_url):
    try:
        session = HTMLSession()
        first_page = session.get('{}1'.format(base_url))
        first_page.html.render()
        first_page_soup = BeautifulSoup(first_page.html.html, 'html.parser')
        first_page_results = first_page_soup.find_all('span', class_='ng-binding')
        number_of_pages = int(first_page_results[6].text.split('/')[1])
        print('Pages: {}'.format(str(number_of_pages)))
        return number_of_pages
    except IndexError:
        print('Error when fetching number of pages for location. Check that your location string argument is valid.')
        sys.exit()


def get_urls_from_cards(page):
    urls_from_cards = []
    soup = BeautifulSoup(page.html.html, 'html.parser')
    results = soup.find_all('a', class_='ot-card')
    for result in results:
        urls_from_cards.append(result['href'])
    return urls_from_cards


def main():
    parser = ArgumentParser(prog=basename(__file__))
    parser.add_argument('--location_string', '-l', type=str, default='%5B%5B64,6,%22Helsinki%22%5D%5D')
    args = vars(parser.parse_args())

    save_oikotie_urls(**args)


if __name__ == '__main__':
    main()
