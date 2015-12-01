import argparse
import urllib.request
import time

from bs4 import BeautifulSoup

base_url = 'http://mangaop.info/capitulos/{}#1'


def download_chapter(chapter):
    url = base_url.format(chapter)
    content = urllib.request.urlopen(url).read()

    soup = BeautifulSoup(content, 'html.parser')
    words = soup.findAll('script')[16].string.split()

    manga_url = ''
    for word in words:
        if 'http' in word:
            manga_url = word
            break
    manga_url = manga_url.replace('"', '')
    number_img = int(soup.find('select', id='capPages').text.split()[-1:][0])

    print('number=', number_img)

    final = ''
    for i in range(1, number_img+1):
        if i in range(1, 10):
            final = '0'+str(i)
        print('final', final)
        urllib.request.urlretrieve(
            manga_url+'-{}.jpg'.format(final),
            'capitulo-{}.jpg'.format(final)
        )
        time.sleep(10)

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
