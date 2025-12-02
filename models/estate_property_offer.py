from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"
    _order = "price desc"
    _rec_name = 'sequence' 

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
    sequence = fields.Char(
        string="Reference",
        readonly=True,
        copy=False,
        default="New"
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
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # 1) get the property record
            property_id = vals.get('property_id')
            property_record = self.env['estate.property'].browse(property_id)

            # Safety: ensure record exists
            if not property_record.exists():
                raise UserError("Invalid Property")

            # 2) Check if price is lower than an existing offer
            existing_prices = property_record.offer_ids.mapped('price')
            if existing_prices and vals.get('price', 0) < max(existing_prices):
                raise UserError(
                    "You cannot create an offer lower than an existing offer."
                )

            # 3) Set property state to offer_received (only if state is 'new')
            if property_record.state == 'new':
                property_record.state = 'offer_received'
            
            # 4) create sequence number for each record
            if vals.get('sequence', "New") == "New":
                vals['sequence'] = self.env['ir.sequence'].next_by_code("estate.property.offer") or "New"

        # 5) Call super() once for all values
        return super().create(vals_list)
    
    # sql constraints to ensure price is positive
    _sql_constraints = [
        ('offer_price_positive', 'CHECK(price > 0)', 'Offer price must be strictly positive!'),
    ]