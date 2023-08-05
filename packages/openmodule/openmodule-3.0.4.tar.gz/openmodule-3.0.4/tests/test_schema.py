import json
import os
from unittest import TestCase

from openmodule.models.backend import AccessRequest, AccessResponse
from openmodule.utils.schema import Schema


class SchemaTest(TestCase):
    def tearDown(self) -> None:
        try:
            os.remove("../schemas.json")
        except FileNotFoundError:
            pass
        Schema.clear()
        super().tearDown()

    def setUp(self) -> None:
        super().setUp()
        try:
            os.remove("../schemas.json")
        except FileNotFoundError:
            pass
        Schema.clear()

    def test_models(self):
        Schema.save_model(AccessRequest)
        schema = Schema.render_schema()
        length = len(schema["components"]["schemas"])
        self.assertEqual(1, len(Schema.models))
        self.assertIn("AccessRequest", schema["components"]["schemas"])
        self.assertEqual(None, schema.get("paths"))

        # same model
        Schema.save_model(AccessRequest)
        schema = Schema.render_schema()
        self.assertEqual(1, len(Schema.models))
        self.assertIn("AccessRequest", schema["components"]["schemas"])
        self.assertEqual(None, schema.get("paths"))
        self.assertEqual(length, len(schema["components"]["schemas"]))

        Schema.save_model(AccessResponse)
        schema1 = Schema.render_schema()
        self.assertEqual(2, len(Schema.models))
        self.assertIn("AccessRequest", schema["components"]["schemas"])
        self.assertIn("AccessResponse", schema1["components"]["schemas"])
        self.assertGreaterEqual(len(schema1["components"]["schemas"]), length)

    def test_rpcs(self):
        Schema.save_rpc("backend", "auth", AccessRequest, AccessResponse)
        self.assertEqual(1, len(Schema.rpcs))

        schema = Schema.render_schema()
        self.assertIn("/backend/auth", schema["paths"])
        self.assertEqual(len(schema["paths"]), 1)

        Schema.save_rpc("backend", "auth", AccessRequest, AccessResponse)
        schema = Schema.render_schema()
        self.assertIn("/backend/auth", schema["paths"])
        self.assertEqual(1, len(Schema.rpcs))
        self.assertEqual(len(schema["paths"]), 1)

        Schema.save_rpc("backend", "abc", AccessRequest, AccessResponse)
        schema = Schema.render_schema()
        self.assertIn("/backend/abc", schema["paths"])
        self.assertIn("/backend/auth", schema["paths"])
        self.assertEqual(2, len(Schema.rpcs))
        self.assertEqual(len(schema["paths"]), 2)

    def test_file(self):
        def get_file_data():
            with open("../schemas.json", "r") as file:
                return json.loads(file.read())

        Schema.to_file()
        data = get_file_data()
        self.assertEqual(None, data.get("paths"))
        self.assertEqual(None, data.get("components"))

        Schema.save_rpc("backend", "auth", AccessRequest, AccessResponse)
        Schema.to_file()
        data = get_file_data()
        self.assertEqual(1, len(data["paths"]))

        Schema.save_rpc("backend", "auth", AccessRequest, AccessResponse)
        Schema.to_file()
        data = get_file_data()
        self.assertEqual(1, len(data["paths"]))

        Schema.save_rpc("backend", "abc", AccessRequest, AccessResponse)
        Schema.to_file()
        data = get_file_data()
        self.assertEqual(2, len(data["paths"]))

        # add empty Schema
        Schema.clear()
        Schema.to_file()
        data = get_file_data()
        self.assertEqual(2, len(data["paths"]))

    def test_clear(self):
        self.assertEqual(0, len(Schema.models))
        self.assertEqual(0, len(Schema.rpcs))
        Schema.save_rpc("backend", "auth", AccessRequest, AccessResponse)

        self.assertEqual(2, len(Schema.models))
        self.assertEqual(1, len(Schema.rpcs))

        Schema.clear()
        self.assertEqual(0, len(Schema.models))
        self.assertEqual(0, len(Schema.rpcs))


