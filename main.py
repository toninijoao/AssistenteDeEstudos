import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('API_KEY')

if not api_key:
    raise ValueError("Erro! API_KEY não encontrada!")

os.system('cls' if os.name == 'nt' else 'clear')

client = genai.Client(api_key=api_key)
chat = client.chats.create(model="gemini-2.5-flash")

while True:

    print("📚 Bem-Vindo ao seu NOVO Assistente de Estudos! 📚\n\n")

    tema = input("👋 Olá, meu amigo! Sobre qual tema você gostaria de tirar dúvidas hoje?\n💬 Seu tema: ")

    prompt = (
        f"O usuário quer uma explicação simples sobre o seguinte tema: {tema}."
        "Explique esse tema de forma resumida, fácil de entender e didática."
        "Explique em até 3 parágrafos."
        "Evite usar termos técnicos ou jargões complicados."
    )
        
    resposta = chat.send_message(prompt)
    explicacao = resposta.text.strip()

    print(f"\nClaro! Aqui está uma explicação simples sobre {tema}:\n\n{explicacao}")
    print("\n")

    perguntas = input("❓ Você gostaria que eu preparasse perguntas para ver se você entendeu o tema? (sim/não): ")

    if perguntas.lower() == 'sim':
        prompt_perguntas = (
            f"Encontre 5 questões de nível médio sobre o tema {tema} para testar o conhecimento do usuário.\n"
            "Escreva APENAS as 5 perguntas, uma por linha, numeradas assim:\n"
            "1. ...\n2. ...\n3. ...\n4. ...\n5. ...\n"
            "Não adicione explicações ou comentários extras."
        )
        resposta_perguntas = chat.send_message(prompt_perguntas)
        texto_perguntas = resposta_perguntas.text.strip()

        perguntas_geradas = [p for p in resposta_perguntas.text.split('\n') if p.strip()]

        nota = 0
        total = len(perguntas_geradas)

        print(f"\nAqui estão 5 perguntas para conferir se você entendeu {tema}:\n\n")

        for pergunta in perguntas_geradas:
            print(f"\n🧩 {pergunta}")
            resposta_usuario = input("💬 Sua Resposta:")

            prompt_correcao = (
                f"A pergunta é: {pergunta}\n"
                f"A resposta do usuário é: {resposta_usuario}\n"
                f"Com base no tema {tema}, diga se a resposta do usuário está correta ou incorreta, e explique brevemente o porquê."
            )

            correcao = chat.send_message(prompt_correcao)
            print(f"\n🤖 Correção: {correcao.text.strip()}\n")

            if "correta" in correcao.text.lower() and "incorreta" not in correcao.text.lower():
                nota = nota + 1

        print(f"📊 Resultado Final: ")
        if nota >= 4:
            print(f"Parabéns! Você acertou {nota} de {total} perguntas. Excelente desempenho! 🎉\n")
        elif nota == 3:
            print(f"Bom, você acertou {nota} de {total} perguntas. Continue praticando! 👍\n")

        else:
            print(f"Você acertou {nota} de {total} perguntas. Não desanime, continue estudando! 💪\n")    

    else:
        print("Ok! Se precisar de algo mais, é só avisar. 🤖\n")       

    repetir = input("Gostaria de tirar dúvidas sobre outro tema? (sim/não): ")
    if repetir.lower != 'sim':
        print("Obrigado por usar o Assistente de Estudos! Até a próxima! 👋\n\n")
        break