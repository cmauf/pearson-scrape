# Pearson Scraper

This little script allows you to scrape a book from Pearson given you have a license to use it.

## Installation

Be sure to have Python 3.6 or higher installed. This script uses two external libraries, you may have to install them via pip:

Beautiful soup 4: `pip install -U bs4`

PIL (Pillow fork): `pip install -U Pillow`

## Usage 

Be licenced to use Pearson books. Save ```scraper.py``` in a folder of your choice. You can use the script in two ways:

1. ``python scraper.py`` - you will see a prompt asking you to give the URL of the book and a desired filename

2. `python scraper.py URL filename.pdf` - URL being the URL of the book (has to be on pearson-studium.de) and 
your desired filename.

In order for the script to work, you need to have access to Pearson, e.g. have a VPN set up to your university or college.

## How does it work?

The script scrapes all image files which comprise the pages of the book. It then converts them and puts them together 
in a PDF file.

The file has no indexes and is not very well compressed. Feel free to contribute for better results.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
