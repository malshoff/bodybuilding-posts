import scrapy
from datetime import datetime,timedelta,timezone
from dateutil import tz


class BBSpider(scrapy.Spider):
    name = "bb"
    start_urls = [
        'https://forum.bodybuilding.com/forumdisplay.php?f=19',
        'https://forum.bodybuilding.com/forumdisplay.php?f=19&page=2&order=desc'
        'https://forum.bodybuilding.com/forumdisplay.php?f=19&page=3&order=desc'
    ]
    
    def parse(self, response):
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('US/Eastern')


        utc = datetime.utcnow()


        utc = utc.replace(tzinfo=from_zone)

        # Convert time zone
        eastern = utc.astimezone(to_zone)

        root_url = 'https://forum.bodybuilding.com/'
        for thread in response.xpath('//*[@id="thread_inlinemod_form"]/div[1]/table[2]/tr'):
            date = thread.xpath('.//*[@class="label"]/text()').extract_first()
            if("Today" in date):
                date = eastern

            elif("Yesterday" in date):
                date = eastern - timedelta(days=1)

            elif("-" in date): # The date is older than Yesterday
                b = date.replace(",","").split("-")
                month = int(b[0][-2:])
                day = int(b[1])
                year = int(b[2][:4])
                date = datetime(year,month,day)
            


            yield {
               'title': thread.xpath('td/div/div/div/h3/a[1]/text()').extract_first().strip(),
               'url':  root_url + thread.xpath('td/div/div/div/h3/a[1]/@href').extract_first(),
               'replies':  int(thread.xpath('td[3]/text()').extract_first().strip().replace(",","")),
               'views':  int(thread.xpath('td[4]/text()').extract_first().strip().replace(",","")),
               'op':  thread.xpath('.//*[@class="label"]/a/text()').extract_first().strip(),
               'date': date
            }