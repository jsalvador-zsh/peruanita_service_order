{
    'name': 'Órdenes de Servicio - PERUANITA',
    'version': '18.0.1.0.0',
    'category': 'Services',
    'summary': 'Gestión de Órdenes de Servicio y Distribución',
    'description': """
        Módulo para gestionar órdenes de servicio y distribución integradas con compras.
        - Órdenes de Servicio con campos específicos
        - Órdenes de Distribución con rutas y detalles de entrega
        - Secuencias independientes para cada tipo
    """,
    'author': 'Juan Salvador',
    'website': 'https://juansalvador.dev',
    'depends': [
        'base',
        'purchase',
        'account',
        'hr'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'views/purchase_order_views.xml',
        'views/service_route_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}