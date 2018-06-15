import argparse
import os
import re
import time
import requests
import shutil

from bs4 import BeautifulSoup

from conf import BASE_URL_ONE_PIECE, HEADER_ONE_PIECE


def create_folder(chapter):
    folder = 'capitulo-{}'.format(chapter)
    try:
        os.mkdir(folder)
        return folder
    except OSError:
        print('Diretório já existente')
        return folder


def download_chapter(chapter):
    # create the correct url with the chapter
    url = BASE_URL_ONE_PIECE.format(chapter)
    HEADER_ONE_PIECE.update(referer=url)
    # makes the request, and assign the content of the response in `content`
    content = requests.get(url).content
    # create the BeautifulSoup object from the content, using 'html.parse'
    # to create the tree HTML
    soup = BeautifulSoup(content, 'html.parser')
    # find the script tag that contains the image URL, then split in a list of
    # strings
    words = soup.findAll('script')[16].string.split()

    manga_url = ''
    for word in words:
        # check if word contains 'http' string
        if 'http' in word:
            # if so, assign it to manga_url and break the for
            manga_url = word
            break
    # remove "" from the manga_url
    manga_url = manga_url.replace('"', '')
    # get the select tag that contains this id, split it and get the last value
    number_img = int(soup.find('select', id='capPages').text.split()[-1:][0])

    print('Número de imagens:  ', number_img)

    final = ''
    folder = create_folder(chapter)
    for i in range(1, number_img + 1):
        # sleep for 5 seconds, to avoid connection refused
        time.sleep(3)
        # check if i is between 1 and 9
        if i in range(1, 10):
            # if so concatenate the 0 plus i
            final = '0' + str(i)
            # concatenate this final with manga_url to create the URL image
            url = manga_url + '-{}.jpg'.format(final)
            # create the filename
            filename = 'capitulo-{}.jpg'.format(final)
        else:
            url = manga_url + '-{}.jpg'.format(i)
            filename = 'capitulo-{}.jpg'.format(i)
        try:
            # create a regex pattern to get the host from the URL image
            regex = re.compile('(^http:\/\/.*\.centraldemangas\.com\.br)')
            host = regex.search(url).group()
            print('host da regex:', host)
            # update dict
            HEADER_ONE_PIECE.update(host=host)
            print('Novo host:', HEADER_ONE_PIECE['host'])
            # create another request, this time to URL image using headers to
            # this specific site
            # try to make request for the image
            print(url)
            content = requests.get(url, headers=HEADER_ONE_PIECE, stream=True)
            # content = urllib.request.urlopen(req)
        except requests.RequestException:
            print('Arquivo {} indisponível'.format(filename))
            continue
        with open(os.path.join(folder, filename), 'wb') as f:
            # import pdb; pdb.set_trace()
            content.raw.decode_content = True
            # write the content of request into file
            shutil.copyfileobj(content.raw, f)
            print('Arquivo salvo com sucesso! - {}'.format(filename))
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
