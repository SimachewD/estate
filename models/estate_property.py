from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import UserError , ValidationError

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "id desc"

    # Basic property info
    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")

    # Location and type / Relationships
    postcode_id = fields.Many2one(
                    'estate.postcode', 
                    string="Postcode"
                )
    property_type_id = fields.Many2one(
                        'estate.property.type',
                        string="Property Type"
                    )
    
    # Default availability date → 3 months from today
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=lambda self: fields.Date.today() + timedelta(days=90)
    )
    
    # Pricing
    expected_price = fields.Float(string="Expected Price", required=True, tracking=True)
    selling_price = fields.Float(
        string="Selling Price",
        readonly=True,
        copy=False,
        tracking=True
    )

    # Currency
    currency_id = fields.Many2one(
        'res.currency', 
        string='Currency', 
        default=lambda self: self.env.company.currency_id
    )

    # Property details
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")

     # ✅ New computed field
    total_area = fields.Integer(
        string="Total Area (sqm)",
        compute="_compute_total_area",
        store=True
    )

    best_price = fields.Float(
        string="Best Offer",
        compute="_compute_best_price",
        store=True
    )
    
    garden_orientation = fields.Selection(
        [
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        string="Garden Orientation"
    )

    # === New fields ===
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        string="Status",
        required=True,
        copy=False,
        default="new",
        tracking=True
    )

    # Relationships
    salesperson_id = fields.Many2one(
        'res.users',
        string="Salesperson",
        default=lambda self: self.env.user
    )

    buyer_id = fields.Many2one(
        'res.partner',
        string="Buyer",
        copy=False
    )

    offer_ids = fields.One2many(
        'estate.property.offer',
        'property_id',
        string="Offers"
    )   

    tag_ids = fields.Many2many(
        'estate.property.tag',
        string="Tags"
    )

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = (record.living_area or 0) + (record.garden_area or 0)

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        """Auto-set defaults when garden is true, clear when false."""
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = False
            self.garden_orientation = False

    @api.onchange("date_availability")
    def _onchange_date_availability(self):
        """Soft warning if availability date is before today"""
        if self.date_availability and self.date_availability < fields.Date.today():
            return {
                "warning": {
                    "title": "Invalid Availability Date",
                    "message": "The availability date cannot be earlier than today.",
                }
            }

    @api.ondelete(at_uninstall=False)
    def _unlink_if_allowed(self):
        """
        Prevent deletion unless state is 'new' or 'canceled'.
        Remember: self may contain multiple records.
        """
        for record in self:
            if record.state not in ['new', 'canceled']:
                raise UserError(
                    "You can only delete properties that are New or Canceled."
                )
    
     # --- BUTTON ACTIONS ---
    def action_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError("Canceled properties cannot be sold.")
            if record.state == 'sold':
                raise UserError("This property is already sold.")
            record.state = 'sold'
        return True

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold properties cannot be canceled.")
            record.state = 'canceled'
        return True

    # --- SQL Constraints ---
    _sql_constraints = [
        ('expected_price_positive', 'CHECK(expected_price > 0)', 'Expected price must be strictly positive!'),
        ('selling_price_positive', 'CHECK(selling_price >= 0)', 'Selling price must be positive!'),
    ]

     # --- Python Constraint ---
    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price and record.expected_price:
                min_allowed = record.expected_price * 0.9
                if record.selling_price < min_allowed:
                    raise ValidationError(
                        f"Selling price ({record.selling_price}) cannot be lower than 90% of the expected price ({record.expected_price})."
                    )