from odoo import api, fields, models


class Partner(models.Model):
    _inherit = "res.partner"
    _name = "res.partner"

    instructor = fields.Boolean("instructor", default=False)
    session_ids = fields.Many2many(
        'test.session', string="Attended Sessions", readonly=True)
