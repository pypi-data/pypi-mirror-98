from requests.auth import AuthBase

class MinioAuth(AuthBase):
    """Attaches HTTP Minio Authentication to the given Request object."""
    def __init__(self, project_token):
        # setup any auth-related data here
        self.project_token = project_token

    def __call__(self, r):
        r.headers['MinioToken'] = self.project_token
        return r
