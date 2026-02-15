
from .base import BaseAgent
from duckduckgo_search import DDGS
import trafilatura
import json

class ResearcherAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="The Researcher", role="Deep Investigation")

    def search_web(self, query, max_results=5):
        self.log(f"Searching web for: {query}")
        results = []
        try:
            with DDGS() as ddgs:
                search_gen = ddgs.text(query, max_results=max_results)
                for r in search_gen:
                    results.append(r)
        except Exception as e:
            self.log(f"Search error: {e}")
        return results

    def scrape_content(self, url):
        try:
            downloaded = trafilatura.fetch_url(url)
            if downloaded:
                return trafilatura.extract(downloaded)
        except Exception:
            return None
        return None

    def process(self, task):
        self.log(f"Researching: {task}")

        # 1. Search Web
        search_results = self.search_web(task, max_results=5)

        web_context = ""
        if search_results:
            self.log(f"Found {len(search_results)} search results. Scraping top 3...")
            for i, res in enumerate(search_results[:3]):
                url = res.get('href')
                content = self.scrape_content(url)
                if content:
                    # Safe string concatenation
                    web_context += "\n--- SOURCE: " + str(url) + " ---\n" + str(content[:2000]) + "\n"

        # 2. Consult Memory
        memory_context = self.consult_memory(task, limit=5)

        # 3. Synthesize
        system_prompt = (
            "You are The Researcher, a deep-dive investigator for WiseClaw. "
            "Your goal is to find comprehensive, accurate information. "
            "Analyze the provided [WEB CONTEXT] and [MEMORY CONTEXT]. "
            "Produce a detailed report on the capabilities, APIs, and advanced features of the requested topics. "
            "Focus on technical possibilities, bot integrations, and automation potential." 
            "Structure the report with clear headings for Discord and Telegram."
        )

        full_prompt = (
            f"{system_prompt}\n\n"
            f"[WEB CONTEXT]\n{web_context}\n[END WEB CONTEXT]\n\n"
            f"[MEMORY CONTEXT]\n{memory_context}\n[END MEMORY CONTEXT]\n\n"
            f"Task: {task}"
        )

        return self.ask_brain(task, full_prompt)
