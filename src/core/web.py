# BSD 3-Clause License
# Copyright (c) 2024, Potatooff
# WIP - Not Implemented Yet

import io
import logging
import requests
import trafilatura
from PyPDF2 import PdfReader
from functools import lru_cache
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from src.core.settings import summarize_web_content, summarize_model


if summarize_web_content:
    from torch import cuda
    from typing import Any 
    from transformers import pipeline

    _summarizer_model: Any = pipeline(
        task="summarization",
        model=summarize_model,
        device=0 if cuda.is_available() else -1,
    )


    def summarize_scraped_content(content: str) -> str: 
        result = _summarizer_model(content)
        return result[0]["summary_text"]


# Configure logging
MAX_RETRIES, BACKOFF_FACTOR = 3, 0.1
RETRY_STATUS_CODES = [500, 502, 503, 504]
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')


@lru_cache(maxsize=1024)
def GetPDFbyUrl(url):
    # Fetch a PDF file from the given URL and return a PdfReader object.
    #Using requests for HTTP requests and caching the result.

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  
        memory_file = io.BytesIO(response.content)

        return PdfReader(memory_file)

    except Exception as e:
        logging.error(f"Failed to fetch PDF from {url}: {e}")

    
def create_session():
    #  Create a requests session with retry logic.

    session = requests.Session()
    retries = Retry(total=MAX_RETRIES, backoff_factor=BACKOFF_FACTOR, status_forcelist=RETRY_STATUS_CODES)
    session.mount('https://', HTTPAdapter(max_retries=retries))

    return session


def scrape_site(url):
    # Scrape the content from the given URL .

    session = create_session()
    
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        proxy = None  # TODO feature for this?
        
        response = session.get(url, headers=headers, proxies=proxy, timeout=3)
        response.raise_for_status()

        if url.endswith(".pdf") or 'application/pdf' in response.headers.get('Content-Type', ''):
            pdf_reader = GetPDFbyUrl(url)
    
            if pdf_reader is not None:
                text = "".join(page.extract_text() or '' for page in pdf_reader.pages)

        else:
            text = trafilatura.extract(response.content, include_links=True, include_comments=False, include_tables=False)

            if text is None:
                raise ValueError("Failed to extract text")
            
            text = " ".join(text.strip().replace("\n", " ").split())

        logging.info(f"Scraped content from `{url}`\n----\n {text[:70]}...\n---\n")

        # Summarize content (if enabled)
        if summarize_web_content:
            return f"Summarized web page content:\n{summarize_scraped_content(text)}"

        return text
    
    except (requests.RequestException, ValueError) as e:
        logging.error(f"Failed to scrape {url}: {e}")
        return "Error: There was a problem with the request.", 0
    
    except Exception as e:
        logging.error(f"Unexpected error while scraping {url}: {e}")
        return "Error: An unexpected error occurred.", 0
    