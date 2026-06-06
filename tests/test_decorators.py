import pytest

from src.decorators import log


def test_log_success(capsys: pytest.CaptureFixture) -> None:
    @log()
    def add(a: int, b: int) -> int:
        return a + b

    assert add(2, 3) == 5
    out = capsys.readouterr().out
    assert "Вызвана функция add" in out
    assert "add - OK - 5" in out


def test_log_error(capsys: pytest.CaptureFixture) -> None:
    @log()
    def div(a: int, b: int) -> float:
        return a / b

    with pytest.raises(ZeroDivisionError):
        div(10, 0)

    out = capsys.readouterr().out
    assert "Вызвана функция div" in out
    assert "ZeroDivisionError" in out
    assert "args: (10, 0)" in out
