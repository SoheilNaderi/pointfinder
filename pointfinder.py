import re
import requests
from urllib.parse import urljoin
import sys

def get_js_files(url):
    url="https://"+url
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []
    
    js_files = re.findall(r'<script[^>]+src=["\'](.*?\.js)["\']', response.text)
    return [urljoin(url, js) for js in js_files]

def extract_urls_from_js(js_file):
    filter = r"[()<>,'$\"]"
    try:
        response = requests.get(js_file)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching {js_file}: {e}")
        return []
    
    js_content = response.text

    url_pattern = re.compile(r'(["\'](https?://[\w./?=&%-]+)["\'])|(["\']([^"\']*)/["\'])')
    
    urls = set()
    paths=set()
    for match in url_pattern.findall(js_content):
        if match[1]:  
            urls.add(match[1])
        if not(re.search(filter, match[3])):
            paths.add(match[3]) 
    paths=sorted(paths)
    return urls,paths

def main(domain):
    js_files = get_js_files(domain)

    for js_file in js_files:
        urls,paths = extract_urls_from_js(js_file)

    with open(domain+".urls", "w") as f:
        for url in urls:
            if domain in url:
                f.write(url + "\n")

    with open(domain+".paths", "w") as f:
        for path in paths:
            f.write(path + "\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print("[*] Wait for finding...")
        main(sys.argv[1])
        print("[*] finish! save in "+sys.argv[1]+".paths " + sys.argv[1]+".urls")
    else:
        print("[!] Give me a domain (like: exmaple.com)")

