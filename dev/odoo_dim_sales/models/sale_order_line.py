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

    # Campos adicionales para dimensiones
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

    # Validación: no permitir valores negativos
    @api.constrains("x_length", "x_width", "x_height")
    def _check_non_negative(self) -> None:
        for line in self:
            if any(
                v is not None and v < 0
                for v in (line.x_length, line.x_width, line.x_height)
            ):
                raise ValidationError("Largo, Ancho y Alto deben ser ≥ 0.")

    # Validación: exigir dimensiones > 0 para productos de tipo consumible o servicio
    @api.constrains("x_length", "x_width", "x_height", "product_id")
    def _check_dimensions_required(self):
        for line in self:
            if line.product_id.type in ("consu", "service"):
                if (line.x_length or 0) <= 0 or (line.x_width or 0) <= 0 or (line.x_height or 0) <= 0:
                    raise ValidationError(
                        "Debe ingresar dimensiones válidas (Largo, Ancho y Alto > 0) "
                        "para productos de tipo Consumible o Servicio."
                    )

    # Cálculo automático de la cantidad según dimensiones
    @api.depends("x_length", "x_width", "x_height")
    def _compute_dimension_qty(self) -> None:
        for line in self:
            l = line.x_length or 0.0                        # Valores nulos o ceros
            w = line.x_width or 0.0
            h = line.x_height or 0.0
            qty = max(l * w * h, 0.0)
            line.x_dimension_qty = qty
            # Fuente única de verdad: sincroniza la cantidad real de venta
            line.product_uom_qty = qty

    # Onchange: recalcula en el cliente y muestra advertencia si todo está en cero
    @api.onchange('x_length', 'x_width', 'x_height')
    def _onchange_dimensions(self):
        for line in self:
            l = line.x_length or 0.0
            w = line.x_width or 0.0
            h = line.x_height or 0.0
            qty = max(l * w * h, 0.0)
            line.product_uom_qty = qty
            line.x_dimension_qty = qty
            if l == 0 and w == 0 and h == 0:
                return {
                    'warning': {
                        'title': "Dimensiones vacías",
                        'message': "Todas las dimensiones son 0 → la cantidad será 0 y el subtotal quedará en 0.",
                    }
                }  # Mensaje de advertencia si todas las dimensiones son 0

    # Override create: asegura que siempre se guarde la cantidad calculada
    @api.model_create_multi
    def create(self, vals_list: list[dict]) -> models.Model:
        for vals in vals_list:
            l = float(vals.get("x_length") or 0.0)
            w = float(vals.get("x_width") or 0.0)
            h = float(vals.get("x_height") or 0.0)
            vals["product_uom_qty"] = max(l * w * h, 0.0)

        records = super().create(vals_list)
        for rec in records:
            _logger.debug("Created SOL %s qty=%s", rec.id, rec.product_uom_qty)
        return records

    # Override write: asegura que al actualizar también se recalcule la cantidad
    def write(self, vals: dict) -> bool:
        if any(k in vals for k in ("x_length", "x_width", "x_height")):
            l = float(vals.get("x_length", self.x_length or 0.0))
            w = float(vals.get("x_width",  self.x_width  or 0.0))
            h = float(vals.get("x_height", self.x_height or 0.0))
            vals["product_uom_qty"] = max(l * w * h, 0.0)
        return super().write(vals)
