class TestPrediction:
    def test_human(self):
        from graphene.test import Client
        from api.schema import Mutation
        import graphene

        gschema = graphene.Schema(mutation=Mutation)
        client = Client(gschema)
        executed = client.execute("""
         mutation {
  predictAI(input_: {text: "Helllo there i am a user"}) {
    ok
    prediction {
      error {
        field
        message
      }
      prediction {
        classId
        probability
        className
      }
    }
  }
}

        """)
        assert executed == {
            "data": {
                "predictAI": {
                    "ok": True,
                    "prediction": {
                        "error": None,
                        "prediction": {
                            "classId": 0,
                            "probability": 0.887,
                            "className": "human",
                        },
                    },
                }
            }
        }

    def test_ai(self):
        from graphene.test import Client
        from api.schema import Mutation
        import graphene

        gschema = graphene.Schema(mutation=Mutation)
        client = Client(gschema)
        executed = client.execute("""
   mutation {
  predictAI(input_: {text: "Fifth reason is that stricter gun control laws work. In countries where they have stricter laws, there are less shootings. Like, in Australia, they have strict laws and hardly no shootings. Its just common sense."}) {
    ok
    prediction {
      error {
        field
        message
      }
      prediction {
        classId
        probability
        className
      }
    }
  }
}

        """)
        assert executed == {
            "data": {
                "predictAI": {
                    "ok": True,
                    "prediction": {
                        "error": None,
                        "prediction": {
                            "classId": 1,
                            "probability": 1,
                            "className": "ai",
                        },
                    },
                }
            }
        }

    def test_error(self):
        from graphene.test import Client
        from api.schema import Mutation
        import graphene

        gschema = graphene.Schema(mutation=Mutation)
        client = Client(gschema)
        executed = client.execute("""
            mutation {
    predictAI(input_: {text: "Helllo there i"}) {
        ok
        prediction {
        error {
            field
            message
        }
        prediction {
            classId
            probability
            className
        }
        }
    }
    }

            """)
        assert executed == {
            "data": {
                "predictAI": {
                    "ok": False,
                    "prediction": {
                        "error": {
                            "field": "input",
                            "message": "The input text must be at least 5 words long.",
                        },
                        "prediction": None,
                    },
                }
            }
        }
