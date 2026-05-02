from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

INSTRUCAO_SISTEMA = """
Você é o 'Parça Universitário', um chatbot empático e informal focado em ajudar estudantes do ensino médio de Santarém (Pará) a escolherem cursos de ensino superior.
Suas respostas devem:
1. Usar linguagem jovem, gírias leves da região e ser muito acessível. Sem jargões acadêmicos.
2. Fornecer informações sobre cursos, localização de campi e mensalidades de Santarém.
3. Ser direto, amigável e dar feedbacks rápidos.
"""

model = genai.GenerativeModel('gemini-pro')

chat = model.start_chat(history=[
    {"role": "user", "parts": [INSTRUCAO_SISTEMA]},
    {"role": "model", "parts": ["Pode deixar, parça! Tô pronto pra ajudar a galera de Santarém. Manda a dúvida!"]}
])

@app.route('/api/chat', methods=['POST'])
def process_chat():
    data = request.get_json()
    user_message = data.get('message')

    if not user_message:
        return jsonify({"error": "Mensagem vazia"}), 400

    try:
        response = chat.send_message(user_message)
        return jsonify({"reply": response.text})

    except Exception as e:
        print(f"Erro na IA: {e}")
        return jsonify({"reply": "Foi mal, parça! Meu sistema deu uma travada. Manda de novo?"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
