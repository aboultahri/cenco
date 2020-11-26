# -*- coding: utf-8 -*-
"""Settings del proyecto."""
import logging
import os
from pathlib import Path
from typing import Optional
from typing import Union

from dotenv import find_dotenv
from dotenv import load_dotenv
from pydantic import BaseSettings
from pydantic import SecretStr  # pylint: disable=no-name-in-module

from cencosud.exc import EnvVarNotFound


def init_dotenv():
    """Localiza y carga archivo `.env`.

    Setea como variables de entorno las variables definidas en el
    archivo `.env`

    """

    candidate = find_dotenv(usecwd=True)

    if not candidate:
        # raise IOError(f"Can't find .env file")
        return

    load_dotenv(candidate)


class Settings(BaseSettings):
    """Configuraciones comumnes."""

    PACKAGE_PATH = Path(__file__).parent

    PROJECT_PATH = PACKAGE_PATH.parent

    DATA_PATH = Path(PROJECT_PATH, "data")

    CONNECTION_STRING: SecretStr


class Production(Settings):
    """Configuraciones ambiente de producción."""


class Development(Settings):
    """Configuraciones ambiente de desarrollo."""


def init_project_settings():
    """Retorna las settings del proyecto de acuerdo a envars."""

    init_dotenv()

    mode = os.environ.get("PROJECT_MODE")

    if not mode:
        raise EnvVarNotFound(env_var="PROJECT_MODE")

    if mode == "Development":
        return Development()

    if mode == "Production":
        return Production()

    raise ValueError("env_var `PROJECT_MODE` debe ser `Development` o `Production`")
