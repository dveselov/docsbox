import os
import ujson
import unittest
import docsbox


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.app = docsbox.app
        self.app.config["TESTING"] = True
        self.app.config["RQ_ASYNC"] = False
        self.samples = os.path.join(
            self.app.config["BASE_DIR"],
            "docs/tests/samples/"
        )
        self.client = docsbox.app.test_client()

    def submit_file(self, filename, options):
        with open(filename, "rb") as source:
            response = self.client.post("/api/v1/", data={
                "file": source,
                "options": ujson.dumps(options),
            })
        return response

class DocumentViewTestCase(BaseTestCase):

    def test_get_task_by_valid_uuid(self):
        filename = os.path.join(self.samples, "sample.docx")
        response = self.submit_file(filename, {
            "formats": ["txt"]
        })
        json = ujson.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.get("id"))
        self.assertEqual(json.get("status"), "queued")
        response = self.client.get("/api/v1/{0}".format(json.get("id")))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ujson.loads(response.data), {
            "id": json.get("id"),
            "status": "queued",
            "result_url": None,
        })

    def test_get_task_by_invalid_uuid(self):
        response = self.client.get("/api/v1/uuid-with-ponies")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(ujson.loads(response.data), {
            "message": "Unknown task_id"
        })

class DocumentCreateViewTestCase(BaseTestCase):

    def test_submit_without_file(self):
        response = self.client.post("/api/v1/", data={
            "options": ujson.dumps(["pdf"])
        })
        json = ujson.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json, {
            "message": "file field is required"
        })

    def test_submit_invalid_mimetype(self):
        response = self.submit_file("/bin/sh", {
            "formats": ["pdf"],
        })
        json = ujson.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json, {
            "message": "Not supported mimetype: 'application/x-sharedlib'"
        })

    def test_submit_empty_formats(self):
        filename = os.path.join(self.samples, "sample.docx")
        response = self.submit_file(filename, {
            "formats": []
        })
        json = ujson.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json, {
            "message": "Invalid 'formats' value"
        })

    def test_submit_invalid_formats(self):
        filename = os.path.join(self.samples, "sample.docx")
        response = self.submit_file(filename, {
            "formats": ["csv"]
        })
        json = ujson.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json, {
            "message": "'application/vnd.openxmlformats-offi"
                       "cedocument.wordprocessingml.document'"
                       " mimetype can't be converted to 'csv'"
        })

    def test_submit_invalid_thumbnails_field(self):
        filename = os.path.join(self.samples, "sample.docx")
        response = self.submit_file(filename, {
            "formats": ["pdf"],
            "thumbnails": 1,
        })
        json = ujson.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json, {
            "message": "Invalid 'thumbnails' value"
        })

    def test_submit_invalid_thumbnails_size_field(self):
        filename = os.path.join(self.samples, "sample.docx")
        response = self.submit_file(filename, {
            "formats": ["pdf"],
            "thumbnails": {
                "size": None,
            },
        })
        json = ujson.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json, {
            "message": "Invalid 'size' value"
        })

    def test_submit_invalid_thumbnails_size_field_value(self):
        filename = os.path.join(self.samples, "sample.docx")
        response = self.submit_file(filename, {
            "formats": ["pdf"],
            "thumbnails": {
                "size": "ZZx43",
            },
        })
        json = ujson.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json, {
            "message": "Invalid 'size' value"
        })

    def test_submit_valid_thumbnails(self):
        filename = os.path.join(self.samples, "sample.docx")
        response = self.submit_file(filename, {
            "formats": ["pdf"],
            "thumbnails": {
                "size": "640x480",
            },
        })
        json = ujson.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.get("status"), "queued")
