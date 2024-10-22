import json
import os

import pytest
from nb2workflow.nbadapter import run


@pytest.fixture
def par_dict():
    # returns the default values set in the web gui
    return {
        "T1": "2017-03-06T13:26:48.0",
        "T2": "2017-03-06T15:32:27.0",
        "RA": 265.97845833,
        "DEC": -29.74516667,
        "src_name": "1E 1740.7-2942",
        "use_default_catalog": True,
        "integral_data_rights": "all-private",
        "host_type": "production",
    }


@pytest.fixture
def notebook_dir():
    base_dir = os.path.abspath(__file__)
    return os.path.join(os.path.dirname(base_dir), "test_notebooks")


def test_picture_workflow(par_dict, notebook_dir):
    # This workflows tests if an image product is returned. We cannot test.

    test_path = os.path.join(notebook_dir, "simple_picture_workflow.ipynb")

    # Beware: the PictureProduct is serialzed before being returned. Thus,
    # we get a string here.
    test_output: str = json.loads(run(test_path, par_dict)["result_image"])
    assert test_output is not None
    assert test_output["img_type"] == "png"


def test_table_workflow(par_dict, notebook_dir):
    # The return of this workflow should be a ODAAstropyTable data product.

    test_path = os.path.join(notebook_dir, "simple_table_workflow.ipynb")

    # in contrast to PictureProduct, ODAAstropyTable is not fully serialized.
    # The root key 'output' has a string as argument which is
    # supposed to be a JSON.
    test_output = run(test_path, par_dict)
    data = json.loads(test_output["output"])

    assert "output" in test_output.keys()
    assert "binary" in data.keys()


def test_boolean_workflow(par_dict, notebook_dir):
    # There is no boolean data product. We use ODATextProduct
    test_path = os.path.join(notebook_dir, "simple_boolean_workflow.ipynb")

    # This test is straight forward. This data product is a JSON.
    test_output = run(test_path, par_dict)
    assert "result" in test_output.keys()
    assert test_output["result"] == "FALSE"


def test_lc_workflow(par_dict, notebook_dir):
    test_path = os.path.join(notebook_dir, "simple_lc_workflow.ipynb")
        
    test_output: str = run(test_path, par_dict)
    assert "result" in test_output.keys()
