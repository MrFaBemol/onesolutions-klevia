/** @odoo-module **/

import { registry } from '@web/core/registry';
import { SaleOrderLineListRenderer } from '@sale/js/sale_order_line_field/sale_order_line_field';

export class CustomSaleOrderLineListRenderer extends SaleOrderLineListRenderer {

    isCellReadonly(column, record) {
        if (column.name === 'add_page_break_after') {
            return false;
        }
        return super.isCellReadonly(column, record);
    }
}


import { saleOrderLineOne2Many } from '@sale/js/sale_order_line_field/sale_order_line_field';
import { ProductLabelSectionAndNoteOne2Many } from '@account/components/product_label_section_and_note_field/product_label_section_and_note_field';

export class CustomSaleOrderLineOne2Many extends ProductLabelSectionAndNoteOne2Many {
    static components = {
        ...ProductLabelSectionAndNoteOne2Many.components,
        ListRenderer: CustomSaleOrderLineListRenderer,
    };
}

const customField = {
    ...saleOrderLineOne2Many,
    component: CustomSaleOrderLineOne2Many,
};

registry.category('fields').add('sol_o2m_custom', customField);
