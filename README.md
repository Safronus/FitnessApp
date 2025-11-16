# Fitness Tracker (PySide6, macOS-friendly)

**Aktuální verze:** 3.2.3b  
**Datum vydání:** 16.11.2025 (Europe/Prague)

Desktopová aplikace pro **sledování výkonu v jednotlivých cvičeních**, s možností **individuálního data zahájení** pro každé cvičení.
PySide6 GUI s tmavým tématem, přehledy, kalendářem, grafy a správou dat (export/import).

---

## ✨ Hlavní funkce
- **🧙‍♂️ Smart Year Wizard** – průvodce vytvořením roku (vícero režimů).
- **🏋️ Vlastní cvičení** – možnost přidat/odebrat typy cvičení.
- **🗓️ Individuální start cvičení** – pro každý typ lze nastavit jiné datum zahájení.
- **📈 Grafy výkonu** – **🕒 Den** / 📅 Týden / 📆 Měsíc / 📊 Rok.
- **📍 Start v grafech** – svislá čára „Start“ podle zvoleného cvičení (respektuje jeho start).
- **↔️ Legenda vpravo vedle grafu** – nepřekrývá data (rezervovaný pravý okraj grafu).
- **🧭 Dynamický titulek grafu** – Den: *den v týdnu + datum*, Týden: *číslo týdne*, Měsíc: *název + rok*, Rok: *rok*.
- **🧩 Přehled záznamů** – seskupení po dnech, multi‑select mazání, strom s rozbalováním.
- **💾 Správa dat** – export/import JSON, migrace s automatickou zálohou.

---

## 🆕 Novinky v řadě 3.2.x
- **3.2.3b (16. 11. 2025)** – „O aplikaci“ kompletně aktualizováno (About/Quickstart/Manuál/FAQ).
- **3.2.3a** – Legenda grafu přesunuta **vpravo vedle grafu** (mimo plochu os).
- **3.2.3** – **Dynamický titulek** grafu podle módu (Den/Týden/Měsíc/Rok).
- **3.2.2** – Odebrány **radio buttony** pro přepínání grafu (ponechána tlačítka).
- **3.2.1** – Ikona **🕒** u tlačítka „Den“.
- **3.2.0** – Přidán nový mód grafu **„Den“**.

> Pozn.: Pokud ve vaší kopii vidíte jinou verzi na úvodní obrazovce, aktualizujte konstanty `VERSION` a `VERSION_DATE` v hlavičce `fitness_tracker.py`.

---

## 🧩 Instalace (macOS)
1. Ujistěte se, že máte **Python 3.10+** (`python3 --version`).
2. Doporučeno: vytvořte si virtuální prostředí:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Nainstalujte závislosti:
   ```bash
   pip install -U pip
   pip install PySide6 matplotlib
   ```

> Aplikace je vyvíjena a testována s důrazem na **macOS + Retina/HiDPI**. Nepoužíváme Windows-only závislosti.

---

## ▶️ Spuštění
```bash
python3 fitness_tracker.py
```

---

## 📂 Kde jsou data?
- Data jsou v souboru **`fitness_data.json`** ve stejné složce jako aplikace.
- Před migrací/úpravou struktur se automaticky vytváří **záloha** (kopie souboru).
- Export/Import najdete v **⚙️ Nastavení**.

---

## 🔧 Základní použití
1. Otevřete aplikaci – vybere se **aktuální rok**.
2. V **⚙️ Nastavení** případně nastavte **individuální datum zahájení** pro jednotlivá cvičení.
3. V záložce cvičení zapisujte výkony (**Přidat výkon**); přehled a graf se aktualizují.
4. V grafu používejte **tlačítka režimů**: **🕒 Den / 📅 Týden / 📆 Měsíc / 📊 Rok**.
5. V „Přehledu záznamů“ využijte **multi‑select** a **smazat vybrané**.

---

## 📈 Grafy – detaily
- **Den:** kumulativní křivka během dne; horizontála **Denní cíl**; časová osa HH:MM.
- **Týden:** bar‑chart posledních 7 dní; cílová křivka; **titulek „Týden <číslo>“**.
- **Měsíc:** aktuální měsíc (respektuje start cvičení); **titulek „Název měsíce <rok>“**.
- **Rok:** celý rok; **svislá čára „Start“** dle data zahájení daného cvičení; **titulek „Rok <rok>“**.
- **Legenda:** je **vpravo vedle grafu**; je vyhrazen pravý okraj (`subplots_adjust(right=0.78)`), aby nic nepřekrývala.

---

## 🧙‍♂️ Smart Year Wizard
- Umí analyzovat předchozí rok a navrhnout **základní cíle** i **týdenní přírůstky**.
- V případě nedostatku dat použije „level‑based“ logiku (začátečník/intermediate/pokročilý).

---

## ⌨️ Klávesové zkratky
- **Tab** – přepínání mezi prvky/sekcemi.
- **Enter** – potvrzení dialogů.
- **Esc** – zavření dialogu.

---

## 🛠️ Troubleshooting
- **Grafy se nezobrazují / Qt chyba:** reinstalujte závislosti:
  ```bash
  pip install --upgrade --force-reinstall PySide6 matplotlib
  ```
- **Nevidíte novou verzi v „O aplikaci“:** upravte konstanty `VERSION` a `VERSION_DATE` v `fitness_tracker.py`.

---

## 🧾 Licence
MIT © safronus

