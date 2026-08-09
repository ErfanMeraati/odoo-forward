/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { useService } from "@web/core/utils/hooks";
import { rpc } from "@web/core/network/rpc";
import { _t } from "@web/core/l10n/translation";


export class ForwardMessageDialog extends Component {
    static template = "discuss_forward_19.ForwardMessageDialog";
    static components = { Dialog };
    static props = ["message", "close"];

    setup() {
        this.notification = useService("notification");
        this.state = useState({
            searchTerm: "",
            targets: [],
            selectedIds: new Set(),
            isLoading: true,
            isSending: false,
        });
        this.loadTargets();
    }

    async loadTargets(searchTerm = "") {
        this.state.isLoading = true;
        try {
            const targets = await rpc("/discuss_forward/get_targets", {
                search_term: searchTerm,
            });
            this.state.targets = targets;
        } finally {
            this.state.isLoading = false;
        }
    }

    onSearchInput(ev) {
        this.state.searchTerm = ev.target.value;
        this.loadTargets(this.state.searchTerm);
    }

    toggleTarget(targetId) {
        if (this.state.selectedIds.has(targetId)) {
            this.state.selectedIds.delete(targetId);
        } else {
            this.state.selectedIds.add(targetId);
        }
        this.state.selectedIds = new Set(this.state.selectedIds);
    }

    isSelected(targetId) {
        return this.state.selectedIds.has(targetId);
    }

    get canSend() {
        return this.state.selectedIds.size > 0 && !this.state.isSending;
    }

    get selectedCountLabel() {
        const count = this.state.selectedIds.size;
        if (!count) {
            return _t("No destination selected");
        }
        return _t("%s destination(s) selected", count);
    }

    async onSendClick() {
        if (!this.canSend) {
            return;
        }
        this.state.isSending = true;
        try {
            const result = await rpc("/discuss_forward/forward_message", {
                message_id: this.props.message.id,
                channel_ids: Array.from(this.state.selectedIds),
            });
            if (result.error) {
                this.notification.add(result.error, { type: "danger" });
            } else {
                this.notification.add(_t("Message forwarded successfully."), { type: "success" });
                this.props.close();
            }
        } finally {
            this.state.isSending = false;
        }
    }

    onCancelClick() {
        this.props.close();
    }
}
