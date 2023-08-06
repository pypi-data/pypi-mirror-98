import os

import pytest

from coralillo import Engine, Model, fields
from coralillo.auth import PermissionHolder

from .models import bound_models


@pytest.fixture
def nrm():
    nrm = Engine(host=os.getenv('REDIS_HOST', 'localhost'))

    nrm.lua.drop(args=['*'])

    bound_models(nrm)

    return nrm


@pytest.fixture
def user(nrm):
    class User(Model, PermissionHolder):
        name = fields.Text()

        class Meta:
            engine = nrm

    return User(
        name='juan',
    ).save()
