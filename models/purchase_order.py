from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    # Identificadores de tipo
    is_service_order = fields.Boolean(
        string='Es Orden de Servicio',
        default=False,
        tracking=True
    )
    
    is_distribution_order = fields.Boolean(
        string='Es Orden de Distribución',
        default=False,
        tracking=True
    )

    # ============== CAMPOS ORDEN DE SERVICIO ==============
    request_area = fields.Many2one(
        'hr.department',
        string='Área Solicitante',
        tracking=True
    )
    
    requester_id = fields.Many2one(
        'res.users',
        string='Solicitante',
        default=lambda self: self.env.user,
        help='Usuario que solicita el servicio'
    )
    
    delivery_date = fields.Date(
        string='Fecha de Entrega del Servicio',
        help='Fecha programada para la entrega/ejecución del servicio'
    )
    
    cancellation_dates = fields.Date(
        string="Fecha de Cancelación"
    )

    # Campos de control de firmas
    elaborated_by = fields.Char(
        string='Elaborado Por',
        default=lambda self: self.env.user.name
    )
    
    received_by = fields.Char(
        string='Recibido Por'
    )
    
    # Control de tesorería
    treasury_approval = fields.Boolean(
        string='Aprobado por Tesorería',
        default=False
    )
    
    treasury_approved_by = fields.Char(
        string='Aprobado por (Tesorería)'
    )
    
    # Conformidad del servicio
    service_conformity = fields.Boolean(
        string='Conformidad del Servicio Prestado',
        default=False,
        help='Marca si el servicio se realizó conforme a lo solicitado'
    )
    
    conformity_signature = fields.Char(
        string='Firma de Conformidad',
        help='Nombre de quien firma la conformidad del servicio'
    )
    
    conformity_observations = fields.Text(
        string='Observaciones de Conformidad',
        help='Observaciones sobre la conformidad del servicio'
    )
    
    conformity_date = fields.Date(
        string='Fecha de Conformidad',
        help='Fecha en que se firmó la conformidad'
    )

    # ============== CAMPOS ORDEN DE DISTRIBUCIÓN ==============
    distributor_id = fields.Many2one(
        'res.partner',
        string='Distribuidor',
        tracking=True,
        help='Distribuidor asignado a la orden de distribución'
    )
    
    destination_municipality_ids = fields.Many2many(
        'res.partner',
        'purchase_order_municipality_rel',
        'purchase_order_id',
        'municipality_id',
        string='Municipios Destino',
        help='Municipios de destino para la distribución'
    )
    
    scheduled_date = fields.Datetime(
        string='Fecha Programada',
        tracking=True
    )
    
    distribution_delivery_date = fields.Datetime(
        string='Fecha de Entrega',
        tracking=True
    )
    
    service_type = fields.Selection([
        ('local', 'Distribución Local'),
        ('national', 'Distribución Nacional'),
        ('express', 'Servicio Express'),
        ('scheduled', 'Servicio Programado')
    ], string='Tipo de Servicio', default='local')
    
    pickup_address_id = fields.Many2one(
        'res.partner',
        string='Dirección de Recojo'
    )
    
    delivery_address_id = fields.Many2one(
        'res.partner',
        string='Dirección de Entrega'
    )
    
    pickup_contact_id = fields.Many2one(
        'res.partner',
        string='Contacto en Recojo',
        domain="[('parent_id', '=', pickup_address_id), ('type', '=', 'contact')]"
    )
    
    pickup_phone = fields.Char(
        string='Teléfono Recojo',
        related='pickup_contact_id.phone',
        readonly=True
    )
    
    delivery_contact_id = fields.Many2one(
        'res.partner',
        string='Contacto en Entrega',
        domain="[('parent_id', '=', delivery_address_id), ('type', '=', 'contact')]"
    )
    
    delivery_phone = fields.Char(
        string='Teléfono Entrega',
        related='delivery_contact_id.phone',
        readonly=True
    )
    
    vehicle_type = fields.Selection([
        ('motorcycle', 'Motocicleta'),
        ('van', 'Camioneta'),
        ('truck', 'Camión'),
        ('trailer', 'Tráiler')
    ], string='Tipo de Vehículo')

    @api.model
    def create(self, vals):
        # Asignar secuencia según el tipo
        if vals.get('is_service_order'):
            vals['name'] = self.env['ir.sequence'].next_by_code('purchase.order.service') or '/'
        elif vals.get('is_distribution_order'):
            vals['name'] = self.env['ir.sequence'].next_by_code('purchase.order.distribution') or '/'
        
        return super(PurchaseOrder, self).create(vals)

    @api.onchange('is_service_order')
    def _onchange_is_service_order(self):
        if self.is_service_order:
            self.is_distribution_order = False

    @api.onchange('is_distribution_order')
    def _onchange_is_distribution_order(self):
        if self.is_distribution_order:
            self.is_service_order = False