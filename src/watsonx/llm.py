from crewai import LLM
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from watsonx.watson_ai_client import WatsonXClient
from dotenv import load_dotenv
import os

load_dotenv(override=True)
API_KEY = os.environ["WAI_API_KEY"]
URL = os.environ["WAI_URL"]
os.environ["WX_URL"] = URL
PROJECT_ID = os.environ["WAI_PROJECT_ID"]
os.environ["WX_TOKEN"] = WatsonXClient.get_access_token(API_KEY)

def standard_llm():
    parameters = {
        GenParams.TOP_K: 1,
        GenParams.TOP_P: 0,
        GenParams.RANDOM_SEED: 42,
        GenParams.REPETITION_PENALTY: 1.05,
        GenParams.MAX_NEW_TOKENS: 600,
    }

    return LLM(
            model="watsonx/meta-llama/llama-3-70b-instruct",
            base_url=URL,
            project_id=PROJECT_ID,
            params=parameters,
        )