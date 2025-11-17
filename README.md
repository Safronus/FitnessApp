# Fitness Tracker (PySide6) — verze 3.8

**Datum vydání:** 2025-11-17 (Europe/Prague)  
**Platforma:** macOS (HiDPI/Retina)  
**GUI:** PySide6 (dark theme)

## Novinky ve verzi 3.8
- Kliknutí na **den v ročním kalendáři** v záložkách jednotlivých cvičení **okamžitě zobrazí denní graf** pro vybraný den.
- Vybraný den se uloží na cvičení; po přepnutí mezi záložkami lze graf znovu přepnout do „Den“ bez ztráty volby.
- Roční selector (combobox) se při kliku pokusí automaticky **sesynchronizovat** na rok zvoleného dne.
- Zachováno stávající chování režimů Týden/Měsíc/Rok. Bez nových závislostí, beze změny datového formátu.

## Instalace (macOS)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install PySide6 matplotlib numpy
```

## Spuštění
```bash
python3 fitness_tracker.py
```

## Ovládání – denní graf z kalendáře
1. Otevřete záložku některého cvičení (např. *Kliky*).
2. V ročním kalendáři **klikněte na libovolné datum**.
3. Graf výkonu pod kalendářem se přepne do režimu **Den** a zobrazí záznamy pro zvolené datum.
4. Pokud je aktivní jiný rok, roční volič se (pokud existuje v UI) **přepne** na rok zvoleného dne.

## Závislosti
- Python 3.10+
- PySide6
- matplotlib
- numpy

## Verzování
- Model: `M.minor.patchLetter`  
- Tato verze: **3.8** (minor – nová funkcionalita bez breaking changes).

## Changelog
- **3.8** — Klik na den v kalendáři → denní graf; synchronizace roku.
- **3.7.x a starší** — předchozí změny.

---

© Původní autor. Licence viz hlavička projektu.
