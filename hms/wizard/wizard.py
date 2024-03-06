from odoo import fields, models


class AddLog(models.TransientModel):
    _name = 'log.wizard'
    _description = 'Add Patient Log Wizard'

    patient_id = fields.Many2one('hms.patient', string="Patient", required=True, default=lambda self: self.env.context.get('active_id'))
    description = fields.Text(string="Description", required=True)

    def add_log(self):
        log_vals = {
            'patient_id': self.patient_id.id,
            'description': self.description,
        }
        patient_log = self.env['hms.patient.log'].create(log_vals)
        return {'type': 'ir.actions.act_window_close'}