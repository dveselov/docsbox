import os.path

"""
TODO:
pylokit.lokit.LoKitExportError: b'no output filter found for provided suffix'
Raised when trying to export to unsupported dest (eg. pptx -> txt)
"""

SUPPORTED_FORMATS = { 
    "pdf": {
        "path": "pdf",
        "fmt": "pdf",
    },
    "txt": {
        "path": "txt",
        "fmt": "txt",
    },
    "html": {
        "path": "html",
        "fmt": "html",
    }
}

SUPPORTED_MIMETYPES = {
    "application/ms-word": {
        "formats": ["pdf", "txt", "html"],
    }
}

DEBUG = True

LIBREOFFICE_PATH = "/usr/lib/libreoffice/program/" # for ubuntu 16.04

BASE_DIR = os.path.abspath(os.path.dirname(__file__)) 

MEDIA_PATH = os.path.join(BASE_DIR, "media/")
MEDIA_URL = "/media/"

ORIGINAL_FILE_TTL = 60 * 10 # 10 minutes
RESULT_FILE_TTL = 60 * 60 * 24 # 24 hours
