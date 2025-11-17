# Fitness Tracker (PySide6) — v3.9.5

**Datum vydání:** 2025-11-17

Moderní desktopová aplikace na **sledování výkonu** a **BMI** s grafy a plánováním cílů. Cílová platforma je **macOS** (podporováno i na dalších OS s Pythonem).

---

## ✨ Hlavní funkce

- **Záložky pro jednotlivá cvičení** (kliky, dřepy, skrčky): denní/ týdenní/ měsíční/ roční grafy výkonu, tmavý motiv, legenda mimo graf.
- **Denní graf výkonu**: kumulativní průběh dne, hladká monotónní křivka (bez smyček), cílová čára *„Denní cíl“*.
- **BMI & váha**: měření, BMI kategorie, přepínatelné grafy (váha/ BMI/ obojí), období Týden/ Měsíc/ Rok.
- **Přidat výkon**: přehled cílů k dnešnímu/ zvolenému datu, rychlá tlačítka, souhrnná tabulka a **plán k dosažení cílového BMI**.
- **Plán k dosažení cílového BMI**:
  - volba **„Začátek plánu“** (perzistentní) — plán začíná přesně zvoleným dnem,
  - perzistentní **Cílové BMI**, **Horizont** a **Režim**, 
  - **automatický přepočet** při změně parametrů,
  - graf **„Plnění plánu po týdnech“** s **denní granularitou** (body každý den) a hladkou monotónní křivkou.
- **Nastavení**: starty cvičení, cíle, správa roků, export/import JSON (se zálohou při migraci).
- **O aplikaci**: kompletní nápověda (O aplikaci, Rychlý start, Manuál, FAQ, BMI, Plán k dosažení cílového BMI).

---

## 🧰 Požadavky

- Python **3.10+**
- Balíčky: `PySide6`, `matplotlib`, `numpy`

Instalace (doporučeno v *virtualenv*)

```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
pip install --upgrade pip
pip install PySide6 matplotlib numpy
```

---

## ▶️ Spuštění

```bash
python fitness_tracker.py
```

Při prvním spuštění vytvoří aplikace soubor **`fitness_data.json`** v pracovním adresáři (data + `app_state`).

---

## 🗂 Struktura dat

```json
{
  "workouts": {
    "YYYY-MM-DD": {
      "<exercise_id>": [ { "value": <float>, "timestamp": "YYYY-MM-DD HH:MM[:SS]" }, ... ]
    }
  },
  "app_state": {
    "plan_start_date": "YYYY-MM-DD",
    "bmi_plan": {
      "target_bmi": 22.0,
      "horizon": "6 měsíců",
      "mode": "Střední"
    }
  }
}
```

---

## 📑 Záložky a části aplikace

### 1) BMI
- Měření váhy a datum, automatický výpočet BMI a kategorie.
- Grafy: přepínač *Váha/ BMI/ Obojí*, období *Týden/ Měsíc/ Rok*.
- Tipy: vyplň **Výšku (cm)**, jinak nelze BMI spočítat.

### 2) Přidat výkon
- Přehled denních cílů k vybranému datu + rychlé přidání výkonu.
- **Plán k dosažení cílového BMI**:
  - **Začátek plánu** — vyber počáteční den (uloží se a obnovuje při dalším spuštění).
  - **Cílové BMI**, **Horizont** a **Režim** — uloženo napříč spuštěními.
  - **Graf plnění** — denní body a hladká křivka, hlavní tick po týdnech, vedlejší po dnech.

### 3) Nastavení
- Starty cvičení, cíle, správa roků, export/import dat.

### 4) O aplikaci (Help)
- **O aplikaci**, **Rychlý start**, **Manuál**, **FAQ**, **🧮 BMI**, **🎯 Plán k dosažení cílového BMI**.

---

## 📝 Release Notes

### v3.9.5 — 2025-11-17
- **Plán**: přidáno pole **„Začátek plánu“** (perzistentní) a automatický přepočet.
- **Plán**: perzistence **Cílové BMI**, **Horizont**, **Režim**.
- **Plán**: graf *Plnění plánu po týdnech* nyní **s denními body** a hladkou monotónní křivkou (stejný styl jako denní graf výkonu).
- **O aplikaci**: nové sub‑tabs **🧮 BMI** a **🎯 Plán k dosažení cílového BMI** s podrobným popisem.

---

## 🧪 Rychlý test po instalaci
1. Spusť aplikaci a zvol datum v **„Začátek plánu“** → graf se přepočte.
2. Změň **Cílové BMI**, **Horizont** a **Režim** → po restartu zůstanou nastavené.
3. Přidej pár výkonů do několika dnů → zkontroluj denní body v grafu plánu.

---

## 🔖 Licence
MIT (pokud není uvedeno jinak v hlavičkách souborů).

## 👤 Autor
Safronus & přispěvatelé.
