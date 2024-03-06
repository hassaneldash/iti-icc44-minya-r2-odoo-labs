from dateutil.relativedelta import relativedelta
from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError


class Patient(models.Model):
    _name = 'hms.patient'
    _description = 'Hospitals Management System Patient'

    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    birth_date = fields.Date(required=True)
    email = fields.Char(string='Email', unique=True)
    history = fields.Html(string='History')
    cr_ratio = fields.Float(string='CR Ratio')
    blood_type = fields.Selection(
        [('a', 'A'), ('b', 'B'), ('ab', 'AB'), ('o', 'O')], required=True)
    rhesus_protein = fields.Selection(
        [('positive', '+'), ('negative', '-')], required=True)
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
        default='undetermined', required=True,
        track_visibility='onchange'
    )
    department_id = fields.Many2one('hms.department', string='Department', required=True)
    department_capacity = fields.Integer(string='Department Capacity', related='department_id.capacity', store=True)
    doctor_ids = fields.Many2many('hms.doctor', string='Doctors', readonly=True)

    @api.depends('birth_date')
    def _compute_age(self):
        for patient in self:
            if patient.birth_date:
                patient.age = relativedelta(fields.Date.today(), patient.birth_date).years
            else:
                patient.age = False

    @api.depends('state')
    def _compute_history_log(self):
        for patient in self:
            if patient.state == 'undetermined':
                patient.history_log = 'Patient state is undetermined.'
            elif patient.state == 'good':
                patient.history_log = 'Patient state is good.'
            elif patient.state == 'fair':
                patient.history_log = 'Patient state is fair.'
            elif patient.state == 'serious':
                patient.history_log = 'Patient state is serious.'

    @api.onchange('birth_date')
    def _onchange_pcr(self):
        if self.age < 30:
            self.pcr = True
            raise Warning('PCR is automatically checked because the age is lower than 30.')

    @api.onchange('state')
    def _onchange_state(self):
        self._create_log_record()
        for patient in self:
            if patient.age > 50:
                patient.history = patient._compute_log_history()
            else:
                patient.history = False

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
                raise ValidationError('You cannot choose a closed department.')

    # @api.onchange('department_id')
    # def _onchange_department_id(self):
    #     for patient in self:
    #         if patient.department_id:
    #             patient.doctor_ids = [(6, 0, patient.department_id.doctor_ids.ids)]

    @api.onchange('pcr')
    def _onchange_pcr(self):
        for patient in self:
            if patient.pcr and not patient.cr_ratio:
                raise ValidationError('CR Ratio is mandatory when PCR is checked.')

    # @api.onchange('age')
    # def _onchange_age(self):
    #     for patient in self:
    #         if patient.age < 50:
    #             patient.history = False
    #         else:
    #             patient.history = patient._compute_log_history()
    #         if patient.age < 30:
    #             patient.pcr = True
    #             raise Warning('PCR is automatically checked because the age is lower than 30.')

    @api.constrains('email')
    def _check_valid_email(self):
        for patient in self:
            if patient.email and '@' not in patient.email:
                raise ValidationError("Invalid email address")