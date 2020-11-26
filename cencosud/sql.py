# -*- coding: utf-8 -*-
"""Queries SQL."""
import csv
from pathlib import Path

from cencosud import SETTINGS
from cencosud.reflect_db import Pricing
from cencosud.reflect_db import Ventas
from cencosud.session import session_scope

CHUNK_SIZE = 5000

# pylint: disable=no-member
# TODO: FILTRAR POR FECHA


def table_to_csv(
    table_class,
    save_path: Path,
    store_id: int = 1,
    category_id: int = 5,
):
    """Guarda en un archivo csv el resultado de query sobre `TABLA_VENTAS` o `TABLA_PRICING`.

    Eventualmente este método podría ser reemplazado usando la librería `pandas`
    leyendo la tabla con el método `pandas.read_sql_table` y luego guardandola
    en un archivo csv. Este método solo usa la funcionalidad de `sqlalchemy`.

    Guardar el archivo como un csv tiene un fin demostrativo y para ser usado
    en el entrenamiento de modelo forecasting , y eventualmente
    se podría guardar el resultado del filtro en otra tabla, o simplemente
    el modelo puede usar la query directamente (sin previamente guardar el resultado)

    Args:
        save_path: Path del archivo de salida.
        store_id: Id de la tienda
        category_id: Id de la categoría del producto.

    """

    if table_class not in [Ventas, Pricing]:
        raise ValueError(
            "Parámetro `table_class` debe ser `cencosud.schemas.Ventas` o`cencosud.schemas.Prcing`"
        )

    with open(save_path, "w", encoding="utf-8") as fh:
        excludes = ["TIENDA", "ID_CATEGORIA"]
        header = [
            c.name for c in table_class.__table__.columns if c.name not in excludes
        ]
        outcsv = csv.writer(fh, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        outcsv.writerow(header)
        with session_scope() as sess:
            batch_iterator = (
                sess.query(table_class)
                .filter_by(TIENDA=store_id, ID_CATEGORIA=category_id)
                .yield_per(CHUNK_SIZE)
            )
            for row in batch_iterator:
                outcsv.writerow(row.to_dict(excludes=excludes).values())
