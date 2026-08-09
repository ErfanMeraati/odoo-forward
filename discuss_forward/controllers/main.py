# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class DiscussForwardController(http.Controller):

    @http.route('/discuss_forward/get_targets', type='json', auth='user')
    def get_targets(self, search_term=""):
        """Return the list of possible targets (users/channels) to display in the forward dialog"""
        return request.env['mail.message'].get_forward_targets(search_term=search_term)

    @http.route('/discuss_forward/forward_message', type='json', auth='user')
    def forward_message(self, message_id, channel_ids):
        """Forward a message to one or more target channels/users"""
        message = request.env['mail.message'].browse(message_id)
        if not message.exists():
            return {'error': 'Message not found.'}

        new_ids = message.action_forward_to_channels(channel_ids)
        return {'success': True, 'new_message_ids': new_ids}
