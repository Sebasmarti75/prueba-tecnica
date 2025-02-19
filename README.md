# Levantar los servicios con Docker compose

docker-compose up --build

utilizando esta linea en la terminal se deben levantar los servicios que estan alojados en cada uno de los contenedores de docker

# comunicacion entre cada uno de los microservicios

1.Cada microservicio corre en un contenedor separado, con su propia dirección IP dentro de la red interna de Docker.

2.Como tal Docker compose crea una red llamada default, donde todos los servicios dentro del docker-compose.yml pueden comunicarse usando sus nombres de servicio.

# Puertos utilizados

usuarios 8001
publicaciones 8000