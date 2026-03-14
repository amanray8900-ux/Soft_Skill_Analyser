import spacy
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

class TextAnalyzer:
    def __init__(self):
        # We assume `python -m spacy download en_core_web_sm` is run.
        self.nlp = spacy.load("en_core_web_sm")
        
    def analyze(self, text):
        doc = self.nlp(text)
        
        words = [token.text.lower() for token in doc if not token.is_punct and not token.is_space]
        total_words = len(words)
        unique_words = len(set(words))
        
        filler_count = sum([1 for word in words if word in {"um", "uh", "like"}])
        text_lower = text.lower()
        filler_count += text_lower.count("you know")
        
        vocab_richness = (unique_words / total_words) if total_words > 0 else 0
        
        return {
            "total_words": total_words,
            "unique_words": unique_words,
            "filler_count": filler_count,
            "vocab_richness": vocab_richness
        }

    def semantic_analysis(self, text):
        """Uses LLM API call for deep semantic structure and style analysis."""
        # List of free and fast Cerebras LLM models to try sequentially (fallback mechanism)
        providers = [
            {
                "name": "Cerebras Llama-3.1-8B",
                "api_key": os.getenv("CEREBUS_API_KEY") or os.getenv("CEREBRAS_API_KEY"),
                "base_url": "https://api.cerebras.ai/v1",
                "model": "llama3.1-8b"
            },
            {
                "name": "Cerebras Llama-3.3-70B",
                "api_key": os.getenv("CEREBUS_API_KEY") or os.getenv("CEREBRAS_API_KEY"),
                "base_url": "https://api.cerebras.ai/v1",
                "model": "llama-3.3-70b"
            }
        ]
            
        prompt_template = PromptTemplate(
            input_variables=["transcript"],
            template="Analyze the following transcript for communication structure, clarity, and professionalism. Provide 3 short, actionable bullet points of feedback.\n\nTranscript: {transcript}\n\nFeedback:"
        )
        
        last_error = None
        for provider in providers:
            # Skip if API key is not set or still default placeholder
            if not provider["api_key"] or "your_" in provider["api_key"].lower():
                continue
                
            try:
                llm = ChatOpenAI(
                    temperature=0.3, 
                    model=provider["model"], 
                    api_key=provider["api_key"],
                    base_url=provider["base_url"],
                    max_retries=1
                )
                chain = prompt_template | llm
                response = chain.invoke({"transcript": text})
                return response.content
            except Exception as e:
                last_error = e
                # Print to console for debugging but continue to the next provider
                print(f"[Warning] Failed calling {provider['name']} LLM: {e}")
                continue
        
        if last_error:
            return f"Error: All available LLM models failed. Last error: {last_error}"
            
        return "No API keys provided for Cerebras (CEREBUS_API_KEY). Skipping deep semantic analysis."
