from odoo import models, fields


class Department(models.Model):
    _name = 'hms.department'
    _description = 'Hospitals Management System Department'

    name = fields.Char(string='Name')
    capacity = fields.Integer(string='Capacity')
    is_opened = fields.Boolean(string='Is Opened')
    patients = fields.One2many('hms.patient', 'department_id', string='Patients')
