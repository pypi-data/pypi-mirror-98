import pytest
import tuxmake
from tuxmake.config import ConfigurableObject


@pytest.fixture(autouse=True)
def setup(mocker, monkeypatch, tmp_path):
    monkeypatch.setattr(tuxmake.config.ConfigurableObject, "basedir", "test")
    mocker.patch("pathlib.Path.parent", return_value=tmp_path)
    (tmp_path / "test").mkdir()
    (tmp_path / "test" / "foo.ini").touch()


def test_constructor_calls___init_config__(mocker):
    __init_config__ = mocker.patch("tuxmake.config.ConfigurableObject.__init_config__")
    ConfigurableObject("foo")
    __init_config__.assert_called()


def test___init_config___not_implemented():
    with pytest.raises(NotImplementedError):
        ConfigurableObject("foo")
