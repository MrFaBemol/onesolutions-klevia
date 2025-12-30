from odoo import fields, models, _
from odoo.exceptions import ValidationError


class ProtectedRecordMixin(models.AbstractModel):
    _name = "protected.record.mixin"
    _description = "protected.record.mixin"

    protected = fields.Boolean(default=False, help="If True, record cannot be deleted (only archived).")

    def unlink(self):
        for rec in self:
            if rec.protected:
                raise ValidationError(_("This record is protected and cannot be deleted. Archive it instead. (%s)" % rec))
        return super().unlink()
