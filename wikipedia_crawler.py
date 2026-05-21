import requests
from bs4 import BeautifulSoup
import random
import networkx as nx
from pyvis.network import Network
import urllib.parse
import webbrowser
import os

def get_valid_wiki_links(soup):
    """Sucht nach echten Wikipedia-Artikeln im HTML."""
    links = soup.find_all("a", href=True)
    valid_links =[]
    seen = set()

    for a in links:
        # Falls ein Link auf ein Kapitel verweist (z.B. /wiki/Computer#Geschichte), 
        # schneiden wir das #Geschichte ab, da wir nur den Hauptartikel brauchen.
        href = a['href'].split("#")[0]
        
        # Nur Links zu anderen Artikeln, keine Bilder, Kategorien oder Hauptseiten
        if href.startswith("/wiki/") and ":" not in href and "Hauptseite" not in href and "Main_Page" not in href:
            if href not in seen:
                valid_links.append(href)
                seen.add(href)
                
    return valid_links

def main():
    print("🕸️ Willkommen beim Wikipedia Graph Crawler! v2 🕸️\n")
    
    start_url = input("Gib eine Wikipedia-URL ein (z.B. https://en.wikipedia.org/wiki/Computer): ").strip()
    try:
        max_hops = int(input("Wie viele Links soll die Kette lang sein? (z.B. 20): ").strip())
    except ValueError:
        print("Ungültige Eingabe. Setze Standardwert: 20")
        max_hops = 20

    # Basis-URL und Start-Titel extrahieren
    parsed_url = urllib.parse.urlparse(start_url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    current_title = urllib.parse.unquote(parsed_url.path.split("/")[-1]).replace('_', ' ')

    # Graph initialisieren
    G = nx.DiGraph()

    print("\n🚀 Starte den Crawl-Vorgang über die Wikipedia-API...")

    for i in range(max_hops):
        print(f"[{i+1}/{max_hops}] Besuche: {current_title}")
        
        # Statt der Webseite rufen wir die offizielle API auf
        api_url = f"{base_url}/w/api.php"
        params = {
            "action": "parse",
            "page": current_title,
            "prop": "text",
            "format": "json",
            "redirects": 1  # Falls ein Link eine Weiterleitung ist, folge ihr
        }
        
        headers = {
            'User-Agent': 'WikiGraphCrawler/2.0 (Ein Python-Lernprojekt)'
        }
        
        try:
            # API-Anfrage stellen
            response = requests.get(api_url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            if "error" in data:
                print(f"API-Fehler: {data['error'].get('info', 'Unbekannter Fehler')}")
                break
                
            # Den reinen Artikel-HTML-Text aus der API-Antwort extrahieren
            html_content = data["parse"]["text"]["*"]
            
        except requests.exceptions.RequestException as e:
            print(f"Netzwerk-Fehler: {e}")
            break
        except KeyError:
            print("Konnte den Artikeltext nicht finden. Möglicherweise existiert die Seite nicht.")
            break

        soup = BeautifulSoup(html_content, 'html.parser')
        valid_links = get_valid_wiki_links(soup)

        if not valid_links:
            print("Keine weiteren gültigen Links auf dieser Seite gefunden. Breche ab.")
            break

        # Nimm die ersten 10 Links (oder weniger)
        top_links = valid_links[:10]
        
        # Wähle einen zufälligen Link aus diesen Top 10
        next_link = random.choice(top_links)
        next_title = urllib.parse.unquote(next_link.split("/")[-1]).replace('_', ' ')

        # Zum Graphen hinzufügen
        G.add_node(current_title, label=current_title, title=current_title, color="#4caf50")
        G.add_node(next_title, label=next_title, title=next_title, color="#2196f3")
        G.add_edge(current_title, next_title, color="#ffffff")

        # Für den nächsten Durchlauf aktualisieren (wir brauchen ab jetzt nur noch den Titel!)
        current_title = next_title

    # 3. Den Graphen zeichnen (Obsidian Style)
    print("\n🎨 Erstelle interaktiven Graphen...")
    
    net = Network(height="100vh", width="100%", bgcolor="#1e1e1e", font_color="white", directed=True)
    net.from_nx(G)
    net.repulsion(node_distance=150, central_gravity=0.1, spring_length=100, spring_strength=0.05)
    
    output_file = "wiki_graph.html"
    net.save_graph(output_file)
    
    print(f"✅ Fertig! Der Graph wurde als '{output_file}' gespeichert.")
    webbrowser.open("file://" + os.path.realpath(output_file))

if __name__ == "__main__":
    main()