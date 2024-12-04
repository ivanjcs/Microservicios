from marshmallow import fields, Schema, post_load
from app.models import Compra

#class CompraSchema(Schema):
#    id = fields.Integer(dump_only=True)
#    producto = fields.Integer(required=True)
#    fecha_compra = fields.DateTime(required=False)
#    direccion_envio = fields.String(required=True)
#    deleted_at = fields.DateTime(dump_only=True)

#    @post_load
#    def make_compra(self, data, **kwargs):
#        return Compra(**data)
    
class CompraSchema(Schema):
    id = fields.Int(dump_only=True)  # Solo se usa al serializar, no al cargar
    producto = fields.Int(required=True)
    direccion_envio = fields.Str(required=True)
    fecha_compra = fields.DateTime(dump_only=True)  # No se requiere al cargar
    deleted_at = fields.DateTime(dump_only=True)   # Opcional, no requerido al cargar
    
    @post_load
    def make_compra(self, data, **kwargs):
        return Compra(**data)