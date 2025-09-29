from odoo import models, fields


class ServiceRoute(models.Model):
    _name = 'service.route'
    _description = 'Rutas de Servicio de Distribución'
    _order = 'name'

    name = fields.Char(
        string='Nombre de Ruta',
        required=True,
        help='Ej: Lima - Callao, Lima - Arequipa'
    )
    
    code = fields.Char(
        string='Código',
        help='Código único de la ruta'
    )
    
    origin_city = fields.Char(
        string='Ciudad de Origen'
    )
    
    destination_city = fields.Char(
        string='Ciudad de Destino'
    )
    
    distance_km = fields.Float(
        string='Distancia (km)',
        digits=(10, 2)
    )
    
    estimated_time = fields.Float(
        string='Tiempo Estimado (horas)',
        digits=(10, 2)
    )
    
    default_price_per_kg = fields.Float(
        string='Precio por Kilo',
        digits=(10, 2),
        help='Precio por defecto por kilogramo para esta ruta'
    )
    
    active = fields.Boolean(
        string='Activo',
        default=True
    )
    
    notes = fields.Text(
        string='Notas'
    )
    
    _sql_constraints = [
        ('code_unique', 'unique(code)', 'El código de la ruta debe ser único!')
    ]