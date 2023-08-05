from ..resource import Resource


class Documents(Resource):
    def upload(self, sample_file, request_body):
        return self._upload_request("documents/", sample_file, **request_body)

    def find(self, document_id:str):
        return self._get(f"documents/{document_id}")

    def all(self, applicant_id:str):
        return self._get(f"documents?applicant_id={applicant_id}")

    def download(self, document_id:str):
        return self._download_request(f"documents/{document_id}/download")
