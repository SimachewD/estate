from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"

    name = fields.Char(string="Property Type", required=True)

    # --- SQL Constraints ---
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Property type name must be unique!'),
    ]