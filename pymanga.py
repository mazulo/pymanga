import argparse
import urllib.request
import time

from bs4 import BeautifulSoup

base_url = 'http://mangaop.info/capitulos/{}#1'
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:42.0) Gecko/20100101 \
Firefox/42.0'
HOST = 'mangas2014.centraldemangas.com.br'
ACCEPT = 'image/png,image/*;q=0.8,*/*;q=0.5'
ACCEPT_LANGUAGE = 'pt-BR,en;q=0.5'
REFERER = 'http://mangaop.info/capitulos/747'
headers = {
    'User-Agent': USER_AGENT,
    'Host': HOST,
    'Accept': ACCEPT,
    'Accept-Language': ACCEPT_LANGUAGE,
    'Referer': REFERER
}


def download_chapter(chapter):
    url = base_url.format(chapter)
    print(url)
    req = urllib.request.Request(url)
    content = urllib.request.urlopen(req).read()

    soup = BeautifulSoup(content, 'html.parser')
    words = soup.findAll('script')[16].string.split()

    manga_url = ''
    for word in words:
        if 'http' in word:
            manga_url = word
            break
    manga_url = manga_url.replace('"', '')
    number_img = int(soup.find('select', id='capPages').text.split()[-1:][0])

    print('Número de imagens:  ', number_img)

    final = ''
    for i in range(1, number_img+1):
        if i in range(1, 10):
            final = '0'+str(i)
            url = manga_url+'-{}.jpg'.format(final)
            filename = 'capitulo-{}.jpg'.format(final)
        else:
            url = manga_url+'-{}.jpg'.format(i)
            filename = 'capitulo-{}.jpg'.format(i)
        print('Filename: ', filename)
        print('URL: ', url)
        time.sleep(5)
        req = urllib.request.Request(url, headers=headers)
        with open(filename, 'wb') as f:
            content = urllib.request.urlopen(req).read()
            f.write(content)

    print(manga_url, number_img)
    return


def main():
    parser = argparse.ArgumentParser(
        prog='PyManga',
        description='An easily way to download your favorite mangas'
    )
    parser.add_argument(
        '-m', '--manga',
        type=str, help="Type the manga's name"
    )
    parser.add_argument(
        '-c', '--chapter',
        type=str, help="Type the chapter you wish"
    )

    args = parser.parse_args()

    if args.manga and args.chapter:
        download_chapter(args.chapter)

if __name__ == '__main__':
    main()
