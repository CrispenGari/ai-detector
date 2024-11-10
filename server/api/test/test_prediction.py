class TestPrediction:
    def test_human(self):
        from graphene.test import Client
        from api.schema import Mutation
        import graphene

        gschema = graphene.Schema(mutation=Mutation)
        client = Client(gschema)
        executed = client.execute("""
         mutation {
  predictAI(input_: {text: "Texting and driving can be avoided in many of the following ways. 1. By pulling over to the side of the road. 2. By keeping your phone out of sight and reach. 3. By turning off do not disturb. 4. By mounting your phone to something if you are using a navigation app. 5. By leaving your phone at home. The list could to on and on. Using your phone and driving is a bad and sometimes expensive habit. You should not do this."}) {
    ok
    prediction {
      error {
        field
        message
      }
      prediction {
        classId
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
  predictAI(input_: {text: "So, in conclusion, we need stricter gun control laws. Guns r dangerous, there's too much violence, guns r easy to get, they are not just for hunting, and stricter laws work. We have to do sum thin bout this. We can't just sit around and let peoples get killed. It's time for change."}) {
    ok
    prediction {
      error {
        field
        message
      }
      prediction {
        classId
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
