import json
import os
import scrapy

class BibleSpider(scrapy.Spider):
    

    name = 'bible'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Load configuration from config.json
        config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config.json')
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        self.bible_id = config['bible_id']
        start_book = config.get('start_book', 'GEN')
        start_chapter = config.get('start_chapter', 1)
        
        self.base_url = f"https://events.bible.com/api/bible/chapter/3.1?id={self.bible_id}&reference="
        self.start_urls = [
            f'https://events.bible.com/api/bible/chapter/3.1?id={self.bible_id}&reference={start_book}.{start_chapter}'
        ]

    def parse(self, response):
        print("XXXXXXXXXXXXXXXXXXX")
        print(response)
        data = json.loads(response.body.decode('utf-8'))
        text = data['content']

        html = scrapy.http.HtmlResponse(
            response.url,
            body=text,
            encoding='utf-8'
        )

        if 'verses' not in response.meta:
            verses = {}
        else:
            verses = response.meta['verses']


        book = data['reference']['human'].split(" ")
        book.pop(-1)
        book = " ".join(book)
        chapter = data['reference']['usfm'][0].split(".")[1]

        next_chapter = data['next']
        if next_chapter is not None:
            next_chapter = next_chapter['usfm'][0]

        for verse in html.css(".verse"):
            number = verse.xpath('@data-usfm').extract_first().split(".")[-1]
            text = verse.css('.content::text').extract()

            if book not in verses:
                verses[book] = {}

            if chapter not in verses[book]:
                verses[book][chapter] = {}

            if number not in verses[book][chapter]:
                verses[book][chapter][number] = ''

            text.extend([' ']) # adding space after the end of the sentence
            texto = ''.join(text)
            if len(texto.strip()) > 0:
                # excluding texts that only contains spaces
                verses[book][chapter][number] += texto

        if next_chapter is None:
            yield verses
        else:
            yield scrapy.Request(
                self.base_url+next_chapter,
                callback=self.parse,
                meta={'verses': verses}
            )
