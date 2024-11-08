class TestMeta:
    def test_meta(self):
        from graphene.test import Client
        from api.schema import Query
        import graphene

        gschema = graphene.Schema(query=Query)
        client = Client(gschema)
        executed = client.execute("""
          {
  meta{
    programmer
    main
    description
    language
    libraries
  }
}
        """)
        assert executed == {
            "data": {
                "meta": {
                    "programmer": "crispengari",
                    "main": "AI or Human",
                    "description": "This is a graphql API predicting AI generated text from large paragraphs.",
                    "language": "python",
                    "libraries": ["pytorch", "torchtext"],
                }
            }
        }
