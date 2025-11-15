# FYP-Pages
Final Year Project GitHub Pages Repo

# Deepfake Detection Flow
![Deepfake Detection Flow](FYP-Diagram.drawio.png)

The above diagram shows the proposed flow for this project. The backend will only be for recieving a POST from a webhook and will send that to the LLM. This returns a confidence score and the backend application sends this to the WhatsApp bot via the WhatsApp API.

I propose to use something like FastAPI, a Python based backend framework.

Below is a useful Youtube video outlining how the backend may send a request to the LLM using FastAPI. Perhaps if the AI is trained to take in these prompts and output the confidence score, this video contains most of the info on how to complete the backends side of this process. I will then also need to configure the response being automatically sent to the WhatsApp API for the chatbot.
[This is an external link to youtube.com](https://www.youtube.com/watch?v=cy6EAp4iNN4)

The WhatsApp Cloud API documentation link below offers useful informationa and guides for how to setup both webhooks and a chatbot for free as long as it is in a testing capacity. This should work well for this project as the number of actual requests will be small, and it will allow me to build and show the proof of concept for the project without needing to incur costs.
[This is an external link to developers.facebook.com](https://developers.facebook.com/docs/whatsapp/cloud-api)


