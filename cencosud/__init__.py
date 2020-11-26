# -*- coding: utf-8 -*-
"""Inicialización del proyecto."""


# from bolsa_emergente._logging import configure_logging
from cencosud.settings import init_project_settings

SETTINGS = init_project_settings()

SETTINGS.DATA_PATH.mkdir(parents=True, exist_ok=True)
