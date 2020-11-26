# Léeme

Una muy simple codificación
### Instalación

Requerimos python 3.7 o más y [poetry](https://python-poetry.org/).

Instalación sin [tox](https://python-poetry.org/). Como observación, al ser una prueba las dev dependencies y prod dependencies pueden considerarse una sola.

```sh
$ cd cencosud
$ python3 -m venv .venv
$ poetry install
```
con tox

```sh
$ cd cencosud
$ tox -e venv
```
### Variables de entorno

Se necesitan las variables de entorno `PROJECT_MODE` y `CONNECTION_STRING`. Dichas variables pueden ser seteadas manualmente usando por ejemplo `export` ó escribirlas en un archivo `.env` de la forma `key=value`. Para esto último editar el archivo `.env.dist` en la raiz del proyecto, al agregar los valores de las variables y luego cambiar su nombre a `.env`. Las variables son `PROJECT_MODE=Development` y `CONNECTION_STRING` es la conection string a la db (`sqlite:///path_to_db`)


### Uso

Los problemas de la prueba están en un jupyter notebook contenido en la raíz del proyecto.

```sh
$ cd cencosud
$ .venv/bin/activate #linux, windows se activa el virtual env usando.venv\Scripts\activate
$ jupyter notebook

```

