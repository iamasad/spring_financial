# -*- coding: utf-8 -*-
{
    "name": "Spring Financial Tasks",
    "summary": "Spring Financial - Technical Assignment",
    "description": """
        Spring Financial - Technical Assignment
    """,
    "author": "Md Asadullah",
    "website": "https://www.linkedin.com/in/a4asad/",
    "category": "Spring Financial",
    "version": "1.0",
    "application": True,
    "depends": [
        "base",
        "web",
        "crm",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/crm_stage_data.xml",
        "views/crm_lead_views.xml",
        "views/crm_stage_views.xml",
        "views/menu_items.xml",
    ],
}
