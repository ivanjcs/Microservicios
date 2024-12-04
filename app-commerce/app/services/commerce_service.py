import logging
from saga import SagaBuilder, SagaError
from app.services import ClienteComprasService, ClientePagosService, ClienteInventarioService, ClienteCatalogoService
from app.models import Carrito, Producto
from app import cache
clienteCompras = ClienteComprasService()
clientePagos = ClientePagosService()
clienteInventario = ClienteInventarioService()
clienteCatalogo = ClienteCatalogoService()

class CommerceService:
    """
    Clase que implementa la funcionalidad de Orquestador en el patron SAGA de microservicios
    """
    # Este método coordina el flujo de compra usando el patrón saga.
    def comprar(self, carrito: Carrito) -> None:
        
        try:
            SagaBuilder.create()\
                .action(lambda: clienteCompras.comprar(carrito.producto, carrito.direccion_envio), lambda: clienteCompras.cancelar_compra()) \
                .action(lambda: clientePagos.registrar_pago(carrito.producto, carrito.medio_pago), lambda: clientePagos.cancelar_pago()) \
                .action(lambda: clienteInventario.retirar_producto(carrito), lambda: clienteInventario.ingresar_producto()) \
                .build().execute()
        except SagaError as e:
            logging.error(e)

    # Este método consulta un producto en el catalogo, usando una caché para optimizar el rendimiento.
    def consultar_catalogo(self, id: int) -> Producto:
        result = cache.get(f"producto_{id}") # Intenta obtener el producto de la caché
        logging.info(f'datos en cache {result}') # Registra un mensaje indicando si el producto fue encontrado.
        if result is None: # SI no está en la cache, consulta al microservicio.
            result = clienteCatalogo.obtener_producto(id) # Llama al microservicio de catalogo para obtener el producto.
            cache.set(f"producto_{id}", result, timeout=60) # Guarda el resultado en la caché con un tiempo de expiración de 60 segundos
        return result
