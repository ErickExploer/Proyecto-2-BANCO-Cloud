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
