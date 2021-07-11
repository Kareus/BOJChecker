import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

def parseUser(username):
    ret = dict()

    try:
        response = urllib.request.urlopen("https://www.acmicpc.net/user/"+username)
    except:
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

    try:
        tier = soup.select_one('#__next > div.ProfileHeaderCard__ProfileHeaderCardWrapper-sc-1ds1sbv-0.dJhVPe > div.ProfileHeaderCardstyles__ProfileHeaderCardTop-wboshd-0.iothCP > div > div > div:nth-child(4) > span:nth-child(3)').b
        imgs = soup.select_one('#__next > div.ProfileHeaderCard__ProfileHeaderCardWrapper-sc-1ds1sbv-0.dJhVPe > div.ProfileHeaderCardstyles__ProfileHeaderCardTop-wboshd-0.iothCP > div > div > div:nth-child(4) > span.ProfileHeaderCardstyles__UserinfoName-wboshd-2.DZXqi').find_all('img')
        
    except: #user not registered in solved.ac

        ret['tier'] = 'Not Registered'
        ret['problems'] = solved
        ret['class'] = '?'
        return ret

    cl = None
    for img in imgs:
        if 'class' in img['src']:
            cl = img

    if cl:
        cl = cl['src']
        cl = cl.split('/')[-1][1:-4]

        if cl[-1] == 's':
            cl = cl[:-1] + '+'
        elif cl[-1] == 'g':
            cl = cl[:-1] + '++'
    else:
        cl = '?'

    ret['tier'] = tier.string
    ret['problems'] = solved
    ret['class'] = cl
    return ret

def parseClass(num):
    if type(num) == int:
        num = str(num)

    ret = dict()
    try:
        req = urllib.request.Request("https://solved.ac/search?query=in_class:" + num, headers = {'User-Agent':'Chrome/66.0.3359.181'})
        response = urllib.request.urlopen(req)
    except:
        return ret

    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.select_one('#__next > div.contents > div:nth-child(4) > div:nth-child(2) > div > div.StickyTable__Wrapper-sc-10gspwa-3.fIeoKp.sticky-table > div').find_all('div', class_='StickyTable__Row-sc-10gspwa-2 hBHiWI sticky-table-row')
    table = table[1:] # remove title
    ret['problem'] = []
    ret['essential'] = []
    for row in table:
        problem = row.select_one('div:nth-child(1) > span > a > span').string
        essential = row.select_one('div:nth-child(2) > span > span.LabelInline-rriii0-0.itAEbz')

        ret['problem'].append(problem)
        if essential:
            ret['essential'].append(problem)
    
    return ret