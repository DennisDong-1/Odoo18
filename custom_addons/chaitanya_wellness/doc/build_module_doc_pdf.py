# -*- coding: utf-8 -*-
"""Generate Chaitanya_Wellness_Module_Documentation.pdf and copy to Downloads."""
import shutil
from pathlib import Path

from fpdf import FPDF

DOC_DIR = Path(__file__).resolve().parent
OUT_PDF = DOC_DIR / "Chaitanya_Wellness_Module_Documentation.pdf"
DOWNLOADS_COPY = Path.home() / "Downloads" / "Chaitanya_Wellness_Module_Documentation.pdf"


class DocPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=14)

    def header(self):
        self.set_font("Helvetica", "B", 11)
        self.cell(
            0,
            8,
            "Chaitanya Wellness - Technical Documentation",
            new_x="LMARGIN",
            new_y="NEXT",
        )
        self.set_font("Helvetica", size=9)
        self.cell(
            0,
            5,
            "Odoo 18 | Module: chaitanya_wellness | Version 18.0.1.0.0",
            new_x="LMARGIN",
            new_y="NEXT",
        )
        self.ln(2)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 8, f"Page {self.page_no()}", align="C")


def section(pdf: DocPDF, title: str):
    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 11)
    pdf.multi_cell(pdf.epw, 6, title)
    pdf.set_font("Helvetica", size=10)


def body(pdf: DocPDF, text: str):
    pdf.multi_cell(pdf.epw, 5, text)
    pdf.ln(1)


def main():
    pdf = DocPDF()
    pdf.set_margins(18, 20, 18)
    pdf.add_page()

    body(
        pdf,
        "Executive summary: Custom Odoo 18 application for spa and wellness operations. "
        "Implements service categories, services (duration, pricing, slot step), therapists, "
        "and weekly working hours. Backend application menu for staff. Website booking, "
        "customer appointments, payments, and vouchers are planned for a later phase.",
    )

    section(pdf, "1. Module metadata")
    body(
        pdf,
        "Technical name: chaitanya_wellness\n"
        "Display name: Chaitanya Wellness\n"
        "Author: Dennis Dong | License: LGPL-3\n"
        "Depends: base, mail\n"
        "Application: Yes (root app menu)\n"
        "Category: Website (future public booking)",
    )

    section(pdf, "2. File structure")
    body(
        pdf,
        "models/: service_category.py, service.py, provider.py, working_day.py\n"
        "views/: service_category_views.xml, service_views.xml, provider_views.xml, menus.xml\n"
        "data/: service_category_data.xml (5 categories, noupdate=1)\n"
        "security/: ir.model.access.csv (base.group_user on all models)\n"
        "doc/: MODULE_DOCUMENTATION.md, this PDF, build_module_doc_pdf.py",
    )

    section(pdf, "3. Model: chaitanya.wellness.service.category")
    body(
        pdf,
        "Fields: name (required, translate), sequence, active, description (html), "
        "website_published, service_ids (one2many), service_count (computed via read_group).\n"
        "Order: sequence, name. Delete: services use ondelete restrict on category_id.",
    )

    section(pdf, "4. Model: chaitanya.wellness.service")
    body(
        pdf,
        "Fields: name, active, sequence, website_published, category_id (many2one), "
        "duration_minutes (default 60, required), slot_step_minutes (default 15), "
        "price (monetary), currency_id, description, benefits, provider_ids (many2many).\n"
        "duration_minutes and slot_step_minutes support future slot generation logic.",
    )

    section(pdf, "5. Model: chaitanya.wellness.provider")
    body(
        pdf,
        "Fields: name (translate), active, bio (html profile), partner_id (optional res.partner), "
        "service_ids (many2many), working_day_ids (one2many).\n"
        "Therapists are linked to services they can perform.",
    )

    section(pdf, "6. Model: chaitanya.wellness.working_day")
    body(
        pdf,
        "Fields: provider_id (required, cascade delete), weekday (0=Mon .. 6=Sun), "
        "start_time and end_time as float hours (9.5 = 09:30).\n"
        "Constraint: end_time must be greater than start_time or save is blocked.",
    )

    section(pdf, "7. Many2many relation table")
    body(
        pdf,
        "Table name: chaitanya_wellness_provider_service_rel\n"
        "Columns: provider_id, service_id\n"
        "Defined on both provider.service_ids and service.provider_ids with matching table name.",
    )

    section(pdf, "8. Seed data (categories)")
    body(
        pdf,
        "Spa (10), Ayurveda (20), Massage (30), Beauty (40), Wellness (50). "
        "Loaded from data/service_category_data.xml with noupdate=1.",
    )

    section(pdf, "9. Security")
    body(
        pdf,
        "Internal users (base.group_user) have full CRUD on all four custom models via "
        "security/ir.model.access.csv.",
    )

    section(pdf, "10. Backend menus")
    body(
        pdf,
        "Root: Chaitanya Wellness\n"
        "  - Service Categories (seq 20)\n"
        "  - Services (seq 25)\n"
        "  - Therapists (seq 30)\n"
        "Provider form: Profile, Services (tags), Working hours (inline list, float_time).",
    )

    pdf.add_page()
    section(pdf, "11. Manifest data load order")
    body(
        pdf,
        "1. security/ir.model.access.csv\n"
        "2. data/service_category_data.xml\n"
        "3. views/service_category_views.xml\n"
        "4. views/service_views.xml\n"
        "5. views/provider_views.xml\n"
        "6. views/menus.xml (must be last - references actions)",
    )

    section(pdf, "12. Installation")
    body(
        pdf,
        "Mount custom_addons on Odoo addons path. Update Apps list. Install Chaitanya Wellness. "
        "After changes: Upgrade module. Ensure __manifest__.py is valid Python (commas in data list).",
    )

    section(pdf, "13. Booking flow alignment (not yet built)")
    body(
        pdf,
        "Supported now: category browse, service master data, therapist profiles, working hours.\n"
        "Not yet: booking record, slot APIs (book by therapist / by availability), website UI, "
        "payment, vouchers, gifts, confirmation PDF.",
    )

    section(pdf, "14. Roadmap")
    body(
        pdf,
        "Phase A: Booking model + overlap rules + availability helpers (timezone-aware).\n"
        "Phase B: website + portal dependencies, controllers, QWeb pages.\n"
        "Phase C: payment, vouchers, gift flow per product design.",
    )

    section(pdf, "15. Document info")
    body(
        pdf,
        "Full editable source: doc/MODULE_DOCUMENTATION.md in the module folder.\n"
        "Regenerate PDF: python doc/build_module_doc_pdf.py\n"
        "Revision: May 2026 - Dennis Dong - initial technical documentation.",
    )

    pdf.output(str(OUT_PDF))
    print("Wrote", OUT_PDF)

    try:
        shutil.copy2(OUT_PDF, DOWNLOADS_COPY)
        print("Copied to", DOWNLOADS_COPY)
    except OSError as exc:
        print("Could not copy to Downloads:", exc)


if __name__ == "__main__":
    main()
