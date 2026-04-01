from search import search_prompt

def main():
    chain = search_prompt()

    if not chain:
        print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        return
    
    print("Chat iniciado. Digite 'sair' para encerrar.\n")

    while True:
        question = input("Pergunta: ")

        if question.lower() in ["sair", "exit", "quit"]:
            print("Encerrando chat.")
            break

        response = chain(question)

        print(f"Resposta: {response}")
        print()

if __name__ == "__main__":
    main()