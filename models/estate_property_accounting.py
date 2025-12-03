from odoo import fields, models, api

class EstatePropertyAccounting(models.Model):
    _name = "estate.property.accounting"
    _description = "Property Accounting"
    _inherits = {
        "estate.property": "property_id"
    }
    _rec_name = 'accounting_sequence' 

    property_id = fields.Many2one(
        "estate.property",
        required=True,
        ondelete="cascade"
    )

    accounting_code = fields.Char()
    tax_rate = fields.Float()
    accounting_sequence = fields.Char(
        string="Reference",
        readonly=True,
        copy=False,
        default="New"
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('accounting_sequence', "New") == "New":
                vals['accounting_sequence'] = self.env['ir.sequence'].next_by_code("estate.property.accounting") or "New"
        return super().create(vals_list)