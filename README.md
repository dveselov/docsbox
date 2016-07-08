# docsbox

Docsbox converts yours doc/docx/etc. documents into pdf/html/txt and creates png previews.

```bash
$ curl -F "file=@kittens.docx" -i http://localhost:5000/api/v1/

{
    "id": "9b643d78-d0c8-4552-a0c5-111a89896176",
    "status": "queued"
}

$ curl -i http://localhost:5000/api/v1/9b643d78-d0c8-4552-a0c5-111a89896176

{
    "id": "9b643d78-d0c8-4552-a0c5-111a89896176",
    "result_url": "/media/9b643d78-d0c8-4552-a0c5-111a89896176.zip",
    "status": "finished"
}

$ curl -O http://localhost:5000/media/9b643d78-d0c8-4552-a0c5-111a89896176.zip

$ unzip -l 9b643d78-d0c8-4552-a0c5-111a89896176.zip 

Archive:  9b643d78-d0c8-4552-a0c5-111a89896176.zip
  Length      Date    Time    Name
---------  ---------- -----   ----
    11135  2016-07-08 05:31   txt
   373984  2016-07-08 05:31   pdf
   147050  2016-07-08 05:31   html
---------                     -------
   532169                     3 files
```

# API

```
POST (multipart/form-data) /api/v1/
file=@kittens.docx
options={ # optional
    "formats": ["pdf"] # desired formats to be converted in, optional
    "thumbnails": { # optional
        "size": "320x240",
    } 
}

GET /api/v1/{task_id}
```

# Settings
```
ORIGINAL_FILE_TTL - original file (word document/presentation/etc.) TTL (default: 10 minutes)
RESULT_FILE_TTL - result file (zip archive) TTL (default: 24 hours)
```

# Install
Currently, installing process is a bit complicated:

```bash
$ sudo apt-get install libffi-dev \ # used by CFFI-based packages
                       libmagic-dev \ # used for files fingerprinting
                       libmagickwand-dev \ # used in PDF-to-PNG conversion
                       libreoffice libreofficekit-dev \ # used for other conversion directions
                       redis-server # used in task queue
$ virtualenv -p python3.5 env
$ source env/bin/activate
$ pip install -r requirements.txt
$ gunicorn wsgi:app # -> http://127.0.0.1:8000
```

```bash
# Start rqworker & rqscheduler
$ rqworker
$ rqscheduler
```
