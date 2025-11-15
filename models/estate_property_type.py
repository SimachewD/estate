from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    _order = "sequence, name"

    name = fields.Char(string="Property Type", required=True)
    property_ids = fields.One2many(
        'estate.property',      # target model
        'property_type_id',     # the Many2one field on estate.property
        string="Properties"
    )
    sequence = fields.Integer(string="Sequence", default=10)

    # --- SQL Constraints ---
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Property type name must be unique!'),
    ]