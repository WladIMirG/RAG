import pandas as pd
import json
import os
from openai import OpenAI
from tqdm import tqdm


_SYSTEM = {
    "role": "system",
    "content":  """
                Você é um anotador de dados.
                Dado um contexto o anotador deve fornecer três perguntas e três respostas para cada pergunta.
                As perguntas devem esclareçam possíveis dúvidas de um usuário sobre esse contexto.
                As respostas devem solucionar a pergunta usando o mesmo contexto.
                As respostas devem estar contida no contexto.
                As respostas devem ser sucintas.
                As respostas devem ser três para a mesma pergunta, onde:
                    a primeira deve ser simples y dar solução na pergunta sim muito argumento,
                    a segunda deve ter um argumento melhor e
                    a terceira resposta deve ser mais completa.

                exemplo:
                    contexto: Em muitas instituições, o TCC é encarado como critério final de avaliação do aluno: em caso de reprovação, o aluno estará impedido de obter o diploma e consequentemente exercer a respectiva profissão até que seja aprovado. O escopo e o formato do TCC (assim como sua própria nomenclatura) variam entre os diversos cursos e entre diferentes instituições, mas na estrutura curricular brasileira ela possui papel de destaque: em cursos ligados às ciências, normalmente é um trabalho que envolve pesquisa experimental, em cursos de caráter profissional, normalmente envolve: pesquisa bibliográfica e/ou empírica, a execução em si e uma apresentação de um projeto perante uma banca examinadora entre 3 e 5 professores (não necessariamente com Mestre ou Doutor). A banca examinadora formada para tal propósito não cria nenhuma expectativa de originalidade. Portanto, pode ser uma compilação (e não cópia) de outros ensaios com uma finalidade, um fio condutor, ou algo que forneça um roteiro, uma continuidade.
                    anotaição: 
                    ```
                        {
                            "perguntas": {
                                "p0": "O que acontece se o aluno reprovar no TCC?",
                                "p1": "Como o TCC é compreendida em instituições?",
                                "p2": "Quantos professores compõem a banca examinadora?"
                            }
                            "respostas": {
                                "p0": {
                                    "r0" : "o aluno estará impedido de obter o diploma",
                                    "r1" : "estará impedido de obter o diploma e consequentemente exercer a respectiva profissão",
                                    "r2" : "estará impedido de obter o diploma",
                                    }
                                "p1": {
                                    "r0" : "como critério final de avaliação do aluno",
                                    "r1" : "como critério final de avaliação do aluno",
                                    "r2" : "como critério final de avaliação do aluno",
                                    }
                                    
                                "p2": {
                                    "r0" : "entre 3 e 5",
                                    "r1" : "entre 3 e 5 professores",
                                    "r2" : "entre 3 e 5 professores (não necessariamente com Mestre ou Doutor)",
                                    }
                            }
                        }
                    ```
                """
    }

def join(context: dict, content: dict, data: list):
    """ Join the context and the content in a list of dict """
    
    # for i in content["perguntas"]:
        # print(i)
        # print(list(content["respostas"][i].values()))
    d = {
        "title": context["title"],
        "context": context["context"],
        "pergunta": content,
        # "pergunta": content["perguntas"][i],
        # "resposta": content["respostas"][i]
    }
    data.append(d)
    df = pd.DataFrame(data)
    df.to_csv("data.csv", index=False)
    return data

def obtener_respuesta_gpt(user_input):
    # Llama a la API de GPT-3.5 Turbo para obtener una respuesta
    # Utiliza la biblioteca openai y tu clave de API
    
    client = OpenAI(
        api_key= os.getenv("OPENAI_API_KEY"),
    )
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=user_input,
    )
    return response.choices[0].message.content

def load_data_context():
    # Read the dataset
    df_context = pd.read_csv('contextos.csv')
    df_context.columns = ['title', 'context']
    return df_context

def dataframe_request(df: pd.DataFrame, request: list, m_max: int = 7):
    data = df.to_dict(orient="records")
    df_data = []
    
    for d in tqdm(data):
        if len(request) == m_max:
            request.pop(1)
            request.pop(2)
        
        request.append({
            "role": "user",
            "content": f"Contexto: {d['context']}\nanotaição:"
        })
        
        response = obtener_respuesta_gpt(request)
        chatbot_message = {"role": "assistant", "content": response}
        request.append(chatbot_message)
        df_data = join(
            context=d,
            content=response,
            data=df_data)
    return pd.DataFrame(df_data)

def main():
    # load data context
    data_context = load_data_context()
    
    
    m_max = 5
    request = [_SYSTEM]
    df_c = data_context.copy()
    df = dataframe_request(df_c, request, m_max)
    df.to_csv("data.csv", index=False)

if __name__ == "__main__":
    main()