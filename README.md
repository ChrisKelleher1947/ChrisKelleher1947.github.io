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

[external linke to Artificial Intelligence to Combat Audio Fraud: A Flask-Deployed Hybrid Deep Learning System](https://ieeexplore.ieee.org/document/10778737)
Found that RNN or Recurrent Neural networks were the most accurate type of nerual network for synthetic speech detection. Used ASVSpoof2019, potential training dataset for this project.
They used the below diagram in experiment setup, usefule to keep: 
![Ai Training Flow](aiTrainingFlow.png)

[external link to IBM What is a recurrent neural network? by Cole Stryker](https://www.ibm.com/think/topics/recurrent-neural-networks)
ChatGPT is an example of RNN. This is an ai that takes past inputs and can then make predictions and conlcusions based on those inputs. Example would be for language translation. Taking speech patterns and predciting what the next word should be. Described as being good at taking previous sensor data and using that to compare new data to serach for anomalites. Good pattern recognition and ability to take data and make predictions based on what it has seen. Could be very useful for the purposes of this project, taking previous syntehtic voices and predicting if the current data matches the same pattern as waht it has seen before.


