from odoo.tests.common import TransactionCase

class TestSaleOrder(TransactionCase):

    def setUp(self):
        super().setUp()
        # Producto de prueba (Consumible)
        self.product = self.env['product.product'].create({
            'name': 'Bloque de prueba',
            'list_price': 50.0,
            'type': 'consu',
        })
        # Orden de venta de prueba
        self.order = self.env['sale.order'].create({
            'partner_id': self.env.ref('base.res_partner_1').id,
        })

    def test_sale_order_subtotal(self):
        """Debe calcular subtotal = L × A × H × precio"""
        line = self.env['sale.order.line'].create({
            'order_id': self.order.id,
            'product_id': self.product.id,
            'price_unit': self.product.list_price,
            'x_length': 2,
            'x_width': 3,
            'x_height': 4,
        })
        expected_qty = 2 * 3 * 4  # = 24
        expected_subtotal = expected_qty * self.product.list_price  # 24 × 50 = 1200

        # Aserciones
        self.assertEqual(
            line.product_uom_qty, expected_qty,
            f"Cantidad debería ser {expected_qty}"
        )
        self.assertEqual(
            line.price_subtotal, expected_subtotal,
            f"Subtotal debería ser {expected_subtotal}"
        )
