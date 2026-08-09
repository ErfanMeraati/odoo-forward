/** @odoo-module **/

import { Message } from "@mail/core/common/message_model";
import { patch } from "@web/core/utils/patch";


patch(Message.prototype, {
    /** @type {number|false} */
    forward_source_id: false,
    /** @type {string|false} */
    forward_source_author_name: false,

    get isForwarded() {
        return Boolean(this.forward_source_author_name);
    },
});
