import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
# Ativa o CORS para permitir que o Google Sites acesse a API sem bloqueios
CORS(app)

# Inicializa o cliente da Groq buscando a chave de API das variáveis de ambiente do Render
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    mensagem_usuario = data.get('message')

    if not mensagem_usuario:
        return jsonify({'reply': 'Mensagem vazia!'}), 400

    try:
        # Chamada oficial para a API da Groq usando o modelo Llama 3.1 ativo
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Você é o Parça Universitário, um assistente virtual focado em ajudar estudantes universitários. Responda de forma amigável, prestativa e direta em português brasileiro."
                },
                {
                    "role": "user",
                    "content": mensagem_usuario,
                }
            ],
            model="llama-3.1-8b-instant",  # Versão estável e operacional
            temperature=0.7,
            max_tokens=1024,
        )
        
        # Extrai o texto da resposta gerada pela IA
        resposta = chat_completion.choices[0].message.content
        return jsonify({'reply': resposta})

    except Exception as e:
        # Registra o erro detalhado nos logs do Render para diagnóstico
        print(f"Erro na integração com a Groq: {e}")
        return jsonify({'reply': 'Putz, meu cérebro deu tela azul. Pode tentar de novo?'}), 500

if __name__ == '__main__':
    # O Render configura a porta automaticamente, mas o padrão de escuta 0.0.0.0 garante a conectividade externa
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
