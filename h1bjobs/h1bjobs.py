import requests
from bs4 import BeautifulSoup
import lxml
import json 



class H1b_jobs:
    def __init__(self) -> None:
        self.jobs = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

        
        pass

    def get_jobs(self, job_title, location='chicago'):
        job_title = job_title.replace(' ', '+')
        location = location.replace(' ', '+')
        #url = 'https://h1bdata.info/jobs.php?q=care+nurse&loc=chicago'
        url = f'https://h1bdata.info/jobs.php?q={job_title}&loc={location}'

        response = requests.get(url, headers=self.headers).text
        jobs = []
        soup = BeautifulSoup(response, 'lxml')
        item_body = soup.findAll('div', {'class':'col-md-8'})
        for i in item_body:
            # print(i)
            # print('_________________________')
            # print(i.find('a')['href']) # works
            # print(i.find('a').text) #works
            # place_loc = i.find('p').text.split('-')
            # print(place_loc[0]) #works
            # print(place_loc[1])
            # print('_______link_________')
            place_loc = i.find('p').text.split('-')
            # compensation = i.find('a').text.split('-')
            self.jobs.append({
                'job title' : i.find('a').text,
                # "compensation": i.find('a').text.split('-')[-1],
                'Company_Name' : place_loc[0],
                'Location': place_loc[1] + ', USA',
                'description' : i.find_all('p')[1].text.strip(),
                'link': i.find('a')['href']
            })
    
    def main(self):

        desired_jobs= ['care nurse', 'home keeper', 'rs nurse']
        for i in desired_jobs:
            self.get_jobs(i)

        print(json.dumps(self.jobs, indent=2, ensure_ascii=False))
        open("h1bDataJobs.json", "a").write(json.dumps(self.jobs, indent=4, ensure_ascii=False))


        



print(H1b_jobs().main())






# headers = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

# url = 'https://h1bdata.info/jobs.php?q=care+nurse&loc=chicago'

# response = requests.get(url, headers=headers).text
# jobs = []
# soup = BeautifulSoup(response, 'lxml')
# item_body = soup.findAll('div', {'class':'col-md-8'})
# for i in item_body:
#     # print(i)
#     # print('_________________________')
#     # print(i.find('a')['href']) # works
#     # print(i.find('a').text) #works
#     # place_loc = i.find('p').text.split('-')
#     # print(place_loc[0]) #works
#     # print(place_loc[1])
#     # print('_______link_________')
#     #print(i)
#     place_loc = i.find('p').text.split('-') #[1] #.text.split('-')
#     # for a in place_loc:
#     #     print(a.text.split())
#     #print(i.find_all('p')[1].text.strip())
#     #print('______________________')
#     #print(i.find('p').text)
#     # compensation = i.find('a').text.split('-')
#     jobs.append({
#         'job title' : i.find('a').text,
#         "compensation": i.find('a').text.split('-')[-1],
#         'Company_Name' : place_loc[0],
#         'Location': place_loc[1],
#         'description' : i.find_all('p')[1].text.strip(),
#         'link': i.find('a')['href']
#     })

# print(json.dumps(jobs, indent=2, ensure_ascii=False))
# # open("h1bDataJobs.json", "a").write(json.dumps(jobs, indent=4, ensure_ascii=False))
 
