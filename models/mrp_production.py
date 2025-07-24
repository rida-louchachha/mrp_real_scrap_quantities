# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools.float_utils import float_is_zero
import logging

_logger = logging.getLogger(__name__)


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    # -------------------------------------------------------------------------
    # Onchange Methods
    # -------------------------------------------------------------------------

    @api.onchange('product_qty')
    def _onchange_product_qty_recompute_raw_moves(self):
        """Recompute raw moves when product quantity is modified in draft state."""
        if self.bom_id and self.state == 'draft':
            self._compute_move_raw_ids()

    @api.onchange('qty_producing')
    def _onchange_qty_producing_update_custom_fields(self):
        """Update visual and scrap quantities on raw moves based on qty_producing."""
        for production in self:
            if not production.bom_id or not production.move_raw_ids:
                continue

            for move in production.move_raw_ids.filtered(lambda m: m.bom_line_id):
                bom_line = move.bom_line_id
                factor = production.qty_producing / production.bom_id.product_qty if production.bom_id.product_qty else 1.0
                move.visual_qty = bom_line.visual_qty * factor
                move.scrap_qty = bom_line.scrap_qty * factor

    # -------------------------------------------------------------------------
    # Core Logic
    # -------------------------------------------------------------------------

    def _get_moves_raw_values(self):
        """Extend default move values to include visual and scrap quantities."""
        res = super()._get_moves_raw_values()
        updated_res = []

        for line in res:
            bom_line = self.bom_id.bom_line_ids.filtered(lambda l: l.id == line.get('bom_line_id'))
            if bom_line:
                bom_line = bom_line[0]
                factor = self.product_qty / self.bom_id.product_qty if self.bom_id.product_qty else 1.0
                line['visual_qty'] = bom_line.visual_qty * factor
                line['scrap_qty'] = bom_line.scrap_qty * factor

            updated_res.append(line)

        return updated_res

    def button_mark_done(self):
        """Handle scrap line creation when marking a production order as done."""
        res = super().button_mark_done()

        for production in self:
            scrap_location = self.env['stock.location'].search([
                ('scrap_location', '=', True),
                ('company_id', '=', production.company_id.id)
            ], limit=1)

            if not scrap_location:
                _logger.warning("No scrap location found for company: %s", production.company_id.name)
                continue

            for move in production.move_raw_ids.filtered(lambda m: m.scrap_qty > 0):
                existing_scrap_line = move.move_line_ids.filtered(
                    lambda ml: ml.location_dest_id.id == scrap_location.id and
                    float_is_zero(abs(ml.qty_done - move.scrap_qty), precision_rounding=move.product_uom.rounding)
                )

                if not existing_scrap_line:
                    move.move_line_ids.create({
                        'move_id': move.id,
                        'product_id': move.product_id.id,
                        'product_uom_id': move.product_uom.id,
                        'qty_done': move.scrap_qty,
                        'location_id': move.location_id.id,
                        'location_dest_id': scrap_location.id,
                    })

        return res
