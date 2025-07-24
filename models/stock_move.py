# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools.float_utils import float_is_zero
import logging

_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = 'stock.move'

    # -------------------------------------------------------------------------
    # Custom Fields
    # -------------------------------------------------------------------------

    visual_qty = fields.Float(
        string="Visual Quantity",
        help="Displayed or expected quantity before scrap."
    )
    scrap_qty = fields.Float(
        string="Scrap Quantity",
        help="Expected quantity to be lost as scrap."
    )
    real_qty = fields.Float(
        string="Real Quantity",
        compute="_compute_real_qty",
        store=True,
        readonly=False,
        help="Actual quantity consumed = Visual - Scrap"
    )
    usage_percent = fields.Float(
        string="Scrap %",
        compute="_compute_usage_percent",
        store=True,
        readonly=True,
        help="Percentage of scrap relative to visual quantity."
    )

    # -------------------------------------------------------------------------
    # Compute Methods
    # -------------------------------------------------------------------------

    @api.depends('visual_qty', 'scrap_qty')
    def _compute_real_qty(self):
        """Compute real quantity consumed after scrap deduction."""
        for move in self:
            move.real_qty = max(move.visual_qty - move.scrap_qty, 0.0)
            if move.raw_material_production_id:
                # Reflect real_qty into move quantity for MO context
                move.quantity = move.real_qty

    @api.depends('visual_qty', 'scrap_qty')
    def _compute_usage_percent(self):
        """Calculate the percentage of quantity scrapped."""
        for move in self:
            if move.visual_qty:
                move.usage_percent = (move.scrap_qty / move.visual_qty) * 100
            else:
                move.usage_percent = 0.0

    # -------------------------------------------------------------------------
    # Onchange Behavior
    # -------------------------------------------------------------------------

    @api.onchange('real_qty')
    def _onchange_real_qty_update_quantity(self):
        """Update product_uom_qty when real_qty is manually adjusted."""
        for move in self:
            if (
                move.raw_material_production_id
                and move.real_qty > 0
                and move.product_uom
            ):
                move.product_uom_qty = move.real_qty
                move.quantity = move.real_qty
