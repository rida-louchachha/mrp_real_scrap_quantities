# -*- coding: utf-8 -*-
{
    'name': 'Mrp Real Scrap Quantities',
    'version': '1.0',
    'summary': 'Adds real, visual quantity and percentage indicators to BoM lines for manufacturing analysis.',
    'description': """
MRP BoM Extended Fields
=======================

This module enhances the Manufacturing Bill of Materials (BoM) by adding useful fields on each BoM component line:

🔹 Real Quantity – the actual quantity consumed during production.  
🔹 Visual Quantity – the estimated or displayed quantity expected.  
🔹 Usage % – a computed percentage (Visual Quantity ÷ Real Quantity × 100).

These fields help manufacturers:
- Analyze deviation between expected and real input
- Track efficiency and waste
- Improve decision-making on process control

All fields are displayed in the BoM form view and editable during configuration.

""",
    'author': 'Rida Louchachha',
    'website': 'https://github.com/rida-louchachha',
    'category': 'Manufacturing',
    'license': 'LGPL-3',
    'depends': ['mrp'],
    'data': [
        'security/ir.model.access.csv',
        'views/mrp_bom_line_view.xml',
        'views/mrp_production_view.xml',
        'views/stock_move_view.xml',
        'views/mrp_production_report_inherit.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
