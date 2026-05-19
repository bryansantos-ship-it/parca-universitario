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
        # Chamada para a API da Groq usando o modelo Llama 3.3 Versatile (70 Bilhões de parâmetros)
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Você é o 'Parça Universitário', um assistente virtual focado em ajudar "
                        "estudantes universitários de Santarém e região. Você domina informações "
                        "sobre cursos locais, projetos de tecnologia, infraestrutura e Redes de "
                        "Computadores no IESPES, além de assuntos gerais da UFOPA. "
                        "Você fala em português brasileiro, usando um tom extremamente amigável, "
                        "prestativo e encorajador. Use gírias leves de estudante (como 'parça', "
                        "'beleza', 'bora', 'tranquilo'), mas sem perder o rigor técnico quando "
                        "explicar conceitos de tecnologia ou estudos. Suas respostas devem ser "
                        "diretas, curtas e formatadas de maneira fácil de ler no celular."
                    )
                },
                {
                    "role": "user",
                    "content": mensagem_usuario,
                }
            ],
            model="llama-3.3-70b-versatile",  # Versão mais potente e inteligente da Groq
            temperature=0.7,  # Nível de criatividade equilibrado
            max_tokens=1024,
        )
        
        # Extrai o texto da resposta gerada pela IA
        resposta = chat_completion.choices[0].message.content
        return jsonify({'reply': resposta})

    except Exception as e:
        # Registra o erro detalhado nos logs do Render para diagnóstico
        print(f"Erro na integração com a Groq: {e}")
        return jsonify({'reply': 'Putz, parça, meu cérebro deu tela azul aqui no servidor. Dá um toque de novo?'}), 500

if __name__ == '__main__':
    # O Render configura a porta automaticamente, mas o padrão de escuta 0.0.0.0 garante a conectividade
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
