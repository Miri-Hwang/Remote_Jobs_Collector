import requests
from bs4 import BeautifulSoup


JOB = "python"
WWR_URL = f"https://weworkremotely.com/remote-jobs/search?term={JOB}&button="
SO_URL = f"https://stackoverflow.com/jobs?q={JOB}&sort=i"

fake_db = []

# url의 html 문서 soup에 담아오기


def get_soup(URL):
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup

# weworkremotely에서 구인 정보 가져와서 fake_db 배열에 담기


def get_wwr_info(soup):
    global fake_db
    jobs = soup.find('div', {'class': 'jobs-container'}
                     ).find_all('li')

    limit = len(jobs)
    jobs = soup.find('div', {'class': 'jobs-container'}
                     ).find_all('li', limit=limit-1)
    for job in jobs:
        company = job.find('span', {'class': 'company'}).string
        title = job.find('span', {'class': 'title'}).string
        url = job.find_all('a')
        if len(url) > 1:
            url = url[1]
        else:
            url = url[0]

        url = url['href']
        fake_db.append({'company': company, 'title': title, 'url': url})


# stackoverflow에서 구인 정보 가져와서 fake_db 배열에 담기

def get_so_info(soup):
    global fake_db
    jobs = soup.find('div', {'class': 'listResults'}).find_all(
        "div", {"class": "grid--cell fl1"})
    for job in jobs:
        title = job.find("a")["title"]
        company = job.find('h3').find('span').string.strip()
        url = job.find('h2').find('a')['href']
        fake_db.append({'company': company, 'title': title, 'url': url})


# weworkremotely
wwr_soup = get_soup(WWR_URL)
get_wwr_info(wwr_soup)

# stackoverflow
so_soup = get_soup(SO_URL)
get_so_info(so_soup)
