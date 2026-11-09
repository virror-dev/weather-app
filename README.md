# Väderappen ☀️🌧️

Välkommen till **Väderappen**! Detta är en pedagogisk webbapplikation byggd i Python och Flask. Appen låter användaren välja en av fem svenska städer, hämtar aktuell väderdata och en 3-dagarsprognos från ett externt väder-API, räknar ut medeltemperatur med **Pandas** samt visualiserar prognosen med ett interaktivt linjediagram skapat i **Plotly**.

---

## Innehållsförteckning

1. [Om projektet](#om-projektet)
2. [Funktioner](#funktioner)
3. [Tekniker och bibliotek](#tekniker-och-bibliotek)
4. [Förutsättningar](#förutsättningar)
5. [Installation och start](#installation-och-start)
6. [Att köra testerna](#att-köra-testerna)
7. [Kodstil och linter](#kodstil-och-linter)
8. [Projektstruktur och arkitektur](#projektstruktur-och-arkitektur)
9. [Frågor att besvara i README](#frågor-att-besvara-i-readme)

---

## Om projektet

Projektet är utvecklat som en skoluppgift för att lära sig grunderna i:
- Hur man bygger en webbapplikation med **Flask**.
- Hur man kommunicerar med externa REST-API:er (**Open-Meteo**) med hjälp av biblioteket **Requests**.
- Hur man strukturerar kod i moduler med tydlig separation av ansvar (klient, tjänst, webblager).
- Hur man utför enkel dataanalys med **Pandas**.
- Hur man skapar visuella diagram med **Plotly**.
- Hur man skriver automatiserade enhetstester och integrationstester med **Pytest** och testdubblar (**Mocks**).

---

## Funktioner

- **Välj stad:** Stöd för fem fördefinierade svenska städer:
  - Stockholm
  - Göteborg
  - Malmö
  - Umeå
  - Kiruna
- **Aktuellt väder:** Visar nuvarande temperatur och vindstyrka i realtid.
- **3-dagarsprognos:** Presenterar max- och min-temperatur samt förväntad nederbörd i millimeter per dag.
- **Statistik med Pandas:** Beräknar medelvärdet av den högsta dagstemperaturen under prognosperioden.
- **Interaktivt Plotly-diagram:** Ritar upp en graf med prognosens högsta och lägsta temperaturer.
- **Robust felhantering:**
  - Validering av godkända städer.
  - Snygg visning av felmeddelanden om API-anropet skulle misslyckas eller få en timeout.
  - Egen anpassad 404-felsida om användaren navigerar till en sida som inte finns.

---

## Tekniker och bibliotek

| Bibliotek / Verktyg | Användningsområde |
| ------------------- | ----------------- |
| **Python 3.11+**    | Programmeringsspråk |
| **Flask**           | Webgramverk för routing och hantering av HTML-mallar |
| **Requests**        | Skickar HTTP-anrop till väder-API:et |
| **Pandas**          | Beräknar statistiska medelvärden på temperaturdata |
| **Plotly**          | Genererar det interaktiva HTML-diagrammet |
| **Bootstrap 5**     | CSS-ramverk för layout, tabeller och formulär |
| **Pytest**          | Testramverk för automatiska tester |
| **Ruff**            | Snabb linter och formaterare för Python-kod |

---

## Förutsättningar

- **Python**: Version 3.11 eller senare installerad på datorn. Kontrollera med:
  ```bash
  python --version
  ```
- **Git** (valfritt, för versionshantering).

---

## Installation och start

Följ dessa steg för att installera och starta projektet lokalt:

### 1. Skapa och aktivera en virtuell miljö (`.venv`)

En virtuell miljö ser till att projektets bibliotek hålls isolerade från datorns övriga Python-paket.

**I Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

*(Om du får fel om script-behörighet i PowerShell kan du köra kommandot direkt via `.venv\Scripts\python.exe` istället).*

**I macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Installera beroenden

Installera både applikationens beroenden och utvecklingsverktygen (som Pytest och Ruff):

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 3. Starta applikationen

Starta webbservern med något av följande kommandon:

```powershell
python app.py
```

eller via Flask CLI:

```powershell
flask --app app run --debug
```

### 4. Öppna i webbläsaren

Gå till följande adress i valfri webbläsare:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## Att köra testerna

Alla tester finns samlade i mappen `tests/` och körs via **Pytest**. Testerna använder mockning så att inga riktiga anrop görs mot internet under testkörningen.

Kör alla tester:
```powershell
pytest
```

Kör testerna med detaljerad information (verbose):
```powershell
pytest -v
```

Om du inte har aktiverat den virtuella miljön kan du köra direkt med:
```powershell
.venv\Scripts\pytest -v
```

### Vad testerna kontrollerar:
- **`tests/test_weather_service.py`**: Testar att stadsvalidering fungerar, att koordinater returneras korrekt, att API-data tolkas rätt, att fel uppstår vid trasig data, samt att Pandas och Plotly beräknar och ritar korrekt.
- **`tests/test_weather_client.py`**: Testar nätverksanropen mot Open-Meteo med `unittest.mock`, samt att timeouts och HTTP-fel (t.ex. serverfel 500) fångas upp och översätts till `WeatherAPIError`.
- **`tests/test_routes.py`**: Testar Flask-routerna (`/`, `/forecast`, och felaktiga URL:er för 404), samt att HTML-sidorna renderas korrekt.

---

## Kodstil och linter

Projektet använder **Ruff** för att säkerställa god kodstil och PEP8-efterlevnad.

Kör linter-kontroll:
```powershell
ruff check .
```

Eller med venv-sökväg:
```powershell
.venv\Scripts\ruff check .
```

---

## Projektstruktur och arkitektur

```text
weather-app/
├── app.py                      # Huvudapplikationen i Flask med alla webb-routes
├── weather_client.py           # Hämtar data från Open-Meteo API med felhantering
├── weather_service.py          # Behandlar data, koordinater, Pandas och Plotly
├── requirements.txt            # Appens produktionsberoenden (Flask, Requests, Pandas, Plotly)
├── requirements-dev.txt        # Utvecklingsberoenden (Pytest)
├── pyproject.toml              # Konfiguration för Pytest och Ruff
├── README.md                   # Projektdokumentation
├── templates/                  # HTML-mallar (Jinja2)
│   ├── base.html               # Grundmall med navigering, Bootstrap 5 och footer
│   ├── index.html              # Startsida med formulär för att välja stad
│   ├── forecast.html           # Resultatsida med väder, tabell och diagram
│   └── 404.html                # Anpassad felsida för saknade adresser
└── tests/                      # Automatiserade tester
    ├── conftest.py             # Pytest-fixturer (Flask test client och testdata)
    ├── test_weather_client.py  # Tester för API-klienten och felhantering
    ├── test_weather_service.py # Tester för databehandling, Pandas och Plotly
    └── test_routes.py          # Tester för Flask-routerna och sidvisning
```

### Ansvarsfördelning i koden:
1. **`weather_client.py` (Nätverkslager):**
   Ansvarar uteslutande för att skicka förfrågningar över internet till Open-Meteo API:et och paketera eventuella nätverksfel i det egna felet `WeatherAPIError`.
2. **`weather_service.py` (Affärslogik och analys):**
   Innehåller stadsregister, koordinater, datatransformering och integration med Pandas och Plotly. Den har inget beroende till Flask, vilket gör den enkel att enhetstesta.
3. **`app.py` (Webblager):**
   Kopplar samman HTTP-förfrågningar med `weather_service` och `weather_client`, samt renderar HTML-mallarna med hjälp av Jinja2.

---

## Frågor att besvara i README

### 1. Varför mockar du anropen mot API:et i dina tester, och vad skulle hända om du inte gjorde det?
Vi mockar API-anropen med `unittest.mock.patch` i `tests/test_weather_client.py` och `tests/test_routes.py` för att testerna ska vara snabba, stabila och helt oberoende av internetuppkoppling. Om vi inte mockade anropen skulle testerna göra riktiga anrop mot Open-Meteo varje gång de körs, vilket gör testkörningen långsam och känslig för driftstopp eller förändringar i väderdata. Dessutom skulle det vara omöjligt att testa felfall, såsom nätverkstimeouts (`requests.Timeout`) eller serverfel (HTTP 500), eftersom vi inte kan tvinga ett externt API att krascha på beställning.

### 2. Vad gör timeout och raise_for_status(), och varför behövs de?
I `weather_client.py` sätter vi `timeout=5` vid anropet med `requests.get()`, vilket gör att anropet avbryts om API-servern inte svarar inom 5 sekunder istället för att programmet hänger sig oändligt. Metoden `response.raise_for_status()` kontrollerar HTTP-statuskoden på API-svaret och kastar automatiskt ett `requests.HTTPError` om servern svarade med en felkod som 404 eller 500 (annars returnerar requests svaret som vanligt). Båda dessa metoder behövs för att garantera att vi upptäcker nätverksfel och problem på serversidan omedelbart så att vi kan fånga dem och kasta vårt eget användarvänliga fel `WeatherAPIError`.

### 3. Hur fungerar mallarv i Jinja2? Förklara med exempel från dina egna mallar.
Mallarv gör det möjligt att återanvända en gemensam HTML-layout över hela webbplatsen så att vi slipper duplicera kod (DRY-principen). I vårt projekt definierar `templates/base.html` den övergripande sidstrukturen med `<head>`, Bootstrap-stilar, navigering, footern samt ett dynamiskt block som heter `{% block content %}{% endblock %}`. Våra andra mallar, såsom `templates/index.html` och `templates/forecast.html`, ärver från basmallen genom direktivet `{% extends "base.html" %}` och ersätter bara innehållet i `content`-blocket med sidans unika formulär eller vädertabell.

### 4. Vad är en fixture, och vilken använder du?
En fixture i Pytest är en funktion som förbereder och tillhandahåller resurser, konfigurationer eller testdata som en eller flera testfunktioner behöver använda. I vår fil `tests/conftest.py` använder vi fixturen `client` som initierar Flasks testklient (`app.test_client()`) med testkonfigurationen påslagen, vilket gör att vi kan skicka virtuella HTTP-förfrågningar till våra routes i `tests/test_routes.py` utan att behöva starta en riktig server. Vi använder också fixturen `fake_weather_data` som levererar ett representativt svar från Open-Meteo så att vi slipper upprepa långa JSON-ordböcker i varje enskilt test.

