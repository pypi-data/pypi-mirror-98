
from . import _VDAPIService, _VDDuplicateableResponse

class _DemandTagKeyAPI(_VDAPIService):

    __API__ = "demand_tags"

    def __init__(self, demand_tag):
        super(_DemandTagKeyAPI, self).__init__()
        self.demand_tag_id = demand_tag.id
        self.account_id = demand_tag.account_id

    @property
    def endpoint(self):
        """
        The api endpoint that is used for this service.  For example:: 
            
            In [1]: import springserve

            In [2]: springserve.supply_tags.endpoint
            Out[2]: '/supply_tags'

        """
        return "/demand_tags/{}/demand_tag_keys".format(self.demand_tag_id)

class _DemandTagResponse(_VDDuplicateableResponse):
    
    def get_key_value_targeting_keys(self):
        # Need to make a new one per bill
        return _DemandTagKeyAPI(self).get()

    def add_key(self, data, **kwargs):
        return _DemandTagKeyAPI(self).post(data, **kwargs)

class _DemandTagAPI(_VDAPIService):

    __RESPONSE_OBJECT__ = _DemandTagResponse
    __API__ = "demand_tags"

class _DemandPartnerAPI(_VDAPIService):

    __API__ = "demand_partners"

class _DemandLabelAPI(_VDAPIService):

    __API__ = "demand_labels"

class _ConnectedDemandAPI(_VDAPIService):

    __RESPONSE_OBJECT__ = _DemandTagResponse
    __API__ = "connected_demand"

class _CampaignAPI(_VDAPIService):

    __API__ = "campaigns"





