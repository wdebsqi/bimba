import hashlib

from requests import Response


class FileHashHelper:
    @staticmethod
    def hash_http_response_content_hash(response: Response) -> str:
        """Returns the MD5 hash of the file content"""
        return hashlib.md5(response.content).hexdigest()
