from odoo import models, fields
from datetime import datetime


class Patient(models.Model):
    _name = 'hms.patient'
    _description = 'Hospitals Management System Patient'

    first_name = fields.Char(string='First Name')
    last_name = fields.Char(string='Last Name')
    birth_date = fields.Date(string='Birth Date')
    history = fields.Html(string='History')
    cr_ratio = fields.Float(string='CR Ratio')
    blood_type = fields.Selection(
        [('A+', 'A+'), ('B+', 'B+'), ('AB+', 'AB+'), ('O+', 'O+'), ('A-', 'A-'), ('B-', 'B-'), ('AB-', 'AB-'),
         ('O-', 'O-')], string='Blood Type')
    pcr = fields.Boolean(string='PCR')
    image = fields.Binary(string='Image')
    address = fields.Text(string='Address')
    age = fields.Integer(string='Age', compute='_compute_age')

    def _compute_age(self):
        today = datetime.today()
        for patient in self:
            if patient.birth_date:
                birth_date = datetime.strptime(patient.birth_date, '%Y-%m-%d')
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                patient.age = age
