import json
from .handler import handle

import flask

app = flask.Flask(__name__)


# Test your handler here

# To disable testing, you can set the build_arg `TEST_ENABLED=false` on the CLI or in your stack.yml
# https://docs.openfaas.com/reference/yaml/#function-build-args-build-args

def test_handle():
    with app.test_request_context('/', data="input"):
        assert flask.request.path == '/'
        raw_output = handle(flask.request)
        output = json.loads(raw_output)

        assert output.get("echo") == "input"
        assert 0.0 <= output.get("random") <= 1.0