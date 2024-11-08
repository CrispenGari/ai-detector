import nltk
import warnings
"""
📖 You only need to uncomment the following lines once.
"""
# import spacy
# spacy.cli.download("en_core_web_sm")

warnings.filterwarnings('ignore')

nltk.download('stopwords')
nltk.download('punkt')

from flask import Flask, redirect
from flask_cors import CORS
from graphene_file_upload.flask import FileUploadGraphQLView
from api.schema import schema



app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return redirect('/graphql', code=302)


app.add_url_rule('/graphql', view_func=FileUploadGraphQLView.as_view(
    'graphql',
    schema=schema,
    graphiql=True,
))
if __name__ == '__main__':
    app.run(port=3001, debug=False, host='0.0.0.0')