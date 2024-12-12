import streamlit as st
from langchain_groq import ChatGroq 
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.tools.tavily_search import TavilySearchResults


# Model and Agent tools
llm =  ChatGroq(api_key=st.secrets.get("GROQ_API_KEY"))
search = TavilySearchResults(max_results=2)
parser = StrOutputParser()
# tools = [search] # add tools to the list

# Page Header
st.title("Sales Assistant Agent")
st.markdown("Assistant Agent Powered by Groq.")


# Data collection/inputs
with st.form("company_info", clear_on_submit=True):

  product_name = st.text_input("Product Name (What product are you selling?)")
  company_url = st.text_input("Company URL")
  product_category=st.text_input("Product Category")
  competitors = st.text_area("Competitors (one URL per line)")
  value_proposition = st.text_area("Value Proposition")
  target_customer = st.text_input("Target Customer")

  

  # For the llm insights result
  company_insights = ""

  # Data process
  if st.form_submit_button("Generate Insights"):
    if product_name and company_url:
      st.spinner("Processing...")

       # search internet
      company_data = search.invoke(company_url)
      print(company_data)

      #prompt = '''You are a Sales and marketting assistant. Analyse 
      #Product name:{product_name}
      #Company details:{company_url}
      #Competitors detail:{competitors}
      #For each competitors provide advantage and disadvantage of the product
      #Include ratings, price. Give the result summary'''
      
      
      prompt = f"""
      Analyze the following company information using the information
      Product name:{product_name}
      Company details: {company_url}
      Competitors:{competitors}
      Product Category:{product_category} and Generate an in-depth sales report with these sections:
        1. Executive Summary: Concisely outline the key opportunity and top 3 selling points.
        2. Company Overview:
              Key initiatives and strategic direction
        3. Competitive Landscape:
           a. company's main competitors
           b. In-depth SWOT analysis of {product_name} vs. competitors
           c. Unique selling propositions and differentiators
        4. Product-Solution Mapping:
           a. company's critical challenges addressed by {product_name}
           b. Feature-by-feature breakdown of how {product_name} solves specific problems
        5. Risk Assessment and Mitigation:
            Potential implementation challenges
        6. Elevator pitch tailored to company's specific situation
        7. Customer success and account growth plan
         
        Your analysis must be meticulously researched, forward-thinking, and provide immediately actionable insights for 
        a highstakes, enterprise-level sale. 
     
      Provide a report in the following format:
      1. Company Strategy:
      2. Competitor Mentions:
      3. Leadership Information:
      4. Product/Strategy Summary:
      5. References:

      

      """

      # Prompt Template
      prompt_template = ChatPromptTemplate([("system", prompt)])

      # Chain
      chain = prompt_template | llm | parser

      # Result/Insights
      company_insights = chain.invoke({"product_name": product_name, "company_url": company_url, "competitors": competitors,
      "Product Category": product_category,"Value Proposition": value_proposition})
                                

st.markdown(company_insights)