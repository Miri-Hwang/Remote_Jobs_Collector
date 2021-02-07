import requests
from bs4 import BeautifulSoup


JOB = "python"
WWR_URL = f"https://weworkremotely.com/remote-jobs/search?term={JOB}&button="
SO_URL = f"https://stackoverflow.com/jobs?q={JOB}&sort=i"
RM_URL = f"https://remoteok.io/remote-{JOB}-jobs"

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}


# url의 html 문서 soup에 담아오기


def get_soup(URL):
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup


def get_soup_head(URL):
    r = requests.get(URL, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup

# weworkremotely에서 구인 정보 가져와서 db 에 담아 return


def get_wwr_info(soup):
    db = []
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

        url = 'https://weworkremotely.com'+url['href']
        db.append({'company': company, 'title': title, 'url': url})
    return db


# stackoverflow에서 구인 정보 가져와서 db 에 담아 return

def get_so_info(soup):
    db = []
    jobs = soup.find('div', {'class': 'listResults'}).find_all(
        "div", {"class": "grid--cell fl1"})
    for job in jobs:
        title = job.find("a")["title"]
        company = job.find('h3').find('span').string.strip()
        url = 'https://stackoverflow.com'+job.find('h2').find('a')['href']
        db.append({'company': company, 'title': title, 'url': url})
    return db


# remoteok에서 구인 정보 가져와서 db 에 담아 return

def get_rm_info(soup):
    db = []
    jobs = soup.find('table', {'id': 'jobsboard'}).find_all('tr')
    for job in jobs:
        try:
            title = job.find('td', {'class': 'company'}).find('h2').string
            company = job.find('td', {'class': 'company'}).find('h3').string
            url = job.find('td', {'class': 'company'}).find(
                'a', {'class': 'preventLink'})['href']
            url = 'https://remoteok.io'+url
            db.append({'company': company, 'title': title, 'url': url})

        except:
            pass
    return db


def collect_info():
    wwr_soup = get_soup(WWR_URL)
    so_soup = get_soup(SO_URL)
    rm_soup = get_soup_head(RM_URL)

    db = get_wwr_info(wwr_soup) + get_so_info(so_soup) + get_rm_info(rm_soup)
    return db
