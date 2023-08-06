import json
import os

import rmk2.api


def test_save_response(tmpdir) -> None:
    """Check that saving function return values as JSON meets expectations"""

    @rmk2.api.save_response(prefix=tmpdir)
    def test_function() -> dict:
        return {"a": 1, "b": 2}

    output_called = test_function()

    output_files = os.listdir(tmpdir)

    assert len(output_files) == 1

    with open(
            os.path.join(tmpdir, output_files[0]), mode="r", encoding="utf-8"
    ) as infile:
        output_parsed = json.load(infile)

        assert output_parsed == output_called


def test_create_url() -> None:
    """Check that creating URLs meets expectations"""
    base_url = "https://example.com/foo/bar"
    path = ["baz", "bat"]
    query = {"foo": "1", "bar": 2}

    url_parsed = rmk2.api._create_url(base_url=base_url, path=path, query=query)

    url_expected = "".join(
        [
            base_url,
            "/",
            "/".join(path),
            f"?{'&'.join([k + '=' + str(v) for k, v in query.items()])}",
        ]
    )

    assert url_parsed == url_expected
