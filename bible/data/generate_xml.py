import json
import os
import xmltodict

# Load configuration from config.json
config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config.json')
with open(config_path, 'r') as f:
    config = json.load(f)

bible_name = config.get('bible_name', 'Bible')

# Load the JSON data
with open('spider.bible_id.json') as f:
    data = json.load(f)

# Handle both list format (old) and dict format (new)
if isinstance(data, list):
    data = data[0]

# Create a new dictionary to hold the modified data
modified_data = {"XMLBIBLE": {"@biblename": bible_name, "BIBLEBOOK": []}}

# Iterate over the books in the Bible
book_index = 1
for book_name, chapters in data.items():
    print(f"Processing book: {book_name}")
    book_data = {"@bnumber": book_index, "@bname": book_name, "CHAPTER": []}

    # Iterate over the chapters in the book
    for chapter_number, verses in chapters.items():
        chapter_data = {"@cnumber": chapter_number, "VERS": []}

        # Iterate over the verses in the chapter
        for verse_number, verse_text in verses.items():
            verse_data = {"@vnumber": verse_number, "#text": verse_text}
            chapter_data["VERS"].append(verse_data)

        book_data["CHAPTER"].append(chapter_data)

    modified_data["XMLBIBLE"]["BIBLEBOOK"].append(book_data)
    book_index += 1

# Convert the modified data to XML
xml_data = xmltodict.unparse(modified_data, pretty=True)

# Write the XML data to a file
with open('spider.bible_id.xml', 'w') as f:
    f.write(xml_data)