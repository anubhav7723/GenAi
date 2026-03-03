#library for retreiving data from dotenv file
import os
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate #for prompts 
from langchain_core.output_parsers import StrOutputParser # for structured o/p
from langchain_groq import ChatGroq #llm


load_dotenv()
api_key=os.environ.get("GROQ_API_KEY")


#initialize basic llm using llama
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.7
)

parser = StrOutputParser()


def get_restaurant_name_and_items(cuisine):
    explain_prompt = ChatPromptTemplate.from_template(
    "I want to open a restaurant for {cuisine} food so suggest me a resturant name. Just give me name not any explanation."
    )

    summary_prompt = ChatPromptTemplate.from_template(
        "suggest me some menu items for {text}. Return it a comma seperated string And show retaurant name at top"
    )

    explanation_chain = explain_prompt | llm 

    summary_chain = summary_prompt | llm

    #this is modern sequential chain
    full_chain = explanation_chain | summary_chain

    result = full_chain.invoke({"cuisine": cuisine})
    
    return result.content

if __name__ == "__main__":
    print(get_restaurant_name_and_items("Italian"))