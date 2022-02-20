# Initial Setup
```
> pip install -r requirements.txt
```

# DATABASE CREATION

## Create Database
```sql
CREATE DATABASE bible_api;
use bible_api;
```

## Download files
Download database files: https://ebible.org/download.php
Choose to download the "BibleWorks import (VPL) + SQL" files and copy the ".sql files" to a folder called `./sources/`, the names of the files should correspond to the names of the tables!

## Load Database data
```
> python -Xutf8 create_database.py
```


# API 
## Launch rest
```
> uvicorn api:app
```

## Example REST request to /text_query/
```
> http://127.0.0.1:8000/text_query/?bible_name=deu1912_vpl&bible_name=engwebpb_vpl&book=GEN&chapter=1
```

## Documention
```
> http://127.0.0.1:8000/redoc
```
