import requests
import re
import urllib.parse
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--logoff", dest="log", help="Off input of the links")
parser.add_argument("-l", "--link", dest="link", help="Link to the site without http")
options = parser.parse_args()

target_url = options.link
if not target_url:
    print("[-] Input the link using -l parameter")
    exit(-1)

target_links = []


def extract_links_from(url):
    response = requests.get(url)
    return re.findall('(?:href=")(.*?)"', str(response.content))

result = open("result_links.txt", "w")


def crawl(url):
    href_links = extract_links_from(url)

    for link in href_links:
        link = urllib.parse.urljoin(url, link)

        if "#" in link:
            link = link.split("#")[0]

        if target_url in link and link not in target_links:
            target_links.append(link)
            result.write(link + "\n")
            if not options.log:
                print("[+] URL --->" + link)
            crawl(link)


crawl(target_url)
