# 🏋️ Fitness Tracker

Aplikace pro sledování cvičení s progresivními cíli vytvořená v PySide6.

## 📋 Popis

Fitness Tracker je desktopová aplikace pro sledování pokroku v cvičení. Umožňuje zaznamenávat denní výkony, sledovat splnění cílů a vizualizovat pokrok v ročním přehledu.

## ✨ Hlavní funkce

- 📊 **Sledování 3 typů cvičení**: Kliky, Dřepy, Skrčky
- 🎯 **Progresivní týdenní cíle**: Automatický nárůst cílů každý týden
- 📅 **Roční přehled**: Barevný kalendář pro každé cvičení samostatně
- ✏️ **Editace záznamů**: Možnost upravit nebo smazat jakýkoliv záznam
- 💾 **Automatické ukládání**: Všechna data a nastavení se ukládají lokálně
- 🌙 **Dark theme**: Moderní tmavé uživatelské rozhraní
- ⏰ **Časové značky**: Každý záznam má informaci o času přidání
- 📈 **Náskok/skluz**: Zobrazení aktuálního stavu oproti plánu

## 🔧 Technické požadavky

- **Python 3.8+**
- **PySide6**

## 📦 Instalace

# Nainstaluj závislosti
pip install PySide6

# Spusť aplikaci
python fitness_tracker.py

## 🚀 Použití

### Základní nastavení

1. V záložce **Nastavení** nastav:
   - Datum zahájení cvičení
   - Základní cíle pro každé cvičení
   - Týdenní přírůstky

### Zaznamenávání cvičení

1. Přejdi do záložky konkrétního cvičení (Kliky/Dřepy/Skrčky)
2. Vyber datum a zadej počet opakování
3. Klikni na "➕ Přidat výkon"

### Správa roků

1. V **Nastavení** můžeš:
   - Přidat nový rok (i budoucí)
   - Smazat data konkrétního roku
   - Přepínat mezi roky

### Roční přehled

Každá záložka cvičení obsahuje roční kalendář s barevným označením:
- 🟩 **Zelená**: Cíl splněn
- 🟨 **Žlutá**: Částečně splněno
- 🟥 **Červená**: Nesplněno/necvičil
- ⬛ **Černá**: Den před začátkem sledování
- 🟦 **Modrá**: Dnešní den
- ⬜ **Šedá**: Budoucí den

## 📊 Výpočet cílů

Aplikace používá progresivní systém s podporou proporcionálního prvního týdne:

- **První (neúplný) týden**: Základní cíl
- **Každý další celý týden**: Základní cíl + (počet týdnů × přírůstek)

### Příklad

Start: **24.10.2025** (čtvrtek)  
Základ: **50 kliků**  
Přírůstek: **10 kliků/týden**

- 24.10. - 27.10. (4 dny) = **50 kliků**
- 28.10. - 3.11. (1. celý týden) = **60 kliků**
- 4.11. - 10.11. (2. celý týden) = **70 kliků**

## 💾 Ukládání dat

Všechna data se ukládají lokálně v souboru `fitness_data.json` ve stejném adresáři jako aplikace.

### Struktura dat

{
  "version": "1.1a",
  "year_settings": {
    "2025": {
      "start_date": "2025-10-24",
      "base_goals": {"kliky": 50, "dřepy": 20, "skrčky": 20},
      "weekly_increment": {"kliky": 10, "dřepy": 5, "skrčky": 10}
    },
    "2026": {
      "start_date": "2026-01-01",
      "base_goals": {"kliky": 60, "dřepy": 25, "skrčky": 25},
      "weekly_increment": {"kliky": 10, "dřepy": 5, "skrčky": 10}
    }
  },
  "workouts": {
    "2025-10-25": {
      "kliky": [
        {"value": 30, "timestamp": "2025-10-25 08:00:00", "id": "uuid1"},
        {"value": 20, "timestamp": "2025-10-25 18:00:00", "id": "uuid2"}
      ]
    }
  }
}













## 📝 Changelog

### v1.5b (26.10.2025 01:28 CEST) - OPRAVNÁ VERZE
**Opravy:**
- ✅ Oprava legendy - jednoduchý design bez duplicitních boxů
- 🔘 Oprava tlačítka "Akce" - nyní viditelné u záznamů
- 📂 **Sbalování záznamů po dnech:**
  - TreeWidget místo tabulky
  - Defaultně sbalené dny
  - Ikona stavu (✅/⏳/❌), souhrnný výkon a počet záznamů
  - Rozbalit/sbalit kliknutím na den

---

### v1.5a (26.10.2025 01:18 CEST) - OPRAVNÁ VERZE
**Vylepšení:**
- 🎨 Seskupení záznamů podle dne - střídání barev pozadí pro lepší přehlednost
- 🔘 Větší tlačítko "Akce" (30×30px) a vyšší řádky tabulky (35px)
- 📊 Nový design legendy kalendáře s ikonami, rámečkem a lepším stylingem

---

### v1.5 (26.10.2025 01:08 CEST)
**Nové funkce:**
- 📏 Kalendář o 50% větší - větší text (16px), pole (42×36px) a názvy měsíců
- 📊 Nový detailní přehled cvičení:
  - Den: Aktuální den s cílem a stavem
  - Týden: Současný týden (Po-Ne) s rozsahem dat
  - Měsíc: Celý měsíc s názvem
  - Zbytek roku: Zbývající dny a cíl do konce roku
- 🎨 Nový sloupec "% cíle" u záznamů s barevným pozadím:
  - Zelená: 100%+ (splněno)
  - Světle zelená: 75-99%
  - Žlutá: 50-74%
  - Oranžová: 25-49%
  - Červená: 0-24%

---

### v1.4b (26.10.2025) - OPRAVNÁ VERZE
**Opravy:**
- ✅ Oprava importu - aplikace se už neukončuje po přepsání dat
- 🔄 Refresh všech záložek a seznamu roků po importu
- 📊 Lepší aktualizace UI po obou režimech importu (Sloučit i Přepsat)

---

### v1.4a (26.10.2025) - OPRAVNÁ VERZE
**Opravy:**
- ✅ Oprava update_year_statistics() - správné zpracování list hodnot
- 📊 Oprava porovnání list/int při výpočtu statistik roku
- 💥 Oprava pádu aplikace při importu dat

---

### v1.4 (26.10.2025)
**Nové funkce:**
- 📤 Export celého cvičení do JSON souboru
  - Exportuje všechny roky, záznamy a nastavení
  - Automatické pojmenování souboru s časovým razítkem
  - Přehled exportovaných dat (roky, počet dnů)
- 📥 Import cvičení z JSON souboru
  - Režim "Sloučit" - přidá nová data k existujícím
  - Režim "Přepsat" - nahradí všechna data importovanými
  - Ochrana před ztrátou dat s potvrzovacím dialogem
- 💾 Nová sekce "Záloha a obnova dat" v záložce Nastavení

---

### v1.3f (26.10.2025) - OPRAVNÁ VERZE
**Opravy:**
- 📊 Oprava skluzu k 31.12. pro budoucí dny - tooltip nyní zobrazuje celkový skluz i do budoucnosti
- 🖼️ Odstranění duplicitního kalendáře v pozadí - lepší čištění vnořených layoutů
- ⚡ Budoucí dny nyní správně počítají a zobrazují skluz do konce roku

---

### v1.3e (26.10.2025) - OPRAVNÁ VERZE
**Opravy:**
- 🖼️ Odstranění "stínového" kalendáře - lepší styling scroll area
- 🎨 Nový design měsíčního kalendáře - větší čísla (11px), menší názvy dnů
- 📐 Fixní velikost kalendáře (220x200px) pro konzistentní zobrazení
- 📊 Skluz do konce roku se zobrazuje i pro budoucí dny
- ✅ Oprava porovnání v calculate_total_difference_to_date() - kontrola typu goal
- 📅 Kalendář v 4 sloupcích místo 3 pro lepší využití prostoru

---

### v1.3d (26.10.2025) - OPRAVNÁ VERZE
**Opravy:**
- ⏸️ Vypnutí auto-refresh (řešení problému s odznačováním checkboxů během mazání)
- 📊 Oprava porovnání v get_day_color_gradient() - kontrola typu goal
- 📝 Změna názvů sloupců: "Datum cvičení" místo "Datum" a "Čas přidání" místo "Čas"

---

### v1.3c (26.10.2025) - OPRAVNÁ VERZE
**Opravy:**
- ✅ Oprava mazání záznamů - správný přístup k checkboxu v QWidget
- ⏸️ Zastavení auto-refresh během mazání (zachování zaškrtnutých checkboxů)
- ✏️ Přidání tlačítka "Edit" do tabulky záznamů
- 🔄 Oprava refresh cílů po smazání/vynulování roku
- 📊 Oprava porovnání v kalendáři

---

### v1.3b (26.10.2025) - OPRAVNÁ VERZE
**Opravy:**
- ✅ Oprava porovnání v create_add_workout_tab() při počítání current_value
- ✅ Správné zpracování list vs dict vs ostatní typy při načítání záznamů

---

### v1.3a (26.10.2025) - OPRAVNÁ VERZE
**Opravy:**
- ✅ Oprava chybějícího importu QCheckBox
- ✅ Oprava calculate_goal() - konzistentní návrat int hodnoty
- 🔄 Přidání tlačítka "Vynulovat záznamy roku" v nastavení
- ⚙️ Vynulování smaže pouze záznamy, nastavení roku (datum, cíle, přírůstky) zůstává zachováno

---

### v1.3 (26.10.2025)
**Nové funkce:**
- 📝 Více záznamů za den - každé cvičení se přidává jako nový záznam
- ☑️ Checkboxy pro výběr záznamů v tabulkách
- 🗑️ Hromadné mazání vybraných záznamů
- ✏️ Editace a mazání jednotlivých záznamů
- 🔄 Automatická migrace dat na nový formát s podporou multiple records

---

### v1.2b (25.10.2025)
**Vylepšení:**
- 📅 Možnost zadat výkon i pro minulé dny (default = dnešní den)
- 🎨 Lepší seskupení sekcí v nastavení (datum + cíle + přírůstky v jedné skupině)
- 🖼️ Oprava designu kalendáře - odstranění duplicitního pozadí
- 📱 Responsive kalendář s lepším layoutem a mezerami
- 💬 Tooltip s celkovým skluzem/náskokem od data do konce roku
- ⚙️ Přesun záložky Nastavení před O aplikaci pro lepší přístup

---

### v1.2a (25.10.2025)
**Vylepšení:**
- 🗑️ Odstranění sloupců "Cíl" a "✓" z tabulek - zobrazení pouze zadaných záznamů
- 🎨 Redesign záložky "Přidat výkon" - každá kategorie má vlastní pole + tlačítko
- 🎯 Přidání přehledu dnešních cílů s real-time aktualizací
- 🚀 Tlačítko "Přidat všechny najednou" pro rychlé zadání
- 📅 Datum vždy aktuální (automaticky dnešní den)

---

### v1.2 (25.10.2025)
**Nové funkce:**
- ➕ Nová záložka "Přidat výkon" pro centralizované přidávání cvičení
- 🎨 Gradientní barevné zobrazení kalendáře podle výkonu (zelená náskok → červená skluz)
- 💬 Tooltip s detaily při najetí myší na den v kalendáři
- 🔵 Zvýraznění dnešního dne modrým rámečkem bez ovlivnění barevného gradientu
- 📊 Tmavší zelená = větší náskok, tmavší červená = větší skluz

**Změny:**
- 🗑️ Odstranění přidávání výkonu z jednotlivých záložek cvičení
- 📋 Záložky cvičení nyní slouží pouze k zobrazení výsledků a historie

---

### v1.1e (25.10.2025) - OPRAVNÁ VERZE
**Opravy:**
- ✅ Oprava zobrazení cílů pro budoucí/minulé roky v záložkách cvičení
- ✅ Kompletní mazání roku včetně year_settings konfigurace
- ✅ Smazaný rok zmizí ze všech seznamů a není vidět k volbě
- 🎯 Správné zobrazení cílů podle zvoleného roku

---

### v1.1d (25.10.2025) - OPRAVNÁ VERZE
**Opravy:**
- ✅ Oprava create_month_calendar_for_exercise() - poslední settings reference v kalendáři
- ✅ Kompletní odstranění všech odkazů na staré globální settings
- ✅ Plně funkční per-year nastavení bez jakýchkoliv chyb
- 🎉 Stabilní verze připravená k použití

---

### v1.1c (25.10.2025) - OPRAVNÁ VERZE
**Opravy:**
- ✅ Oprava get_goal_calculation_text() - poslední reference na staré settings
- ✅ Kompletní migrace všech funkcí na year_settings formát
- ✅ Stabilní verze pro per-year nastavení bez chyb

---

### v1.1b (25.10.2025) - OPRAVNÁ VERZE
**Opravy:**
- ✅ Oprava KeyError: 'settings' v get_available_years()
- ✅ Oprava diagnostiky výpočtu cílů pro nový formát year_settings
- ✅ Stabilizace aplikace po migraci na per-year settings

---

### v1.1a (25.10.2025)
**Nové funkce:**
- 🎯 Nastavení specifická pro každý rok (datum začátku, základní cíle, týdenní přírůstky)
- 📅 Každý rok má vlastní konfiguraci - můžeš měnit parametry nezávisle
- 🚀 Automatické vytvoření výchozího nastavení při přidání nového roku
- ⚙️ Kliknutím na rok v seznamu se načte jeho konfigurace k úpravě
- 💾 Migrace starých dat na nový formát year_settings

---

### v1.1 (25.10.2025)
**Nové funkce:**
- ℹ️ Nová záložka "O aplikaci" s informacemi o verzi
- 📊 Přesunutí diagnostiky a poznámek o výpočtech do záložky "O aplikaci"
- 🎯 Zjednodušené nastavení - přepínání roku kliknutím v seznamu roků
- 🧹 Odstranění redundantního přepínače roku z nastavení

---

### v1.0.1c (25.10.2025) - OPRAVNÁ VERZE
**Opravy:**
- ✅ Oprava vytváření nových roků - nyní se skutečně ukládají do dat
- ✅ Rok zůstane v seznamu i po restartu aplikace
- ✅ Přidané roky jsou nyní perzistentní

---

### v1.0.1b (25.10.2025) - OPRAVNÁ VERZE
**Opravy:**
- ✅ Oprava chybějící metody `update_exercise_tab`
- ✅ Kompletní implementace všech metod
- ✅ Vylepšená stabilita při přepínání roků
- ✅ Oprava chyb při vytváření nových roků

**Nové funkce:**
- 📄 README.md s kompletní dokumentací

---

### v1.0.1a (25.10.2025) - OPRAVNÁ VERZE
**Opravy:**
- ✅ Oprava KeyError: 'app_state' při zavírání aplikace
- ✅ Oprava ValueError při prázdném year selectoru
- ✅ Bezpečné ukládání stavu aplikace

**Nové funkce:**
- 💬 Dialog pro nastavení parametrů nového roku
- 🔄 Přepínač roků v záložce Nastavení
- 🛡️ Vylepšená stabilita a error handling

---

### v1.0.1 (25.10.2025)
**Nové funkce:**
- 📊 Roční přehled integrovaný do každé záložky cvičení
- 🗓️ Možnost vytvořit libovolný rok (i budoucí)
- 📅 Individuální kalendář pro každé cvičení
- 🎨 Optimalizovaný split-view layout

**Změny:**
- ❌ Odstranění redundantní záložky "Roční přehled"
- 📐 Kompaktnější design (1400x800 minimální rozlišení)

---

### v1.0.0 (25.10.2025)
**První stabilní verze:**
- ✅ Správa roků v nastavení
- ⏰ Časové značky pro všechny záznamy
- 🔢 Verzování aplikace
- 📆 Plná podpora kalendářních roků
- 🌙 Dark theme design
- ✏️ Editace a mazání záznamů
- 📈 Náskok/skluz oproti plánu
- 📊 Proporcionální první týden
- 💾 Automatické ukládání stavu

## 🐛 Známé problémy

Žádné známé problémy v aktuální verzi.

## 🤝 Přispění

Aplikace je v aktivním vývoji. Pro nahlášení chyb nebo návrhy na vylepšení použij GitHub Issues.

## 📄 Licence

Tento projekt je open-source software.

## 👨‍💻 Autor

Vytvořeno v roce 2025

## 🔗 Odkazy

- [GitHub Repository](https://github.com/Safronus/FitnessApp)
- [Issues](https://github.com/Safronus/FitnessApp/issues)

---
**Poslední aktualizace:** 26.10.2025 01:28 CEST  
**Aktuální verze:** 1.5b
