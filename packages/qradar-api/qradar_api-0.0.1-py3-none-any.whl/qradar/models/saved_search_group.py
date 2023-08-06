from .qradarmodel import QRadarModel


class SavedSearchGroup(QRadarModel):
    def __init__(self, *, id=None, parent_id=None, type=None, level=None, name=None, description=None,  owner=None, modified_time=None, child_group_ids=None):
        self.id = id
        self.parent_id = parent_id
        self.type = type
        self.level = level
        self.name = name
        self.description = description
        self.owner = owner
        self.modified_time = modified_time
        self.child_group_ids = child_group_ids
