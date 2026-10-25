# Spanar Systems product portfolio

The portfolio includes available products plus products in pilot or early access. LeadCatch is presented as **Pilot** and ImportSure as **Early access**. Existing products remain **Available**. AalayApp runs on Android and web (see the `aalay repo` folder). Sample screens are illustrative UI with dummy data.

## How the site is built
Product data lives in `tools/products_data.py`, solution data in `tools/build_solutions.py`. Run `python3 tools/build_solutions.py` to regenerate `index.html`, `/products/*`, `/solutions/*`, `sitemap.xml` and `robots.txt`. Do not hand-edit the generated HTML. Set `SALES_EMAIL` / `SALES_PHONE` in the script to change contact details site-wide.
