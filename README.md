
# val_cal 
 ![build+test](https://github.com/geogreen-dev/val-cal/actions/workflows/python-app.yml/badge.svg)
 
 ![Integration](https://github.com/geogreen-dev/val-cal/actions/workflows/integration.yml/badge.svg) If this is failing with the above succeeding likely vlr.gg have changed their site structure.

A python script that builds calendar files (.ics) for competetive Valorant matches.

I am running this nightly with the files available at http://vlr.geogreen.cc/. You can then import the URL to the calendar software of your choice to receive automatic updates.


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

## Acknowledgements

 - [data scraped from vlr.gg](https://vlr.gg)


