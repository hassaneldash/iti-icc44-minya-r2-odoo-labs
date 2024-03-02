from odoo import models, fields, api
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
        [('a', 'A'), ('b', 'B'), ('ab', 'AB'), ('o', 'O')], string='Blood Type')
    pcr = fields.Boolean(string='PCR')
    image = fields.Binary(string='Image')
    address = fields.Text(string='Address')
    age = fields.Integer(string='Age', compute='_compute_age')
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious')],
        string='State',
        default='undetermined',
        track_visibility='onchange')

    # def _compute_age(self):
    #     today = datetime.today()
    #     for patient in self:
    #         if patient.birth_date:
    #             birth_date = datetime.strptime(patient.birth_date, '%Y-%m-%d')
    #             age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    #             patient.age = age

    department_id = fields.Many2one('hms.department', string='Department', required=True)
    doctor_ids = fields.Many2many('hms.doctor', string='Doctors', readonly=True)

    @api.depends('birth_date')
    def _compute_age(self):
        for patient in self:
            if patient.birth_date:
                birth_date = fields.Date.from_string(patient.birth_date)
                today = fields.Date.today()
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                patient.age = age

    @api.depends('age')
    def _compute_history(self):
        for patient in self:
            if patient.age < 50:
                patient.history = False
            else:
                patient.history = patient._compute_log_history()

    def _compute_log_history(self):
        # Logic to compute patient history log
        return "Patient history log"

    @api.onchange('age')
    def _onchange_pcr(self):
        if self.age < 30:
            self.pcr = True
            raise Warning('PCR is automatically checked because the age is lower than 30.')

    @api.onchange('state')
    def _onchange_state(self):
        self._create_log_record()

    def _create_log_record(self):
        log_description = f'State changed to {self.state.upper()}'
        self.env['hms.patient.log'].create({
            'patient_id': self.id,
            'created_by': self.env.user.id,
            'description': log_description
        })

    @api.constrains('department_id')
    def _check_department_is_opened(self):
        for patient in self:
            if patient.department_id and not patient.department_id.is_opened:
                raise exceptions.ValidationError('You cannot choose a closed department.')

    @api.onchange('department_id')
    def _onchange_department_id(self):
        for patient in self:
            if patient.department_id:
                patient.doctor_ids = [(6, 0, patient.department_id.doctor_ids.ids)]

    @api.onchange('pcr')
    def _onchange_pcr(self):
        for patient in self:
            if patient.pcr and not patient.cr_ratio:
                raise exceptions.ValidationError('CR Ratio is mandatory when PCR is checked.')

    @api.onchange('age')
    def _onchange_age(self):
        for patient in self:
            if patient.age < 50:
                patient.history = False
            else:
                patient.history = patient._compute_log_history()
            if patient.age < 30:
                raise Warning('PCR is automatically checked because the age is lower than 30.')
                patient.pcr = True
