from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"

    name = fields.Char(string="Tag Name", required=True)

    # --- SQL Constraints ---
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Tag name must be unique!'),
    ]