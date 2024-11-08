
import graphene
from graphene_file_upload.scalars import Upload

class Error(graphene.ObjectType):
    field = graphene.String(required=True)
    message = graphene.String(required=True)


class Prediction(graphene.ObjectType):
    class_id = graphene.Int(required=True)
    probability = graphene.Float(required=True)
    class_name = graphene.String(required=True)
    text = graphene.String(required=True)



class MetaResponse(graphene.ObjectType):
    programmer = graphene.String(required=True)
    main = graphene.String(required=True)
    description = graphene.String(required=True)
    language = graphene.String(required=True)
    libraries = graphene.NonNull(graphene.List(graphene.String))

class PredictionResponse(graphene.ObjectType):
    ok = graphene.Boolean(required=True)
    error = graphene.Field(Error, required=False)
    prediction = graphene.Field(Prediction, required=False)


class AIHumanInput(graphene.InputObjectType):
    text = graphene.String(required=False)
    file = Upload(required=False)


# curl http://localhost:3001/graphql -F operations='{"query": "mutation PredictAI($input: AIHumanInput!) { predictAI(input_: $input) { ok } }", "variables": { "input": {"file": null, text: "hello"} } }'  -F map='{ "0": ["variables.input.file"] }'  -F 0=@ai.txt
# curl http://localhost:3001/graphql -F 'operations={"query": "mutation PredictAI($input: AIHumanInput!) { predictAI(input_: $input) { ok } }", "variables": { "input": { "file": null, "text": "Sample text" } } }' -F 'map={ "0": ["variables.input.file"] }' -F '0=@ai.txt'
