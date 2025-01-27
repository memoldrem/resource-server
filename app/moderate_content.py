# Contains the LangChain workflows for content moderation, user support, and any other AI functionality.
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain

# Define AI model for content moderation
def create_moderation_chain():
    prompt = PromptTemplate(
        input_variables=["content"],
        template="Is this content appropriate for a public forum? Answer with 'Yes' or 'No'.\n{content}"
    )
    llm = OpenAI(temperature=0)
    return LLMChain(llm=llm, prompt=prompt)

def moderate_content(content):
    moderation_chain = create_moderation_chain()
    response = moderation_chain.run(content)
    return response
