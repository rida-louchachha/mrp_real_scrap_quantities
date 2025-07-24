# -*- coding: utf-8 -*-
from odoo import models, fields, api


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    # -------------------------------------------------------------------------
    # Custom Fields
    # -------------------------------------------------------------------------

    visual_qty = fields.Float(
        string="Visual Quantity",
        help="Displayed or expected quantity before scrap."
    )
    scrap_qty = fields.Float(
        string="Scrap Quantity",
        help="Estimated quantity to be lost as scrap."
    )
    real_qty = fields.Float(
        string="Real Quantity",
        compute="_compute_real_qty",
        store=True,
        readonly=True,
        help="Actual quantity consumed = Visual - Scrap"
    )
    usage_percent = fields.Float(
        string="Usage %",
        compute="_compute_usage_percent",
        store=True,
        help="Percentage of quantity scrapped from the visual quantity."
    )

    # -------------------------------------------------------------------------
    # Compute Methods
    # -------------------------------------------------------------------------

    @api.depends('visual_qty', 'scrap_qty')
    def _compute_real_qty(self):
        """Compute the real quantity after removing scrap."""
        for line in self:
            line.real_qty = max(line.visual_qty - line.scrap_qty, 0.0)

    @api.depends('visual_qty', 'scrap_qty')
    def _compute_usage_percent(self):
        """Calculate percentage of scrap based on visual quantity."""
        for line in self:
            if line.visual_qty:
                line.usage_percent = (line.scrap_qty / line.visual_qty) * 100
            else:
                line.usage_percent = 0.0

    # -------------------------------------------------------------------------
    # Onchange Behavior
    # -------------------------------------------------------------------------

    @api.onchange('visual_qty')
    def _onchange_visual_qty_set_product_qty(self):
        """Auto-sync product_qty with visual_qty for ease of use."""
        for line in self:
            line.product_qty = line.visual_qty
