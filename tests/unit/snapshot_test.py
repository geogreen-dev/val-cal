
import unittest
import validators
from testutils import match_from_json_file
from testutils import soup_from_html_file
from unittest.mock import MagicMock
from src.match import Match
from src import val_cal

class Test(unittest.TestCase):

	def test_get_match_links(self):
		soup = soup_from_html_file("res/matches.html")
		empty_soup = soup_from_html_file("res/matches_empty.html")
		val_cal.soup_it = MagicMock(side_effect=[soup, empty_soup])
		matches = val_cal.get_match_links_by_id("dummyUrl")
		self.assertEqual(41, len(matches))
		for k, v in matches.items():
			self.assertTrue(validators.url(v))

	def test_parse_match_all_known(self):
		soup = soup_from_html_file("res/future_match_known_all.html")
		val_cal.soup_it = MagicMock(return_value=soup)
		# actual URL is irrelevant but we need at least a valid structure as we do some string manip on it
		actual = val_cal.parse_match_page("https://www.vlr.gg/282834/dsyre-vs-kpi-gaming-crossfire-cup-2023-finals-qf")
		expected = match_from_json_file("res/future_match_known_all.json")
		self.assertEqual(expected, actual)
		self.assertNotEqual("TBD", actual.team_one)
		self.assertNotEqual("TBD", actual.team_two)
		self.assertNotEqual(None, actual.id)
		self.assertNotEqual(None, actual.league)
		self.assertNotEqual(None, actual.time)

	def test_parse_match_known_time(self):
		soup = soup_from_html_file("res/future_match_known_time.html")
		val_cal.soup_it = MagicMock(return_value=soup)
		actual = val_cal.parse_match_page("https://www.vlr.gg/282834/dsyre-vs-kpi-gaming-crossfire-cup-2023-finals-qf")
		expected = match_from_json_file("res/future_match_known_time.json")
		self.assertEqual(expected, actual)
		self.assertEqual("TBD", actual.team_one)
		self.assertEqual("TBD", actual.team_two)
		self.assertNotEqual(None, actual.id)
		self.assertNotEqual(None, actual.league)
		self.assertNotEqual(None, actual.time)


	def test_parse_match_unknown_single_team(self):
		soup = soup_from_html_file("res/future_match_unknown_single_team.html")
		val_cal.soup_it = MagicMock(return_value=soup)
		actual = val_cal.parse_match_page("https://www.vlr.gg/282834/dsyre-vs-kpi-gaming-crossfire-cup-2023-finals-qf")
		expected = match_from_json_file("res/future_match_unknown_single_team.json")
		self.assertEqual(expected, actual)
		self.assertTrue(("TBD" == actual.team_one) != ("TBD" == actual.team_two))
		self.assertNotEqual(None, actual.id)
		self.assertNotEqual(None, actual.league)
		self.assertNotEqual(None, actual.time)

	def test_parse_match_unknown_time(self):
		soup = soup_from_html_file("res/future_match_unknown_time.html")
		val_cal.soup_it = MagicMock(return_value=soup)
		actual = val_cal.parse_match_page("https://www.vlr.gg/282834/dsyre-vs-kpi-gaming-crossfire-cup-2023-finals-qf")
		expected = match_from_json_file("res/future_match_unknown_time.json")
		self.assertEqual(expected, actual)


if __name__ == '__main__':
	unittest.main()
