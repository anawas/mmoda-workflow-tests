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
def notebook_path():
    def _notebook_path(notebook_name: str):
        base_dir = os.path.abspath(__file__)
        base_dir = os.path.join(os.path.dirname(base_dir), "test_notebooks/simple")
        return os.path.join(base_dir, f"simple_{notebook_name}_workflow.ipynb")
    
    return _notebook_path


def test_args(notebook_path):
    path = notebook_path("test")
    assert "simple_test_workflow" in path


def test_picture_workflow(par_dict, notebook_path):
    # This workflows tests if an image product is returned. We cannot test.

    test_path = notebook_path("picture")

    # Beware: the PictureProduct is serialzed before being returned. Thus,
    # we get a string here.
    test_output: str = json.loads(run(test_path, par_dict)["result_image"])
    assert test_output is not None
    assert test_output["img_type"] == "png"


def test_table_workflow(par_dict, notebook_path):
    # The return of this workflow should be a ODAAstropyTable data product.

    test_path = notebook_path("table")

    # in contrast to PictureProduct, ODAAstropyTable is not fully serialized.
    # The root key 'output' has a string as argument which is
    # supposed to be a JSON.
    test_output = run(test_path, par_dict)
    data = json.loads(test_output["output"])

    assert "output" in test_output.keys()
    assert "binary" in data.keys()


def test_boolean_workflow(par_dict, notebook_path):
    # There is no boolean data product. We use ODATextProduct
    test_path = notebook_path("boolean")

    # This test is straight forward. This data product is a JSON.
    test_output = run(test_path, par_dict)
    assert "result" in test_output.keys()
    assert test_output["result"] == "FALSE"


def test_lc_workflow(par_dict, notebook_path):
    # This returns a LightCurveList
    test_path = notebook_path("lc")
        
    test_output: str = run(test_path, par_dict)
    assert "result" in test_output.keys()

def test_sleep_workflow(par_dict, notebook_path):
    # This returns a ODATextProduct
    # This runs for 10 secs and then returns
    test_path = notebook_path("sleeping")
        
    test_output: str = run(test_path, par_dict)
    assert "out_text" in test_output.keys()
    assert "Sleeped".lower() in test_output["out_text"].lower() 

def test_param_workflow(par_dict, notebook_path):
    # This workflow returns no product. It's kind of useless.
    # But it's part of 'nb2w-example' written by D. Savchenko.
    test_path = notebook_path("param")
        
    test_output: str = run(test_path, par_dict)
    assert "result" not in test_output.keys()

