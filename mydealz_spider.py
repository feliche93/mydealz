import scrapy

class MyDealzSpider(scrapy.Spider):
    name = 'mydealz'

    #start_urls = ['https://www.mydealz.de/']
    #https://www.mydealz.de/gruppe/airpods?page=2
    #'https://www.mydealz.de/deals?page={
    #https://www.mydealz.de/deals?page=3
    #https://www.mydealz.de/deals?page={}
    
    #def start_requests(self):
    #    urls = ('https://www.mydealz.de/deals?page={}'.format(i) for i in range(0,2))
    #    for url in urls:
    #        yield scrapy.Request(url=url, callback=self.parse)

    def start_requests(self):
        urls = ('https://www.mydealz.de/deals?page={}'.format(i) for i in range(0,1))
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)            
              


    def parse(self, response):
        # follow links to author pages
        for href in response.css('a.cept-tt.thread-link.linkPlain.thread-title--list::attr(href)'):
            yield response.follow(href, self.parse_mydealz)
            
        # follow pagination links
        for href in response.css('a.cept-next-page.pagination-next.lbox--v-4.text--color-brandPrimary::attr(href)'):
            yield response.follow(href, self.parse)

    def parse_mydealz(self, response):
        yield {
            'title': response.css('span.thread-title--item::text').extract_first(),
            'temp1':response.css('span.cept-vote-temp.vote-temp.vote-temp--burn::text').extract_first(),
            'temp2': response.css('span.cept-vote-temp.vote-temp.vote-temp--hot::text').extract_first(),
            'temp3' : response.css('span.space--h-2.text--b::text').extract_first(),
            'old_price' : response.css('span.mute--text.text--lineThrough.size--all-l.size--fromW3-xl::text').extract_first(),
            'new_price' : response.css('span.thread-price.text--b.vAlign--all-tt.cept-tp.size--all-l.size--fromW3-xl::text').extract_first(),
            'username' : response.css('span.thread-username::text').extract_first(),
            'number_of_comments' : response.css('a.cept-comment-link.btn.space--h-3.btn--mode-boxSec ::text').extract_first(),
            'deal_link' :  response.css('a.twitter-share-button.btn.btn--twitter.hide--toW2.space--ml-2::attr(href)').extract_first(),
            #'until' : response.css('span.lbox--v-3.flex--toW3.overflow--wrap-off.space--fromW3-l-3.text--color-greyShade span.space--fromW3-ml-1.size--all-s span::text').extract_first(),
            'publication_date' : response.css('span.space--fromW3-ml-1.size--all-s::text').extract(),
            'description' : response.xpath("string(//div[@class='userHtml'])").extract()
        }
        
        