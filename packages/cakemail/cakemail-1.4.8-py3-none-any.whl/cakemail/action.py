from cakemail_openapi import ActionApi
from cakemail.wrapper import WrappedApi


class Action(WrappedApi):
    create: ActionApi.create_action
    delete: ActionApi.delete_action
    get: ActionApi.get_action
    list_links: ActionApi.list_action_links
    list: ActionApi.list_actions
    update: ActionApi.patch_action
    render: ActionApi.render_action
    send_test: ActionApi.send_test_action

    def __init__(self, superclass):
        super().__init__(
            superclass=superclass,
            namemap={
                'create': 'create_action',
                'delete': 'delete_action',
                'get': 'get_action',
                'list_links': 'list_action_links',
                'list': 'list_actions',
                'update': 'patch_action',
                'render': 'render_action',
                'send_test': 'send_test_action',
            }
        )
