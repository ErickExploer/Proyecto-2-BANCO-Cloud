#!/bin/bash
services=(TABLA-CUENTA TABLA-PAGOS TABLA-PRESTAMOS TABLA-SOLICITUD-PRESTAMO TABLA-SOPORTE TABLA-TARJETAS TABLA-TOKENS_ACCESO TABLA-TRANSACCION TABLA-USUARIOS)

for service in "${services[@]}"
do
  echo "Deploying $service..."
  cd $service
  npx serverless deploy
  cd ..
done
