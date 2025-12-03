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
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_type_id",
        string="Offers"
    )
    sequence = fields.Integer(string="Sequence", default=10)

    offer_count = fields.Integer(
        compute="_compute_offer_count",
        string="Offer Count"
    )

    # ✅ Compute method
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    # ✅ Action method to open related offers
    def action_open_estate_property_offers(self):
        """Return an action that opens the offers related to this property type"""
        self.ensure_one()
        return {
            'name': 'Property Offers',
            'type': 'ir.actions.act_window',
            'res_model': 'estate.property.offer',
            'view_mode': 'tree,form',
            'domain': [('property_type_id', '=', self.id)],
            'context': {'default_property_type_id': self.id},
        }

    # --- SQL Constraints ---
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Property type name must be unique!'),
    ]