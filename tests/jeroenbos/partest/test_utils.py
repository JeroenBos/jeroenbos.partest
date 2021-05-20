import pytest

from jeroenbos.partest import utils


class TestUtilsMarkup:
    def test_markup_with_red(self):
        output = utils.markup("text", "red")
        assert output == "\x1b[31mtext\x1b[0m"

    def test_markup_without_returns_text_verbatim(self):
        output = utils.markup("text")
        assert output == "text"

    def test_markup_with_unknown_color_fails(self):
        with pytest.raises(ValueError):
            utils.markup("text", "nonexistentcolor")
