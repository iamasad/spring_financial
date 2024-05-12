# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request, route
from odoo.exceptions import ValidationError
import json


class ContactAPI(http.Controller):

    def validation(self, data):
        field_list = {
            "name": (str, True),
            "phone": (str, False),
            "email": (str, False),
            "street": (str, False),
            "city": (str, False),
            "zip": (str, False),
            "state_id": (str, False),
            "country_id": (str, False),
        }
        required = list(filter(lambda k: field_list[k][1], field_list.keys()))
        valid_fields = list(
            filter(
                lambda k: (k in data.keys() and bool(str(data[k]).strip()))
                and type(data[k]) == field_list[k][0],
                required,
            )
        )
        fields = list(set(required) - set(valid_fields))
        if any(fields):
            return (
                False,
                "Following fields are required and missing or are not in correct format: %s"
                % (", ".join(fields)),
            )
        return (True, "")

    def _prepare_contact_values_dict(self, kwargs):
        errors = []
        name = kwargs.get("name", "")
        phone = kwargs.get("phone", "")
        email = kwargs.get("email", "")
        street = kwargs.get("street", "")
        city = kwargs.get("city", "")
        zip = kwargs.get("zip", "")
        state = kwargs.get("state", "")
        country = kwargs.get("country", "")
        state_id = (
            request.env["res.country.state"]
            .sudo()
            .search([("code", "=", state)], limit=1)
        )
        country_id = (
            request.env["res.country"].sudo().search([("name", "=", country)], limit=1)
        )
        if not country_id:
            errors.append(("Country", country))
        if not state_id:
            errors.append(("State", state))
        if errors:
            raise ValidationError(
                "%s not found !"
                % (", ".join("%s: '%s'" % (x[0], x[1]) for x in errors))
            )
        return {
            "name": name,
            "phone": phone,
            "email": email,
            "street": street,
            "city": city,
            "zip": zip,
            "state_id": state_id.id,
            "country_id": country_id.id,
        }

    @route("/api/create_contact", type="json", auth="user", methods=["POST"], csrf=False)
    def create_contact(self, **kwargs):
        try:
            payload = json.loads(request.httprequest.data)
            status, message = self.validation(payload)
            if status:
                try:
                    contact_values = self._prepare_contact_values_dict(payload)
                    contact = request.env["res.partner"].sudo().create(contact_values)
                    status = True
                    message = (
                        "Contact successfully created in Odoo with ID: %s" % contact.id
                    )
                except Exception as e:
                    return {"status": False, "message": str(e)}
            return {"status": status, "message": message}
        except Exception as e:
            return {"status": False, "message": str(e)}
