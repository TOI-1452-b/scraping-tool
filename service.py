from googleapiclient.discovery import build
import json
import os
from dotenv import load_dotenv
from firecrawl import FirecrawlApp
import requests

# Load environment variables
load_dotenv()

api_key = os.getenv('GOOGLE_API_KEY')
cse_id = os.getenv('GOOGLE_CSE_ID')
firecrawl_app = FirecrawlApp(api_key=os.getenv('FIRECRAWL_API_KEY'))

def write_to_file(results: list):
    with open('results.json', 'w') as f:
        json.dump(results, f)
                  
def google_search(query: str, api_key: str, cse_id: str, num_results: int):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=query, cx=cse_id, num=num_results).execute()
    results = []
    for item in res['items']:
       results.append({
           "title": item['title'],
           "link": item['link'],
           "snippet": item['snippet']
       })
    write_to_file(results)
    return results

def scrape_url():
    try:
        with open('results.json', 'r', encoding='utf-8') as f:
            daten = json.load(f)
            link_array = []
            for item in daten:
                link_array.append(item['link'])
            
            results = []
            for link in link_array:
                try:                
                    response = firecrawl_app.scrape_url(
                                link,
                                params={'formats': ['markdown', 'html']}
                            )
                    results.append({"url": link, "content": response, "status": "success"})
                    
                except Exception as e:
                    print(f"Fehler beim Scrapen von {link}: {e}")
                    results.append({"url": link, "content": None, "status": f"error: {str(e)}"})
            with open('firecrawl_data.json', 'w') as f:
                json.dump(results, f)
            return results
    except Exception as e:
        print(f"Fehler beim Scrapen der URLs: {e}")
        return (f"Fehler beim Scrapen der URLs: {e}")

def send_data_to_ai():
    try:
        llama_api_url = 'http://localhost:11434/api/generate'
        prompt = "DU bist ein Betriebswirtschaftlicher Wissenschaftler der den folgenden Content zusammenfasst!"
        
        with open('firecrawl_data.json', 'r', encoding='utf-8') as f:
            daten = json.load(f)
            
        all_responses = []  # Liste für alle Antworten
              
        for item in daten:
            if item["status"] == "success":
                # Erhalte URL und Content aus dem aktuellen Item
                url = item["url"]
                content = item['content'].get('markdown', item['content'].get('html', ''))
                
                # Sende Anfrage an LLM
                response = requests.post(
                    llama_api_url, 
                    json={
                        "prompt": prompt + content,
                        "model": "llama3.1",
                        "stream": False
                    }
                )
                
                # Extrahiere nur den "response"-Teil aus der LLM-Antwort
                llm_full_response = response.json()
                llm_text_response = llm_full_response.get("response", "")
                
                # Speichere das Ergebnis im gewünschten Format
                result = {
                    "url": url,
                    "llm-response": llm_text_response  # Nur der tatsächliche Textinhalt
                }
                
                all_responses.append(result)
                
                # Schreibe das aktuelle Ergebnis sofort in die Datei
                # Wenn die Datei existiert, lesen wir den vorhandenen Inhalt
                try:
                    with open('ai_analysis_results.json', 'r', encoding='utf-8') as f:
                        existing_data = json.load(f)
                except (FileNotFoundError, json.JSONDecodeError):
                    existing_data = []
                
                # Füge das neue Ergebnis hinzu
                existing_data.append(result)
                
                # Schreibe alle Daten zurück in die Datei
                with open('ai_analysis_results.json', 'w', encoding='utf-8') as f:
                    json.dump(existing_data, f, ensure_ascii=False, indent=2)
                
                print(f"Verarbeitet und gespeichert: {url}")
        
        return all_responses
            
    except Exception as e:
        print(f"Fehler bei der Verarbeitung durch das LLM: {e}")
        return None