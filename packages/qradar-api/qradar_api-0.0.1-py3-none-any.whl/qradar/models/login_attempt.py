from .qradarmodel import QRadarModel


class LoginAttempt(QRadarModel):
    def __init__(self, *, attempt_time=None, user_id=None, remote_ip=None, attempt_result=None, attempt_method=None):
        self.attempt_time = attempt_time
        self.user_id = user_id
        self.remote_ip = remote_ip
        self.attempt_result = attempt_result
        self.attempt_method = attempt_method
