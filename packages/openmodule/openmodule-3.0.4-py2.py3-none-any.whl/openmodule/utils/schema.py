import json
import os


class RPCSchema:
    def __init__(self, channel, typ, request, response):
        self.channel = channel
        self.type = typ
        self.request = request.__name__
        self.response = response.__name__

    def render(self):
        return dict(post=dict(summary=f"{self.channel} - {self.type} rpc", requestBody=dict(
            content={"application/json": dict(schema={"$ref": f"#/components/schemas/{self.request}"})},
            required=True), responses={"200": dict(description="response", content={
            "application/json": dict(schema={"$ref": f"#/components/schemas/{self.response}"})})}))


class SchemaClass:
    """
    Renders a valid OpenApi JSON Schema of rpcs and pydantic models that can be displayed  with Swagger
    """

    def __init__(self):
        self.rpcs = dict()
        self.models = dict()

    def save_rpc(self, channel, typ, request, response):
        rpc_key = f"/{channel}/{typ}"
        self.rpcs[rpc_key] = RPCSchema(channel, typ, request, response)
        self.save_model(request)
        self.save_model(response)

    def save_model(self, model):
        self.models[model.__name__] = model

    def __str__(self):
        return json.dumps(self.render_schema())

    def clear(self):
        self.rpcs = dict()
        self.models = dict()

    def render_schema(self):
        res = dict(openapi="3.0.0", info=dict(title="RPC API", version="1.0.0"))
        paths = self.render_rpcs()
        if paths:
            res["paths"] = paths
        models = self.render_models()
        if models:
            res["components"] = dict(schemas=models)
        return res

    def render_rpcs(self):
        result = dict()
        for key, value in self.rpcs.items():
            result[key] = value.render()
        return result

    def render_models(self):
        result = dict()
        for name, model in self.models.items():
            model_schema = model.schema().copy()
            definitions = model_schema.pop("definitions", {})
            result[name] = model_schema
            for key, value in definitions.items():
                result[key] = value
        result = json.loads(json.dumps(result).replace("#/definitions/", "#/components/schemas/"))
        return result

    def to_file(self, file_name=None):
        file_name = file_name or os.environ.get("SCHEMA_FILE", "../schemas.json")
        if os.path.exists(file_name):
            with open(file_name, "r") as file:
                schema = json.loads(file.read())
                models = self.render_models()
                rpcs = self.render_rpcs()
                if schema.get("paths"):
                    schema["paths"].update(rpcs)
                else:
                    schema["paths"] = rpcs
                if schema.get("components"):
                    schema["components"]["schemas"] = models
                else:
                    schema["components"] = dict(schemas=models)
                data = json.dumps(schema)
        else:
            data = str(self)
        with open(file_name, "w") as file:
            file.write(data)


Schema = SchemaClass()
