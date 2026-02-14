import sys
import os
from .base import BaseAgent
try:
    from ddgs import DDGS
except ImportError:
    DDGS = None
import trafilatura

class ResearcherAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="The Researcher", role="Analysis")

    def search_web(self, query, max_results=5):
        if not DDGS:
            return "[ERROR] ddgs (DuckDuckGo) not installed."

        self.log(f"Deep Searching (DDG) for: {query}...")
        context = "WEB SEARCH REPORT:\n"

        try:
            # 1. Get Results from DuckDuckGo
            results = DDGS().text(query, max_results=max_results)
            if not results:
                return "No results found."

            # 2. Process each result
            for r in results:
                url = r.get('href')
                title = r.get('title')
                snippet = r.get('body')

                self.log(f"Found: {title} ({url})")

                # 3. Deep Dive with Trafilatura
                content = ""
                try:
                    downloaded = trafilatura.fetch_url(url)
                    if downloaded:
                        text = trafilatura.extract(downloaded, include_comments=False, include_tables=True)
                        if text:
                            content = text[:4000] # Increased limit for better context
                        else:
                            content = "(Content extraction failed, using snippet) " + snippet
                    else:
                        content = "(Download failed, using snippet) " + snippet
                except Exception as e:
                    content = f"(Error reading: {e}) " + snippet

                context += f"\n### SOURCE: {title}\nURL: {url}\nCONTENT:\n{content}\n"

            return context

        except Exception as e:
            return f"[SEARCH ERROR] {str(e)}"

    def process(self, task):
        self.log(f"Analyzing task: {task}")

        # 1. Perform Deep Web Search
        search_context = self.search_web(task)

        # 2. Synthesize with Brain (Gemini)
        system_prompt = (
            "You are The Researcher, an advanced AI analyst with Deep Web Search capabilities. "
            "Your goal is to provide a comprehensive, factual analysis based on the provided real-world data. "
            "\n\nINSTRUCTIONS:"
            "\n- Analyze the 'WEB SEARCH REPORT' provided below."
            "\n- Answer the user's task strictly based on the search results."
            "\n- Synthesize the information into a clear report with headings."
            "\n- Cite the URLs used."
            "\n- If the search results are insufficient, state clearly what is missing."
        )

        full_prompt = f"USER TASK: {task}\n\n{search_context}"

        return self.ask_brain(full_prompt, system_prompt)
