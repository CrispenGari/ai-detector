### ai-detector

🤖 Detecting AI generated text in real time using Deep-Leaning. This repository contain a GraphQL Server served to a Next.js application to detect AI generated text.

<p align="center"><img src="/images/logo.png" alt="ai-detector" width="200"/></p>

You can access the hosted web app at: https://ai-detector-sage.vercel.app/ which serves a graphql API which is served at [GraphQL API](https://ai-detector-2g6m.onrender.com/graphql). Here is the preview of the app.

<p align="center"><img src="/images/preview.jpg" alt="ai-detector" width="100%"/></p>

This app allows you to distinguish AI from Human Generated text from paragraphs of `300` words. You can detect text from:

1. Text files
2. Typed Text in the Text Area

### Architecture

The architecture of this system is as follows:

<p align="center"><img src="/images/achitecture.png" alt="ai-detector" width="80%"/></p>

### AI Model Architecture

The model was build using pytorch and it is simple as it contains `3` layers and bellow is the model architecture of the `Bi-LSTM` model.

<p align="center"><img src="/images/model-achitecture.png" alt="ai-detector" width="80%"/></p>

The model results can be found in [this notebook](https://github.com/CrispenGari/nlp-pytorch/blob/main/13_AI_DETECTION_FROM_TEXT/00_HUMAN_OR_AI.ipynb).

### LICENSE

This project is using the [MIT LICENSE](/LICENSE).
