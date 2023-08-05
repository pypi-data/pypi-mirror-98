from cakemail_openapi import WorkflowBlueprintApi
from cakemail.wrapper import WrappedApi


class WorkflowBlueprint(WrappedApi):
    get: WorkflowBlueprintApi.get_workflow_blueprint
    get_action: WorkflowBlueprintApi.get_workflow_blueprint_action
    list_actions: WorkflowBlueprintApi.list_workflow_blueprint_actions
    list: WorkflowBlueprintApi.list_workflow_blueprints

    def __init__(self, superclass):
        super().__init__(
            superclass=superclass,
            namemap={
                'get': 'get_workflow_blueprint',
                'get_action': 'get_workflow_blueprint_action',
                'list_actions': 'list_workflow_blueprint_actions',
                'list': 'list_workflow_blueprints',
            }
        )
