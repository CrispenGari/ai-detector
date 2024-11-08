import graphene
from graphene import ObjectType, Schema
from api.types import MetaResponse, AIHumanInput, PredictionResponse,  Error, Prediction
from api.models import predict_ai
from  api.models.pytorch import device, bilstm

class Query(ObjectType):
    meta = graphene.Field(
        MetaResponse
    )

    def resolve_meta(root, info):
        return MetaResponse(
            programmer="crispengari", language="python", libraries=["pytorch", "torchtext"],
            description="This is a graphql API predicting AI generated text from large paragraphs.",
            main="AI or Human"
        )
    

class PredictAI(graphene.Mutation):
    class Arguments:
        input_ = AIHumanInput(required=True)

    ok = graphene.Boolean()
    prediction = graphene.Field(lambda: PredictionResponse)
    def mutate(root, info, input_=None):
        try:
            if len(input_.text.strip().split()) < 5:
                return PredictAI(
                    ok = False,
                    prediction = PredictionResponse(
                        error = Error(
                            field = "input",
                            message = "The input text must be at least 5 words long."
                        ),
                        prediction = None
                    ),
                )
            preds = predict_ai(bilstm, input_.text, device)
            return PredictAI(
                    ok = True,
                    prediction = PredictionResponse(
                        error =  None,
                        prediction = Prediction(
                           **preds
                        )
                    ),
                )
        except Exception as e:
            return PredictAI(
                    ok = False,
                    prediction = PredictionResponse(
                        error = Error(
                            field = "server",
                            message =  str(e)
                        ),
                        prediction = None
                    ),
                )

    
class Mutation(ObjectType):
    predictAI = PredictAI.Field(
        name="predictAI",
        description="Predicting AI generated text mutation."
    )
       
schema = Schema(query=Query, mutation=Mutation)