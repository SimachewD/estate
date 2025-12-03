from odoo import models, fields

class EstatePostcode(models.Model):
    _name = "estate.postcode"
    _description = "Postcode"

    name = fields.Char(string="Postcode", required=True)
