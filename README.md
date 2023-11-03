
# val-cal 
 ![build+test](https://github.com/geogreen-dev/val-cal/actions/workflows/python-app.yml/badge.svg)
 
 ![Integration](https://github.com/geogreen-dev/val-cal/actions/workflows/integration.yml/badge.svg)

## About
A python script that builds calendar files (.ics) for competetive Valorant matches. 

I was fed up with so many websites providing this info but no good way to add it to a mobile calendar. I am running this nightly with the files available at http://vlr.geogreen.cc/. 

Matches are split by team and league so you can customise your subscription. You can then import the URL to the calendar software of your choice to receive automatic updates. I have only tested with Google Calendars but .ics will likely work in your software of choice.

## Usage
```
usage: val-cal.py [-h] [-f] [-t THREADS] -o OUTDIR

required args:
  -o OUTDIR, --outdir OUTDIR
                        output directory for match snapshot and calendar files

optional args:
  -f, --force           will reload matches we have complete data for
  -t THREADS, --threads THREADS
                        threadpool size for http requests
```

## Testing

Using pytest with run config wrapped in Makefile
```
# From project root will run pytest
make test-unit
make test-integration
```
If only Integration tests are failing it is likey that vlr.gg have changed their site structure and some re-write is required.

## Acknowledgements

 - [data scraped from vlr.gg](https://vlr.gg)


