import os

"""
TODO:
pylokit.lokit.LoKitExportError: b'no output filter found for provided suffix'
Raised when trying to export to unsupported dest (eg. pptx -> txt)
"""

DEBUG = os.environ.get("DEBUG", False)

REDIS_URL = os.environ.get("REDIS_URL", "redis://redis:6379/0")
RQ_REDIS_URL = REDIS_URL

BASE_DIR = os.path.abspath(os.path.dirname(__file__)) 
MEDIA_PATH = os.path.join(BASE_DIR, "media/")
MEDIA_URL = "/media/"

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
    },
    "csv": {
        "path": "csv",
        "fmt": "csv",
    }
}

DOCUMENT_EXPORT_FORMATS = ["pdf", "txt", "html"]
SPREADSHEET_EXPORT_FORMATS = ["pdf", "csv", "html"]

SUPPORTED_MIMETYPES = {
    # Microsoft Word 2003
    "application/msword": {
        "formats": DOCUMENT_EXPORT_FORMATS,
    },
    # Microsoft Word 2007
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": {
        "formats": DOCUMENT_EXPORT_FORMATS,
    },
    # LibreOffice Writer
    "application/vnd.oasis.opendocument.text": {
        "formats": DOCUMENT_EXPORT_FORMATS,
    },

    # Microsoft Excel 2003
    "application/vnd.ms-excel": {
        "formats": SPREADSHEET_EXPORT_FORMATS,
    },

    # Microsoft Excel 2007
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": {
        "formats": SPREADSHEET_EXPORT_FORMATS,
    },

    # LibreOffice Calc
    "application/vnd.oasis.opendocument.spreadsheet": {
        "formats": SPREADSHEET_EXPORT_FORMATS,
    },
}

DEFAULT_OPTIONS = {
    "formats": ["pdf"]
}

LIBREOFFICE_PATH = os.environ.get("LIBREOFFICE_PATH", "/usr/lib/libreoffice/program/") # for ubuntu 16.04

ORIGINAL_FILE_TTL = int(os.environ.get("ORIGINAL_FILE_TTL", str(60 * 10))) # 10 minutes
RESULT_FILE_TTL = int(os.environ.get("RESULT_FILE_TTL", str(60 * 60 * 24))) # 24 hours
