import urllib.request
from bs4 import BeautifulSoup

page_num = 1
next_link = True

clear_dict = {}

while next_link:
    request = urllib.request.Request('https://www.fflogs.com/zone/rankings/table/29/progress/-1/101/8/1/Any/Any/0/0/1/0/0?page=' + str(page_num))
    response = urllib.request.urlopen(request)
    page_html = response.read()

    soup = BeautifulSoup(page_html, 'html.parser')
    clears = soup.findAll('a', {'class':'main-table-realm'})
    navigation = soup.findAll('li', {'class':'page-item'})

    for clear in clears:
        realm = clear.text
        if realm in clear_dict:
            clear_dict[realm] += 1
        else:
            clear_dict[realm] = 1

    for nav in navigation:
        if 'Next' in nav.text:
            if nav.has_attr('aria-disabled'):
                next_link = False
    page_num += 1

clear_dict = {k: v for k, v in sorted(clear_dict.items(), key=lambda item: item[1], reverse=True)}

with open('clears.md', 'w') as file:
    file.write("|Rank|Realm|Clears|\n")
    file.write("|---|---|---|\n")
    counter = 1
    for realm in clear_dict.items():
        file.write("|" + str(counter) + "|" + str(realm[0]) + "|" + str(realm[1]) + "|\n")
        counter += 1