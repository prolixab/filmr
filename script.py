import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(api_key=api_key)


def create_script(prompt, topic, topia):
    print(f'Writing script about {topic} {topia}')
    final_prompt = ChatPromptTemplate.from_messages([
        ("system", '{prompt}'),
        ("user", '{topic}'),
        ("user", '{topia}')
    ])
    output_parser = StrOutputParser()
    chain = final_prompt | llm | output_parser
    response = chain.invoke({"prompt": prompt, "topic": topic, "topia": topia})
    return response


def save_script(script, path, topic, topia):
    filename = f'{topic}-{topia}.txt'
    file_path = os.path.join(path, filename)
    print(f'Saving script to {file_path}')
    with open(file_path, "w") as f:
        f.write(script)
