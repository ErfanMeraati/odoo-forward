# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError, AccessError
from odoo.tools import html2plaintext


class MailMessage(models.Model):
    _inherit = 'mail.message'

    forward_source_id = fields.Many2one(
        'mail.message',
        string='Forward Source Message',
        index=True,
        ondelete='set null',
        copy=False,
    )
    forward_source_author_name = fields.Char(
        string='Source Author Name',
        copy=False,
    )

    def action_forward_to_channels(self, channel_ids):
        """
        Forward this message (self, a mail.message record) to one or more discuss.channel records.
        A separate, independent message is created for each target channel (like Telegram),
        without adding followers and without unrelated notifications.

        Important note: the source message may have an empty body but contain only an
        attachment (image/file). Such a message's attachment_ids must also be forwarded,
        otherwise the new message would be created completely empty and the client would
        hide it from the UI as an empty message (isEmpty).

        :param channel_ids: list of target discuss.channel ids
        :return: list of ids of the newly created messages
        """
        self.ensure_one()

        if not channel_ids:
            raise UserError("No forward destination selected.")

        channels = self.env['discuss.channel'].browse(channel_ids).exists()
        if not channels:
            raise UserError("Target channels not found.")

        if not self.body and not self.attachment_ids:
            raise UserError("This message has no content to forward.")

        author_name = (
            self.author_id.name
            if self.author_id
            else (self.email_from or "Unknown user")
        )

        new_message_ids = []
        for channel in channels:
            channel.check_access('write')

            new_attachment_ids = []
            if self.attachment_ids:
                for attachment in self.attachment_ids:
                    new_attachment = attachment.copy({
                        'res_model': 'discuss.channel',
                        'res_id': channel.id,
                    })
                    new_attachment_ids.append(new_attachment.id)

            new_message = channel.message_post(
                body=self.body or '',
                message_type='comment',
                subtype_xmlid='mail.mt_comment',
                author_id=self.env.user.partner_id.id,
                attachment_ids=new_attachment_ids,
            )
            new_message.write({
                'forward_source_id': self.id,
                'forward_source_author_name': author_name,
            })
            new_message_ids.append(new_message.id)

        return new_message_ids

    @api.model
    def get_forward_targets(self, search_term=""):
        domain = [
            ('channel_type', 'in', ['chat', 'group', 'channel']),
            ('channel_member_ids.partner_id', '=', self.env.user.partner_id.id),
        ]
        member_channels = self.env['discuss.channel'].search(domain)
        current_partner_id = self.env.user.partner_id.id

        results = []
        for channel in member_channels:
            if channel.channel_type == 'chat':
                other_members = channel.channel_member_ids.filtered(
                    lambda m: m.partner_id.id != current_partner_id
                )
                if other_members:
                    display_name = ", ".join(other_members.mapped('partner_id.name'))
                else:
                    display_name = channel.display_name
            else:
                display_name = channel.display_name

            if search_term and search_term.lower() not in (display_name or '').lower():
                continue

            results.append({
                'id': channel.id,
                'name': display_name,
                'channel_type': channel.channel_type,
                'avatar_url': f'/discuss/channel/{channel.id}/avatar_128' if channel.channel_type != 'chat' else False,
            })

        return results

    def _extras_to_store(self, store, format_reply):
        super()._extras_to_store(store, format_reply=format_reply)
        for message in self:
            store.add(message, {
                'forward_source_id': message.forward_source_id.id or False,
                'forward_source_author_name': message.forward_source_author_name or False,
            })
