from flask import Flask
from flask.ext.rq2 import RQ
from flask_restful import Api
from flask_env_settings import Settings


app = Flask(__name__)
app.config.from_object("docsbox.settings")

Settings(app, rules={
    "REDIS_JOB_TIMEOUT": (int, 60 * 10),
    "ORIGINAL_FILE_TTL": (int, 60 * 10),
    "RESULT_FILE_TTL": (int, 60 * 60 * 24),

    "LIBREOFFICE_PATH": (str, "/usr/lib/libreoffice/program/"),

    "THUMBNAILS_DPI": (int, 90),
    "THUMBNAILS_QUANTIZE": (bool, False),
    "THUMBNAILS_QUANTIZE_COLORS": (int, 128),
    "THUMBNAILS_QUANTIZE_COLORSPACE": (str, "rgb"),
})

api = Api(app)
rq = RQ(app)

from docsbox.docs.views import DocumentView, DocumentCreateView
    
api.add_resource(DocumentView, "/api/v1/<task_id>")
api.add_resource(DocumentCreateView, "/api/v1/")

if __name__ == "__main__":
    app.run()
