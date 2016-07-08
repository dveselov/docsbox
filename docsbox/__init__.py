from flask import Flask
from flask.ext.rq2 import RQ
from flask_restful import Api


app = Flask(__name__)
app.config.from_object("docsbox.settings")

api = Api(app)
rq = RQ(app)

from docsbox.docs.views import DocumentView, DocumentCreateView
    
api.add_resource(DocumentView, "/api/v1/<task_id>")
api.add_resource(DocumentCreateView, "/api/v1/")

if __name__ == "__main__":
    app.run()
