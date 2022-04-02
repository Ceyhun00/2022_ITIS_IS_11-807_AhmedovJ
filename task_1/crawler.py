import shutil
from typing import Optional

import requests

from bs4 import BeautifulSoup


def get_next_link(bs: BeautifulSoup) -> Optional[str]:
    a_tags = bs.select("a.navlink")
    if len(a_tags) > 0:
        for a in a_tags:
            if  a.attrs.get("href") is not None:
                r = requests.get('https://ilibrary.ru'+a.attrs["href"])
                return r.url
    else:
        return None


def main():
    i = 1
    link_start = 'https://ilibrary.ru/text/11/p.109/index.html'
    index = open("index.txt", "w", encoding="utf-8")
    while link_start is not None and i <= 100:
        print(f"Парсинг {i}-ой страницы")
        response = requests.get(link_start)
        soup = BeautifulSoup(response.text, 'html.parser')
        site = open(f"sites/{i}.txt", "w", encoding="utf-8")

        article = soup.find('span', {"class": "p"}).get_text(separator=" ").strip()
        h3 = soup.select('h3')[0].text.strip()

        site.write(f"{h3}\n{article}")
        site.close()
        index.write(f"{i} {link_start}\n")
        i += 1
        link_start = get_next_link(soup)

    index.close()
    shutil.make_archive("archive", 'zip', "sites")


main()
