import datetime
import urllib.parse

from bs4 import BeautifulSoup
import requests
import feedgenerator
import csv

feed_file = open('feed.csv')
feeds = csv.reader(feed_file)

index = open('feeds/index.html', 'w')
index.write('<!DOCTYPE html><html><body><ul>')

for feed in feeds:
    print(feed)
    comics_url = feed[1]
    comics = requests.get(comics_url).text

    soup = BeautifulSoup(comics, 'html.parser')

    rss = feedgenerator.Atom1Feed(
        title=soup.find('title').text,
        link=comics_url,
        description='',
        language="ja",
        image=''
    )

    for episode in soup.find('div', class_="chapter").find_all('li'):
        if episode.get('class') is not None:
            continue

        print(episode)
        href = episode.a.get('href')

        rss.add_item(
            unique_id=href.rsplit('/', 1)[1],
            title=episode.div.select('div')[-3].text + ' ' + episode.div.select('div')[-2].text,
            link=urllib.parse.urljoin(comics_url, href),
            description="",
            pubdate=datetime.datetime.strptime(episode.div.select('div')[-1].text + ' 00:00:00+0900', '%Y/%m/%d %H:%M:%S%z')
        )

    with open('feeds/' + feed[0] + '.xml', 'w') as fp:
        rss.write(fp, 'utf-8')

    index.write('<li><a href="{href}">{title}</a></li>'.format(href=feed[0] + '.xml', title=urllib.parse.unquote(feed[1])))

index.write('</ul></body></html>')
