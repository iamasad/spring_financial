# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID
from odoo.addons.crm.models.crm_lead import CRM_LEAD_FIELDS_TO_MERGE

CRM_LEAD_FIELDS_TO_MERGE += ["lead_stage_id"]


class Lead(models.Model):
    _inherit = "crm.lead"

    opportunity_type = fields.Selection(
        selection=[("Technology", "Technology"), ("Business", "Business")],
        string="Opportunity Type",
        tracking=True,
        index=True,
    )
    opportunity_name = fields.Text(string="Opportunity Name")
    lead_stage_id = fields.Many2one(
        comodel_name="crm.lead.stage",
        string="Lead Stage",
        index=True,
        tracking=True,
        compute="_compute_lead_stage_id",
        readonly=False,
        store=True,
        copy=False,
        group_expand="_read_group_lead_stage_ids",
        ondelete="restrict",
        domain="['|', ('team_id', '=', False), ('team_id', '=', team_id)]",
    )
    is_lead_complete = fields.Boolean(
        string="Is Lead Complete?", related="lead_stage_id.is_complete", store=True
    )

    @api.depends("team_id", "type")
    def _compute_lead_stage_id(self):
        for lead in self:
            if not lead.lead_stage_id:
                lead.lead_stage_id = lead._lead_stage_find(
                    domain=[("fold", "=", False)]
                ).id

    @api.model
    def _read_group_lead_stage_ids(self, lead_stages, domain, order):
        team_id = self._context.get("default_team_id")
        if team_id:
            search_domain = [
                "|",
                ("id", "in", lead_stages.ids),
                "|",
                ("team_id", "=", False),
                ("team_id", "=", team_id),
            ]
        else:
            search_domain = [
                "|",
                ("id", "in", lead_stages.ids),
                ("team_id", "=", False),
            ]
        lead_stage_ids = lead_stages._search(
            search_domain, order=order, access_rights_uid=SUPERUSER_ID
        )
        return lead_stages.browse(lead_stage_ids)

    def _lead_stage_find(
        self, team_id=False, domain=None, order="sequence, id", limit=1
    ):
        team_ids = set()
        if team_id:
            team_ids.add(team_id)
        for lead in self:
            if lead.team_id:
                team_ids.add(lead.team_id.id)
        if team_ids:
            search_domain = [
                "|",
                ("team_id", "=", False),
                ("team_id", "in", list(team_ids)),
            ]
        else:
            search_domain = [("team_id", "=", False)]
        if domain:
            search_domain += list(domain)
        return self.env["crm.lead.stage"].search(
            search_domain, order=order, limit=limit
        )
