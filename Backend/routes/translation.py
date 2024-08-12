from flask import Blueprint, request, jsonify, current_app
from llama_index.agent.openai import OpenAIAgent
from llama_index.llms.openai import OpenAI

translation_route = Blueprint("translate", __name__)

@translation_route.route('/create', methods=["POST"])
def translate():
    req = request.get_json()
    text = str(req['text'])
    llm = OpenAI(model="gpt-3.5-turbo", temperature=0)
    agent = OpenAIAgent.from_tools(llm=llm, verbose=True)
    response = agent.chat(f"Please translate following text to Chinese - {text}")
    current_app.logger.info(response)
    return jsonify({'data': response}), 201
