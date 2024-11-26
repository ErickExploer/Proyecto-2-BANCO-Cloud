# Proyecto-2-BANCO-Cloud

   ```bash
   #!/bin/bash
   services=(TABLA-CUENTA TABLA-PAGOS TABLA-PRESTAMOS TABLA-SOLICITUD-PRESTAMO TABLA-SOPORTE TABLA-TARJETAS TABLA-TOKENS_ACCESO TABLA-TRANSACCION TABLA-USUARIOS)

   for service in "${services[@]}"
   do
     echo "Deploying $service..."
     cd $service
     npx serverless deploy
     cd ..
   done
   ```

   Hazlo ejecutable:
   ```bash
   chmod +x deploy.sh
   ```

   Luego, ejecútalo:
   ```bash
   ./deploy.sh
   ```

Si esto no resuelve tu problema, indícame los pasos exactos que seguiste o cualquier mensaje adicional de error que aparezca. ¡Podemos seguir iterando hasta solucionarlo!


:~/Proyecto-2-BANCO-Cloud (main) $ ./deploy.sh
Deploying TABLA-CUENTA...

Deploying "api-cuentas" to stage "dev" (us-east-1)

✔ Service deployed to stack api-cuentas-dev (29s)

endpoints:
  POST - https://buey4muco2.execute-api.us-east-1.amazonaws.com/dev/cuentas/crear
  POST - https://buey4muco2.execute-api.us-east-1.amazonaws.com/dev/cuentas/listar
  POST - https://buey4muco2.execute-api.us-east-1.amazonaws.com/dev/cuentas/buscar
  DELETE - https://buey4muco2.execute-api.us-east-1.amazonaws.com/dev/cuentas/eliminar
  PUT - https://buey4muco2.execute-api.us-east-1.amazonaws.com/dev/cuentas/modificar
  POST - https://buey4muco2.execute-api.us-east-1.amazonaws.com/dev/cuentas/agregar-saldo
functions:
  CrearCuenta: api-cuentas-dev-CrearCuenta (4.8 kB)
  ListarCuentas: api-cuentas-dev-ListarCuentas (4.8 kB)
  BuscarCuenta: api-cuentas-dev-BuscarCuenta (4.8 kB)
  EliminarCuenta: api-cuentas-dev-EliminarCuenta (4.8 kB)
  ModificarCuenta: api-cuentas-dev-ModificarCuenta (4.8 kB)
  AgregarSaldoCuenta: api-cuentas-dev-AgregarSaldoCuenta (4.8 kB)

Deploying TABLA-PAGOS...

Deploying "api-pagos" to stage "dev" (us-east-1)

No changes to deploy. Deployment skipped. (1s)

Deploying TABLA-PRESTAMOS...

Deploying "api-prestamos" to stage "dev" (us-east-1)

✔ Service deployed to stack api-prestamos-dev (33s)

endpoints:
  POST - https://yawxyakxc7.execute-api.us-east-1.amazonaws.com/dev/prestamo/crear
  POST - https://yawxyakxc7.execute-api.us-east-1.amazonaws.com/dev/prestamo/obtener
  POST - https://yawxyakxc7.execute-api.us-east-1.amazonaws.com/dev/prestamo/actualizar-estado
  POST - https://yawxyakxc7.execute-api.us-east-1.amazonaws.com/dev/prestamo/listar-usuario
  DELETE - https://yawxyakxc7.execute-api.us-east-1.amazonaws.com/dev/prestamo/eliminar
functions:
  crearPrestamo: api-prestamos-dev-crearPrestamo (6.4 kB)
  obtenerPrestamo: api-prestamos-dev-obtenerPrestamo (6.4 kB)
  actualizarEstadoPrestamo: api-prestamos-dev-actualizarEstadoPrestamo (6.4 kB)
  listarPrestamobyID: api-prestamos-dev-listarPrestamobyID (6.4 kB)
  eliminarPrestamo: api-prestamos-dev-eliminarPrestamo (6.4 kB)

Deploying TABLA-SOLICITUD-PRESTAMO...

Deploying "api-solicitud-prestamo" to stage "dev" (us-east-1)

✔ Service deployed to stack api-solicitud-prestamo-dev (23s)

endpoints:
  POST - https://bka3b9061j.execute-api.us-east-1.amazonaws.com/dev/solicitud-prestamo/crear
  POST - https://bka3b9061j.execute-api.us-east-1.amazonaws.com/dev/solicitud-prestamo/listar
  POST - https://bka3b9061j.execute-api.us-east-1.amazonaws.com/dev/solicitud-prestamo/aceptar
  POST - https://bka3b9061j.execute-api.us-east-1.amazonaws.com/dev/solicitud-prestamo/rechazar
  POST - https://bka3b9061j.execute-api.us-east-1.amazonaws.com/dev/solicitud-prestamo/obtener
  POST - https://bka3b9061j.execute-api.us-east-1.amazonaws.com/dev/solicitud-prestamo/listar-estado
  DELETE - https://bka3b9061j.execute-api.us-east-1.amazonaws.com/dev/solicitud-prestamo/eliminar
functions:
  crearSolicitudPrestamo: api-solicitud-prestamo-dev-crearSolicitudPrestamo (7.8 kB)
  listarSolicitudesPrestamo: api-solicitud-prestamo-dev-listarSolicitudesPrestamo (7.8 kB)
  aceptarSolicitudPrestamo: api-solicitud-prestamo-dev-aceptarSolicitudPrestamo (7.8 kB)
  rechazarSolicitudPrestamo: api-solicitud-prestamo-dev-rechazarSolicitudPrestamo (7.8 kB)
  obtenerSolicitudPrestamo: api-solicitud-prestamo-dev-obtenerSolicitudPrestamo (7.8 kB)
  listarPorEstado: api-solicitud-prestamo-dev-listarPorEstado (7.8 kB)
  eliminarSolicitudPrestamo: api-solicitud-prestamo-dev-eliminarSolicitudPrestamo (7.8 kB)

Deploying TABLA-SOPORTE...

Deploying "api-soporte" to stage "dev" (us-east-1)

✔ Service deployed to stack api-soporte-dev (23s)

endpoints:
  POST - https://on7ysj1462.execute-api.us-east-1.amazonaws.com/dev/soporte/crear
  DELETE - https://on7ysj1462.execute-api.us-east-1.amazonaws.com/dev/soporte/eliminar
  PUT - https://on7ysj1462.execute-api.us-east-1.amazonaws.com/dev/soporte/editar
  POST - https://on7ysj1462.execute-api.us-east-1.amazonaws.com/dev/soporte/obtener
  POST - https://on7ysj1462.execute-api.us-east-1.amazonaws.com/dev/soporte/listar
  POST - https://on7ysj1462.execute-api.us-east-1.amazonaws.com/dev/soporte/listar-usuario
  POST - https://on7ysj1462.execute-api.us-east-1.amazonaws.com/dev/soporte/responder
functions:
  CrearSolicitud: api-soporte-dev-CrearSolicitud (5.7 kB)
  EliminarSolicitud: api-soporte-dev-EliminarSolicitud (5.7 kB)
  EditarSolicitud: api-soporte-dev-EditarSolicitud (5.7 kB)
  ObtenerSolicitud: api-soporte-dev-ObtenerSolicitud (5.7 kB)
  ListarSolicitudes: api-soporte-dev-ListarSolicitudes (5.7 kB)
  ListarSolicitudesPorUsuario: api-soporte-dev-ListarSolicitudesPorUsuario (5.7 kB)
  ResponderSolicitud: api-soporte-dev-ResponderSolicitud (5.7 kB)

Deploying TABLA-TARJETAS...

Deploying "api-tarjetas" to stage "dev" (us-east-1)

✔ Service deployed to stack api-tarjetas-dev (23s)

endpoints:
  POST - https://wg2jlya60g.execute-api.us-east-1.amazonaws.com/dev/tarjetas/crear
  POST - https://wg2jlya60g.execute-api.us-east-1.amazonaws.com/dev/tarjetas/listar
  POST - https://wg2jlya60g.execute-api.us-east-1.amazonaws.com/dev/tarjetas/buscar
  PUT - https://wg2jlya60g.execute-api.us-east-1.amazonaws.com/dev/tarjetas/modificar
  DELETE - https://wg2jlya60g.execute-api.us-east-1.amazonaws.com/dev/tarjetas/eliminar
  POST - https://wg2jlya60g.execute-api.us-east-1.amazonaws.com/dev/tarjetas/recargar
  POST - https://wg2jlya60g.execute-api.us-east-1.amazonaws.com/dev/tarjetas/retirar
functions:
  CrearTarjeta: api-tarjetas-dev-CrearTarjeta (6.2 kB)
  ListarTarjetas: api-tarjetas-dev-ListarTarjetas (6.2 kB)
  BuscarTarjeta: api-tarjetas-dev-BuscarTarjeta (6.2 kB)
  ModificarTarjeta: api-tarjetas-dev-ModificarTarjeta (6.2 kB)
  EliminarTarjeta: api-tarjetas-dev-EliminarTarjeta (6.2 kB)
  RecargarTarjeta: api-tarjetas-dev-RecargarTarjeta (6.2 kB)
  RetirarTarjeta: api-tarjetas-dev-RetirarTarjeta (6.2 kB)

Deploying TABLA-TOKENS_ACCESO...

Deploying "api-tokens" to stage "dev" (us-east-1)

✔ Service deployed to stack api-tokens-dev (22s)

endpoint: POST - https://u64vwhx8z1.execute-api.us-east-1.amazonaws.com/dev/tokens/validar
functions:
  ValidarToken: api-tokens-dev-ValidarToken (658 B)

Deploying TABLA-TRANSACCION...

Deploying "api-transacciones" to stage "dev" (us-east-1)

✔ Service deployed to stack api-transacciones-dev (23s)

endpoints:
  POST - https://lpv8wsrqed.execute-api.us-east-1.amazonaws.com/dev/transaccion/crear
  DELETE - https://lpv8wsrqed.execute-api.us-east-1.amazonaws.com/dev/transaccion/eliminar
  POST - https://lpv8wsrqed.execute-api.us-east-1.amazonaws.com/dev/transaccion/obtener
  POST - https://lpv8wsrqed.execute-api.us-east-1.amazonaws.com/dev/transaccion/listar
functions:
  CrearTransaccion: api-transacciones-dev-CrearTransaccion (2.9 kB)
  EliminarTransaccion: api-transacciones-dev-EliminarTransaccion (2.9 kB)
  ObtenerTransaccion: api-transacciones-dev-ObtenerTransaccion (2.9 kB)
  ListarTransacciones: api-transacciones-dev-ListarTransacciones (2.9 kB)

Deploying TABLA-USUARIOS...

Deploying "api-usuarios" to stage "dev" (us-east-1)

✔ Service deployed to stack api-usuarios-dev (28s)

endpoints:
  POST - https://ot0i7774d1.execute-api.us-east-1.amazonaws.com/dev/usuarios/crear
  POST - https://ot0i7774d1.execute-api.us-east-1.amazonaws.com/dev/usuarios/listar
  POST - https://ot0i7774d1.execute-api.us-east-1.amazonaws.com/dev/usuarios/buscar
  DELETE - https://ot0i7774d1.execute-api.us-east-1.amazonaws.com/dev/usuarios/eliminar
  PUT - https://ot0i7774d1.execute-api.us-east-1.amazonaws.com/dev/usuarios/modificar
  POST - https://ot0i7774d1.execute-api.us-east-1.amazonaws.com/dev/usuarios/login
functions:
  CrearUsuario: api-usuarios-dev-CrearUsuario (4.7 kB)
  ListarUsuarios: api-usuarios-dev-ListarUsuarios (4.7 kB)
  BuscarUsuario: api-usuarios-dev-BuscarUsuario (4.7 kB)
  EliminarUsuario: api-usuarios-dev-EliminarUsuario (4.7 kB)
  ModificarUsuario: api-usuarios-dev-ModificarUsuario (4.7 kB)
  LoginUsuario: api-usuarios-dev-LoginUsuario (4.7 kB)
