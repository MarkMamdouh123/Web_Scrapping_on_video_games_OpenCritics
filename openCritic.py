import requests
from bs4 import BeautifulSoup
import csv

def extract_game_data(page_content):
    soup = BeautifulSoup(page_content, "lxml")
    games = soup.findAll('div', {'class': 'row no-gutters py-2 game-row align-items-center'})

    extracted_data = []
    for game in games:
        rank = game.find('div', {'class': 'rank'}).text.strip()
        score = game.find('div', {'class': 'score'}).text.strip()
        tier = game.find('div', {'class': 'tier'}).find('img')['alt']
        num_reviews = game.find('div', {'class': 'num-reviews'}).text.strip()
        game_name = game.find('div', {'class': 'game-name'}).find('a').text.strip()
        release_date = game.find('div', {'class': 'first-release-date'}).find('span').text.strip()

        extracted_data.append([rank, score, tier, num_reviews, game_name, release_date])

    return extracted_data

def write_to_csv(data, filename):
    with open(filename, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Game Number", "Score", "Tier", "Number of Reviews", "Game Name", "Release Date"])
        writer.writerows(data)
        
        


def main():
    for page_no in range(1, 101):
        url = f"https://opencritic.com/browse/ps4/all-time/num-reviews?page={page_no}"
        page = requests.get(url)

        extracted_data = extract_game_data(page.content)
        write_to_csv(extracted_data, 'game_data.csv')
        print(f"Data from page {page_no} has been successfully extracted and appended to 'game_data.csv' file.")

if __name__ == "__main__":
    main()
