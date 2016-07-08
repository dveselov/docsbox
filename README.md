# docsbox

Docsbox converts yours doc/docx/etc. documents into pdf/html/txt and creates png previews.

```bash
$ curl -F "file=@kittens.docx" -i http://localhost:5000/api/v1/

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 77
Server: Werkzeug/0.11.10 Python/3.5.1+
Date: Fri, 08 Jul 2016 02:31:54 GMT

{
    "id": "9b643d78-d0c8-4552-a0c5-111a89896176",
    "status": "queued"
}

$ curl -i http://localhost:5000/api/v1/9b643d78-d0c8-4552-a0c5-111a89896176

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 148
Server: Werkzeug/0.11.10 Python/3.5.1+
Date: Fri, 08 Jul 2016 02:32:27 GMT

{
    "id": "9b643d78-d0c8-4552-a0c5-111a89896176",
    "result_url": "/media/9b643d78-d0c8-4552-a0c5-111a89896176.zip",
    "status": "finished"
}

$ curl -O http://localhost:5000/media/9b643d78-d0c8-4552-a0c5-111a89896176.zip
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   233  100   233    0     0   9052      0 --:--:-- --:--:-- --:--:--  9320

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
