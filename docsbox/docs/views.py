import datetime

from magic import Magic
from tempfile import NamedTemporaryFile

from flask import request
from flask_restful import Resource, abort

from docsbox import app, rq
from docsbox.docs.tasks import remove_file, process_document


class DocumentView(Resource):

    def get(self, task_id):
        queue = rq.get_queue()
        task = queue.fetch_job(task_id)
        if task:
            return {
                "id": task.id,
                "status": task.status,
                "result_url": task.result
            }
        else:
            return abort(404, message="Unknown task_id")


class DocumentCreateView(Resource):

    def post(self):
        if "file" not in request.files:
            return abort(400, message="file field is required")
        else:
            with NamedTemporaryFile(delete=False) as tmp_file:
                request.files["file"].save(tmp_file)
                remove_file.schedule(
                    datetime.timedelta(seconds=app.config["ORIGINAL_FILE_TTL"])
                , tmp_file.name)
                task = process_document.queue(tmp_file.name, {
                    "formats": ["pdf", "txt", "html"]
                })
        return {
            "id": task.id,
            "status": task.status,
        }
