/** @odoo-module **/

import { useComponent } from "@odoo/owl";
import { messageActionsRegistry } from "@mail/core/common/message_actions";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { ForwardMessageDialog } from "@discuss_forward/js/forward_dialog";


messageActionsRegistry.add("forward-message", {
    icon: "fa fa-share",
    title: _t("Forward"),
    onClick: (component) => {
        component.dialog.add(ForwardMessageDialog, {
            message: component.props.message,
        });
    },
    condition: (component) => Boolean(component.props.message?.id),
    setup: () => {
        const component = useComponent();
        component.dialog = useService("dialog");
    },
    sequence: 55,
});
