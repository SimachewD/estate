from odoo import fields, models

class EstatePropertyAccounting(models.Model):
    _name = "estate.property.accounting"
    _description = "Property Accounting"
    _inherits = {
        "estate.property": "property_id"
    }

    property_id = fields.Many2one(
        "estate.property",
        required=True,
        ondelete="cascade"
    )

    accounting_code = fields.Char()
    tax_rate = fields.Float()
