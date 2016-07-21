import os

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
PRESENTATION_EXPORT_FORMATS = ["pdf", "html"]
PDF_EXPORT_FORMATS = ["html"]

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

    # Portable Document Format
    "application/pdf": {
        "formats": PDF_EXPORT_FORMATS,
    },

    # Rich Text Format
    "text/rtf": {
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

    # Microsoft Powerpoint 2003
    "application/vnd.ms-powerpoint": {
        "formats": PRESENTATION_EXPORT_FORMATS,
    },

    # Microsoft Powerpoint 2007
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": {
        "formats": PRESENTATION_EXPORT_FORMATS,
    },

    # LibreOffice Impress
    "application/vnd.oasis.opendocument.presentation": {
        "formats": PRESENTATION_EXPORT_FORMATS,
    },
}

DEFAULT_OPTIONS = {
    "formats": ["pdf"]
}
