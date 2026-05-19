import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app)

# Inicializa o cliente da Groq puxando a chave do Render
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    mensagem_usuario = data.get('message')

    if not mensagem_usuario:
        return jsonify({'reply': 'Mensagem vazia!'}), 400

    try:
        # Chamada para a API da Groq rodando o Llama 3
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Você é o Parça Universitário, um assistente virtual focado em ajudar estudantes universitários. Responda de forma amigável e direta em português brasileiro."
                },
                {
                    "role": "user",
                    "content": mensagem_usuario,
                }
            ],
            model="llama3-8b-8192", 
            temperature=0.7,
            max_tokens=1024,
        )
        
        # Extrai a resposta
        resposta = chat_completion.choices[0].message.content
        return jsonify({'reply': resposta})

    except Exception as e:
        print(f"Erro na Groq: {e}")
        return jsonify({'reply': 'Putz, meu cérebro deu tela azul. Tenta de novo?'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
