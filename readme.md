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
"version": "1.0.1b",
"settings": {
"start_date": "2025-10-24",
"base_goals": {
"kliky": 50,
"dřepy": 20,
"skrčky": 20
},
"weekly_increment": {
"kliky": 10,
"dřepy": 5,
"skrčky": 10
}
},
"workouts": {
"2025-10-25": {
"kliky": {
"value": 50,
"timestamp": "2025-10-25 14:30:45"
}
}
}
}

## 📝 Changelog

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

Žádné známé problémy ve verzi 1.0.1b.

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

**Poslední aktualizace:** 25.10.2025  
**Aktuální verze:** 1.0.1b
