import os
import shutil
import datetime

from pylokit import Office
from rq import get_current_job
from tempfile import NamedTemporaryFile, TemporaryDirectory

from docsbox import app, rq



@rq.job
def remove_file(path):
    """
    Just removes a file.
    Used for deleting original files (uploaded by user) and result files (result of converting) 
    """
    return os.remove(path)


@rq.job
def process_document(path, options):
    current_task = get_current_job()
    with Office(app.config["LIBREOFFICE_PATH"]) as office: # acquire libreoffice lock
        with office.documentLoad(path) as original_document: # open original document
            with TemporaryDirectory() as tmp_dir: # create temp dir where output'll be stored
                for fmt in options["formats"]: # iterate over requested formats
                    current_format = app.config["SUPPORTED_FORMATS"][fmt]
                    output_path = os.path.join(tmp_dir, current_format["path"])
                    original_document.saveAs(output_path, fmt=current_format["fmt"])
                output_path = os.path.join(app.config["MEDIA_PATH"], current_task.id)
                output_path = shutil.make_archive(output_path, "zip", tmp_dir)
                result_url = os.path.join(app.config["MEDIA_URL"], output_path.split("/")[-1])
        remove_file.schedule(datetime.timedelta(seconds=app.config["RESULT_FILE_TTL"]), output_path)
    return result_url
