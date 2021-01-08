from bs4 import BeautifulSoup
from requests_html import HTMLSession

base_url = "https://asunnot.oikotie.fi/myytavat-asunnot?locations=%5B%5B64,6,%22Helsinki%22%5D%5D&cardType=100&pagination="

def main():
    urls = get_urls()
    f = open('urls.txt', 'w')
    string = '\n'.join(urls)
    f.write(string)
    f.close()
    print("Wrote file with " + str(len(urls)) + " rows.")

def get_urls():
    urls = []
    session = HTMLSession()
    number_of_pages = get_number_of_pages()

    for i in range(1, number_of_pages + 1):
        page = session.get(base_url + str(i))
        page.html.render()
        urls_from_cards = get_urls_from_cards(page)
        for url in urls_from_cards:
            urls.append(url)
        print("Page: " + str(i) + ", Total number of urls: " + str(len(urls)))
    
    return urls

def get_number_of_pages():
    session = HTMLSession()
    first_page = session.get(base_url + "1")
    first_page.html.render()
    first_page_soup = BeautifulSoup(first_page.html.html, 'html.parser')
    first_page_results = first_page_soup.find_all("span", class_="ng-binding")
    number_of_pages = int(first_page_results[6].text.split('/')[1])
    print("Pages: " + str(number_of_pages))
    return number_of_pages

def get_urls_from_cards(page):
    urls_from_cards = []
    soup = BeautifulSoup(page.html.html, 'html.parser')
    results = soup.find_all('a', class_='ot-card')
    for result in results:
        urls_from_cards.append(result['href'])
    return urls_from_cards



main()