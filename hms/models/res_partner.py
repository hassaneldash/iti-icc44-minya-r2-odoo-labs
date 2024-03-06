from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one('hms.patient', string='Related Patient')

    @api.constrains('email')
    def _check_email_unique_in_patient(self):
        for partner in self:
            if partner.email and self.env['hms.patient'].search_count([('email', '=', partner.email)]):
                raise ValidationError("Email already exists in patient records")

    def unlink(self):
        for partner in self:
            if partner.related_patient_id:
                raise ValidationError("You cannot delete a customer linked to a patient")
        return super(ResPartner, self).unlink()

