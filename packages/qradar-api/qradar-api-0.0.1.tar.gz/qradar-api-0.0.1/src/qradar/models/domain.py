from .qradarmodel import QRadarModel

class Domain(QRadarModel):

    def __init__(self, *, id=None, name=None, description=None, tenant_id=None, deleted=None, event_collector_ids=None, log_source_ids=None,
                 log_source_group_ids=None, custom_properties=None, flow_source_ids=None, flow_collector_ids=None, asset_scanner_ids=None, qvm_scanner_ids=None, flow_vlans_ids=None):

        self.id = id
        self.name = name
        self.description = description
        self.tenant_id = tenant_id
        self.deleted = deleted
        self.event_collector_ids = event_collector_ids
        self.log_source_ids = log_source_ids
        self.log_source_group_ids = log_source_group_ids
        self.custom_properties = custom_properties
        self.flow_source_ids = flow_source_ids
        self.flow_collector_ids = flow_collector_ids
        self.asset_scanner_ids = asset_scanner_ids
        self.qvm_scanner_ids = qvm_scanner_ids
        self.flow_vlans_ids = flow_vlans_ids

