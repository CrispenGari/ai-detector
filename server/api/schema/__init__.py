import graphene
from graphene import ObjectType, Schema
from api.types import MetaResponse, AIHumanInput, PredictionResponse, Error, Prediction
from api.models import predict_ai
from api.models.pytorch import device, bilstm
import re
import io

allowed_extensions = [".txt", ".TXT"]
class Query(ObjectType):
    meta = graphene.Field(MetaResponse)

    def resolve_meta(root, info):
        return MetaResponse(
            programmer="crispengari",
            language="python",
            libraries=["pytorch", "torchtext"],
            description="This is a graphql API predicting AI generated text from large paragraphs.",
            main="AI or Human",
        )


class PredictAI(graphene.Mutation):
    class Arguments:
        input_ = AIHumanInput(required=True)

    ok = graphene.Boolean()
    prediction = graphene.Field(lambda: PredictionResponse)

    def mutate(root, info, input_=None):
        try:
            if input_.text is None and input_.file is None:
                return PredictAI(
                    ok=False,
                    prediction=PredictionResponse(
                        error=Error(
                            field="input",
                            message="You should upload a file or type text.",
                        ),
                        prediction=None,
                    ),
                )
            if input_.file is not None:
                ext = "." + str(input_.file.filename).split(".")[-1]
                if ext not in allowed_extensions:
                    return PredictAI(
                        ok=False,
                        prediction=PredictionResponse(
                            error=Error(
                                field="input",
                                message=f'Only images with extensions ({", ".join(allowed_extensions)}) are allowed.',
                            ),
                            prediction=None,
                        ),
                    )
                file_stream = io.BytesIO(input_.file.read())
                text = file_stream.getvalue().decode("utf-8")
            else:
                text = input_.text

            if len(text.strip().split()) < 5:
                return PredictAI(
                    ok=False,
                    prediction=PredictionResponse(
                        error=Error(
                            field="input",
                            message="The input text must be at least 5 words long.",
                        ),
                        prediction=None,
                    ),
                )
            preds = predict_ai(bilstm, text, device)
            text = re.sub(r"[\r\n]", "", text)
            text = re.sub(r"\s+", text, " ", re.MULTILINE)
            return PredictAI(
                ok=True,
                prediction=PredictionResponse(
                    error=None, prediction=Prediction(**preds, text=text)
                ),
            )
        except Exception as e:
            return PredictAI(
                ok=False,
                prediction=PredictionResponse(
                    error=Error(field="server", message=str(e)), prediction=None
                ),
            )


class Mutation(ObjectType):
    predictAI = PredictAI.Field(
        name="predictAI", description="Predicting AI generated text mutation."
    )


schema = Schema(query=Query, mutation=Mutation)
