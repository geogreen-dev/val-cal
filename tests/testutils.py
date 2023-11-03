
import json
import os
import bs4
from src.match import Match

def match_from_json_file(filepath):
	test_dir = os.path.dirname(__file__)
	abs_path = os.path.join(test_dir, filepath)
	with open(abs_path) as f:
		return Match.from_json(json.load(f))

def soup_from_html(filepath):
	test_dir = os.path.dirname(__file__)
	abs_path = os.path.join(test_dir, filepath)
	with open(abs_path) as page:
		return bs4.BeautifulSoup(page.read(), features="html5lib")

