**Groq Chat Bot with Multiple Language Models**
=====================================================

Welcome to the Groq Chat Bot with Multiple Language Models, a demo application that showcases the capabilities of various AI models using the Groq API. This application allows users to interact with different language models, including LLaMA3, Gemma, and Mixtral, and explore their responses to user input.

**What is Groq?**
----------------

Groq is a cloud-based API that provides access to a wide range of AI models, including language models, computer vision models, and more. Groq allows developers to easily integrate these models into their applications, enabling features such as chatbots, language translation, and image recognition.

**How to Use the Application**

--------------------------------

### Installation

To run the application locally, follow these steps:

Clone the repository: `git clone https://github.com/SauravSrivastav/Groq-Chat-Bot-with-Multiple-Language-Models.git`


**Setting up the Environment**
-----------------------------

1. Create a new virtual environment using `python -m venv myenv`.
2. Activate the virtual environment using `source myenv/bin/activate` (on Linux/Mac) or `myenv\Scripts\activate` (on Windows).
3. Install the required dependencies using `pip install -r requirements.txt`.

**Setting up the GROQ_API_KEY**
-----------------------------

1. Create a new file called `.env` in the root directory of your project.
2. Add the following line to the `.env` file: `GROQ_API_KEY=YOUR_API_KEY_HERE`.
3. Replace `YOUR_API_KEY_HERE` with your actual Groq API key.

**Running the App**
------------------

1. Run the app using `streamlit run app.py`.
2. Open a web browser and navigate to `http://localhost:8501`.
3. Interact with the chatbot by typing in your prompt and pressing enter.

### Usage

1. Select a model from the sidebar: Choose a model from the list of available models, including LLaMA3, Gemma, and Mixtral.
2. Adjust the maximum tokens: Use the slider to adjust the maximum number of tokens (words) for the model's response.
3. Enter your prompt: Type a message or prompt in the chat input field.
4. View the response: The chatbot will respond with a message based on the selected model and input prompt.

**Code Structure**
-------------------

The application consists of a single file, `app.py`, which contains the following components:

* **Model selection and configuration**: The sidebar allows users to select a model and adjust the maximum tokens for the response.
* **Chat input and response**: The chat input field allows users to enter a prompt, and the chatbot responds with a message based on the selected model and input prompt.
* **Groq API integration**: The application uses the Groq API to fetch responses from the selected model.

**References**
--------------

* [Groq API documentation](https://groq.com/docs)
* [Streamlit documentation](https://docs.streamlit.io/)
* [Python dotenv library](https://github.com/theskumar/python-dotenv)


**Author**
---------

[Saurav Srivastav](https://github.com/SauravSrivastav/)
