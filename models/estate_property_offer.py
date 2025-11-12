from odoo import models, fields, api
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"

    price = fields.Float(string="Offer Price")

    status = fields.Selection(
        [
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        string="Status",
        copy=False
    )

    partner_id = fields.Many2one(
        'res.partner',
        string="Buyer",
        required=True
    )

    property_id = fields.Many2one(
        'estate.property',
        string="Property",
        required=True
    )

    # Related field
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
        related="property_id.property_type_id",
        store=True,
    )

     # === New Fields ===
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True,
    )

    # ✅ Compute function
    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        """Compute the deadline as create_date + validity days"""
        for record in self:
            create_date = record.create_date or fields.Datetime.now()
            record.date_deadline = (create_date + timedelta(days=record.validity)).date()

    # ✅ Inverse function
    def _inverse_date_deadline(self):
        """When user changes the deadline, adjust the validity"""
        for record in self:
            create_date = record.create_date or fields.Datetime.now()
            if record.date_deadline:
                delta = record.date_deadline - create_date.date()
                record.validity = delta.days