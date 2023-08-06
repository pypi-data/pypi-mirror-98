from .qradarmodel import QRadarModel

class LogsourceGroup(QRadarModel):

    def __init__(self, *, id=None, name=None, description=None, parent_id=None, owner=None, modification_date=None, child_groups=None):
        self.id = id
        self.name = name
        self.description = description
        self.parent_id = parent_id
        self.owner = owner
        self.modification_date = modification_date
        self.child_groups = child_groups
