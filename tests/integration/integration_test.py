
import unittest
import validators
from testutils import match_from_json_file
from testutils import soup_from_html
from src.match import Match
from src import val_cal

class IntegrationTest(unittest.TestCase):
	
	MATCH_PAGE=""

	def test_get_match_links(self):
		print("getting matches")
		matches = val_cal.get_match_links_by_id("https://www.vlr.gg/matches?page={}")
		# we at least get some matches back and they resolve to valid URLs
		self.assertTrue(len(matches)>1)
		for k, v in matches.items():
			self.assertTrue(validators.url(v))
			MATCH_PAGE=v

	def test_parse_match_all_known(self):
		matches = val_cal.get_match_links_by_id("https://www.vlr.gg/matches?page={}")

		# running against all matches can be quite slow
		for match in list(matches.values())[:10]:
			if match == None: pass
			else: val_cal.parse_match_page(match)

if __name__ == '__main__':
	unittest.main()
