import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

def parseUser(username):
    ret = dict()

    try:
        response = urllib.request.urlopen("https://www.acmicpc.net/user/"+username)
    except urllib.error.HTTPError:
        return ret

    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    problemset = soup.find('div', class_='col-md-9').find('div', class_='panel-body')
    solved = []
    for problem in problemset:
        problem = problem.string
        if problem != '\n':
            solved.append(problem)

    req = urllib.request.Request(url='https://solved.ac/profile/'+username, headers= {'User-Agent':'Chrome/66.0.3359.181'})
    response = urllib.request.urlopen(req)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    tier = soup.select_one('#__next > div.ProfileHeaderCard__ProfileHeaderCardWrapper-sc-1jyljpm-0.bsLsWg > div.ProfileHeaderCardstyles__ProfileHeaderCardTop-s3gh4u-0.dlfIwk > div > div > div:nth-child(4) > span:nth-child(3)').b

    ret['tier'] = tier.string
    ret['problems'] = solved
    return ret