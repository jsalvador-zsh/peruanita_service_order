from odoo import models, fields, api


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    # Campos específicos para órdenes de distribución
    route_id = fields.Many2one(
        'service.route',
        string='Ruta'
    )
    
    route_name = fields.Char(
        string='Descripción de Ruta',
        related='route_id.name',
        readonly=True
    )
    
    weight = fields.Float(
        string='Kilos',
        digits='Product Unit of Measure'
    )
    
    price_per_kg = fields.Float(
        string='Precio por Kilo',
        digits='Product Unit of Measure'
    )
    
    distribution_price = fields.Float(
        string='Precio Distribución',
        digits='Product Unit of Measure'
    )
    
    distribution_subtotal = fields.Float(
        string='Total Distribución',
        compute='_compute_distribution_subtotal',
        store=True,
        digits=(10, 2)
    )
    
    volume = fields.Float(
        string='Volumen (m³)',
        digits=(10, 3)
    )
    
    packaging_type = fields.Selection([
        ('box', 'Caja'),
        ('envelope', 'Sobre'),
        ('pallet', 'Pallet'),
        ('bag', 'Bolsa'),
        ('other', 'Otro')
    ], string='Tipo de Empaque')
    
    special_handling = fields.Boolean(
        string='Manejo Especial'
    )
    
    fragile = fields.Boolean(
        string='Frágil'
    )
    
    distribution_notes = fields.Text(
        string='Notas de Distribución'
    )
    
    is_distribution_line = fields.Boolean(
        string='Es Línea de Distribución',
        related='order_id.is_distribution_order',
        store=True
    )

    @api.depends('weight', 'price_per_kg', 'distribution_price')
    def _compute_distribution_subtotal(self):
        for line in self:
            if line.is_distribution_line:
                if line.weight and line.price_per_kg:
                    line.distribution_subtotal = line.weight * line.price_per_kg
                elif line.distribution_price:
                    line.distribution_subtotal = line.distribution_price
                else:
                    line.distribution_subtotal = 0.0
            else:
                line.distribution_subtotal = 0.0

    @api.onchange('weight', 'price_per_kg')
    def _onchange_weight_price(self):
        if self.is_distribution_line and self.weight and self.price_per_kg:
            self.distribution_price = self.weight * self.price_per_kg