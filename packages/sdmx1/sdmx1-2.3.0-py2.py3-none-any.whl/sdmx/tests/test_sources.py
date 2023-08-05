"""Tests against the actual APIs for specific data sources.

HTTP responses from the data sources are cached in tests/data/cache.
To force the data to be retrieved over the Internet, delete this directory.
"""
# TODO add a pytest argument for clearing this cache in conftest.py
import logging
from pathlib import Path
from typing import Any, Dict, Type

import pytest
import requests_mock

import sdmx
from sdmx import Client
from sdmx.exceptions import HTTPError

# Mark the whole file so the tests can be excluded/included
pytestmark = pytest.mark.source

log = logging.getLogger(__name__)


class DataSourceTest:
    """Base class for data source tests."""

    # TODO also test structure-specific data

    # Must be one of the IDs in sources.json.
    source_id: str

    # Mapping of endpoint → Exception subclass.
    # Tests of these endpoints are expected to fail.
    xfail: Dict[str, Type[Exception]] = {}

    # True to xfail if a 503 Error is returned
    tolerate_503 = False

    # Keyword arguments for particular endpoints
    endpoint_args: Dict[str, Dict[str, Any]] = {}

    @pytest.fixture
    def cache_path(self, test_data_path):
        # Use a common cache file for all agency tests
        (test_data_path / ".cache").mkdir(exist_ok=True)

        yield test_data_path / ".cache" / self.source_id

    @pytest.fixture
    def client(self, cache_path):
        return Client(self.source_id, cache_name=str(cache_path), backend="sqlite")

    # NB the following can be added to any subclass below for SSL failures. Update the
    #    docstring to describe the nature of the problem.
    # @pytest.fixture
    # def client(self, cache_path):
    #     """Identical to DataSourceTest, except skip SSL certificate verification.
    #
    #     As of [DATE], this source returns an invalid certificate.
    #     """
    #     return Client(
    #         self.source_id, cache_name=str(cache_path), backend="sqlite", verify=False
    #     )

    @pytest.mark.network
    def test_endpoint(self, cache_path, client, endpoint, args):
        # See sdmx.testing._generate_endpoint_tests() for values of `endpoint`
        cache = cache_path.with_suffix(f".{endpoint}.xml")
        result = client.get(endpoint, tofile=cache, **args)

        # For debugging
        # print(cache, cache.read_text(), result, sep='\n\n')
        # assert False

        sdmx.to_pandas(result)

        del result


class TestABS(DataSourceTest):
    source_id = "ABS"


class TestECB(DataSourceTest):
    source_id = "ECB"
    xfail = {
        # 404 Client Error: Not Found
        "provisionagreement": HTTPError
    }


# Data for requests_mock; see TestESTAT.mock()
estat_mock = {
    "http://ec.europa.eu/eurostat/SDMX/diss-web/rest/data/nama_10_gdp/..B1GQ+P3.": {
        "body": Path("ESTAT", "footer2.xml"),
        "headers": {
            "Content-Type": "application/vnd.sdmx.genericdata+xml; version=2.1"
        },
    },
    "http://ec.europa.eu/eurostat/SDMX/diss-web/file/7JUdWyAy4fmjBSWT": {
        # This file is a trimmed version of the actual response for the above query
        "body": Path("ESTAT", "footer2.zip"),
        "headers": {"Content-Type": "application/octet-stream"},
    },
}


class TestESTAT(DataSourceTest):
    source_id = "ESTAT"
    xfail = {
        # 404 Client Error: Not Found
        # NOTE the ESTAT service does not give a general response that contains all
        #      datastructures; this is really more of a 501.
        "datastructure": HTTPError
    }

    @pytest.fixture
    def mock(self, test_data_path):
        # Prepare the mock requests
        fixture = requests_mock.Mocker()
        for url, args in estat_mock.items():
            # str() here is for Python 3.5 compatibility
            args["body"] = open(str(test_data_path / args["body"]), "rb")
            fixture.get(url, **args)

        return fixture

    @pytest.mark.network
    def test_xml_footer(self, mock):
        client = Client(self.source_id)

        with mock:
            msg = client.get(url=list(estat_mock.keys())[0], get_footer_url=(1, 1))

        assert len(msg.data[0].obs) == 43

    @pytest.mark.network
    def test_ss_data(self, client):
        """Test a request for structure-specific data.

        Examples from:
        https://ec.europa.eu/eurostat/web/sdmx-web-services/example-queries
        """
        df_id = "nama_10_gdp"
        args = dict(resource_id=df_id)

        # Query for the DSD
        dsd = client.dataflow(**args).dataflow[df_id].structure

        # Even with ?references=all, ESTAT returns a short message with the
        # DSD as an external reference. Query again to get its actual contents.
        if dsd.is_external_reference:
            dsd = client.get(resource=dsd).structure[0]
            log.info(repr(dsd))

        assert not dsd.is_external_reference

        # Example query, using the DSD already retrieved
        args.update(
            dict(
                key=dict(UNIT=["CP_MEUR"], NA_ITEM=["B1GQ"], GEO=["LU"]),
                params={"startPeriod": "2012", "endPeriod": "2015"},
                dsd=dsd,
                # commented: for debugging
                # tofile='temp.xml',
            )
        )
        client.data(**args)


class TestIMF(DataSourceTest):
    source_id = "IMF"


class TestILO(DataSourceTest):
    source_id = "ILO"
    xfail = {
        # 413 Client Error: Client Entity Too Large
        "codelist": HTTPError
    }

    @pytest.mark.network
    def test_codelist(self, cache_path, client):
        client.get(
            "codelist", "CL_ECO", tofile=cache_path.with_suffix("." + "codelist-CL_ECO")
        )


class TestINEGI(DataSourceTest):
    source_id = "INEGI"
    endpoint_args = dict(
        # 404 Not Found when the own source's ID ("INEGI") is used
        conceptscheme=dict(provider="ALL")
    )


class TestINSEE(DataSourceTest):
    source_id = "INSEE"


class TestISTAT(DataSourceTest):
    source_id = "ISTAT"

    @pytest.mark.network
    def test_gh_75(self, specimen, client):
        """Test of https://github.com/dr-leo/pandaSDMX/pull/75.

        As of the original report on 2019-06-02, the 4th dimension was ``TIPO_DATO``,
        and the 5th ``TIPO_GESTIONE``. As of 2021-01-30, these are transposed, and the
        4th dimension name is ``TIPO_GEST``.
        """

        df_id = "47_850"

        # Reported Dataflow query works
        # Without references="datastructure", this is a very slow query
        df = client.dataflow(df_id, params={"references": "datastructure"}).dataflow[
            df_id
        ]

        # dict() key for the query
        data_key = dict(
            FREQ=["A"],
            ITTER107=["001001+001002"],
            SETTITOLARE=["1"],
            TIPO_GEST=["ALL"],
            TIPO_DATO=["AUTP"],
            TIPSERVSOC=["ALL"],
        )

        # Dimension components are in the correct order
        assert [dim.id for dim in df.structure.dimensions.components] == list(
            data_key.keys()
        ) + ["TIME_PERIOD"]

        # Reported data query works
        # NB the reported query key was "A.001001+001002.1.AUTP.ALL.ALL"; adjusted per
        #    the DSD change (above).
        client.data(df_id, key="A.001001+001002.1.ALL.AUTP.ALL")

        # Use a dict() key to force Client to make a sub-query for the DSD
        client.data(df_id, key=data_key)


class TestLSD(DataSourceTest):
    source_id = "LSD"
    endpoint_args = {
        # Using the example from the documentation
        "data": dict(
            resource_id="S3R629_M3010217",
            params=dict(startPeriod="2005-01", endPeriod="2007-01"),
        )
    }

    @pytest.fixture
    def client(self, cache_path):
        """Identical to DataSourceTest, except skip SSL certificate verification.

        As of 2021-01-30, this source returns a certificate that is treated as invalid
        by the GitHub Actions job runner; but *not* on a local machine.
        """
        return Client(
            self.source_id, cache_name=str(cache_path), backend="sqlite", verify=False
        )


class TestNB(DataSourceTest):
    """Norges Bank.

    This source returns a valid SDMX Error message (100 No Results Found) for the
    'categoryscheme' endpoint.
    """

    source_id = "NB"


class TestNBB(DataSourceTest):
    source_id = "NBB"
    endpoint_args = {
        "data": dict(
            resource_id="REGPOP",
            key="POPULA.000.",
            params=dict(startTime=2013, endTime=2017),
        )
    }


class TestOECD(DataSourceTest):
    source_id = "OECD"
    endpoint_args = {
        "data": dict(
            resource_id="ITF_GOODS_TRANSPORT", key=".T-CONT-RL-TEU+T-CONT-RL-TON"
        )
    }


class TestSGR(DataSourceTest):
    source_id = "SGR"


class TestSPC(DataSourceTest):
    source_id = "SPC"
    endpoint_args = {
        "data": dict(
            resource_id="DF_CPI",
            key="A.CK+FJ..",
            params=dict(startPeriod=2010, endPeriod=2015),
        )
    }


class TestSTAT_EE(DataSourceTest):
    source_id = "STAT_EE"
    endpoint_args = {
        # Using the example from the documentation
        "data": dict(
            resource_id="VK12",
            key="TRD_VAL+TRD_VAL_PREV..TOTAL.A",
            params=dict(startTime=2013, endTime=2017),
        )
    }


class TestUNESCO(DataSourceTest):
    """UNESCO.

    Most endpoints are marked XFAIL because the service requires registration.
    """

    source_id = "UNESCO"
    xfail = {
        # Requires registration
        "categoryscheme": HTTPError,
        "codelist": HTTPError,
        "conceptscheme": HTTPError,
        "dataflow": HTTPError,
        "provisionagreement": HTTPError,
        # Because 'supports_series_keys_only' was set
        # TODO check
        # 'datastructure': NotImplementedError,
    }


class TestUNICEF(DataSourceTest):
    source_id = "UNICEF"

    @pytest.mark.network
    def test_data(self, client):
        dsd = client.dataflow("GLOBAL_DATAFLOW").structure[0]
        client.data("GLOBAL_DATAFLOW", key="ALB+DZA.MNCH_INSTDEL.", dsd=dsd)


class TestUNSD(DataSourceTest):
    source_id = "UNSD"


class TestWB(DataSourceTest):
    source_id = "WB"


class TestWB_WDI(DataSourceTest):
    source_id = "WB_WDI"
    endpoint_args = {
        # Example from the documentation website
        "data": dict(
            resource_id="WDI",
            key="A.SP_POP_TOTL.AFG",
            params=dict(startPeriod="2011", endPeriod="2011"),
        )
    }
