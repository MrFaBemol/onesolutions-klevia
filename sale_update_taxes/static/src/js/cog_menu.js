/** @odoo-module **/
import { DropdownItem } from "@web/core/dropdown/dropdown_item";
import { registry } from "@web/core/registry";
const { Component } = owl;
import { useService } from "@web/core/utils/hooks";
const cogMenuRegistry = registry.category("cogMenu");

export class CogMenu extends Component {

    setup() {
        this.action = useService("action");
    }

    async actionNewOption() {
        var currentModel = this.env.searchModel.resModel;
        let saleOrderId = sessionStorage.getItem('saleOrderId');

        if (!saleOrderId || saleOrderId === "null" || saleOrderId === "undefined") {
            if (this.env.searchModel?.globalContext?.params?.resId) {
                saleOrderId = this.env.searchModel.globalContext.params.resId;
                sessionStorage.setItem('saleOrderId', saleOrderId);
            }
        }
        console.log(currentModel)
        this.action.doAction({
            type:'ir.actions.act_window',
            res_model:'update.line.taxes',
            view_mode:'form',
            views: [[false, "form"]],
            target: "new",
            context:{
                default_sale_order_id:parseInt(saleOrderId, 10),
            }
        })
    }
}
CogMenu.template = "blog_cog_menu.NewOption";
CogMenu.components = { DropdownItem };
export const CogMenuItem = {
    Component: CogMenu,
    groupNumber: 100,
    isDisplayed: ({ config }) => {
        console.log("CogMenu Check:", config);
        return config.viewType === "form" && config.rawArch.includes('o_sale_order');
    },
};
cogMenuRegistry.add("new-option", CogMenuItem, { sequence: 10 });
















