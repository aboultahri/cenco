# -*- coding: utf-8 -*-
"""Reflexión del schema de base de datos en Object Relational Mapper (ORM)."""
from typing import List
from typing import Optional

from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

from cencosud.exc import TableNotFound
from cencosud.session import ENGINE


class _Base:
    """Clase base con definiciones comunes para todas las tablas."""

    def to_dict(self, excludes: Optional[List[str]] = None):
        """Serialización de filas."""

        serialized = {
            c.name: getattr(self, c.name)
            for c in self.__table__.columns  # pylint: disable=no-member
            if c.name  
        }
        if excludes:
            for exc in excludes:
                del serialized[exc]

        return serialized


def reflect_database(engine=ENGINE):
    """Refleja schema de base de datos en ORM.
    
    Simplemente reflejamos la base de datos en clases (tablas -> clases)
    Usamos definición dinámica de clases usando la función `type`. Notar
    que las tablas presentadas en el ejmplo no venían con primary_keys en
    su esquema, y el sqlalchemy necesita al menos una llave primaria para
    hacer el mapeo ORM. Sin embargo, una solución rápida a este pequeño
    problema, es considerar la fila entera como primary_key, por eso
    en el seteo dinámico de las clases agregamos el `__mapper_args__`
    
    """

    Base = declarative_base()
    metadata = MetaData(bind=engine)
    Base.metadata = metadata
    metadata.reflect()
    tables_dict = {}

    for tablename, tableobj in metadata.tables.items():

        tables_dict[tablename] = type(
            str(tablename),
            (
                _Base,
                Base,
            ),
            {
                "__table__": tableobj,
                "__mapper_args__": {"primary_key": [c for c in tableobj.columns]},
            },
        )

    return tables_dict


TABLES = reflect_database()

try:
    Categorias = TABLES["TABLA_CATEGORIAS"]

    Pais = TABLES["TABLA_PAIS"]

    Pricing = TABLES["TABLA_PRICING"]

    Tiendas = TABLES["TABLA_TIENDAS"]

    Transacciones = TABLES["TABLA_TRANSACCIONES"]

    Ventas = TABLES["TABLA_VENTAS"]

except KeyError as exc:
    raise TableNotFound from exc
