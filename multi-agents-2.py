
from autogen import AssistantAgent, GroupChatManager, UserProxyAgent
from autogen.agentchat import GroupChat

# Configuration for connecting to a model server
config_list = [
    {
        "model": "ollama/mistral",
        "base_url": "http://localhost:"+API_PORT,  # litellm compatible endpoint
        "api_key": "NULL",  # placeholder
    }
]


llm_config = {"config_list": config_list}

# Setup Agents
researcher = AssistantAgent(
    name="Researcher",
    llm_config=llm_config,
    system_message="""Researcher. Extract and rank keywords based on their relevance and meaning from given texts. Specialized in ontology analysis and biology.""",
)

pubmed_master = AssistantAgent(
    name="PubMed Master",
    llm_config=llm_config,
    system_message="""PubMed Master. Your role is to generate and optimize PubMed queries by intelligently using logical operators like AND and OR. You are specialized in crafting effective search queries for biomedical literature. Your task involves creating queries in a structured 'AND/OR' format, where you will pair each extracted keyword with every other keyword in a combinatory fashion. For each pair of keywords, formulate a query using the format: (Keyword1 AND Keyword2) OR Keyword3. This approach ensures a comprehensive exploration of the research topic by covering various keyword combinations. Your goal is to generate a list of queries that effectively capture the diverse aspects of the research topic, facilitating the retrieval of the most relevant and informative articles from PubMed.""",
)

admin = UserProxyAgent(
    name="Admin",
    system_message="A human admin. Reviews and approves the plan and query created by the agents.",
    llm_config=llm_config,
    code_execution_config=False,
)

# Group Chat Setup
groupchat = GroupChat(
    agents=[admin, researcher, pubmed_master],
    messages=[],
    max_round=10,
)

manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

# # Abstract to be analyzed
abstract = "Most Staphylococcus aureus strains can grow as a multicellular biofilm, a phenotype of utmost importance to clinical infections such as endocarditis, osteomyelitis, and implanted medical device infection. As biofilms are inherently more tolerant to the host immune system and antibiotics, understanding the S. aureus genes and regulatory circuits that contribute to biofilm development is an active and ongoing field of research. This chapter details a high-throughput and standardized way to grow S. aureus biofilms using a classical microtiter plate assay. Biofilms can be quantified using crystal violet or by confocal microscopy imaging and COMSTAT analysis."

# Initiating the Chat with the Abstract
admin.initiate_chat(
    manager,
    message=f"Extract keywords from the following abstract and create a set of PubMed queries using the 'AND/OR' format: {abstract}",
)

