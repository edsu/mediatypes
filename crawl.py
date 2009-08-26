#!/usr/bin/env python

import urllib
import csv 

from BeautifulSoup import BeautifulSoup

def soupify(url):
    return BeautifulSoup(urllib.urlopen(url).read())

def content_types():
    soup = soupify('http://www.iana.org/assignments/media-types/')
    for anchor in soup.findAll('a'):
        if anchor['href'].startswith('/assignments/media-types'):
            content_type = anchor.string
            if content_type == 'example':
                continue
            yield content_type

def sub_types(content_type):
    url = 'http://www.iana.org/assignments/media-types/%s' % content_type
    soup = soupify(url)
    for tr in soup.findAll('tr'):
        cells = tr.findAll('td')
        if len(cells) == 3 or len(cells) == 4:
            sub_type = app_url = rfc_url = None
            if cells[1].a: 
                if cells[1].a.has_key('href'):
                    app_url = 'http://www.iana.org' + cells[1].a['href']
                sub_type = cells[1].a.string.strip()
            elif cells[1].font:
                sub_type = cells[1].font.string.strip()
            elif cells[1].string:
                sub_type = cells[1].string.strip()
            if cells[2].a and 'RFC' in cells[2].a.string:
                rfc_url = cells[2].a['href']
            yield sub_type, app_url, rfc_url

def main():
    csv_writer = csv.writer(open('mediatypes.csv', 'w'))
    for content_type in content_types():
        for sub_type, app_url, rfc_url in sub_types(content_type):
            if sub_type == '&nbsp;':
                continue
            name = "%s/%s" % (content_type, sub_type)
            csv_writer.writerow([name, content_type, sub_type, app_url, 
                                 rfc_url])

if __name__ == '__main__':
    main()
