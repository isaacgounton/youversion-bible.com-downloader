import json
import os
import scrapy
from urllib.parse import urljoin


class BibleAudioSpider(scrapy.Spider):
    
    name = 'bible_audio'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Load configuration from config.json
        config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config.json')
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        self.bible_id = config['bible_id']
        self.bible_name = config.get('bible_name', 'Bible')
        start_book = config.get('start_book', 'GEN')
        start_chapter = config.get('start_chapter', 1)
        
        # Create audio output directory
        self.audio_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'audio', self.bible_name)
        os.makedirs(self.audio_dir, exist_ok=True)
        
        self.base_url = f"https://events.bible.com/api/bible/chapter/3.1?id={self.bible_id}&reference="
        self.start_urls = [
            f'https://events.bible.com/api/bible/chapter/3.1?id={self.bible_id}&reference={start_book}.{start_chapter}'
        ]

    def parse(self, response):
        data = json.loads(response.body.decode('utf-8'))
        
        # Get chapter reference
        reference = data['reference']['usfm'][0]  # e.g., "GEN.1"
        book, chapter = reference.split('.')
        
        # Check if audio is available
        audio_list = data.get('audio', [])
        if audio_list:
            audio_info = audio_list[0]  # Get first audio option
            download_urls = audio_info.get('download_urls', {})
            
            # Prefer MP3 format
            mp3_url = download_urls.get('format_mp3_32k')
            if mp3_url:
                # Add https: if URL starts with //
                if mp3_url.startswith('//'):
                    mp3_url = 'https:' + mp3_url
                
                filename = f"{book}_{chapter}.mp3"
                filepath = os.path.join(self.audio_dir, filename)
                
                yield scrapy.Request(
                    mp3_url,
                    callback=self.save_audio,
                    meta={
                        'filepath': filepath,
                        'reference': reference,
                        'next_chapter': data.get('next')
                    }
                )
        else:
            self.logger.warning(f"No audio available for {reference}")
            # Continue to next chapter even if no audio
            next_chapter = data.get('next')
            if next_chapter:
                next_ref = next_chapter['usfm'][0]
                yield scrapy.Request(
                    self.base_url + next_ref,
                    callback=self.parse
                )

    def save_audio(self, response):
        filepath = response.meta['filepath']
        reference = response.meta['reference']
        next_chapter = response.meta['next_chapter']
        
        # Save the audio file
        with open(filepath, 'wb') as f:
            f.write(response.body)
        
        self.logger.info(f"Downloaded audio: {reference} -> {filepath}")
        
        # Continue to next chapter
        if next_chapter:
            next_ref = next_chapter['usfm'][0]
            yield scrapy.Request(
                self.base_url + next_ref,
                callback=self.parse
            )
        else:
            self.logger.info("Audio download complete!")
