# Spanar Systems product portfolio

## In development
- **Velocity**: AI-native multi-tenant SaaS operating platform.
- **AalayApp** (formerly Temple): bilingual English/Telugu spiritual hub; web and Android (see the `aalay repo` folder). No iOS build submitted.
- **Travai**: AI travel companion and adaptive trip planner.

## Concepts (can be built for clients on request)
Scribe (clinics), Sentinel (security), Ledger (CA/finance), Concierge (WhatsApp/web assistant), Tutor (education), Route (logistics), Relay (workflow), Prism (analytics).

## Product language rules
Do not present roadmap ideas as shipped features. Use **In development** or **Concept** only. Sample screens are illustrative UI with dummy data.

## How the site is built
Product data lives in `tools/products_data.py`, solution data in `tools/build_solutions.py`. Run `python3 tools/build_solutions.py` to regenerate `index.html`, `/products/*`, `/solutions/*`, `sitemap.xml` and `robots.txt`. Do not hand-edit the generated HTML. Set `SALES_EMAIL` / `SALES_PHONE` in the script to change contact details site-wide.
