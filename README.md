
# val_cal

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

Testing is currently just comparing previous json outputs vs newly parsed objects from the same html stored in tests/res. 

It is fairly brittle as it will not fail should vlr.gg change their site structure. Ultimately some integration tests should cover this.

```
# From project root will run pytest
make test
```

## Acknowledgements

 - [data scraped from vlr.gg](https://vlr.gg)


