"""Fetch and save listing URLs for a given city."""

import datetime
import glob
import re
import sys
import time
from argparse import ArgumentParser
from os.path import basename

from bs4 import BeautifulSoup
from requests_html import HTMLSession
from tqdm import trange


def iterate_listings(url_file_time, url_file_city):
    urls = read_urls_from_file(url_file_time, url_file_city)

    total_time = 3600 - 0.65 * len(urls)
    time_per_iteration = total_time / len(urls)
    time_per_iteration = 0

    listings = []
    session = HTMLSession()

    for i in trange(len(urls), desc='iterating URLs'):
        page = session.get(urls[i])
        prerender_soup = BeautifulSoup(page.html.html, 'html.parser')

        listing_details = {}
        details = prerender_soup.find_all(['dd', 'dt'], class_=re.compile('details-grid__item-.*'))
        for j in trange(len(details), desc='iterating details'):
            if details[j]['class'] == ['details-grid__item-title']:
                listing_details[details[j].text] = details[j + 1].text.replace('\xa0', ' ')

        listing = {
            'Osoite': prerender_soup.find('meta', attrs={'property': 'og:street-address'})['content'],
            'Postinumero': prerender_soup.find('meta', attrs={'property': 'og:postal_code'})['content'],
            'Id': prerender_soup.find('meta', attrs={'name': 'SAC:card_ID'})['content'],
            'Latitude': prerender_soup.find('meta', attrs={'property': 'place:location:latitude'})['content'],
            'Longitude': prerender_soup.find('meta', attrs={'property': 'place:location:latitude'})['content'],
        }

        complete_listing = {**listing_details, **listing}

        listings.append(complete_listing)

        time.sleep(time_per_iteration)

    finish_time = str(datetime.datetime.now()).replace('-', '').replace(':', '').replace(' ', '_').split('.')[0]

    with open('output/{}_content_{}.html'.format(finish_time, url_file_city), 'w') as content_file:
        string = str(listings)
        string = string.replace("'", '"')
        content_file.write(string)
        print('Content file written with {} rows.'.format(str(len(listings))))
    write_log_file(url_file_city, len(listings), finish_time)


def read_urls_from_file(url_file_time, url_file_city):
    file_names = glob.glob('output/*.txt')
    if url_file_time == 'latest':
        print('Finding latest URL file for {} area'.format(str(url_file_city)))
        latest = ''
        for file_name in file_names:
            if file_name.split('.')[0].split('_')[-1] == url_file_city:
                if latest == '':
                    latest = file_name
                else:
                    if file_name > latest:
                        latest = file_name
        print('Latest file is {}'.format(str(latest)))
        with open(latest) as url_file:
            urls = url_file.read().splitlines()
        return urls
    print('Finding URL file for time {} for {} area'.format(str(url_file_time), str(url_file_city)))
    print('Not implemented yet. Exiting.')
    sys.exit()
    return []


def write_log_file(city, number_of_urls, finish_time):
    with open('output/history.log', 'a') as log_file:
        log_file.write('Wrote contents of {} URLs at {} for {} area.\n'.format(str(number_of_urls), finish_time, city))
    print('Log file written.')


def main():
    parser = ArgumentParser(prog=basename(__file__))
    parser.add_argument('--url_file_time', '-t', type=str, default='latest')
    parser.add_argument('--url_file_city', '-c', type=str, default='Helsinki')
    args = vars(parser.parse_args())

    iterate_listings(**args)


if __name__ == '__main__':
    main()
