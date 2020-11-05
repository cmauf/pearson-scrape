#!usr/bin/python3

import sys
import requests
import threading
import os
import tempfile
from urllib.request import urlretrieve
import bs4 as bs
from PIL import Image
from time import sleep
import re


def extract_values(pretty_soup):
    list_args = pretty_soup.splitlines()
    for i in range(0, 4):
        list_args.pop(0)
        list_args.pop()

    whitespaces = re.compile(r'^\s+|/s+$')
    all_items = dict()
    for item in list_args:
        item = re.sub(whitespaces, '', item)
        kv = item.split(':', 1)
        # print(kv)
        lhs = ""
        if len(kv) == 2:
            lhs = kv[1]
        if len(lhs) >= 2:
            lhs = lhs[1:-2]
        # print(kv[0], lhs)
        if len(kv[0]) > 0:
            all_items[kv[0]] = lhs
        # print(item)
    return all_items


def get_img_list(list_img):
    list_img = list_img.split(',')
    new_img_list = []
    for image_str in list_img:
        image_str = image_str[1:-1]
        nil = image_str.split("\\")
        new_img_str = ""
        for item in nil:
            new_img_str += item
        new_img_list.append(new_img_str)
    return new_img_list


def download_single_image(img_url, img_name):
    # print("KEKW")
    urlretrieve(img_url, img_name)


def make_pdf(path, file_list):
    list_pages = []
    save_path = cwd+'/'+name
    # print(save_path)
    head = Image.open(path+'/'+file_list[0])
    head = head.convert('RGB')
    for file in file_list[1:]:
        img = Image.open(path+'/'+file)
        img = img.convert('RGB')
        list_pages.append(img)

    head.save(save_path, save_all=True, append_images=list_pages)


def clean_up(tmp_dir):
    os.chdir(tmp_dir)
    for f in os.listdir(tmp_dir):
        os.remove(os.path.join(tmp_dir, f))
    os.rmdir(tmp_dir)


def download_images(list_img):
    tmp_dir = tempfile.mkdtemp()
    os.chdir(tmp_dir)
    list_names = []
    for img in list_img:
        # get image name
        split_url = img.split('?')
        name_list = split_url[0].split('/')
        img_name = name_list[len(name_list)-1]
        list_names.append(img_name)
        while threading.activeCount() >= 100:
            sleep(1)
        threading.Thread(target=download_single_image, args=(img, img_name)).start()
        # urllib.urlretrieve(img, "name")
    while threading.activeCount() != 1:
        sleep(1)
    list_names.sort()
    # print(list_names)
    make_pdf(tmp_dir, list_names)
    clean_up(tmp_dir)


def main(res_url):
    # get Pearson e-reader site
    # must be in HU VPN
    p_page = requests.get(res_url)
    soup = bs.BeautifulSoup(p_page.content, 'html.parser')
    script = soup.body.script
    contents = script.prettify()
    all_items = extract_values(contents)

    list_images = all_items.get('list')
    list_images = get_img_list(list_images)
    download_images(list_images)


if __name__ == '__main__':
    url = ""
    name = ""
    if len(sys.argv) == 1:
        url = input("Give URL for resource: ")
        name = input("Give desired filename: ")
        # url = "https://www.pearson-studium.de/drm/reader/fr/usr/160309/isbn/9783863267391"
    else:
        assert len(sys.argv) == 3, "make sure to use it like that: 'scraper.py URL filename.pdf'"
        url = sys.argv[1]
        name = sys.argv[2]
    cwd = os.getcwd()
    # url = "https://www.pearson-studium.de/drm/reader/fr/usr/160309/isbn/9783863267391"
    if "pearson-studium" not in url:
        exit("Wrong URL!")
    main(url)
