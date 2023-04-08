import time, json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from parsel import Selector
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class JOBS:
    def __init__(self) -> None:
        self.google_jobs_results = []

        pass
    def page_nav(self,url):
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument('--lang=en')
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36")
        #driver = webdriver.Chrome('/Users/c1oud4o4/Downloads/chromedriver_mac_arm64 (1)/chromedriver',options=options)
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)
        # wait = WebDriverWait(driver, 10)
        # element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.zxU94d')))
        # element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#immersive_desktop_root > div > div.lteri > div.zxU94d.gws-plugins-horizon-jobs__tl-lvc')))

        old_height = driver.execute_script("""
        function getHeight() {
            return document.querySelector('.zxU94d').scrollHeight;
            }return getHeight();
        """)
        while True:
            driver.execute_script("document.querySelector('.zxU94d').scrollTo(0, document.querySelector('.zxU94d').scrollHeight)")
            time.sleep(2)
            new_height = driver.execute_script("""
            function getHeight() {
                return document.querySelector('.zxU94d').scrollHeight;}
                return getHeight();
                """)
            if new_height == old_height:
                break
            old_height = new_height
            selector = Selector(driver.page_source)
            driver.quit()
            return selector

    def get_jobs(self, selector):
        for result in selector.css('.iFjolb'):
            #link = result.xpath('/html/body/div[2]/div/div[2]/div[1]/div/div/div[3]/div[2]/div/div[1]/div/div/g-scrolling-carousel/div[1]/div/div/span/a').get().split('"')[5]
            
            #print(link)
            link = result.css('.DaDV9e a::attr(href)').get() #works perfect
            title = result.css('.BjJfJf::text').get()
            company = result.css('.vNEEBe::text').get()
            container = result.css('.Qk80Jf::text').getall()

            if container[0][0:3] == 'via':
                location = 'UNKNOWN' #container[0]
                via = container[0]
            else:
                location = container[0]
                via = container[1]

            thumbnail = result.css('.pJ3Uqf img::attr(src)').get()
            extensions = result.css('.KKh3md span::text').getall()

            self.google_jobs_results.append({
                'title': title,
                'Company_Name': company,
                'location': location,
                'via': via,
                'Apply Link': link,
                'thumbnail': thumbnail,
                'extensions': extensions
                })
            print(json.dumps(self.google_jobs_results, indent=2, ensure_ascii=False))
            #open("jobs.db.json", "a").write(json.dumps(self.google_jobs_results, indent=4, ensure_ascii=False))

    def main(self):
        # https://site-analyzer.pro/services-seo/uule/ 
        #link above allows you generate the country encoded location which you 
        # include into the params uule and change "gl" to that country short code


        job_lists = ['python backend', 'cloud engineer', 'python engineer']
        for i in job_lists:
            params = {
                'q': f'{i}',						# search string
                'ibp': 'htl;jobs',							# google jobs
                #'uule': 'w+CAIQICINVW5pdGVkIFN0YXRlcw',		# encoded location (USA)
                # 'uule': 'w+CAIQICIHbmlnZXJpYQ'                #encoded location (nigeria)
                'uule': 'w+CAIQICICdWs',             #glasgow #'w+CAIQICIHZ2xhc2dvdw',                    # encoded location (UK)
                'hl': 'en',									# language 
                'gl': 'uk',									# country of the search
                }
            URL = f"https://www.google.com/search?q={params['q']}&ibp={params['ibp']}&uule={params['uule']}&hl={params['hl']}&gl={params['gl']}"
            #print(URL)
            #a = 'https://www.google.com/search?q='

            result = self.page_nav(URL)
            self.get_jobs(result)
        open("jobs.db.json", "a").write(json.dumps(self.google_jobs_results, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    JOBS().main()