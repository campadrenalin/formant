import pytest
from formant import template

def test_trivial():
    assert template("Hello world") == "Hello world"
    assert template("Hello, <% name %>.", name="Clarice") == "Hello, Clarice."

def test_missing_value():
    with pytest.raises(NameError):
        template("Hello, <% name %>.")

def test_bare():
    assert template("Hello, $name.", name='Joe') == "Hello, $name."

def test_eval():
    assert template("Hello, <% name.upper() %>.", name="Clarice") == "Hello, CLARICE."

def test_manual_sources():
    src1 = { "title": "SRC1 title", "body": "SRC1 body" }
    src2 = { "title": "SRC2 title", "author": "SRC2 author" }
    tmpl = "<% title %>, by <% author %>, says <% body %>."

    # Confirm that the priority order is kwargs, src1, src2... srcN
    with pytest.raises(NameError):
        template(tmpl)

    assert template(tmpl, src1, author="...") == "SRC1 title, by ..., says SRC1 body."
    assert template(tmpl, src2, body="...")   == "SRC2 title, by SRC2 author, says ...."
    assert template(tmpl, src1, src2) == "SRC1 title, by SRC2 author, says SRC1 body."
    assert template(tmpl, src1, src2, body='custom body') == "SRC1 title, by SRC2 author, says custom body."
