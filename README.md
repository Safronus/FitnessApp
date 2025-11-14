# 🏋️ Fitness Tracker

Aplikace pro sledování cvičení s progresivními cíli a AI-powered doporučením vytvořená v PySide6.

**Aktuální verze:** 3.0  
**Poslední aktualizace:** 15.11.2025 00:09 CET

## 📋 Popis

Fitness Tracker je desktopová aplikace pro sledování pokroku v cvičení s inteligentním doporučením cílů. Umožňuje zaznamenávat denní výkony, sledovat splnění cílů, vizualizovat pokrok v ročním přehledu a využívat AI-powered analýzy pro optimální nastavení.

## ✨ Hlavní funkce

### 🧙‍♂️ **Smart Year Wizard** (v3.0 - NOVĚ!)
- **Analýza předchozího roku** — automatická analýza tvého pokroku s detailními statistikami
- **Fitness level selector** — začátečník/intermediate/pokročilý s přizpůsobenými cíli
- **Personalizované doporučení** — podle dostupného času, hlavních cílů a historie
- **Multi-step průvodce** — intuitivní 5-krokový proces
- **Inteligentní algoritmus** — AI-powered výpočty založené na progressive overload
- **Vizualizace projekce** — předpověď finálního cíle na konci roku

### 🏋️ **Dynamické cvičení** (v2.0)
- **Přidávání vlastních cvičení** — shyby, běh, plank, cokoliv chceš
- **Editace cvičení** — změň název, ikonu, rychlá tlačítka
- **Správa cvičení** — smazání včetně všech dat nebo deaktivace
- **Aktivace/deaktivace** — skryj záložku bez ztráty dat

### 📊 **Sledování výkonu**
- **3 výchozí cvičení** (Kliky, Dřepy, Skrčky) + neomezené vlastní
- **Progresivní týdenní cíle** s automatickým nárůstem
- **Rychlá tlačítka** pro okamžité zaznamenání výkonu
- **Barevný kalendář** pro každé cvičení samostatně
- **TreeWidget** se záznamy a možností editace/smazání

### 📈 **Grafy a vizualizace**
- **Dynamické grafy** pro každé cvičení (týden/měsíc/rok)
- **Progress bar nad 100%** — zelený náskok, červený skluz
- **Vizualizace začátku** cvičení v grafech
- **Respektování start_date** z nastavení roku
- **Matplotlib integrace** s Qt5Agg backendem

### 💾 **Správa dat**
- **Automatické ukládání** — vše se ukládá lokálně do JSON
- **Export/import** — záloha a přenos mezi zařízeními
- **Migrace mezi verzemi** — automatická aktualizace formátu
- **Backward compatibility** — zachování kompatibility se staršími verzemi

## 🆕 Co je nového v 3.0?

### 🧙‍♂️ Smart Year Wizard - Inteligentní průvodce

**Multi-step průvodce vytvořením roku s 5 kroky:**

#### **Krok 1: Uvítání** 🎉
- Přehled celého procesu
- Informace o wizardu a jeho výhodách

#### **Krok 2: Analýza předchozího roku** 📊
```
🔍 Analýza roku 2024:

💪 Kliky:
  • Dní s tréninkem: 287
  • Průměr/den: 125.3
  • Průměr (posl. 3 měs.): 142.7
  • Finální cíl: 150

🦵 Dřepy:
  • Dní s tréninkem: 245
  • Průměr/den: 38.2
  • Průměr (posl. 3 měs.): 45.1
  • Finální cíl: 50
```

#### **Krok 3: Fitness level** 💪
- 🟢 **Začátečník** — pro ty, kdo začínají nebo se vracejí
- 🟡 **Intermediate** — pravidelný trénink, základní kondice
- 🔴 **Pokročilý** — pokročilá kondice, dlouhodobý trénink

#### **Krok 4: Preference** ⚙️
**Dostupný čas:**
- 3× týdně — nižší denní cíle, více odpočinku
- 5× týdně — balanced přístup
- Každý den — vyšší denní cíle, progresivní růst

**Hlavní cíl:**
- 🏋️ Nárůst svalové hmoty — vyšší intenzita
- 🔥 Hubnutí — kombinace cardio + síla
- 💪 Síla a kondice — vyvážený přístup

#### **Krok 5: Chytré doporučení** 🎯
```
✅ Tvé nové cíle pro rok 2025:

💪 Kliky:
  • Základní cíl (1. týden): 130 opakování/den
  • Týdenní přírůstek: +13 opakování
  • Finální cíl (52. týden): 806 opakování/den
  • Metoda: history_based

🦵 Dřepy:
  • Základní cíl (1. týden): 40 opakování/den
  • Týdenní přírůstek: +4 opakování
  • Finální cíl (52. týden): 248 opakování/den
  • Metoda: history_based

💡 Tyto hodnoty můžeš kdykoliv upravit v Nastavení.
```

---

## 🔬 Algoritmus výpočtu

### **Historie-based** (vysoká spolehlivost)
Pokud existují data z předchozího roku (min. 30 dní s tréninkem):

```python
base_goal = avg_last_3_months × fitness_level × time × goal_type × 0.9
weekly_increment = base_goal × 0.10  # 10% růst/týden
```

**Výhody:**
- ✅ Založeno na skutečných datech
- ✅ Respektuje tvůj aktuální level
- ✅ Progresivní růst (2.5-5% týdně)

---

### **Level-based** (střední spolehlivost)
Pokud neexistují data z předchozího roku:

```python
base_goal = default × fitness_level × time × goal_type
weekly_increment = base_goal × 0.10
```

**Výhody:**
- ✅ Realistické startovní hodnoty
- ✅ Bezpečné pro začátečníky
- ✅ Přizpůsobené podle fitness levelu

---

### **Multipliers**

| Kategorie | Hodnota | Multiplier |
|-----------|---------|------------|
| **Fitness Level** | | |
| 🟢 Začátečník | | 0.5× |
| 🟡 Intermediate | | 1.0× |
| 🔴 Pokročilý | | 1.5× |
| **Dostupný čas** | | |
| 3× týdně | | 0.7× |
| 5× týdně | | 1.0× |
| Každý den | | 1.2× |
| **Hlavní cíl** | | |
| 🔥 Hubnutí | | 1.0× |
| 💪 Kondice | | 1.1× |
| 🏋️ Svalová hmota | | 1.2× |

---

## 📝 Kompletní Changelog

### v3.0 (15.11.2025)
- **MAJOR UPDATE**: Smart Year Wizard
  - Multi-step průvodce vytvořením roku (5 kroků)
  - Analýza předchozího roku s detailními statistikami
  - Fitness level selector (začátečník/intermediate/pokročilý)
  - Personalizované doporučení podle času, cílů a historie
  - SmartGoalCalculator třída pro AI-powered výpočty
  - NewYearWizardDialog s progress barem a navigací
  - Inteligentní algoritmus založený na progressive overload
  - Vizualizace projekce finálního cíle
  - Historie-based vs level-based metody s fallback

### v2.0.5 (14.11.2025)
- Odstranění všech hardcoded referencí na cvičení
- Dynamické načítání pro všechny funkce (refresh, auto_refresh)
- Oprava zobrazení dat pro všechna cvičení

### v2.0.4 (14.11.2025)
- Dynamické načítání nastavení pro všechna cvičení
- Oprava `load_year_settings_to_ui()` a `save_settings()`

### v2.0.3 (14.11.2025)
- Dialog přidání cvičení s nastavením základního cíle a týdenního přírůstku

### v2.0.2 (14.11.2025)
- Oprava názvů metod (`on_year_selected_for_settings`, `add_custom_year`)
- Přidání `QLineEdit` do importů

### v2.0.1 (14.11.2025)
- Migrace klíčů cvičení na verzi bez diakritiky (dřepy→drepy, skrčky→skrcky)
- Automatická migrace starých dat
- Fallback pro zpětnou kompatibilitu

### v2.0 (14.11.2025)
- **MAJOR UPDATE**: Dynamické cvičení
  - Možnost přidávat vlastní typy cvičení
  - Možnost přejmenovat cvičení
  - Dynamické záložky podle aktivních cvičení
  - Dialog pro správu cvičení v Nastavení
  - Editace rychlých tlačítek pro každé cvičení
  - Migrace na nový formát dat s 'exercises' sekcí

### v1.8h (14.11.2025)
- Progress bar zobrazuje náskok nad 100%
- Barevné odlišení: zelená (náskok), červená (skluz), žlutá (přesně)

### v1.8g (14.11.2025)
- Rozšířen year selector pro viditelnost celých roků

### v1.8f (14.11.2025)
- Přehled pro jiné roky než aktuální zobrazuje roční souhrn
- Status podle roku: 🏁 Uzavřený / 🔮 Budoucí / 📊 Aktuální

### v1.8e (14.11.2025)
- Oprava vytváření nových roků (čistý start, automatický refresh)

### v1.8d (14.11.2025)
- Sekce DNES/TÝDEN/MĚSÍC/ZBYTEK ROKU respektují vybraný rok

### v1.8c (14.11.2025)
- Graf respektuje vybraný rok ze selektoru

### v1.8b (14.11.2025)
- Všechny módy grafu respektují startovní datum
- Vizuální označení začátku cvičení v grafech

### v1.8a (14.11.2025)
- Graf respektuje startovní datum z nastavení roku

### v1.8 (14.11.2025)
- Grafy výkonu v záložkách jednotlivých cvičení
- Přepínání zobrazení: týden/měsíc/rok
- Integrace matplotlib s Qt5Agg

### v1.7 (14.11.2025)
- Rychlá tlačítka v záložce "Přidat výkon"

### v1.6 (26.10.2025)
- Vylepšené záložky Nastavení
- Nastavení cílů ve 3 sloupcích

_(starší verze zkráceny)_

---

## 🎯 Jak používat

### Vytvoření nového roku s wizardem

1. **Otevři Nastavení** (⚙️ záložka)
2. V sekci **"Správa roků"** klikni **"➕ Přidat rok"**
3. Zadej rok (např. 2026)
4. **Průvodce tě provede:**
   - ✅ Analýza předchozího roku
   - ✅ Výběr fitness levelu
   - ✅ Nastavení preferencí (čas + cíl)
   - ✅ Zobrazení chytrého doporučení
   - ✅ Potvrzení a vytvoření
5. **Rok je vytvořen** s optimálními cíli!

---

### Přidání vlastního cvičení

1. **Jdi do Nastavení** → **Správa cvičení**
2. Klikni **"➕ Přidat cvičení"**
3. Zadej:
   - **Název:** Shyby
   - **Ikona:** 🤸 (emoji)
   - **Základní cíl:** 10 opakování/den
   - **Týdenní přírůstek:** 5 opakování
   - **Rychlá tlačítka:** 5, 10, 15
4. Klikni **"Vytvořit"**
5. **Restartuj aplikaci** → Nová záložka se objeví!

---

### Editace cvičení

1. **Nastavení** → **Správa cvičení**
2. Vyber cvičení ze seznamu
3. Klikni **"✏️ Upravit cvičení"**
4. Změň název, ikonu nebo rychlá tlačítka
5. Klikni **"Uložit"**
6. **Restartuj aplikaci** pro aplikování změn

---

### Smazání cvičení

1. **Nastavení** → **Správa cvičení**
2. Vyber cvičení
3. Klikni **"🗑️ Smazat cvičení"**
4. ⚠️ **Potvrzení:** Všechna data budou smazána!
5. **Restartuj aplikaci**

---

## 🔧 Technické informace

### Požadavky

```bash
Python 3.8+
PySide6
matplotlib
```

### Instalace

```bash
pip install PySide6 matplotlib
python fitness_tracker.py
```

### Struktura dat

Data jsou uložena v `fitness_data.json`:

```json
{
  "version": "3.0",
  "exercises": {
    "kliky": {
      "name": "Kliky",
      "icon": "💪",
      "order": 0,
      "active": true,
      "quick_buttons": [10, 15, 20]
    }
  },
  "year_settings": {
    "2025": {
      "start_date": "2025-01-01",
      "base_goals": {
        "kliky": 50,
        "drepy": 20
      },
      "weekly_increment": {
        "kliky": 10,
        "drepy": 5
      }
    }
  },
  "workouts": {
    "2025-11-14": {
      "kliky": [
        {
          "value": 50,
          "timestamp": "2025-11-14 10:30:00",
          "id": "uuid"
        }
      ]
    }
  }
}
```

---

## 🎓 Vědecké pozadí

### Progressive Overload Principle

Smart Year Wizard je založen na **progressive overload principu** — základním kamenem silového tréninku:

- **2.5-5% růst týdně** je fyziologicky optimální
- **10% růst týdně** v aplikaci = rychlejší progrese s bezpečnostní rezervou
- **Periodizace** — automatická adaptace podle historie

### Analýza posledních 3 měsíců

Použití průměru **posledních 3 měsíců** místo celého roku:
- ✅ Reflektuje **aktuální kondici**
- ✅ Eliminuje **sezónní výkyvy**
- ✅ Účtuje **progres** během roku

---

## 📊 Příklady výpočtů

### Příklad 1: Intermediate s historií

**Vstupní data:**
- Průměr posl. 3 měs.: 142.7 kliků/den
- Fitness level: Intermediate (×1.0)
- Čas: 5× týdně (×1.0)
- Cíl: Kondice (×1.1)

**Výpočet:**
```python
base = 142.7 × 1.0 × 1.0 × 1.1 × 0.9 = 141.3 → 141/den
increment = 141 × 0.10 = 14/týden
final = 141 + (52 × 14) = 869/den
```

---

### Příklad 2: Začátečník bez historie

**Vstupní data:**
- Výchozí: 50 kliků (default)
- Fitness level: Začátečník (×0.5)
- Čas: 3× týdně (×0.7)
- Cíl: Hubnutí (×1.0)

**Výpočet:**
```python
base = 50 × 0.5 × 0.7 × 1.0 = 17.5 → 18/den
increment = 18 × 0.10 = 2/týden
final = 18 + (52 × 2) = 122/den
```

---

## 🏆 Best Practices

### Jak dosáhnout nejlepších výsledků

1. **Pravidelnost** — tréning 3-5× týdně
2. **Progrese** — respektuj doporučené přírůstky
3. **Odpočinek** — 1-2 dny pauzy/týden
4. **Monitoring** — sleduj pokrok v grafech
5. **Flexibilita** — upravuj cíle podle potřeby

### Tipy pro začátečníky

- 🟢 Začni s **nižšími cíli** a postupně zvyšuj
- 🟢 Používej **rychlá tlačítka** pro jednoduché zaznamenání
- 🟢 Sleduj **barevný kalendář** pro motivaci
- 🟢 Nevzdávej to — **konzistence je klíč**!

### Tipy pro pokročilé

- 🔴 Experimentuj s **vlastními cvičeními**
- 🔴 Používaj **grafy** pro analýzu trendů
- 🔴 Nastavuj **agresivnější přírůstky** pokud zvládáš
- 🔴 Sleduj **náskok** v progress baru (nad 100%)

---

## 🐛 Známé problémy a řešení

### Aplikace nespouští

```bash
# Zkontroluj Python verzi
python --version  # Musí být 3.8+

# Reinstaluj závislosti
pip install --upgrade PySide6 matplotlib
```

### Graf se nezobrazuje

- Zkontroluj, že máš nainstalován `matplotlib`
- Restartuj aplikaci

### Data se neukládají

- Zkontroluj oprávnění k zápisu v složce
- Ujisti se, že `fitness_data.json` není read-only

---

## 🤝 Přispívání

Pull requesty jsou vítány! Pro větší změny otevři nejdřív issue.

---

## 📄 Licence

MIT License - viz LICENSE soubor

---

## 👤 Autor

**safronus**

GitHub: [FitnessApp](https://github.com/safronus/FitnessApp)

---

## 🙏 Poděkování

- PySide6 team za skvělý Qt binding
- Matplotlib za vizualizace
- Všem, kdo přispěli návrhami a reporty bugů

---

**Verze:** 3.0  
**Datum:** 15.11.2025  
**Status:** ✅ Stable
