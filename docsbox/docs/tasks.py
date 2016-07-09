import os
import shutil
import datetime

from pylokit import Office
from wand.image import Image
from tempfile import NamedTemporaryFile, TemporaryDirectory

from rq import get_current_job

from docsbox import app, rq



@rq.job(timeout=app.config["REDIS_JOB_TIMEOUT"])
def remove_file(path):
    """
    Just removes a file.
    Used for deleting original files (uploaded by user) and result files (result of converting) 
    """
    return os.remove(path)


@rq.job(timeout=app.config["REDIS_JOB_TIMEOUT"])
def process_document(path, options):
    current_task = get_current_job()
    with Office(app.config["LIBREOFFICE_PATH"]) as office: # acquire libreoffice lock
        with office.documentLoad(path) as original_document: # open original document
            with TemporaryDirectory() as tmp_dir: # create temp dir where output'll be stored
                for fmt in options["formats"]: # iterate over requested formats
                    current_format = app.config["SUPPORTED_FORMATS"][fmt]
                    output_path = os.path.join(tmp_dir, current_format["path"])
                    original_document.saveAs(output_path, fmt=current_format["fmt"])
                if options.get("thumbnails", None):
                    if "pdf" not in options["formats"]:
                        with NamedTemporaryFile() as pdf_tmp_file:
                            original_document.saveAs(pdf_tmp_file.name, fmt="pdf")
                            image = Image(filename=pdf_tmp_file.name)
                    else:
                        pdf_path = os.path.join(tmp_dir, "pdf")
                        image = Image(filename=pdf_path)
                    thumbnails_folder = os.path.join(tmp_dir, "thumbnails/")
                    os.mkdir(thumbnails_folder)
                    (width, height) = options["thumbnails"]["size"]
                    for index, page in enumerate(image.sequence):
                        with Image(page) as page:
                            filename = os.path.join(thumbnails_folder, "{0}.png".format(index))
                            page.resize(width, height)
                            page.save(filename=filename)
                    else:
                        image.close()
                output_path = os.path.join(app.config["MEDIA_PATH"], current_task.id)
                output_path = shutil.make_archive(output_path, "zip", tmp_dir)
                result_url = os.path.join(app.config["MEDIA_URL"], output_path.split("/")[-1])
        remove_file.schedule(datetime.timedelta(seconds=app.config["RESULT_FILE_TTL"]), output_path)
    return result_url
