# AuroraBorealis

This is a small project I did just to learn in practice how to deploy a tiny FastAPI server.

Using it you can download, analyse and plot Kp value.


## Data source

```
-------------------  DATA SOURCE -------------------
# LICENSE: CC BY 4.0
# SOURCE: Geomagnetic Observatory Niemegk, GFZ Helmholtz Centre for Geosciences
# PLEASE CITE: Matzka, J., Stolle, C., Yamazaki, Y., Bronkalla, O. and Morschhauser, A., 2021. The geomagnetic Kp index 
# and derived indices of geomagnetic activity. Space Weather, https://doi.org/10.1029/2020SW002641
----------------------------------------------------
```


## Demo

You can download the data from code

```python
from srcdata.scraper import DataScraper
data = DataScraper().load_data()
```

or using FastAPI app deployed on Huggingface:


```python
import requests

url='https://clarkmaio-aurora-api.hf.space/get_lastdays?days=10'
results = requests.get(url)

data = pl.from_records(results.json()).with_columns(
    pl.col('valuedate').str.strptime(pl.Datetime, "%Y-%m-%d %H:%M:%S")
)
```

[Here](https://clarkmaio-aurora-api.hf.space/docs) you can find api operations docs.

