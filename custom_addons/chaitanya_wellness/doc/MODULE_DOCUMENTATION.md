# Chaitanya Wellness — Technical Documentation

| | |
|---|---|
| **Module** | `chaitanya_wellness` |
| **Odoo** | 18.0 |
| **Version** | 18.0.1.0.0 |
| **Author** | Dennis Dong |
| **License** | LGPL-3 |
| **Document date** | May 2026 |
| **Status** | Backend catalog & scheduling foundation complete; bookings and website pending |

---

## 1. Executive summary

**Chaitanya Wellness** is a custom Odoo 18 application for spa and wellness operations. It implements the data layer required before public booking: **service categories**, **services** (duration, pricing, slot grid step), **therapists (providers)**, and **weekly working hours**.

The module installs as an **application** with a dedicated root menu. Internal users manage master data from the backend. Website booking, customer bookings, payments, vouchers, and gifts are **out of scope** for this release and listed in the roadmap.

---

## 2. Dependencies

| Module | Purpose |
|--------|---------|
| `base` | Core platform |
| `mail` | Reserved for future chatter on booking records |

**Planned later:** `website`, `portal`, `payment`, `auth_signup`.

---

## 3. Repository structure

```
custom_addons/chaitanya_wellness/
├── __init__.py
├── __manifest__.py
├── doc/
│   ├── MODULE_DOCUMENTATION.md
│   ├── Chaitanya_Wellness_Module_Documentation.pdf
│   └── build_module_doc_pdf.py
├── data/
│   └── service_category_data.xml
├── models/
│   ├── __init__.py
│   ├── service_category.py
│   ├── service.py
│   ├── provider.py
│   └── working_day.py
├── security/
│   └── ir.model.access.csv
└── views/
    ├── menus.xml
    ├── service_category_views.xml
    ├── service_views.xml
    └── provider_views.xml
```

---

## 4. Manifest and load order

```python
'depends': ['base', 'mail'],
'data': [
    'security/ir.model.access.csv',
    'data/service_category_data.xml',
    'views/service_category_views.xml',
    'views/service_views.xml',
    'views/provider_views.xml',
    'views/menus.xml',
],
'application': True,
```

**Load order rationale:** Security and seed data first; view files define window actions; `menus.xml` last so menu items can reference actions.

---

## 5. Data models

### 5.1 `chaitanya.wellness.service.category`

**Table:** `chaitanya_wellness_service_category`  
**Order:** `sequence, name`

| Field | Type | Description |
|-------|------|-------------|
| `name` | Char | Required; translatable |
| `sequence` | Integer | Default 10; list drag order |
| `active` | Boolean | Archive flag |
| `description` | Html | Translatable category copy |
| `website_published` | Boolean | Future website filter |
| `service_ids` | One2many → service | Inverse: `category_id` |
| `service_count` | Integer (computed) | Count of linked services via `read_group` |

**Business rules:** Services reference category with `ondelete='restrict'` — categories in use cannot be deleted.

---

### 5.2 `chaitanya.wellness.service`

**Table:** `chaitanya_wellness_service`  
**Order:** `category_id, sequence, name`

| Field | Type | Description |
|-------|------|-------------|
| `name` | Char | Required; translatable |
| `active` | Boolean | |
| `sequence` | Integer | Default 10 |
| `website_published` | Boolean | Future website filter |
| `category_id` | Many2one → category | `ondelete='restrict'` |
| `duration_minutes` | Integer | Required; default 60 — appointment length |
| `slot_step_minutes` | Integer | Default 15 — grid step for slot generation |
| `price` | Monetary | Uses `currency_id` |
| `currency_id` | Many2one → `res.currency` | Company default |
| `description` | Html | Overview; translatable |
| `benefits` | Html | Benefits copy; translatable |
| `provider_ids` | Many2many → provider | Therapists who perform this service |

---

### 5.3 `chaitanya.wellness.provider`

**Table:** `chaitanya_wellness_provider`  
**Order:** `name`

| Field | Type | Description |
|-------|------|-------------|
| `name` | Char | Required; translatable |
| `active` | Boolean | |
| `bio` | Html | Therapist profile |
| `partner_id` | Many2one → `res.partner` | Optional CRM/contact link |
| `service_ids` | Many2many → service | Services offered |
| `working_day_ids` | One2many → working_day | Weekly schedule lines |

---

### 5.4 `chaitanya.wellness.working_day`

**Table:** `chaitanya_wellness_working_day`  
**Order:** `provider_id, weekday`

| Field | Type | Description |
|-------|------|-------------|
| `provider_id` | Many2one → provider | Required; `ondelete='cascade'` |
| `weekday` | Selection | `'0'` Monday … `'6'` Sunday |
| `start_time` | Float | 24h fractional (9.5 = 09:30) |
| `end_time` | Float | 24h fractional (17.0 = 17:00) |

**Constraint `_check_times`:** `end_time` must be strictly greater than `start_time`; otherwise `ValidationError`.

---

## 6. Relations diagram

```
Service Category (1) ──────< (N) Service
                                    │
                    Many2many (chaitanya_wellness_provider_service_rel)
                                    │
Provider (1) ──────< (N) Working Day
```

**Relation table:** `chaitanya_wellness_provider_service_rel`  
**Columns:** `provider_id`, `service_id`  
Must be identical on `provider.service_ids` and `service.provider_ids` (column order swapped on the inverse side).

---

## 7. Seed data

**File:** `data/service_category_data.xml`  
**Flag:** `noupdate="1"` (upgrades do not overwrite renamed categories)

| XML ID | Name | Sequence |
|--------|------|----------|
| `category_spa` | Spa | 10 |
| `category_ayurveda` | Ayurveda | 20 |
| `category_massage` | Massage | 30 |
| `category_beauty` | Beauty | 40 |
| `category_wellness` | Wellness | 50 |

---

## 8. Security

**File:** `security/ir.model.access.csv`

All four custom models grant **read, write, create, unlink** to **`base.group_user`** (internal employees).

| Access ID | Model |
|-----------|--------|
| `access_chaitanya_wellness_service_category` | `chaitanya.wellness.service.category` |
| `access_chaitanya_wellness_service` | `chaitanya.wellness.service` |
| `access_chaitanya_wellness_provider` | `chaitanya.wellness.provider` |
| `access_chaitanya_wellness_working_day` | `chaitanya.wellness.working_day` |

---

## 9. Backend user interface

| Menu (sequence) | Window action | Model |
|-----------------|---------------|--------|
| Chaitanya Wellness (root) | — | — |
| Service Categories (20) | `action_chaitanya_wellness_service_category` | Category |
| Services (25) | `action_chaitanya_wellness_service` | Service |
| Therapists (30) | `action_chaitanya_wellness_provider` | Provider |

**Category views:** List (sequence handle, name, service_count, published, active); form (metadata + description).

**Service views:** List (sequence, name, category, duration, price, published, active); form (pricing group, notebook: overview, benefits, therapists).

**Provider views:** List (name, partner, active); form notebook — Profile (bio), Services (tags), Working hours (inline editable list, `float_time` widgets).

---

## 10. Installation and operations

1. Add `custom_addons` to Odoo **addons path** (e.g. Docker: `./custom_addons` → `/mnt/extra-addons`).
2. **Apps → Update Apps List →** install **Chaitanya Wellness**.
3. After code/XML changes: **Apps → Upgrade** the module.
4. Valid `__manifest__.py` (commas in `data` list) is required or the module will not appear in Apps.

---

## 11. Alignment with booking flow (PDF)

| Flow step | Current support |
|-----------|-----------------|
| Browse categories (Spa, Ayurveda, …) | Categories + seed data |
| Service detail (duration, price, benefits) | Service model + form |
| Therapist info | Provider `bio` + service link |
| Book by therapist / by availability | **Not implemented** — needs booking model + slot APIs |
| Sign-in, payment, voucher, gift | **Not implemented** — needs website + payment modules |

---

## 12. Roadmap

1. **Booking** model — service, provider, start/end datetimes, state machine, overlap prevention.
2. **Availability helpers** — `get_available_slots`, `get_available_providers` (timezone-aware).
3. **Website** — controllers, QWeb templates, portal authentication.
4. **Commerce** — payment integration, vouchers, gift bookings.

---

## 13. Document maintenance

- **Edit:** `doc/MODULE_DOCUMENTATION.md`
- **Regenerate PDF:** `python doc/build_module_doc_pdf.py` from the module directory (requires `fpdf2`).

---

## Revision history

| Date | Author | Changes |
|------|--------|---------|
| May 2026 | Dennis Dong | Initial technical documentation — full backend foundation |
