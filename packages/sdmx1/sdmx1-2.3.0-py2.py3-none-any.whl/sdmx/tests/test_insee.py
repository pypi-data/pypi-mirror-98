# TODO tidy these tests to use fixtures/methods from sdmx.tests
from collections import OrderedDict
from pathlib import Path

import pytest

import sdmx

BASE_PATH = Path(".") / "INSEE"

DATAFLOW_FP = "dataflow.xml"

DATASETS = {
    "IPI-2010-A21": {
        "data-fp": "IPI-2010-A21.xml",
        "datastructure-fp": "IPI-2010-A21-structure.xml",
        "series_count": 20,
    },
    "CNA-2010-CONSO-SI-A17": {
        "data-fp": "CNA-2010-CONSO-SI-A17.xml",
        "datastructure-fp": "CNA-2010-CONSO-SI-A17-structure.xml",
        "series_count": 1,
    },
}

SERIES = {"UNEMPLOYMENT_CAT_A_B_C": {"data-fp": "bug-series-freq-data.xml"}}


class TestINSEE:
    @pytest.fixture
    def base_path(self, test_data_path):
        yield test_data_path / "INSEE"

    def test_load_dataset(self, base_path):
        dataset_code = "IPI-2010-A21"

        # Load all dataflows
        dataflows_response = sdmx.read_sdmx(base_path / DATAFLOW_FP)
        dataflows = dataflows_response.dataflow

        assert len(dataflows) == 663
        assert dataset_code in dataflows

        # Load datastructure for current dataset_code
        fp_datastructure = base_path / DATASETS[dataset_code]["datastructure-fp"]
        datastructure_response = sdmx.read_sdmx(fp_datastructure)
        assert dataset_code in datastructure_response.dataflow
        dsd = datastructure_response.dataflow[dataset_code].structure

        # Verify dimensions list
        dimensions = OrderedDict(
            [dim.id, dim]
            for dim in dsd.dimensions
            if dim.id not in ["TIME", "TIME_PERIOD"]
        )
        dim_keys = list(dimensions.keys())
        assert dim_keys == ["FREQ", "PRODUIT", "NATURE"]

        # Load datas for the current dataset
        fp_data = base_path / DATASETS[dataset_code]["data-fp"]
        data = sdmx.read_sdmx(fp_data)

        # Verify series count and values
        series = data.data[0].series
        series_count = len(series)
        assert series_count == DATASETS[dataset_code]["series_count"]

        first_series = series[0]
        observations = first_series

        first_obs = observations[0]
        last_obs = observations[-1]

        assert first_obs.dim == "2015-10"
        assert first_obs.value == "105.61"

        assert last_obs.dim == "1990-01"
        assert last_obs.value == "139.22"

    def test_fixe_key_names(self, base_path):
        """Verify key or attribute contains '-' in name."""
        dataset_code = "CNA-2010-CONSO-SI-A17"

        fp_datastructure = base_path / DATASETS[dataset_code]["datastructure-fp"]
        datastructure_response = sdmx.read_sdmx(fp_datastructure)
        assert dataset_code in datastructure_response.dataflow
        dsd = datastructure_response.dataflow[dataset_code].structure

        dimensions = OrderedDict(
            [dim.id, dim]
            for dim in dsd.dimensions
            if dim.id not in ["TIME", "TIME_PERIOD"]
        )
        dim_keys = list(dimensions.keys())
        assert dim_keys == ["SECT-INST", "OPERATION", "PRODUIT", "PRIX"]

        fp_data = base_path / DATASETS[dataset_code]["data-fp"]
        data = sdmx.read_sdmx(fp_data)
        series = data.data[0].series
        series_key = list(series.keys())[0]

        assert list(series_key.values.keys()) == [
            "SECT-INST",
            "OPERATION",
            "PRODUIT",
            "PRIX",
        ]

        assert list(series_key.attrib.keys()) == [
            "FREQ",
            "IDBANK",
            "TITLE",
            "LAST_UPDATE",
            "UNIT_MEASURE",
            "UNIT_MULT",
            "REF_AREA",
            "DECIMALS",
            "BASE_PER",
            "TIME_PER_COLLECT",
        ]

    def test_freq_in_series_attribute(self, base_path):
        # Test that we don't have regression on Issues #39 and #41
        # INSEE time series provide the FREQ value as attribute on the series
        # instead of a dimension. This caused a runtime error when writing as
        # pandas dataframe.
        data_response = sdmx.read_sdmx(
            base_path / SERIES["UNEMPLOYMENT_CAT_A_B_C"]["data-fp"]
        )
        sdmx.to_pandas(data_response)
