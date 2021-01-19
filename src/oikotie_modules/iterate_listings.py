'''
Fetch and save listing URLs for a given city.
'''
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from tqdm import trange
from argparse import ArgumentParser
from os.path import basename
import glob
import sys
import datetime
import time


def iterate_listings(url_file_time, url_file_city):
    urls = read_urls_from_file(url_file_time, url_file_city)

    total_time = 3600 - 0.65 * len(urls)
    time_per_iteration = total_time / len(urls)

    listings = []
    session = HTMLSession()

    for i in trange(len(urls), desc='iterating URLs'):
        page = session.get(urls[i])
        prerender_soup = BeautifulSoup(page.html.html, 'html.parser')
        listing = str(prerender_soup.find_all(class_=["details-grid__item-title", "details-grid__item-value"]))
        listings.append(listing)
        time.sleep(time_per_iteration)

    finish_time = str(datetime.datetime.now()).replace('-', '').replace(':', '').replace(' ', '_').split('.')[0]
    
    content_file = open('output/' + finish_time + '_content_' + url_file_city + '.html', 'w')
    string = '\n'.join(listings)
    content_file.write(string)
    content_file.close()
    print("Content file written with {} rows.".format(str(len(listings))))
    write_log_file(url_file_city, len(listings), finish_time)


def read_urls_from_file(url_file_time, url_file_city):
    file_names = glob.glob('output/*.txt')
    if url_file_time == "latest":
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
        with open(latest) as f:
            urls = f.read().splitlines()
        return urls
    else:
        print('Finding URL file for time {} for {} area'.format(str(url_file_time), str(url_file_city)))
        print('Not implemented yet. Exiting.')
        sys.exit()
        return []


def write_log_file(city, number_of_urls, finish_time):
    log_file = open('output/history.log', 'a')
    log_file.write('Wrote contents of {} URLs at {} for {} area.\n'.format(str(number_of_urls), finish_time, city))
    log_file.close()
    print("Log file written.")


def main():
    parser = ArgumentParser(prog=basename(__file__))
    parser.add_argument('--url_file_time', '-t', type=str, default="latest")
    parser.add_argument('--url_file_city', '-c', type=str, default="Helsinki")
    args = vars(parser.parse_args())

    iterate_listings(**args)


if __name__ == "__main__":
    main()
