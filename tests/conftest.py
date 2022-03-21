# coding: utf-8
from pathlib import Path
import pytest
from decouple import AutoConfig


@pytest.fixture
def config(path):
    return AutoConfig(path)


@pytest.fixture
def path(request):
    return Path(__file__).parent.joinpath('autoconfig', *request.param).as_posix()
