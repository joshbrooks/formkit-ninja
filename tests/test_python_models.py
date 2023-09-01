import json
from importlib.resources import files

import pytest

from formkit_ninja import formkit_schema, models, samples
from tests.fixtures import sf11, sf11meetinginfo


@pytest.fixture
def element_schema():
    schema = json.loads(files(samples).joinpath("element.json").read_text())
    return formkit_schema.FormKitSchema.parse_obj(schema)


@pytest.fixture
def sf11_schema():
    schema = json.loads(files(samples).joinpath("sf11_v2.json").read_text())
    return formkit_schema.FormKitSchema.parse_obj(schema)


def test_node_parse():
    schema = json.loads(files(samples).joinpath("element.json").read_text())
    formkit_schema.FormKitNode.parse_obj(schema[0])
    formkit_schema.FormKitSchema.parse_obj(schema)


@pytest.mark.django_db()
def test_create_schema():
    c = models.FormKitSchema.objects.create()


@pytest.mark.django_db()
def test_create_from_schema(element_schema):
    """
    Create a database entry from a FormKit schema
    """
    c = models.FormKitSchema.from_pydantic(element_schema)
    # This test schema has one node
    assert c.nodes.count() == 1

    # The node...
    dictify = c.nodes.first().get_node().dict(exclude_none=True)

    # The node looks like this:
    # {'children': [], 'node_type': 'element', 'el': 'div', 'attrs': {'style': {...}, 'data-foo': 'bar'}}

    assert set(dictify.keys()) == {"node_type", "children", "el", "attrs"}
    assert dictify["children"] == []
    assert dictify["node_type"] == "element"
    assert dictify["el"] == "div"
    assert set(dictify["attrs"].keys()) == {"style", "data-foo"}


@pytest.mark.django_db()
def test_create_from_schema(sf11_schema):
    """
    Create a database entry from the 'old' SF11 schema
    """
    c = models.FormKitSchema.from_pydantic(sf11_schema)
    # This test schema has one node
    # assert c.nodes.count() == 94

    # A 'group' node

    first_node = c.nodes.first()

    c.nodes.first().get_node().dict(exclude_none=True, exclude={"children"})


@pytest.mark.django_db()
def test_parse_sf11(sf11: list[dict]):
    """
    This tests that we can successfully import the 'SF11' form from Partisipa
    """
    from formkit_ninja.formkit_schema import FormKitSchema as BaseModel
    schema = BaseModel.parse_obj(sf11)
    schema_in_the_db = models.FormKitSchema.from_pydantic(schema)
    schema_back_from_db = schema_in_the_db.to_pydantic()
    
    # Check that schema sections retained their order
    assert [n['html_id'] for n in sf11] == [n.html_id for n in schema_back_from_db.__root__]
    
    # The input dict and output dict should be equal
    sf11_out = schema_back_from_db.dict()['__root__']

    # Check that the label is not altered
    # This should be the ""
    assert schema_back_from_db.__root__[2].children[0].label == "$pgettext('partisipants', 'Total participants male')"

    # Nested (children) should retain their order
    assert [n.key for n in schema_back_from_db.__root__[0].children] == [n['key'] for n in sf11[0]['children']]