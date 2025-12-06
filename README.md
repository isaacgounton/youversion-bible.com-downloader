# bible.com scraper

Download Bible translations from bible.com (YouVersion) to JSON and XML formats.

**Requires Python 3.9**

## Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/isaacgounton/youversion-bible.com-downloader.git
   cd youversion-bible.com-downloader
   ```

2. **Create and activate virtual environment with Python 3.9**:
   ```bash
   python3.9 -m venv venv
   source venv/bin/activate
   ```

3. **Install requirements**:
   ```bash
   pip install -r requirements.txt
   pip install xmltodict
   ```

4. **Configure the Bible version** in `config.json`:
   ```json
   {
       "bible_id": 2405,
       "bible_name": "BWL23",
       "bible_url": "https://www.bible.com/bible/2405/",
       "start_book": "GEN",
       "start_chapter": 1
   }
   ```
   
   - `bible_id`: The ID from the Bible.com URL (e.g., `https://www.bible.com/bible/2405/` → `2405`)
   - `bible_name`: Name/abbreviation for the XML output
   - `start_book`: Starting book code (default: "GEN")
   - `start_chapter`: Starting chapter (default: 1)

5. **Run the text scraper**:
   ```bash
   scrapy crawl bible
   ```

6. **Convert JSON to XML**:
   ```bash
   cd bible/data
   python generate_xml.py
   ```

7. **Download audio files** (optional):
   ```bash
   scrapy crawl bible_audio
   ```

## Output Files

The downloaded files are saved in `bible/data/`:
- `spider.bible_id.json` - JSON format (text)
- `spider.bible_id.xml` - XML format (text)
- `audio/{bible_name}/` - Audio MP3 files (e.g., `audio/BWL23/GEN_1.mp3`)

### JSON Structure
```json
{
  "BookName": {
    "ChapterNumber": {
      "VerseNumber": "Verse text..."
    }
  }
}
```

### XML Structure
```xml
<?xml version="1.0" encoding="utf-8"?>
<XMLBIBLE biblename="BWL23">
  <BIBLEBOOK bnumber="1" bname="Genesis">
    <CHAPTER cnumber="1">
      <VERS vnumber="1">In the beginning...</VERS>
    </CHAPTER>
  </BIBLEBOOK>
</XMLBIBLE>
```

## Finding Bible Version IDs

1. Go to [bible.com](https://www.bible.com/bible/)
2. Select your desired Bible translation
3. The ID is in the URL: `https://www.bible.com/bible/[ID]/GEN.1`

Example IDs:
- ESV: 59
- NIV: 111
- Gun (BWL23): 2405

## Credits

- Original project by [@mightmay](https://github.com/mightmay)
- JSON to XML conversion and improvements by contributors
