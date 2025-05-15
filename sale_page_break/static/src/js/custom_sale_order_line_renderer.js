/** @odoo-module **/

import { registry } from '@web/core/registry';
import { BooleanField } from '@web/views/fields/boolean/boolean_field';
import { SaleOrderLineListRenderer } from '@sale/js/sale_order_line_field/sale_order_line_field';
import {ProductLabelSectionAndNoteOne2Many } from '@account/components/product_label_section_and_note_field/product_label_section_and_note_field';



export class CustomSaleOrderLineListRenderer extends SaleOrderLineListRenderer {

    PAGE_BREAK_FIELD_NAME = 'add_page_break_after';


    isCellReadonly(column, record) {
        if (column.name === this.PAGE_BREAK_FIELD_NAME) {
            return false;
        }
        return super.isCellReadonly(column, record) || (
            this.isComboItem(record)
                && ![this.titleField, 'tax_id', 'qty_delivered', this.PAGE_BREAK_FIELD_NAME].includes(column.name)
        );
    }


    getCellClass(column, record) {
        const classNames = super.getCellClass(column, record);
        if (this.isSectionOrNote(record) && column.name === this.PAGE_BREAK_FIELD_NAME) {
            return classNames.replace('o_hidden', '').trim();
        }
        return classNames;
    }


    getColumns(record) {
        let columns = super.getColumns(record);
        if (this.isSectionOrNote(record)) {
            const addPageBreakAfterCol = this.columns.find(col => col.name === this.PAGE_BREAK_FIELD_NAME);
            if (addPageBreakAfterCol && !columns.find(col => col.name === this.PAGE_BREAK_FIELD_NAME)) {
                const titleFieldIdx = columns.findIndex(col => col.name === this.titleField);

                if (titleFieldIdx !== -1) {
                    if (columns[titleFieldIdx].colspan > 1) {
                        columns[titleFieldIdx].colspan -= 1;
                    }
                    columns.splice(titleFieldIdx, 0, addPageBreakAfterCol);
                } else {
                    columns.push(addPageBreakAfterCol);
                }
            }
        }
        return columns;
    }
}




import { saleOrderLineOne2Many } from '@sale/js/sale_order_line_field/sale_order_line_field';

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
