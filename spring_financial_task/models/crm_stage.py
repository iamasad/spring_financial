# -*- coding: utf-8 -*-

from odoo import api, fields, models


class LeadStage(models.Model):
    _name = 'crm.lead.stage'
    _description = 'CRM Lead Stages'
    _order = 'sequence, name, id'

    @api.model
    def default_get(self, fields):
        if 'default_team_id' in self.env.context:
            ctx = dict(self.env.context)
            ctx.pop('default_team_id')
            self = self.with_context(ctx)
        return super(LeadStage, self).default_get(fields)

    name = fields.Char(string='Stage Name', required=True, translate=True)
    sequence = fields.Integer(string='Sequence', default=1)
    is_complete = fields.Boolean(string='Is Complete Stage?')
    requirements = fields.Text(string='Requirements')
    team_id = fields.Many2one(comodel_name='crm.team', string='Sales Team', ondelete='set null')
    fold = fields.Boolean(string='Folded in Pipeline')
    team_count = fields.Integer(string='team_count', compute='_compute_team_count')

    @api.depends('team_id')
    def _compute_team_count(self):
        self.team_count = self.env['crm.team'].search_count([])
