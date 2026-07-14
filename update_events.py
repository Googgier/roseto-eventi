#!/usr/bin/env python3
"""
Aggiorna la pagina eventi di Roseto e dintorni.
Cerca nuovi eventi online e rigenera index.html con i dati aggiornati.
"""
import json, os, subprocess, sys, re
from datetime import datetime, date

REPO_DIR = os.path.expanduser("~/ai-projects/roseto-eventi")

def cerca_eventi():
    """Cerca eventi online – da lanciare via Hermes cron con strumenti web."""
    return None  # Hermes l'agent chiama web_search, non questo script standalone

def eventi_default():
    """Eventi base di luglio 2026 – lo script di aggiornamento Hermes li sovrascrive."""
    return [
        {"data":"15 Lug 2026","titolo":"Concerto di apertura – I Musici Lotariani","luogo":"Villa Comunale, Roseto","desc":"Apre la 30ª edizione Roseto Opera Prima.","citta":"Roseto"},
        {"data":"15–18 Lug 2026","titolo":"Roseto Opera Prima – 30ª edizione","luogo":"Villa Comunale, Roseto","desc":"Rassegna culturale. Ore 21-23.","citta":"Roseto"},
        {"data":"19 Lug 2026","titolo":"The Avengers – Spettacolo","luogo":"Piazza Repubblica, Roseto","desc":"Supereroi dal vivo. Ore 21.","citta":"Roseto"},
        {"data":"14 Lug 2026","titolo":"Buozzi Summer Sound","luogo":"Piazza Buozzi, Giulianova","desc":"Lucy Soul Band. Ore 21.","citta":"Giulianova"},
        {"data":"17 Lug 2026","titolo":"Magia tra le Dune","luogo":"Le Dune, Silvi Marina","desc":"Musica 80'/90'. Ore 21:30.","citta":"Silvi"},
        {"data":"21 Lug 2026","titolo":"Matteo Mancuso","luogo":"Portorose, Roseto","desc":"Abbazie Summer Festival.","citta":"Roseto"},
        {"data":"22 Lug 2026","titolo":"Billy Cobham – Time Machine","luogo":"Portorose, Roseto","desc":"Abbazie Summer Festival.","citta":"Roseto"},
        {"data":"22–26 Lug 2026","titolo":"Sagra De lu Stennmass","luogo":"Cologna Paese, Roseto","desc":"17ª edizione. Enogastronomia.","citta":"Roseto"},
    ]

def leggi_eventi_html(path):
    """Estrae la lista eventi dall'HTML esistente."""
    with open(path) as f:
        html = f.read()
    # Cerca il blocco JS con const eventi = [...]
    m = re.search(r'const eventi\s*=\s*(\[[\s\S]*?\]);', html)
    if m:
        try:
            return json.loads(m.group(1))
        except:
            return None
    return None

def scrivi_html(path, eventi_list):
    """Riscrive index.html con eventi aggiornati."""
    with open(path) as f:
        html = f.read()
    
    # Sostituisci l'array eventi
    eventi_json = json.dumps(eventi_list, indent=2, ensure_ascii=False)
    nuovo = re.sub(
        r'const eventi\s*=\s*(\[[\s\S]*?\]);',
        f'const eventi = {eventi_json};',
        html
    )
    
    # Aggiorna la data
    oggi = datetime.now().strftime("%d/%m/%Y")
    nuovo = re.sub(
        r'aggiornato il <span id="aggiornato"></span>',
        f'aggiornato il <span id="aggiornato">{oggi}</span>',
        nuovo
    )
    
    with open(path, 'w') as f:
        f.write(nuovo)
    return True

if __name__ == "__main__":
    path = os.path.join(REPO_DIR, "index.html")
    print(f"📅 Eventi Roseto – aggiornamento {datetime.now().isoformat()}")
    
    # Per uso standalone di test: stampa gli eventi correnti
    ev = leggi_eventi_html(path)
    if ev:
        print(f"Eventi trovati nell'HTML: {len(ev)}")
    else:
        print("Nessun evento letto dall'HTML")
