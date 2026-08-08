/** @odoo-module **/

import { registerMessageAction } from "@mail/core/common/message_actions";
import { _t } from "@web/core/l10n/translation";
import { ForwardMessageDialog } from "@discuss_forward_19/js/forward_dialog";


registerMessageAction("forward-message", {
    icon: "fa fa-share",
    name: _t("Forward"),
    condition: ({ message }) => Boolean(message?.id),
    onSelected: ({ message, store }) => {
        store.env.services.dialog.add(ForwardMessageDialog, {
            message,
        });
    },
    sequence: 55,
});
