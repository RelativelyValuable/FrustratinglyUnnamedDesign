import gzip
import requests
from bs4 import BeautifulSoup
from pathlib import Path

def _retrieve_sitemap_file_locations(sitemap_directory_link):
    resp = requests.get(sitemap_directory_link)
    sitemap_directory = BeautifulSoup(resp.text, 'xml')
    sitemap_links = [sitemap_location.text for sitemap_location in sitemap_directory.find_all('loc')]

    return sitemap_links

def _extract_sitemap(sitemap_download_path, local_download_path):
    local_download_path.mkdir(parents=False, exist_ok=True)
    sitemap_file = requests.get(sitemap_download_path)
    local_filename = local_download_path.joinpath(sitemap_download_path.split('/')[-1])
    with open(local_filename, 'wb') as fh:
        for chunk in sitemap_file.iter_content(1024):
            if chunk:
                fh.write(chunk)

    return local_filename

def download_sitemap_files(sitemap_directory_link, local_download_path):
    sitemap_download_paths = _retrieve_sitemap_file_locations(sitemap_directory_link)
    for path in sitemap_download_paths:
        _extract_sitemap(
            sitemap_download_path=path,
            local_download_path=local_download_path
        )


if __name__ == '__main__':
    # output_path = Path(__file__).parents[2].joinpath('data', 'sitemaps')
    # link = retrieve_sitemap_file_locations('https://www.foodnetwork.com/sitemaps/sitemap_food_index.xml')
    # sitemap_extractor(link, output_path)
    pass