from odoo import models, fields


class Department(models.Model):
    _name = 'hms.department'
    _description = 'Hospitals Management System Department'

    name = fields.Char()
    capacity = fields.Integer()
    is_opened = fields.Boolean()
    patients = fields.One2many('hms.patient', 'department_id')
    doctors = fields.Many2many('hms.doctor')
