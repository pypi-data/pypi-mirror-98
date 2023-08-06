from .qradarmodel import QRadarModel


class Logsource(QRadarModel):
    def __init__(self, *, id=None, name=None, description=None, type_id=None, protocol_type_id=None, protocol_parameters=None, enabled=None, group_ids=None, average_eps=None):
        self.id = id
        self.name = name
        self.description = description
        self.type_id = type_id
        self.protocol_type_id = protocol_type_id
        self.protocol_parameters = protocol_parameters
        self.enabled = enabled
        self.group_ids = group_ids
        self.average_eps = average_eps
