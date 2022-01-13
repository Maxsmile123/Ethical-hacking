import requests
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-o", "--logoff", dest="log", help="Off input of the links")
parser.add_argument("-l", "--link", dest="link", help="Link to the site without http")
options = parser.parse_args()

paths = []


def crawl(url):
    with open("common_dir.txt", "r") as wordlist_file:
        with open("paths.txt", "w") as result:
            for line in wordlist_file:
                word = line.strip()
                test_url = url + "/" + word
                response = requests.get("http://" + test_url)
                if response:
                    if not options.log:
                        print("[+] Discovered URL ---> " + test_url)
                    result.write("http://" + test_url + "\n")


url = options.link
if not url:
    print("[-] Input the link using -l parameter")
    exit(-1)
crawl(url)


