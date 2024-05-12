# -*- coding: utf-8 -*-

from odoo import models, api, _
from odoo.exceptions import UserError


class Lead2OpportunityPartner(models.TransientModel):
    _inherit = 'crm.lead2opportunity.partner'

    @api.model
    def default_get(self, fields):
        result = super(Lead2OpportunityPartner, self).default_get(fields)
        if result.get('lead_id'):
            lead = self.env['crm.lead'].browse(result['lead_id'])
            if lead and not lead.lead_stage_id.is_complete:
                raise UserError(_("Only complete leads can be converted into opportunities."))
        return result

    def _convert_and_allocate(self, leads, user_ids, team_id=False):
        incomplete_leads = leads.filtered(lambda l: not l.lead_stage_id.is_complete)
        if incomplete_leads:
            raise UserError(_("Only complete leads can be converted into opportunities."))
        leads = leads.filtered(lambda l: l.lead_stage_id.is_complete)
        duplicate_leads = self.env['crm.lead']
        for lead in leads:
            duplicate_leads |= lead.copy({'opportunity_type': 'Business'})
        leads.write({'opportunity_type': 'Technology'})
        leads |= duplicate_leads
        super()._convert_and_allocate(leads, user_ids, team_id)
