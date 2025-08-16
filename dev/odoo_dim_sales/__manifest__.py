# -*- coding: utf-8 -*-
{
    "name": "Dimensional Sales (Qty from L×A×H)",
    "summary": "Cantidad = Largo × Ancho × Alto; PDF de venta con columnas L/A/H.",
    "version": "18.0.1.0.0",
    "author": "Dylan Venegas Lopez",
    "license": "LGPL-3",
    "depends": ["sale"],
    "data": [
        "views/sale_views.xml",
        "views/report_saleorder.xml",
    ],
    "application": False,
    "installable": True,
}