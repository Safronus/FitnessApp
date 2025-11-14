# 🏋️ Fitness Tracker

Aplikace pro sledování cvičení s progresivními cíli vytvořená v PySide6.

**Aktuální verze:** 2.0  
**Poslední aktualizace:** 14.11.2025 23:27 CET

## 📋 Popis

Fitness Tracker je desktopová aplikace pro sledování pokroku v cvičení. Umožňuje zaznamenávat denní výkony, sledovat splnění cílů a vizualizovat pokrok v ročním přehledu.

## ✨ Hlavní funkce (v2.0)

- 🏋️ **Dynamické cvičení**: Přidávej vlastní typy cvičení (shyby, běh, plank...)
- ✏️ **Správa cvičení**: Přejmenování, změna ikon, nastavení rychlých tlačítek
- 📊 **Sledování výkonu**: 3 výchozí typy cvičení (Kliky, Dřepy, Skrčky) + vlastní
- 🎯 **Progresivní týdenní cíle**: Automatický nárůst cílů každý týden
- ⚡ **Rychlá tlačítka**: Přednastavené hodnoty pro okamžité zaznamenání výkonu
- 📅 **Roční přehled**: Barevný kalendář pro každé cvičení samostatně
- 📈 **Grafy výkonu**: Týdenní/měsíční/roční grafy s vizualizací cílů
- 💾 **Automatické ukládání**: Všechna data a nastavení se ukládají lokálně
- 🌙 **Dark theme**: Moderní tmavé uživatelské rozhraní

## 🆕 Co je nového v 2.0?

### Dynamické cvičení
- **Přidávání vlastních cvičení** — vyber název, ikonu a rychlá tlačítka
- **Editace cvičení** — změň název, ikonu, aktivuj/deaktivuj
- **Smazání cvičení** — odstraň včetně všech dat (nevratné!)

### Vylepšená správa
- Sekce **"Správa cvičení"** v Nastavení
- Každé cvičení má vlastní konfiguraci rychlých tlačítek
- Dynamické záložky podle aktivních cvičení

## 📝 Changelog
### v2.0.3 (14.11.2025)
- **Vylepšení**: Dialog přidání cvičení nyní umožňuje nastavit základní cíl a týdenní přírůstek
  - Základní cíl: počet opakování pro 1. týden
  - Týdenní přírůstek: o kolik se zvyšuje každý týden

### v2.0.2 (14.11.2025)
- **Oprava**: Název metody pro výběr roku v nastavení

### v2.0.1 (14.11.2025)
- **Oprava**: Migrace klíčů cvičení na verzi bez diakritiky
  - Sjednocení: dřepy → drepy, skrčky → skrcky
  - Automatická migrace starých dat
  - Fallback pro zpětnou kompatibilitu

### v2.0 (14.11.2025)

- **MAJOR UPDATE**: Dynamické cvičení
  - Možnost přidávat vlastní typy cvičení
  - Možnost přejmenovat cvičení
  - Dynamické záložky podle aktivních cvičení
  - Dialog pro správu cvičení v Nastavení
  - Editace rychlých tlačítek pro každé cvičení

### v1.8h (14.11.2025)
- Progress bar zobrazuje náskok nad 100%
- Barevné odlišení: zelená (náskok), červená (skluz), žlutá (přesně)

### v1.8 (14.11.2025)
- Grafy výkonu v záložkách jednotlivých cvičení
- Přepínání zobrazení: týden/měsíc/rok
- Integrace matplotlib

### v1.7 (14.11.2025)
- Rychlá tlačítka v záložce "Přidat výkon"

_(starší changelog zkrácen)_

---

**Vytvořil:** safronus  
**Licence:** MIT
