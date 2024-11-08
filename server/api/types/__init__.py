
import graphene

class Error(graphene.ObjectType):
    field = graphene.String(required=True)
    message = graphene.String(required=True)


class Prediction(graphene.ObjectType):
    class_id = graphene.Int(required=True)
    probability = graphene.Float(required=True)
    class_name = graphene.String(required=True)



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
    text = graphene.String(required=True)
