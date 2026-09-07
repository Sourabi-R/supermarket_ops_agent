import os
import sys

ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app.database.init_db import initialize_database
from app.services.documents_service import generate_invoice_pdf, generate_analysis_pptx
from app.services.store_service import StoreService


def main():
    initialize_database(force_recreate=False)
    service = StoreService()
    output_dir = os.path.join(ROOT, 'sample_outputs')
    os.makedirs(output_dir, exist_ok=True)
    invoice = generate_invoice_pdf(service, os.path.join(output_dir, 'sample_invoice.pdf'))
    deck = generate_analysis_pptx(service, os.path.join(output_dir, 'sample_analysis_deck.pptx'))
    with open(os.path.join(output_dir, 'sample_telegram_responses.md'), 'w', encoding='utf-8') as f:
        f.write('# Sample Telegram responses\n\n- Good morning\n- What\'s low in stock?\n- What needs my attention?\n- How much atta do I have?\n')
    with open(os.path.join(output_dir, 'sample_store_brief.md'), 'w', encoding='utf-8') as f:
        f.write('# Morning brief\n\nThis file is generated from the database at runtime.\n')
    with open(os.path.join(output_dir, 'sample_reorder_report.md'), 'w', encoding='utf-8') as f:
        f.write('# Reorder report\n\nThis file is generated from the database at runtime.\n')
    with open(os.path.join(output_dir, 'sample_attention_report.md'), 'w', encoding='utf-8') as f:
        f.write('# Attention report\n\nThis file is generated from the database at runtime.\n')
    print(f'Generated invoice: {invoice}')
    print(f'Generated deck: {deck}')


if __name__ == '__main__':
    main()
