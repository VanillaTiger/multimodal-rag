import requests
from bs4 import BeautifulSoup
import csv
import os
from loguru import logger
from tqdm import tqdm

def scrape_page(url):
    """
    scrape the page and return the title, content, images and article_url from given url to the batch issue
    """
    response = requests.get(url)
    if response.status_code != 200:
        # print("Failed to retrieve the page")
        return 0
    
    soup = BeautifulSoup(response.text, 'html.parser')
    results = []
    
    h1_tags = soup.find_all('h1')
    for h1 in h1_tags:
        title = h1.get_text(strip=True)
        content = ""
        images = ""
        
        next_element = h1.find_next_sibling()
        while next_element and next_element.name != 'h1':
            if next_element.name == 'p':
                content += next_element.get_text(strip=True) + "\n"
            elif next_element.name == 'figure':
                img_tag = next_element.find('img')
                if img_tag:
                    images = img_tag['src']
            # elif next_element.name == 'img':
            #     images.append(next_element['src'])
            next_element = next_element.find_next_sibling()
        
        if images and content:
            results.append({"title": title, "content": content, "images": images, "article_url": url})
    
    return results

def create_file():
    """
    create the file to store the data with headers
    """
    if not os.path.exists("data"):
        os.makedirs("data")
    with open('data/data_img_str_url.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["title", "content", "images","article_url"])
    
    logger.info("File created successfully")
    

def save_to_csv(data):
    """
    save the data to the csv file
    """
    with open('data/data_img_str_url.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        for d in data:
            writer.writerow([d["title"], d["content"], d["images"], d["article_url"]])


if __name__ == "__main__":
    create_file()
    # url = "https://www.deeplearning.ai/the-batch/issue-286/"
    logger.info("Start scraping 286 issues of The Batch")
    for i in tqdm(range(286, 0, -1)):
        url = f"https://www.deeplearning.ai/the-batch/issue-{i}/"
        data = scrape_page(url)
        if data:
            save_to_csv(data)
    logger.info("Finished scraping 286 issues of The Batch")
    
    