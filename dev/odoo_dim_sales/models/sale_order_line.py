# -*- coding: utf-8 -*-
from __future__ import annotations
import logging
from typing import Final

from odoo import api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

DIGITS_2: Final = (16, 2)

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    x_length = fields.Float(string="Largo", digits=DIGITS_2, help="Unidad: metros (m)")
    x_width  = fields.Float(string="Ancho", digits=DIGITS_2, help="Unidad: metros (m)")
    x_height = fields.Float(string="Alto",  digits=DIGITS_2, help="Unidad: metros (m)")

    # Opcional: visible para diagnóstico / KPI internos
    x_dimension_qty = fields.Float(
        string="Cantidad (L×A×H)",
        compute="_compute_dimension_qty",
        store=True,
        digits=DIGITS_2,
        help="Cantidad derivada de dimensiones (por defecto m³ si usas metros).",
    )

    @api.constrains("x_length", "x_width", "x_height")
    def _check_non_negative(self) -> None:
        for line in self:
            if any(
                v is not None and v < 0
                for v in (line.x_length, line.x_width, line.x_height)
            ):
                raise ValidationError("Largo, Ancho y Alto deben ser ≥ 0.")

    @api.depends("x_length", "x_width", "x_height")
    def _compute_dimension_qty(self) -> None:
        for line in self:
            l = line.x_length or 0.0
            w = line.x_width or 0.0
            h = line.x_height or 0.0
            qty = max(l * w * h, 0.0)
            line.x_dimension_qty = qty
            # Fuente única de verdad: sincroniza la cantidad real de venta
            line.product_uom_qty = qty

    @api.onchange("x_length", "x_width", "x_height")
    def _onchange_dimensions(self) -> None:
        for line in self:
            l = line.x_length or 0.0
            w = line.x_width or 0.0
            h = line.x_height or 0.0
            line.product_uom_qty = max(l * w * h, 0.0)

    @api.model
    def create(self, vals: dict) -> models.Model:
        l = float(vals.get("x_length") or 0.0)
        w = float(vals.get("x_width") or 0.0)
        h = float(vals.get("x_height") or 0.0)
        vals["product_uom_qty"] = max(l * w * h, 0.0)
        rec = super().create(vals)
        _logger.debug("Created SOL %s qty=%s", rec.id, rec.product_uom_qty)
        return rec

    def write(self, vals: dict) -> bool:
        if any(k in vals for k in ("x_length", "x_width", "x_height")):
            l = float(vals.get("x_length", self.x_length or 0.0))
            w = float(vals.get("x_width",  self.x_width  or 0.0))
            h = float(vals.get("x_height", self.x_height or 0.0))
            vals["product_uom_qty"] = max(l * w * h, 0.0)
        return super().write(vals)
