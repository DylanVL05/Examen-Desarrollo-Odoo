# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestDimensionalQty(TransactionCase):
    def setUp(self):
        super().setUp()
        self.Product = self.env["product.product"]
        self.Sale = self.env["sale.order"]
        self.partner = self.env["res.partner"].create({"name": "Cliente Demo"})
        self.product = self.Product.create({
            "name": "Panel 3D",
            "type": "consu",
            "list_price": 100.0,  # solo informativo si no usas pricelist/onchange
        })

    def test_qty_and_subtotal(self):
        # Pedido con partner; no dependemos de pricelist/onchange
        so = self.Sale.create({"partner_id": self.partner.id})

        # Línea: fijamos price_unit y limpiamos impuestos para que sea 100 * qty exacto
        line = self.env["sale.order.line"].create({
            "order_id": so.id,
            "product_id": self.product.id,
            "name": "Panel 3D",
            "price_unit": 100.0,
            "tax_id": [(6, 0, [])],
            "x_length": 2.0, "x_width": 3.0, "x_height": 4.0,  # 2*3*4 = 24
        })

        # Tu módulo debe computar product_uom_qty a partir de LxAxH
        self.assertEqual(line.product_uom_qty, 24.0)
        # No llamamos _amount_all; el compute de la línea ya calculó el subtotal
        self.assertAlmostEqual(line.price_subtotal, 2400.0, places=2)

        # Al cambiar una dimensión debe recalcular qty y subtotal
        line.write({"x_height": 1.0})  # 2*3*1 = 6
        self.assertEqual(line.product_uom_qty, 6.0)
        self.assertAlmostEqual(line.price_subtotal, 600.0, places=2)
