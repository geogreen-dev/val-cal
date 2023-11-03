#!/usr/bin/python

import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import json
from ics import Calendar, Event
from multiprocessing import Pool
import os
from .model.match import Match
import logging
import argparse
import sys

ROOT="https://www.vlr.gg/"
MATCHES=ROOT+"matches/?page={}"
OUTDIR=""
CAL_DIR="calendars"
SUB_DIRS=["leagues", "teams"]
SNAPSHOT="matches-snapshot.json"

logging.basicConfig(level=logging.INFO)

def soup_it(url):
    r = requests.get(url)
    return BeautifulSoup(r.content, "html5lib")

def get_upcoming_match_ids(url):
    soup = soup_it(url)
    return list(map(lambda x:(ROOT+x['href']).split('/')[4], soup.find_all("a", attrs = {'class': 'match-item'})))

def get_match_links_by_id(matches_url):
    matches = {}
    page = 1

    while True:
        url = matches_url.format(page)
        logging.info("Parsing match page {}".format(url))
        ids = get_upcoming_match_ids(url)
        page_matches = {id:ROOT+id for id in ids}
        if(len(page_matches)==0):
            break
        else:
            matches.update(page_matches)
            page+=1

    return matches

# ics lib unicode encoder struggles with some valid chars
def sanitize_string(string):
    # go İstanbul Wildcats!
    return string.replace("\u0130","I")

def parse_match_page(url):
    soup = soup_it(url)
    date_time = soup.find(attrs = {'class': 'match-header-date'}).find(attrs = {'class': 'moment-tz-convert'})['data-utc-ts']
    league_meta = [x for x in list(map(lambda x: ' '.join(x.text.split()), soup.find(attrs = {'class': 'match-header-event-series'}).parent)) if x]
    teams = list(map(lambda x: ' '.join(x.find(attrs = {'class': 'wf-title-med'}).text.split()), soup.find_all(attrs = {'class': 'match-header-link-name'})))
    id = url.split('/')[3]
    # vlr claim to use UTC but in reality they do not
    time = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S") + timedelta(hours=4)
    league = sanitize_string(league_meta[0])
    try:
        note = sanitize_string(league_meta[1])
    except:
        note = ""
    team_one = sanitize_string(teams[0])
    team_two = sanitize_string(teams[1])
    match = Match(id, time, league, team_one, team_two, note)
    logging.info(match)
    return match

def event_from_match(match):
    e = Event() 
    # turkish chars were giving me a headache 
    e.name = (match.team_one + " vs. " + match.team_two)
    e.location = match.league
    e.description = match.note
    e.begin = match.time
    e.duration = timedelta(hours=2)
    return e

def build_calendar(matches, filename):
    events = []
    for match in matches:
        events+=[event_from_match(match)]

    cal = Calendar()

    for e in events:
        cal.events.add(e)

    with open(filename, 'w') as cal_file:
        cal_file.writelines(cal.serialize_iter())


def load_matches_from_json(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        logging.error("No local data found at {}".format(filepath))
        sys.exit(-1)

    matches = []

    for match in data:
        matches += [json.loads(match, object_hook=Match.from_json)]

    # map by id
    return {match.id:match for match in matches}




if __name__ == "__main__":

     parser = argparse.ArgumentParser()
     parser._action_groups.pop()
     required = parser.add_argument_group("required args")
     optional = parser.add_argument_group("optional args")

     optional.add_argument("-f", "--force", help="will reload matches we have complete data for", action="store_true")
     optional.add_argument("-t", "--threads", help="threadpool size for http requests")
     required.add_argument("-o", "--outdir", help="output directory for match snapshot and calendar files", required=True)
     args = parser.parse_args()

     if not args.threads:
         poolsize=1
     else:
         poolsize=int(args.threads)

     logging.debug("Poolsize = {}".format(poolsize))

     OUTDIR=args.outdir
     for dir in SUB_DIRS:
         if not os.path.exists(os.path.join(OUTDIR, CAL_DIR, dir)):
             os.makedirs(os.path.join(OUTDIR, CAL_DIR, dir), 0o755)

     logging.debug("Outdir = {}".format(OUTDIR))

     match_links = get_match_links_by_id(MATCHES)

     if not args.force:
         disk_matches = load_matches_from_json(os.path.join(OUTDIR, SNAPSHOT))     
         # based on last snapshot we only want to recheck TBD matches and load new stuff
         tbd_matches = {k:v for k, v in disk_matches.items() if v.is_tbd()}
         tbd_links = {k:v for k, v in match_links.items() if tbd_matches.get(k) is not None}
         logging.info("{} TBD matches need refreshing".format(len(tbd_links)))
         new_links = {k:v for k, v in match_links.items() if disk_matches.get(k) is None}
         logging.info("{} new matches discovered".format(len(new_links)))
         tbd_links.update(new_links)
         match_links = tbd_links
     else:
         logging.info("Running in force mode. Loading all ({}) matches".format(len(match_links)))
         disk_matches = {}


     with Pool(poolsize) as p:
         matches = p.map(parse_match_page, match_links.values())
         matches = {match.id:match for match in matches}
         p.close()
         p.join()

     # new data always overrides
     disk_matches.update(matches)

     # save snapshot to disk
     with open(os.path.join(OUTDIR, SNAPSHOT), 'w', encoding='utf-8') as f:
         json.dump(list(disk_matches.values()), f, default=Match.to_json)

     leagues = set()
     teams = set()

     matches = disk_matches.values()

     for match in matches:
         leagues.add(match.league)
         teams.add(match.team_one)
         teams.add(match.team_two)

     logging.info("Building league calendars...")
     for league in leagues:
         league_matches = list(filter(lambda x: x.league==league, matches))
         build_calendar(league_matches, os.path.join(OUTDIR, CAL_DIR, "leagues", league.replace(':',' -').replace('/','+')+".ics"))

     logging.info("Building team calendars...")
     for team in teams:
         team_matches = list(filter(lambda x: x.team_one==team or x.team_two==team, matches))
         build_calendar(team_matches, os.path.join(OUTDIR, CAL_DIR, "teams", team.replace(':',' -').replace('?','')+".ics"))

