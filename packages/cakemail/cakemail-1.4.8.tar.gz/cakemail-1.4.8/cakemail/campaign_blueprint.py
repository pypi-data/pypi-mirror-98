from cakemail_openapi import CampaignBlueprintApi
from cakemail.wrapper import WrappedApi


class CampaignBlueprint(WrappedApi):
    get: CampaignBlueprintApi.get_campaign_blueprint
    list: CampaignBlueprintApi.list_campaign_blueprints
    render: CampaignBlueprintApi.render_campaign_blueprint

    def __init__(self, superclass):
        super().__init__(
            superclass=superclass,
            namemap={
                'get': 'get_campaign_blueprint',
                'list': 'list_campaign_blueprints',
                'render': 'render_campaign_blueprint',
            }
        )
