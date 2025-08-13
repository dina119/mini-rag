from enum import Enum

class Response_Signal(Enum):
    FILE_VALIDATE_SUCCESS="File Validate Success"
    FILE_TYPE_NOTSUPPORTED="file type not supported"
    FILE_MAX_SIZE_EXCEEDED="file size exceeded"
    FILE_UPLOAD_SUCCESS="file upload success"
    FILE_UPLOAD_FAILED="file upload failed"
    PROCESSING_FAILED="file processing fail"
    PROCESSING_SUCCESS="file processing success"