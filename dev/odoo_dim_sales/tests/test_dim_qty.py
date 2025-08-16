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
            "list_price": 100.0,
        })

    def test_qty_and_subtotal(self):
        so = self.Sale.create({"partner_id": self.partner.id})
        line = self.env["sale.order.line"].create({
            "order_id": so.id,
            "product_id": self.product.id,
            "name": "Panel 3D",
            "x_length": 2.0, "x_width": 3.0, "x_height": 4.0,  # 24
        })
        self.assertEqual(line.product_uom_qty, 24.0)
        so._amount_all()
        self.assertAlmostEqual(line.price_subtotal, 2400.0, places=2)

        line.write({"x_height": 1.0})  # 6
        self.assertEqual(line.product_uom_qty, 6.0)
        so._amount_all()
        self.assertAlmostEqual(line.price_subtotal, 600.0, places=2)
