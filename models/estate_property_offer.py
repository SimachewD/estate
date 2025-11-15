from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"
    _order = "price desc"

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

    # === Action Methods ===
    def action_accept(self):
        for offer in self:
            # --- Only one accepted offer allowed ---
            if offer.property_id.offer_ids.filtered(lambda o: o.status == "accepted"):
                raise UserError("Only one offer can be accepted for a property.")

            offer.status = "accepted"

            # --- update the property ---
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id.id
            offer.property_id.state = "offer_accepted"

        return True

    def action_refuse(self):
        for offer in self:
            offer.status = "refused"
        return True
    
    # sql constraints to ensure price is positive
    _sql_constraints = [
        ('offer_price_positive', 'CHECK(price > 0)', 'Offer price must be strictly positive!'),
    ]