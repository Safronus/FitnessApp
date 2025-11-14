#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fitness Tracker - Aplikace pro sledování cvičení s progresivními cíli
Verze 2.0

Changelog:
v2.0 (14.11.2025)
- **MAJOR UPDATE**: Dynamické cvičení
- Možnost přidávat vlastní typy cvičení
- Možnost přejmenovat cvičení
- Dynamické záložky podle aktivních cvičení
- Dialog pro správu cvičení v Nastavení

v1.8h - v1.0
- Předchozí verze
"""

import sys
import json
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QLabel, QSpinBox, QPushButton, QDateEdit, QTableWidget,
    QTableWidgetItem, QGroupBox, QFormLayout, QHeaderView, QMessageBox,
    QGridLayout, QComboBox, QScrollArea, QFrame, QProgressBar, QTextEdit,
    QDialog, QListWidget, QListWidgetItem, QInputDialog, QCheckBox, QFileDialog,
    QTreeWidget, QTreeWidgetItem, QLineEdit  # ← PŘIDÁNO
)
from PySide6.QtCore import Qt, QDate, QTimer
from PySide6.QtGui import QColor, QAction

# Matplotlib imports
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

TITLE = "Fitness Tracker"
VERSION = "2.0"
VERSION_DATE = "14.11.2025"

# Dark Theme Stylesheet
DARK_THEME = """
QMainWindow, QWidget {
    background-color: #1e1e1e;
    color: #e0e0e0;
}

QTabWidget::pane {
    border: 1px solid #3d3d3d;
    background-color: #1e1e1e;
}

QTabBar::tab {
    background-color: #2d2d2d;
    color: #e0e0e0;
    padding: 8px 16px;
    margin-right: 2px;
    border: 1px solid #3d3d3d;
    border-bottom: none;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}

QTabBar::tab:selected {
    background-color: #1e1e1e;
    border-bottom: 2px solid #0d7377;
}

QTabBar::tab:hover {
    background-color: #3d3d3d;
}

QGroupBox {
    background-color: #2d2d2d;
    border: 2px solid #3d3d3d;
    border-radius: 5px;
    margin-top: 10px;
    padding-top: 10px;
    color: #e0e0e0;
    font-weight: bold;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 5px;
    color: #e0e0e0;
}

QLabel {
    color: #e0e0e0;
    background-color: transparent;
}

QSpinBox {
    background-color: #2d2d2d;
    color: #e0e0e0;
    border: 1px solid #3d3d3d;
    border-radius: 3px;
    padding: 5px;
}

QSpinBox::up-button, QSpinBox::down-button {
    background-color: #3d3d3d;
    border: 1px solid #3d3d3d;
}

QSpinBox::up-button:hover, QSpinBox::down-button:hover {
    background-color: #4d4d4d;
}

QDateEdit {
    background-color: #2d2d2d;
    color: #e0e0e0;
    border: 1px solid #3d3d3d;
    border-radius: 3px;
    padding: 5px;
}

QDateEdit::drop-down {
    background-color: #3d3d3d;
    border: 1px solid #3d3d3d;
}

QDateEdit::down-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 6px solid #e0e0e0;
}

QCalendarWidget {
    background-color: #2d2d2d;
    color: #e0e0e0;
}

QCalendarWidget QToolButton {
    background-color: #3d3d3d;
    color: #e0e0e0;
    border: 1px solid #4d4d4d;
    border-radius: 3px;
    padding: 5px;
}

QCalendarWidget QToolButton:hover {
    background-color: #4d4d4d;
}

QCalendarWidget QMenu {
    background-color: #2d2d2d;
    color: #e0e0e0;
}

QCalendarWidget QSpinBox {
    background-color: #3d3d3d;
    color: #e0e0e0;
}

QCalendarWidget QAbstractItemView {
    background-color: #2d2d2d;
    color: #e0e0e0;
    selection-background-color: #0d7377;
}

QPushButton {
    background-color: #0d7377;
    color: #e0e0e0;
    border: none;
    border-radius: 5px;
    padding: 8px 16px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #14919b;
}

QPushButton:pressed {
    background-color: #0a5a5d;
}

QPushButton:disabled {
    background-color: #3d3d3d;
    color: #6d6d6d;
}

QComboBox {
    background-color: #2d2d2d;
    color: #e0e0e0;
    border: 1px solid #3d3d3d;
    border-radius: 3px;
    padding: 5px;
}

QComboBox::drop-down {
    background-color: #3d3d3d;
    border: none;
}

QComboBox::down-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 6px solid #e0e0e0;
}

QComboBox QAbstractItemView {
    background-color: #2d2d2d;
    color: #e0e0e0;
    selection-background-color: #0d7377;
    border: 1px solid #3d3d3d;
}

QListWidget {
    background-color: #2d2d2d;
    color: #e0e0e0;
    border: 1px solid #3d3d3d;
    border-radius: 5px;
}

QListWidget::item {
    padding: 8px;
    border-bottom: 1px solid #3d3d3d;
}

QListWidget::item:selected {
    background-color: #0d7377;
}

QListWidget::item:hover {
    background-color: #3d3d3d;
}

QTableWidget {
    background-color: #2d2d2d;
    color: #e0e0e0;
    gridline-color: #3d3d3d;
    border: 1px solid #3d3d3d;
    border-radius: 5px;
}

QTableWidget::item {
    padding: 5px;
}

QTableWidget::item:selected {
    background-color: #0d7377;
}

QHeaderView::section {
    background-color: #3d3d3d;
    color: #e0e0e0;
    padding: 5px;
    border: 1px solid #4d4d4d;
    font-weight: bold;
}

QScrollBar:vertical {
    background-color: #2d2d2d;
    width: 12px;
    border: none;
}

QScrollBar::handle:vertical {
    background-color: #4d4d4d;
    border-radius: 6px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #5d5d5d;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background-color: #2d2d2d;
    height: 12px;
    border: none;
}

QScrollBar::handle:horizontal {
    background-color: #4d4d4d;
    border-radius: 6px;
    min-width: 20px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #5d5d5d;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

QScrollArea {
    background-color: #1e1e1e;
    border: 1px solid #3d3d3d;
}

QTextEdit {
    background-color: #2d2d2d;
    color: #e0e0e0;
    border: 1px solid #3d3d3d;
    border-radius: 5px;
}

QProgressBar {
    background-color: #2d2d2d;
    border: 2px solid #3d3d3d;
    border-radius: 5px;
    text-align: center;
    color: #e0e0e0;
    height: 25px;
}

QProgressBar::chunk {
    background-color: #0d7377;
    border-radius: 3px;
}

QFrame {
    background-color: #2d2d2d;
    border: 1px solid #3d3d3d;
}

QDialog {
    background-color: #1e1e1e;
    color: #e0e0e0;
}

QMessageBox {
    background-color: #1e1e1e;
    color: #e0e0e0;
}

QMessageBox QPushButton {
    min-width: 80px;
}

QToolTip {
    background-color: #2d2d2d;
    color: #e0e0e0;
    border: 1px solid #0d7377;
    padding: 5px;
}
"""

class SmartGoalCalculator:
    """Chytrý kalkulátor cílů pro nový rok"""
    
    FITNESS_LEVELS = {
        "beginner": {"name": "🟢 Začátečník", "multiplier": 0.5},
        "intermediate": {"name": "🟡 Intermediate", "multiplier": 1.0},
        "advanced": {"name": "🔴 Pokročilý", "multiplier": 1.5}
    }
    
    TIME_AVAILABILITY = {
        "low": {"name": "3× týdně", "multiplier": 0.7},
        "medium": {"name": "5× týdně", "multiplier": 1.0},
        "high": {"name": "Každý den", "multiplier": 1.2}
    }
    
    GOAL_TYPES = {
        "muscle": {"name": "🏋️ Nárůst svalové hmoty", "multiplier": 1.2},
        "weight_loss": {"name": "🔥 Hubnutí", "multiplier": 1.0},
        "endurance": {"name": "💪 Síla a kondice", "multiplier": 1.1}
    }
    
    def __init__(self, data):
        self.data = data
    
    def analyze_previous_year(self, year, exercise_id):
        """Analyzuje předchozí rok a vrátí statistiky"""
        year_str = str(year)
        
        if year_str not in self.data.get("year_settings", {}):
            return None
        
        # Získat finální cíl
        settings = self.data["year_settings"][year_str]
        base_goal = settings.get("base_goals", {}).get(exercise_id, 50)
        weekly_increment = settings.get("weekly_increment", {}).get(exercise_id, 10)
        
        # Spočítat finální cíl (52 týdnů)
        final_goal = base_goal + (52 * weekly_increment)
        
        # Analyzovat skutečný výkon
        total_performed = 0
        total_goal = 0
        days_count = 0
        last_3_months_performed = []
        
        for date_str, workouts in self.data.get("workouts", {}).items():
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            
            if date_obj.year != year:
                continue
            
            if exercise_id in workouts:
                records = workouts[exercise_id]
                if isinstance(records, list):
                    perf = sum(r["value"] for r in records)
                elif isinstance(records, dict):
                    perf = records.get("value", 0)
                else:
                    perf = 0
                
                total_performed += perf
                days_count += 1
                
                # Poslední 3 měsíce
                if date_obj >= datetime(year, 10, 1).date():
                    last_3_months_performed.append(perf)
        
        avg_daily = total_performed / days_count if days_count > 0 else 0
        avg_last_3_months = sum(last_3_months_performed) / len(last_3_months_performed) if last_3_months_performed else 0
        
        return {
            "base_goal": base_goal,
            "final_goal": final_goal,
            "total_performed": total_performed,
            "avg_daily": avg_daily,
            "avg_last_3_months": avg_last_3_months,
            "days_count": days_count,
            "weekly_increment": weekly_increment
        }
    
    def calculate_smart_goals(self, exercise_id, previous_year=None, 
                             fitness_level="intermediate", time_availability="medium", 
                             goal_type="endurance"):
        """Vypočítá chytré cíle pro nový rok"""
        
        # Multipliers
        fitness_mult = self.FITNESS_LEVELS[fitness_level]["multiplier"]
        time_mult = self.TIME_AVAILABILITY[time_availability]["multiplier"]
        goal_mult = self.GOAL_TYPES[goal_type]["multiplier"]
        
        # Pokud existuje předchozí rok, použij jeho data
        if previous_year:
            analysis = self.analyze_previous_year(previous_year, exercise_id)
            
            if analysis and analysis["days_count"] > 30:  # Dostatek dat
                # Použij průměr posledních 3 měsíců jako základ
                base_from_history = analysis["avg_last_3_months"]
                
                # Aplikuj multipliers
                recommended_base = int(base_from_history * fitness_mult * time_mult * goal_mult * 0.9)
                recommended_increment = int(recommended_base * 0.10)  # 10% růst týdně
                
                return {
                    "base_goal": max(recommended_base, 10),
                    "weekly_increment": max(recommended_increment, 5),
                    "method": "history_based",
                    "confidence": "high"
                }
        
        # Fallback: použij fitness level jako základ
        base_defaults = {
            "kliky": 50,
            "drepy": 20,
            "skrcky": 30
        }
        
        base = base_defaults.get(exercise_id, 40)
        recommended_base = int(base * fitness_mult * time_mult * goal_mult)
        recommended_increment = int(recommended_base * 0.10)
        
        return {
            "base_goal": max(recommended_base, 10),
            "weekly_increment": max(recommended_increment, 5),
            "method": "level_based",
            "confidence": "medium"
        }

class NewYearWizardDialog(QDialog):
    """Multi-step wizard pro vytvoření nového roku"""
    
    def __init__(self, year, parent=None):
        super().__init__(parent)
        self.year = year
        self.parent_app = parent
        self.current_page = 0
        self.calculator = SmartGoalCalculator(parent.data)
        
        # Uložení odpovědí
        self.answers = {
            "fitness_level": "intermediate",
            "time_availability": "medium",
            "goal_type": "endurance",
            "use_smart_recommendations": True
        }
        
        self.setWindowTitle(f"🧙‍♂️ Průvodce vytvořením roku {year}")
        self.setMinimumSize(700, 500)
        
        layout = QVBoxLayout(self)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(5)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)
        
        # Stack widget pro stránky
        self.stack = QWidget()
        self.stack_layout = QVBoxLayout(self.stack)
        layout.addWidget(self.stack)
        
        # Tlačítka navigace
        buttons_layout = QHBoxLayout()
        self.back_btn = QPushButton("← Zpět")
        self.back_btn.clicked.connect(self.go_back)
        self.back_btn.setEnabled(False)
        buttons_layout.addWidget(self.back_btn)
        
        buttons_layout.addStretch()
        
        self.next_btn = QPushButton("Další →")
        self.next_btn.clicked.connect(self.go_next)
        buttons_layout.addWidget(self.next_btn)
        
        self.finish_btn = QPushButton("✅ Vytvořit rok")
        self.finish_btn.clicked.connect(self.accept)
        self.finish_btn.setVisible(False)
        buttons_layout.addWidget(self.finish_btn)
        
        layout.addLayout(buttons_layout)
        
        # Vytvoř stránky
        self.pages = [
            self.create_welcome_page(),
            self.create_analysis_page(),
            self.create_fitness_level_page(),
            self.create_preferences_page(),
            self.create_summary_page()
        ]
        
        self.show_page(0)
    
    def create_welcome_page(self):
        """Stránka 1: Uvítání"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel(f"🎉 Vytvoření roku {self.year}")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #14919b;")
        layout.addWidget(title)
        
        intro = QLabel(
            f"Vítej v průvodci vytvořením nového roku!\n\n"
            f"Tento wizard ti pomůže nastavit <b>optimální cíle</b> pro rok {self.year} "
            f"na základě tvého fitness levelu, dostupného času a cílů.\n\n"
            f"<b>Proces má 5 kroků:</b>\n"
            f"1️⃣ Analýza předchozího roku\n"
            f"2️⃣ Výběr fitness levelu\n"
            f"3️⃣ Nastavení preferencí\n"
            f"4️⃣ Chytré doporučení\n"
            f"5️⃣ Finální konfirmace"
        )
        intro.setWordWrap(True)
        intro.setStyleSheet("font-size: 13px; padding: 20px; background-color: #2d2d2d; border-radius: 5px;")
        layout.addWidget(intro)
        
        layout.addStretch()
        return page
    
    def create_analysis_page(self):
        """Stránka 2: Analýza předchozího roku"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("📊 Analýza předchozího roku")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #14919b;")
        layout.addWidget(title)
        
        self.analysis_text = QTextEdit()
        self.analysis_text.setReadOnly(True)
        self.analysis_text.setMaximumHeight(300)
        self.analysis_text.setStyleSheet("background-color: #2d2d2d; border: 1px solid #3d3d3d; font-family: monospace;")
        layout.addWidget(self.analysis_text)
        
        # Analýza
        self.perform_analysis()
        
        layout.addStretch()
        return page
    
    def perform_analysis(self):
        """Provede analýzu předchozího roku"""
        previous_year = self.year - 1
        analysis_text = f"🔍 <b>Analýza roku {previous_year}:</b><br><br>"
        
        found_data = False
        
        for exercise_id in self.parent_app.get_active_exercises():
            config = self.parent_app.get_exercise_config(exercise_id)
            analysis = self.calculator.analyze_previous_year(previous_year, exercise_id)
            
            if analysis and analysis["days_count"] > 0:
                found_data = True
                analysis_text += f"<b>{config['icon']} {config['name']}:</b><br>"
                analysis_text += f"  • Dní s tréninkem: {analysis['days_count']}<br>"
                analysis_text += f"  • Průměr/den: {analysis['avg_daily']:.1f}<br>"
                analysis_text += f"  • Průměr (posl. 3 měs.): {analysis['avg_last_3_months']:.1f}<br>"
                analysis_text += f"  • Finální cíl: {analysis['final_goal']}<br><br>"
        
        if not found_data:
            analysis_text += f"❌ Nenašel jsem dostatek dat z roku {previous_year}.<br><br>"
            analysis_text += f"💡 Cíle budou nastaveny podle tvého fitness levelu."
        
        self.analysis_text.setHtml(analysis_text)
    
    def create_fitness_level_page(self):
        """Stránka 3: Fitness level"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("💪 Jaký je tvůj současný fitness level?")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #14919b;")
        layout.addWidget(title)
        
        desc = QLabel("Vyber úroveň, která nejlépe odpovídá tvé aktuální kondici:")
        desc.setStyleSheet("font-size: 12px; color: #a0a0a0; padding: 10px;")
        layout.addWidget(desc)
        
        self.fitness_buttons = QWidget()
        fitness_layout = QVBoxLayout(self.fitness_buttons)
        
        for level_id, level_data in SmartGoalCalculator.FITNESS_LEVELS.items():
            btn = QPushButton(level_data["name"])
            btn.setCheckable(True)
            btn.setStyleSheet("""
                QPushButton {
                    padding: 15px;
                    font-size: 14px;
                    text-align: left;
                    background-color: #2d2d2d;
                    border: 2px solid #3d3d3d;
                }
                QPushButton:checked {
                    background-color: #0d7377;
                    border: 2px solid #14919b;
                }
            """)
            btn.clicked.connect(lambda checked, l=level_id: self.set_fitness_level(l))
            
            if level_id == "intermediate":
                btn.setChecked(True)
            
            fitness_layout.addWidget(btn)
        
        layout.addWidget(self.fitness_buttons)
        layout.addStretch()
        return page
    
    def create_preferences_page(self):
        """Stránka 4: Preference (čas + cíl)"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("⚙️ Tvoje preference")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #14919b;")
        layout.addWidget(title)
        
        # Čas
        time_label = QLabel("⏰ Kolik času můžeš trénovat?")
        time_label.setStyleSheet("font-size: 14px; font-weight: bold; padding-top: 10px;")
        layout.addWidget(time_label)
        
        self.time_buttons = QWidget()
        time_layout = QVBoxLayout(self.time_buttons)
        
        for time_id, time_data in SmartGoalCalculator.TIME_AVAILABILITY.items():
            btn = QPushButton(time_data["name"])
            btn.setCheckable(True)
            btn.setStyleSheet("""
                QPushButton {
                    padding: 10px;
                    font-size: 13px;
                    background-color: #2d2d2d;
                    border: 2px solid #3d3d3d;
                }
                QPushButton:checked {
                    background-color: #0d7377;
                    border: 2px solid #14919b;
                }
            """)
            btn.clicked.connect(lambda checked, t=time_id: self.set_time_availability(t))
            
            if time_id == "medium":
                btn.setChecked(True)
            
            time_layout.addWidget(btn)
        
        layout.addWidget(self.time_buttons)
        
        # Cíl
        goal_label = QLabel("🎯 Jaký je tvůj hlavní cíl?")
        goal_label.setStyleSheet("font-size: 14px; font-weight: bold; padding-top: 20px;")
        layout.addWidget(goal_label)
        
        self.goal_buttons = QWidget()
        goal_layout = QVBoxLayout(self.goal_buttons)
        
        for goal_id, goal_data in SmartGoalCalculator.GOAL_TYPES.items():
            btn = QPushButton(goal_data["name"])
            btn.setCheckable(True)
            btn.setStyleSheet("""
                QPushButton {
                    padding: 10px;
                    font-size: 13px;
                    background-color: #2d2d2d;
                    border: 2px solid #3d3d3d;
                }
                QPushButton:checked {
                    background-color: #0d7377;
                    border: 2px solid #14919b;
                }
            """)
            btn.clicked.connect(lambda checked, g=goal_id: self.set_goal_type(g))
            
            if goal_id == "endurance":
                btn.setChecked(True)
            
            goal_layout.addWidget(btn)
        
        layout.addWidget(self.goal_buttons)
        layout.addStretch()
        return page
    
    def create_summary_page(self):
        """Stránka 5: Souhrn a doporučení"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("✅ Tvé nové cíle pro rok " + str(self.year))
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #14919b;")
        layout.addWidget(title)
        
        self.summary_text = QTextEdit()
        self.summary_text.setReadOnly(True)
        self.summary_text.setStyleSheet("background-color: #2d2d2d; border: 1px solid #3d3d3d; font-family: monospace;")
        layout.addWidget(self.summary_text)
        
        layout.addStretch()
        return page
    
    def generate_summary(self):
        """Vygeneruje souhrn doporučení"""
        summary_html = f"<b>🎯 Doporučené cíle pro rok {self.year}:</b><br><br>"
        
        self.recommendations = {}
        
        for exercise_id in self.parent_app.get_active_exercises():
            config = self.parent_app.get_exercise_config(exercise_id)
            
            goals = self.calculator.calculate_smart_goals(
                exercise_id,
                previous_year=self.year - 1,
                fitness_level=self.answers["fitness_level"],
                time_availability=self.answers["time_availability"],
                goal_type=self.answers["goal_type"]
            )
            
            self.recommendations[exercise_id] = goals
            
            summary_html += f"<b>{config['icon']} {config['name']}:</b><br>"
            summary_html += f"  • Základní cíl (1. týden): <span style='color: #32c766;'>{goals['base_goal']}</span> opakování/den<br>"
            summary_html += f"  • Týdenní přírůstek: <span style='color: #FFD700;'>+{goals['weekly_increment']}</span> opakování<br>"
            
            # Vypočti finální cíl
            final_goal = goals['base_goal'] + (52 * goals['weekly_increment'])
            summary_html += f"  • Finální cíl (52. týden): <span style='color: #0d7377;'>{final_goal}</span> opakování/den<br>"
            summary_html += f"  • Metoda: {goals['method']}<br><br>"
        
        summary_html += "<br><i>💡 Tyto hodnoty můžeš kdykoliv upravit v Nastavení.</i>"
        
        self.summary_text.setHtml(summary_html)
    
    def set_fitness_level(self, level):
        self.answers["fitness_level"] = level
        # Uncheck ostatní
        for btn in self.fitness_buttons.findChildren(QPushButton):
            btn.setChecked(False)
        sender = self.sender()
        sender.setChecked(True)
    
    def set_time_availability(self, time):
        self.answers["time_availability"] = time
        for btn in self.time_buttons.findChildren(QPushButton):
            btn.setChecked(False)
        sender = self.sender()
        sender.setChecked(True)
    
    def set_goal_type(self, goal):
        self.answers["goal_type"] = goal
        for btn in self.goal_buttons.findChildren(QPushButton):
            btn.setChecked(False)
        sender = self.sender()
        sender.setChecked(True)
    
    def show_page(self, index):
        """Zobrazí stránku podle indexu"""
        # Skrytí všech stránek
        for page in self.pages:
            page.setVisible(False)
        
        # Zobraz aktuální stránku
        self.stack_layout.addWidget(self.pages[index])
        self.pages[index].setVisible(True)
        
        self.current_page = index
        self.progress_bar.setValue(index + 1)
        
        # Navigační tlačítka
        self.back_btn.setEnabled(index > 0)
        
        if index == len(self.pages) - 1:
            self.next_btn.setVisible(False)
            self.finish_btn.setVisible(True)
            self.generate_summary()
        else:
            self.next_btn.setVisible(True)
            self.finish_btn.setVisible(False)
    
    def go_next(self):
        if self.current_page < len(self.pages) - 1:
            self.show_page(self.current_page + 1)
    
    def go_back(self):
        if self.current_page > 0:
            self.show_page(self.current_page - 1)
    
    def get_recommendations(self):
        """Vrátí doporučení pro všechna cvičení"""
        return self.recommendations


class SimpleYearDialog(QDialog):
    """Dialog pro nastavení nového roku"""
    def __init__(self, year, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Nastavení roku {year}")
        self.year = year
        
        layout = QVBoxLayout(self)
        
        info_label = QLabel(f"Nastavení parametrů pro rok {year}")
        info_label.setStyleSheet("font-weight: bold; font-size: 14px; padding: 10px; color: #14919b;")
        layout.addWidget(info_label)
        
        question_label = QLabel(
            "Chceš použít aktuální nastavení (základní cíle a přírůstky)\n"
            "nebo zadat nové hodnoty pro tento rok?"
        )
        question_label.setStyleSheet("padding: 10px; color: #e0e0e0;")
        question_label.setWordWrap(True)
        layout.addWidget(question_label)
        
        buttons_layout = QHBoxLayout()
        
        use_current_btn = QPushButton("✅ Použít aktuální nastavení")
        use_current_btn.clicked.connect(self.use_current_settings)
        buttons_layout.addWidget(use_current_btn)
        
        new_settings_btn = QPushButton("⚙️ Zadat nové hodnoty")
        new_settings_btn.clicked.connect(self.set_new_settings)
        buttons_layout.addWidget(new_settings_btn)
        
        cancel_btn = QPushButton("❌ Zrušit")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        layout.addLayout(buttons_layout)
        
        self.use_current = True
    
    def use_current_settings(self):
        self.use_current = True
        self.accept()
    
    def set_new_settings(self):
        self.use_current = False
        self.accept()

class AddExerciseDialog(QDialog):
    """Dialog pro přidání nového cvičení"""
    def __init__(self, existing_ids, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Přidat nové cvičení")
        self.existing_ids = existing_ids
        
        layout = QVBoxLayout(self)
        
        # Info
        info_label = QLabel("📝 Vytvoření nového typu cvičení")
        info_label.setStyleSheet("font-weight: bold; font-size: 14px; padding: 10px; color: #14919b;")
        layout.addWidget(info_label)
        
        # Form
        form_layout = QFormLayout()
        
        # Název
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Např. Shyby, Plank, Běh")
        form_layout.addRow("Název cvičení:", self.name_input)
        
        # ID (automaticky z názvu)
        self.id_label = QLabel("(vygeneruje se automaticky)")
        self.id_label.setStyleSheet("font-size: 10px; color: #a0a0a0;")
        form_layout.addRow("ID:", self.id_label)
        
        # Ikona
        self.icon_input = QLineEdit()
        self.icon_input.setText("🏋️")
        self.icon_input.setMaxLength(2)
        form_layout.addRow("Ikona (emoji):", self.icon_input)
        
        # **NOVĚ: Základní cíl**
        self.base_goal_spin = QSpinBox()
        self.base_goal_spin.setRange(1, 1000)
        self.base_goal_spin.setValue(50)
        self.base_goal_spin.setSuffix(" opakování/den")
        form_layout.addRow("🎯 Základní cíl (1. týden):", self.base_goal_spin)
        
        # **NOVĚ: Týdenní přírůstek**
        self.weekly_increment_spin = QSpinBox()
        self.weekly_increment_spin.setRange(0, 100)
        self.weekly_increment_spin.setValue(10)
        self.weekly_increment_spin.setSuffix(" opakování")
        form_layout.addRow("📈 Týdenní přírůstek:", self.weekly_increment_spin)
        
        # Rychlá tlačítka
        quick_label = QLabel("Rychlá tlačítka (oddělte čárkou):")
        self.quick_input = QLineEdit()
        self.quick_input.setText("10, 20, 30")
        self.quick_input.setPlaceholderText("10, 20, 30")
        form_layout.addRow(quick_label, self.quick_input)
        
        layout.addLayout(form_layout)
        
        # Tlačítka
        buttons_layout = QHBoxLayout()
        
        save_btn = QPushButton("Vytvořit")
        save_btn.clicked.connect(self.validate_and_accept)
        buttons_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("Zrušit")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        layout.addLayout(buttons_layout)
    
    def validate_and_accept(self):
        """Validace a přijetí"""
        name = self.name_input.text().strip()
        
        if not name:
            QMessageBox.warning(self, "Chyba", "Zadej název cvičení!")
            return
        
        # Vygeneruj ID z názvu (lowercase, bez diakritiky)
        import unicodedata
        exercise_id = ''.join(
            c for c in unicodedata.normalize('NFD', name.lower())
            if unicodedata.category(c) != 'Mn'
        ).replace(' ', '_')
        
        # Kontrola duplicity
        if exercise_id in self.existing_ids:
            QMessageBox.warning(self, "Chyba", f"Cvičení s ID '{exercise_id}' již existuje!")
            return
        
        self.exercise_id = exercise_id
        self.accept()
    
    def get_exercise_data(self):
        """Vrátí data pro nové cvičení"""
        # Parse rychlých tlačítek
        quick_text = self.quick_input.text().strip()
        try:
            quick_buttons = [int(x.strip()) for x in quick_text.split(',') if x.strip()]
        except:
            quick_buttons = [10, 20, 30]
        
        return {
            "name": self.name_input.text().strip(),
            "icon": self.icon_input.text().strip() or "🏋️",
            "order": 999,  # Na konec
            "active": True,
            "quick_buttons": quick_buttons,
            "base_goal": self.base_goal_spin.value(),  # **NOVĚ**
            "weekly_increment": self.weekly_increment_spin.value()  # **NOVĚ**
        }

    
    def validate_and_accept(self):
        """Validace a přijetí"""
        name = self.name_input.text().strip()
        
        if not name:
            QMessageBox.warning(self, "Chyba", "Zadej název cvičení!")
            return
        
        # Vygeneruj ID z názvu (lowercase, bez diakritiky)
        import unicodedata
        exercise_id = ''.join(
            c for c in unicodedata.normalize('NFD', name.lower())
            if unicodedata.category(c) != 'Mn'
        ).replace(' ', '_')
        
        # Kontrola duplicity
        if exercise_id in self.existing_ids:
            QMessageBox.warning(self, "Chyba", f"Cvičení s ID '{exercise_id}' již existuje!")
            return
        
        self.exercise_id = exercise_id
        self.accept()
    
    def get_exercise_data(self):
        """Vrátí data pro nové cvičení"""
        # Parse rychlých tlačítek
        quick_text = self.quick_input.text().strip()
        try:
            quick_buttons = [int(x.strip()) for x in quick_text.split(',') if x.strip()]
        except:
            quick_buttons = [10, 20, 30]
        
        return {
            "name": self.name_input.text().strip(),
            "icon": self.icon_input.text().strip() or "🏋️",
            "order": 999,
            "active": True,
            "quick_buttons": quick_buttons,
            "base_goal": self.base_goal_spin.value(),  # ← MUSÍ BÝT
            "weekly_increment": self.weekly_increment_spin.value()  # ← MUSÍ BÝT
        }


class EditExerciseDialog(QDialog):
    """Dialog pro editaci existujícího cvičení"""
    def __init__(self, exercise_id, exercise_config, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Upravit cvičení: {exercise_config['name']}")
        self.exercise_id = exercise_id
        
        layout = QVBoxLayout(self)
        
        # Info
        info_label = QLabel(f"✏️ Úprava cvičení '{exercise_config['name']}'")
        info_label.setStyleSheet("font-weight: bold; font-size: 14px; padding: 10px; color: #14919b;")
        layout.addWidget(info_label)
        
        # ID (nepřejmenovatelné)
        id_info = QLabel(f"ID: {exercise_id} (nelze změnit)")
        id_info.setStyleSheet("font-size: 10px; color: #a0a0a0; padding: 5px;")
        layout.addWidget(id_info)
        
        # Form
        form_layout = QFormLayout()
        
        # Název
        self.name_input = QLineEdit()
        self.name_input.setText(exercise_config['name'])
        form_layout.addRow("Název cvičení:", self.name_input)
        
        # Ikona
        self.icon_input = QLineEdit()
        self.icon_input.setText(exercise_config.get('icon', '🏋️'))
        self.icon_input.setMaxLength(2)
        form_layout.addRow("Ikona (emoji):", self.icon_input)
        
        # Rychlá tlačítka
        quick_buttons = exercise_config.get('quick_buttons', [10, 20, 30])
        self.quick_input = QLineEdit()
        self.quick_input.setText(', '.join(map(str, quick_buttons)))
        form_layout.addRow("Rychlá tlačítka:", self.quick_input)
        
        # Aktivní
        self.active_checkbox = QCheckBox("Aktivní (zobrazit záložku)")
        self.active_checkbox.setChecked(exercise_config.get('active', True))
        form_layout.addRow("", self.active_checkbox)
        
        layout.addLayout(form_layout)
        
        # Tlačítka
        buttons_layout = QHBoxLayout()
        
        save_btn = QPushButton("Uložit")
        save_btn.clicked.connect(self.accept)
        buttons_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("Zrušit")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        layout.addLayout(buttons_layout)
    
    def get_exercise_data(self):
        """Vrátí aktualizovaná data"""
        # Parse rychlých tlačítek
        quick_text = self.quick_input.text().strip()
        try:
            quick_buttons = [int(x.strip()) for x in quick_text.split(',') if x.strip()]
        except:
            quick_buttons = [10, 20, 30]
        
        return {
            "name": self.name_input.text().strip(),
            "icon": self.icon_input.text().strip() or "🏋️",
            "active": self.active_checkbox.isChecked(),
            "quick_buttons": quick_buttons
        }

class EditWorkoutDialog(QDialog):
    """Dialog pro editaci existujícího záznamu"""
    def __init__(self, exercise_type, date_str, current_value, timestamp, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Upravit záznam - {exercise_type}")
        self.delete_requested = False
        
        layout = QVBoxLayout(self)
        
        info_label = QLabel(f"Úprava záznamu pro {date_str}")
        info_label.setStyleSheet("font-weight: bold; font-size: 13px; padding: 5px; color: #14919b;")
        layout.addWidget(info_label)
        
        if timestamp:
            time_label = QLabel(f"Původně přidáno: {timestamp}")
            time_label.setStyleSheet("font-size: 10px; color: #a0a0a0; padding: 2px;")
            layout.addWidget(time_label)
        
        form_layout = QFormLayout()
        
        self.value_spin = QSpinBox()
        self.value_spin.setRange(0, 1000)
        self.value_spin.setValue(current_value)
        form_layout.addRow("Počet:", self.value_spin)
        
        layout.addLayout(form_layout)
        
        buttons_layout = QHBoxLayout()
        
        save_btn = QPushButton("💾 Uložit")
        save_btn.clicked.connect(self.accept)
        buttons_layout.addWidget(save_btn)
        
        delete_btn = QPushButton("🗑️ Smazat")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        delete_btn.clicked.connect(self.delete_record)
        buttons_layout.addWidget(delete_btn)
        
        cancel_btn = QPushButton("❌ Zrušit")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        layout.addLayout(buttons_layout)
    
    def get_value(self):
        return self.value_spin.value()
    
    def delete_record(self):
        self.delete_requested = True
        self.accept()


class FitnessTrackerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{TITLE} v{VERSION} - Sledování cvičení")
        self.setMinimumSize(1400, 800)
        
        self.data_file = Path("fitness_data.json")
        self.exercise_year_selectors = {}
        self.exercise_calendar_widgets = {}
        self.current_settings_year = datetime.now().year
        
        self.load_data()
        self.ensure_app_state()
        self.migrate_data()
        self.migrate_to_year_settings()
        self.migrate_to_exercises()
        self.migrate_exercise_keys()  # **NOVĚ: Migrace klíčů bez diakritiky**
        
        self.setup_ui()
        self.restore_app_state()
        
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.auto_refresh)
        self.update_timer.start(5000)

    def add_exercise(self):
        """Přidá nové cvičení"""
        existing_ids = list(self.data.get("exercises", {}).keys())
        
        dialog = AddExerciseDialog(existing_ids, self)
        if dialog.exec():
            exercise_id = dialog.exercise_id
            exercise_data = dialog.get_exercise_data()
            
            # Přidej do dat
            if "exercises" not in self.data:
                self.data["exercises"] = {}
            
            # **BEZPEČNÉ extrahování cílů z dialogu (s fallback)**
            base_goal = exercise_data.pop("base_goal", 50)  # Výchozí 50
            weekly_increment = exercise_data.pop("weekly_increment", 10)  # Výchozí 10
            
            self.data["exercises"][exercise_id] = exercise_data
            
            # Přidej do year_settings pro všechny roky s hodnotami z dialogu
            for year_str in self.data.get("year_settings", {}).keys():
                if exercise_id not in self.data["year_settings"][year_str]["base_goals"]:
                    self.data["year_settings"][year_str]["base_goals"][exercise_id] = base_goal
                if exercise_id not in self.data["year_settings"][year_str]["weekly_increment"]:
                    self.data["year_settings"][year_str]["weekly_increment"][exercise_id] = weekly_increment
            
            # Přidej do app_state
            if "app_state" in self.data and "exercise_years" in self.data["app_state"]:
                self.data["app_state"]["exercise_years"][exercise_id] = datetime.now().year
            
            self.save_data()
            
            self.show_message("Úspěch", f"Cvičení '{exercise_data['name']}' bylo přidáno!\n\nZákladní cíl: {base_goal}\nTýdenní přírůstek: {weekly_increment}\n\nRestartuj aplikaci pro zobrazení nové záložky.", QMessageBox.Information)

    def edit_exercise(self, exercise_id):
        """Edituje existující cvičení"""
        if "exercises" not in self.data or exercise_id not in self.data["exercises"]:
            self.show_message("Chyba", "Cvičení nenalezeno!", QMessageBox.Warning)
            return
        
        config = self.data["exercises"][exercise_id]
        
        dialog = EditExerciseDialog(exercise_id, config, self)
        if dialog.exec():
            updated_data = dialog.get_exercise_data()
            
            # Aktualizuj data
            self.data["exercises"][exercise_id].update(updated_data)
            self.save_data()
            
            self.show_message("Úspěch", f"Cvičení bylo aktualizováno!\n\nRestartuj aplikaci pro aplikování změn.", QMessageBox.Information)
    
    
    def delete_exercise(self, exercise_id):
        """Smaže cvičení (včetně všech dat!)"""
        if "exercises" not in self.data or exercise_id not in self.data["exercises"]:
            return
        
        config = self.data["exercises"][exercise_id]
        
        msg = QMessageBox(self)
        msg.setWindowTitle("Potvrzení smazání")
        msg.setText(f"Opravdu chceš smazat cvičení '{config['name']}'?")
        msg.setInformativeText("⚠️ Budou smazána VŠECHNA data (záznamy, cíle) pro toto cvičení!\n\nTato akce je nevratná!")
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        
        yes_btn = msg.button(QMessageBox.Yes)
        yes_btn.setText("Ano, smazat")
        no_btn = msg.button(QMessageBox.No)
        no_btn.setText("Ne, zrušit")
        
        if msg.exec() == QMessageBox.Yes:
            # Smaž z exercises
            del self.data["exercises"][exercise_id]
            
            # Smaž všechny záznamy
            for date_str in list(self.data["workouts"].keys()):
                if exercise_id in self.data["workouts"][date_str]:
                    del self.data["workouts"][date_str][exercise_id]
            
            # Smaž z year_settings
            for year_str in self.data.get("year_settings", {}).keys():
                if exercise_id in self.data["year_settings"][year_str].get("base_goals", {}):
                    del self.data["year_settings"][year_str]["base_goals"][exercise_id]
                if exercise_id in self.data["year_settings"][year_str].get("weekly_increment", {}):
                    del self.data["year_settings"][year_str]["weekly_increment"][exercise_id]
            
            # Smaž z app_state
            if "app_state" in self.data and "exercise_years" in self.data["app_state"]:
                if exercise_id in self.data["app_state"]["exercise_years"]:
                    del self.data["app_state"]["exercise_years"][exercise_id]
            
            self.save_data()
            
            self.show_message("Smazáno", f"Cvičení '{config['name']}' bylo smazáno.\n\nRestartuj aplikaci.", QMessageBox.Information)
        
    def closeEvent(self, event):
        try:
            self.save_app_state()
        except Exception as e:
            print(f"Chyba při ukládání stavu: {e}")
        event.accept()
    
    def ensure_app_state(self):
        """Zajistí, že app_state vždy existuje"""
        if 'app_state' not in self.data:
            self.data['app_state'] = {
                'last_tab': 0,
                'window_geometry': None,
                'exercise_years': {
                    'kliky': datetime.now().year,
                    'dřepy': datetime.now().year,
                    'skrčky': datetime.now().year
                }
            }
        
        if 'exercise_years' not in self.data['app_state']:
            self.data['app_state']['exercise_years'] = {
                'kliky': datetime.now().year,
                'dřepy': datetime.now().year,
                'skrčky': datetime.now().year
            }
    
    def migrate_data(self):
        """Migrace starých dat na nový formát s timestampy a lists"""
        migrated = False
        
        for date_str, workouts in self.data['workouts'].items():
            for exercise, value in list(workouts.items()):
                # Migrace z single value na dict
                if isinstance(value, (int, float)):
                    workouts[exercise] = [{
                        'value': int(value),
                        'timestamp': f"{date_str} 12:00:00",
                        'id': str(uuid.uuid4())
                    }]
                    migrated = True
                # Migrace z single dict na list
                elif isinstance(value, dict) and 'value' in value:
                    workouts[exercise] = [{
                        'value': value['value'],
                        'timestamp': value.get('timestamp', f"{date_str} 12:00:00"),
                        'id': str(uuid.uuid4())
                    }]
                    migrated = True
                # Už je list - zkontroluj že má všechny záznamy ID
                elif isinstance(value, list):
                    for record in value:
                        if 'id' not in record:
                            record['id'] = str(uuid.uuid4())
                            migrated = True
        
        if migrated:
            self.save_data()
            print("Data byla migrována na nový formát s multiple records")

    def migrate_to_year_settings(self):
        """Migrace starého formátu settings na year_settings"""
        if 'year_settings' not in self.data:
            self.data['year_settings'] = {}
            
            if 'settings' in self.data:
                old_settings = self.data['settings']
                start_year = int(old_settings['start_date'].split('-')[0])
                
                self.data['year_settings'][str(start_year)] = {
                    'start_date': old_settings['start_date'],
                    'base_goals': old_settings['base_goals'].copy(),
                    'weekly_increment': old_settings['weekly_increment'].copy()
                }
                
                del self.data['settings']
                
                self.save_data()
                print(f"Data migrována na nový formát year_settings pro rok {start_year}")
                
    def migrate_to_exercises(self):
        """Migrace na nový formát s exercises (verze 2.0)"""
        if "exercises" not in self.data:
            print("Migrace na verze 2.0: Vytváření struktury 'exercises'...")
            
            # Výchozí cvičení
            self.data["exercises"] = {
                "kliky": {
                    "name": "Kliky",
                    "icon": "💪",
                    "order": 0,
                    "active": True,
                    "quick_buttons": [10, 15, 20]
                },
                "drepy": {
                    "name": "Dřepy",
                    "icon": "🦵",
                    "order": 1,
                    "active": True,
                    "quick_buttons": [5, 10, 15, 20]
                },
                "skrcky": {
                    "name": "Skrčky",
                    "icon": "🧘",
                    "order": 2,
                    "active": True,
                    "quick_buttons": [10, 15, 20, 30, 40]
                }
            }
            
            self.save_data()
            print("Migrace dokončena: Struktura 'exercises' vytvořena.")

    def migrate_exercise_keys(self):
        """Migrace klíčů cvičení - sjednocení na verzi bez diakritiky (v2.0)"""
        # Mapování starých klíčů na nové (bez diakritiky)
        key_mapping = {
            "dřepy": "drepy",
            "skrčky": "skrcky"
        }
        
        changed = False
        
        # Migrace v year_settings
        for year_str in self.data.get("year_settings", {}).keys():
            year_settings = self.data["year_settings"][year_str]
            
            # base_goals
            if "base_goals" in year_settings:
                for old_key, new_key in key_mapping.items():
                    if old_key in year_settings["base_goals"]:
                        year_settings["base_goals"][new_key] = year_settings["base_goals"].pop(old_key)
                        changed = True
            
            # weekly_increment
            if "weekly_increment" in year_settings:
                for old_key, new_key in key_mapping.items():
                    if old_key in year_settings["weekly_increment"]:
                        year_settings["weekly_increment"][new_key] = year_settings["weekly_increment"].pop(old_key)
                        changed = True
        
        # Migrace v workouts
        for date_str in list(self.data.get("workouts", {}).keys()):
            for old_key, new_key in key_mapping.items():
                if old_key in self.data["workouts"][date_str]:
                    self.data["workouts"][date_str][new_key] = self.data["workouts"][date_str].pop(old_key)
                    changed = True
        
        # Migrace v app_state
        if "app_state" in self.data and "exercise_years" in self.data["app_state"]:
            for old_key, new_key in key_mapping.items():
                if old_key in self.data["app_state"]["exercise_years"]:
                    self.data["app_state"]["exercise_years"][new_key] = self.data["app_state"]["exercise_years"].pop(old_key)
                    changed = True
        
        if changed:
            print("Migrace klíčů cvičení dokončena: dřepy → drepy, skrčky → skrcky")
            self.save_data()
    
    def get_year_settings(self, year):
        """Vrátí nastavení pro daný rok"""
        year_str = str(year)
        
        if year_str not in self.data['year_settings']:
            self.data['year_settings'][year_str] = {
                'start_date': f'{year}-01-01',
                'base_goals': {
                    'kliky': 50,
                    'dřepy': 20,
                    'skrčky': 20
                },
                'weekly_increment': {
                    'kliky': 10,
                    'dřepy': 5,
                    'skrčky': 10
                }
            }
            self.save_data()
        
        return self.data['year_settings'][year_str]
    
    def get_active_exercises(self):
        """Vrátí seznam aktivních cvičení (ID) seřazených podle order"""
        if "exercises" not in self.data:
            return ["kliky", "drepy", "skrcky"]
        
        active = [
            (ex_id, config) 
            for ex_id, config in self.data["exercises"].items() 
            if config.get("active", True)
        ]
        
        # Seřadit podle order
        active.sort(key=lambda x: x[1].get("order", 999))
        
        return [ex_id for ex_id, _ in active]
    
    
    def get_exercise_config(self, exercise_id):
        """Vrátí konfiguraci pro dané cvičení"""
        if "exercises" not in self.data:
            # Fallback pro starou strukturu
            defaults = {
                "kliky": {"name": "Kliky", "icon": "💪", "order": 0, "active": True, "quick_buttons": [10, 15, 20]},
                "drepy": {"name": "Dřepy", "icon": "🦵", "order": 1, "active": True, "quick_buttons": [5, 10, 15, 20]},
                "skrcky": {"name": "Skrčky", "icon": "🧘", "order": 2, "active": True, "quick_buttons": [10, 15, 20, 30, 40]}
            }
            return defaults.get(exercise_id, {"name": exercise_id.capitalize(), "icon": "🏋️", "order": 999, "active": True, "quick_buttons": [10, 20, 30]})
        
        return self.data["exercises"].get(exercise_id, {
            "name": exercise_id.capitalize(),
            "icon": "🏋️",
            "order": 999,
            "active": True,
            "quick_buttons": [10, 20, 30]
        })

    def load_data(self):
        """Načte data ze souboru nebo vytvoří výchozí strukturu"""
        if self.data_file.exists():
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        else:
            current_year = datetime.now().year
            self.data = {
                "version": VERSION,
                "exercises": {
                    "kliky": {
                        "name": "Kliky",
                        "icon": "💪",
                        "order": 0,
                        "active": True,
                        "quick_buttons": [10, 15, 20]
                    },
                    "drepy": {  # BEZ DIAKRITIKY
                        "name": "Dřepy",
                        "icon": "🦵",
                        "order": 1,
                        "active": True,
                        "quick_buttons": [5, 10, 15, 20]
                    },
                    "skrcky": {  # BEZ DIAKRITIKY
                        "name": "Skrčky",
                        "icon": "🧘",
                        "order": 2,
                        "active": True,
                        "quick_buttons": [10, 15, 20, 30, 40]
                    }
                },
                "year_settings": {
                    str(current_year): {
                        "start_date": f"{current_year}-01-01",
                        "base_goals": {
                            "kliky": 50,
                            "drepy": 20,  # BEZ DIAKRITIKY
                            "skrcky": 20  # BEZ DIAKRITIKY
                        },
                        "weekly_increment": {
                            "kliky": 10,
                            "drepy": 5,   # BEZ DIAKRITIKY
                            "skrcky": 10  # BEZ DIAKRITIKY
                        }
                    }
                },
                "workouts": {},
                "app_state": {
                    "last_tab": 0,
                    "window_geometry": None,
                    "exercise_years": {
                        "kliky": datetime.now().year,
                        "drepy": datetime.now().year,   # BEZ DIAKRITIKY
                        "skrcky": datetime.now().year   # BEZ DIAKRITIKY
                    }
                }
            }
            self.save_data()

    def save_data(self):
        self.data['version'] = VERSION
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def save_app_state(self):
        """Bezpečné ukládání stavu"""
        try:
            self.ensure_app_state()
            
            if hasattr(self, 'tabs'):
                self.data['app_state']['last_tab'] = self.tabs.currentIndex()
            
            self.data['app_state']['window_geometry'] = {
                'x': self.x(),
                'y': self.y(),
                'width': self.width(),
                'height': self.height()
            }
            
            for exercise, selector in self.exercise_year_selectors.items():
                if selector and selector.currentText():
                    try:
                        self.data['app_state']['exercise_years'][exercise] = int(selector.currentText())
                    except ValueError:
                        self.data['app_state']['exercise_years'][exercise] = datetime.now().year
            
            self.save_data()
        except Exception as e:
            print(f"Chyba při ukládání app_state: {e}")
    
    def restore_app_state(self):
        try:
            self.ensure_app_state()
            
            if self.data['app_state'].get('window_geometry'):
                geom = self.data['app_state']['window_geometry']
                self.setGeometry(geom['x'], geom['y'], geom['width'], geom['height'])
            
            if 'last_tab' in self.data['app_state'] and hasattr(self, 'tabs'):
                self.tabs.setCurrentIndex(self.data['app_state']['last_tab'])
            
            if 'exercise_years' in self.data['app_state']:
                for exercise, year in self.data['app_state']['exercise_years'].items():
                    if exercise in self.exercise_year_selectors:
                        selector = self.exercise_year_selectors[exercise]
                        index = selector.findText(str(year))
                        if index >= 0:
                            selector.setCurrentIndex(index)
        except Exception as e:
            print(f"Chyba při obnovování stavu: {e}")
    
    def setup_ui(self):
        """Vytvoří UI - dynamické záložky podle active exercises"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        self.tabs = QTabWidget()
        self.tabs.currentChanged.connect(self.on_tab_changed)
        layout.addWidget(self.tabs)
        
        # Záložka "Přidat výkon" - vždy první
        self.tabs.addTab(self.create_add_workout_tab(), "➕ Přidat výkon")
        
        # **DYNAMICKÉ ZÁLOŽKY PRO CVIČENÍ**
        active_exercises = self.get_active_exercises()
        for exercise_id in active_exercises:
            config = self.get_exercise_config(exercise_id)
            tab_label = f"{config['icon']} {config['name']}"
            self.tabs.addTab(self.create_exercise_tab(exercise_id, config['icon']), tab_label)
        
        # Záložka "Nastavení"
        self.tabs.addTab(self.create_settings_tab(), "⚙️ Nastavení")
        
        # Záložka "O aplikaci"
        self.tabs.addTab(self.create_about_tab(), "ℹ️ O aplikaci")

    def add_single_workout(self, exercise_type, value):
        """Přidá výkon pro jednu kategorii"""
        if value <= 0:
            self.show_message("Chyba", f"Zadej nenulovou hodnotu pro {exercise_type}!", QMessageBox.Warning)
            return
        
        selected_date_str = self.add_date_edit.date().toString("yyyy-MM-dd")
        
        if selected_date_str not in self.data["workouts"]:
            self.data["workouts"][selected_date_str] = {}
        
        if exercise_type not in self.data["workouts"][selected_date_str]:
            self.data["workouts"][selected_date_str][exercise_type] = []
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_record = {
            "value": value,
            "timestamp": timestamp,
            "id": str(uuid.uuid4())
        }
        
        self.data["workouts"][selected_date_str][exercise_type].append(new_record)
        self.save_data()
        
        # Aktualizuj všechny záložky
        active_exercises = self.get_active_exercises()
        for exercise in active_exercises:
            self.update_exercise_tab(exercise)
            self.refresh_exercise_calendar(exercise)
        
        self.refresh_add_tab_goals()
        
        config = self.get_exercise_config(exercise_type)
        self.show_message("Přidáno", f"Výkon byl zaznamenán:\n{value}× {config['name']}")
        
        # Reset správného SpinBoxu
        if exercise_type in self.exercise_spinboxes:
            self.exercise_spinboxes[exercise_type].setValue(0)

    def add_all_workouts(self):
        """Přidá všechny výkony najednou"""
        active_exercises = self.get_active_exercises()
    
        # Sbírej hodnoty
        values = {}
        for exercise_id in active_exercises:
            if exercise_id in self.exercise_spinboxes:
                val = self.exercise_spinboxes[exercise_id].value()
                if val > 0:
                    values[exercise_id] = val
        
        if not values:
            self.show_message("Chyba", "Zadej alespoň jednu nenulovou hodnotu!", QMessageBox.Warning)
            return
        
        selected_date_str = self.add_date_edit.date().toString("yyyy-MM-dd")
        
        if selected_date_str not in self.data["workouts"]:
            self.data["workouts"][selected_date_str] = {}
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        added = []
        
        for exercise_id, val in values.items():
            if exercise_id not in self.data["workouts"][selected_date_str]:
                self.data["workouts"][selected_date_str][exercise_id] = []
            
            self.data["workouts"][selected_date_str][exercise_id].append({
                "value": val,
                "timestamp": timestamp,
                "id": str(uuid.uuid4())
            })
            
            config = self.get_exercise_config(exercise_id)
            added.append(f"{config['icon']} {config['name']}: {val}")
        
        self.save_data()
        
        # Aktualizuj všechny záložky
        for exercise in active_exercises:
            self.update_exercise_tab(exercise)
            self.refresh_exercise_calendar(exercise)
        
        self.refresh_add_tab_goals()
        self.show_message("Přidáno", f"Výkony zaznamenány:\n" + "\n".join(added))
        
        # Reset všech SpinBoxů
        for exercise_id in active_exercises:
            if exercise_id in self.exercise_spinboxes:
                self.exercise_spinboxes[exercise_id].setValue(0)


    def create_add_workout_tab(self):
        """Záložka pro přidávání výkonů - dynamická podle aktivních cvičení"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Titulek
        title_label = QLabel("📝 Přidání výkonů")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #14919b; padding: 10px;")
        layout.addWidget(title_label)
        
        # Výběr data
        date_row = QHBoxLayout()
        date_row.addWidget(QLabel("Datum:"))
        self.add_date_edit = QDateEdit()
        self.add_date_edit.setDate(QDate.currentDate())
        self.add_date_edit.setCalendarPopup(True)
        self.add_date_edit.dateChanged.connect(self.refresh_add_tab_goals)
        date_row.addWidget(self.add_date_edit)
        date_row.addStretch()
        layout.addLayout(date_row)
        
        # Přehled cílů pro zvolené datum
        goals_group = QGroupBox("🎯 Cíle pro zvolené datum")
        goals_layout = QVBoxLayout()
        goals_layout.setObjectName("add_goals_layout")
        
        self.add_goals_labels = {}
        selected_date_str = self.add_date_edit.date().toString("yyyy-MM-dd")
        
        active_exercises = self.get_active_exercises()
        for exercise_id in active_exercises:
            config = self.get_exercise_config(exercise_id)
            goal = self.calculate_goal(exercise_id, selected_date_str)
            
            # Spočítej aktuální hodnotu
            current_value = 0
            if selected_date_str in self.data["workouts"] and exercise_id in self.data["workouts"][selected_date_str]:
                records = self.data["workouts"][selected_date_str][exercise_id]
                if isinstance(records, list):
                    current_value = sum(r["value"] for r in records)
                elif isinstance(records, dict):
                    current_value = records.get("value", 0)
            
            if current_value >= goal:
                status = f"✅ Splněno ({current_value}/{goal})"
                color = "#32c766"
            elif current_value > 0:
                status = f"🔄 Rozpracováno ({current_value}/{goal})"
                color = "#FFD700"
            else:
                status = f"❌ Nesplněno (0/{goal})"
                color = "#ff6b6b"
            
            goal_label = QLabel(f"{config['icon']} {config['name']}: {status}")
            goal_label.setStyleSheet(f"font-size: 13px; padding: 5px; color: {color}; font-weight: bold;")
            goal_label.setObjectName(f"goal_label_{exercise_id}")
            self.add_goals_labels[exercise_id] = goal_label
            goals_layout.addWidget(goal_label)
        
        goals_group.setLayout(goals_layout)
        layout.addWidget(goals_group)
        
        # Přidávání výkonů - dynamické řádky
        add_group = QGroupBox("➕ Zadat výkon")
        add_layout = QVBoxLayout()
        
        # Společné styly
        main_button_style = "font-size: 12px; padding: 8px; min-height: 35px; background-color: #0d7377;"
        quick_button_style = "font-size: 11px; padding: 8px; min-height: 35px; background-color: #2a4d50; color: #b0b0b0;"
        
        # **DYNAMICKY VYTVOŘIT ŘÁDEK PRO KAŽDÉ CVIČENÍ**
        self.exercise_spinboxes = {}  # Uložení SpinBoxů
        
        for exercise_id in active_exercises:
            config = self.get_exercise_config(exercise_id)
            
            exercise_row = QHBoxLayout()
            
            # Label
            label = QLabel(f"{config['icon']} {config['name']}:")
            label.setFixedWidth(80)
            exercise_row.addWidget(label)
            
            # SpinBox
            spinbox = QSpinBox()
            spinbox.setRange(0, 10000)
            spinbox.setValue(0)
            spinbox.setFixedWidth(100)
            exercise_row.addWidget(spinbox)
            self.exercise_spinboxes[exercise_id] = spinbox
            
            # Hlavní tlačítko "Přidat"
            main_btn = QPushButton("Přidat")
            main_btn.setStyleSheet(main_button_style)
            main_btn.setFixedWidth(80)
            main_btn.clicked.connect(lambda checked, ex=exercise_id: self.add_single_workout(ex, self.exercise_spinboxes[ex].value()))
            exercise_row.addWidget(main_btn)
            
            # Rychlá tlačítka
            quick_buttons = config.get("quick_buttons", [10, 20, 30])
            for quick_val in quick_buttons:
                quick_btn = QPushButton(str(quick_val))
                quick_btn.setFixedWidth(50)
                quick_btn.setStyleSheet(quick_button_style)
                quick_btn.clicked.connect(lambda checked, ex=exercise_id, val=quick_val: self.add_single_workout(ex, val))
                exercise_row.addWidget(quick_btn)
            
            exercise_row.addStretch()
            add_layout.addLayout(exercise_row)
        
        add_group.setLayout(add_layout)
        layout.addWidget(add_group)
        
        # Tlačítko pro přidání všeho najednou
        add_all_btn = QPushButton("➕ Přidat všechny výkony najednou")
        add_all_btn.setStyleSheet("font-size: 14px; padding: 12px; background-color: #0d7377;")
        add_all_btn.clicked.connect(self.add_all_workouts)
        layout.addWidget(add_all_btn)
        
        layout.addStretch()
        return widget

    def refresh_add_tab_goals(self):
        """Aktualizuje přehled cílů při změně data"""
        selected_date_str = self.add_date_edit.date().toString("yyyy-MM-dd")
        
        # **OPRAVENO: Dynamicky získat aktivní cvičení**
        for exercise_id in self.get_active_exercises():
            goal = self.calculate_goal(exercise_id, selected_date_str)
            
            current_value = 0
            if selected_date_str in self.data["workouts"] and exercise_id in self.data["workouts"][selected_date_str]:
                records = self.data["workouts"][selected_date_str][exercise_id]
                if isinstance(records, list):
                    current_value = sum(r["value"] for r in records)
                elif isinstance(records, dict):
                    current_value = records.get("value", 0)
            
            if current_value >= goal:
                status = f"✅ Splněno ({current_value}/{goal})"
                color = "#32c766"
            elif current_value > 0:
                status = f"🔄 Rozpracováno ({current_value}/{goal})"
                color = "#FFD700"
            else:
                status = f"❌ Nesplněno (0/{goal})"
                color = "#ff6b6b"
            
            if exercise_id in self.add_goals_labels:
                config = self.get_exercise_config(exercise_id)
                self.add_goals_labels[exercise_id].setText(f"{config['icon']} {config['name']}: {status}")
                self.add_goals_labels[exercise_id].setStyleSheet(f"font-size: 13px; padding: 5px; color: {color}; font-weight: bold;")

    def on_tab_changed(self, index):
        """Refresh při přepnutí záložky"""
        try:
            tab_name = self.tabs.tabText(index)
            
            # **OPRAVENO: Dynamicky najít cvičení podle názvu v záložce**
            for exercise_id in self.get_active_exercises():
                config = self.get_exercise_config(exercise_id)
                if config['icon'] in tab_name and config['name'] in tab_name:
                    self.update_exercise_tab(exercise_id)
                    self.refresh_exercise_calendar(exercise_id)
                    break
        except Exception as e:
            print(f"Chyba při přepnutí záložky: {e}")

    def auto_refresh(self):
        """Automatický refresh aktuální záložky"""
        try:
            current_tab = self.tabs.currentIndex()
            tab_name = self.tabs.tabText(current_tab)
            
            # **OPRAVENO: Dynamicky najít cvičení podle názvu v záložce**
            for exercise_id in self.get_active_exercises():
                config = self.get_exercise_config(exercise_id)
                if config['icon'] in tab_name and config['name'] in tab_name:
                    self.update_exercise_tab(exercise_id)
                    break
        except Exception as e:
            print(f"Chyba při automatické aktualizaci: {e}")

    
    def show_message(self, title, text, icon=QMessageBox.Information):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(icon)
        msg.setStandardButtons(QMessageBox.Ok)
        
        ok_btn = msg.button(QMessageBox.Ok)
        ok_btn.setText("OK")
        
        msg.exec()
    
    def get_available_years(self):
        """Vrátí seznam všech roků"""
        current_year = datetime.now().year
        years = set([current_year])
        
        for date_str in self.data['workouts'].keys():
            year = int(date_str.split('-')[0])
            years.add(year)
        
        if 'year_settings' in self.data:
            for year_str in self.data['year_settings'].keys():
                years.add(int(year_str))
        
        return sorted(years, reverse=True)
    
    def delete_year_data(self, year):
        """Smaže všechna data pro daný rok"""
        msg = QMessageBox(self)
        msg.setWindowTitle("Potvrzení smazání roku")
        msg.setText(f"Opravdu chceš smazat VŠECHNA data pro rok {year}?\n\nTato akce je nevratná!")
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        
        yes_btn = msg.button(QMessageBox.Yes)
        yes_btn.setText("Ano, smazat")
        no_btn = msg.button(QMessageBox.No)
        no_btn.setText("Ne, zrušit")
        
        if msg.exec() == QMessageBox.Yes:
            dates_to_delete = []
            for date_str in self.data['workouts'].keys():
                if int(date_str.split('-')[0]) == year:
                    dates_to_delete.append(date_str)
            
            for date_str in dates_to_delete:
                del self.data['workouts'][date_str]
            
            year_str = str(year)
            if year_str in self.data['year_settings']:
                del self.data['year_settings'][year_str]
            
            self.save_data()
            self.update_all_year_selectors()
            self.tabs.setCurrentIndex(0)
            
            self.show_message("Smazáno", f"Všechna data pro rok {year} byla smazána.")
            
            for exercise in ['kliky', 'dřepy', 'skrčky']:
                self.update_exercise_tab(exercise)
    
    def update_all_year_selectors(self):
        """Aktualizuje všechny year selectory"""
        available_years = self.get_available_years()
        
        for exercise in ['kliky', 'dřepy', 'skrčky']:
            if exercise in self.exercise_year_selectors:
                selector = self.exercise_year_selectors[exercise]
                current_text = selector.currentText()
                
                selector.clear()
                for y in available_years:
                    selector.addItem(str(y))
                
                if current_text and selector.findText(current_text) >= 0:
                    selector.setCurrentText(current_text)
                else:
                    selector.setCurrentText(str(datetime.now().year))
        
        if hasattr(self, 'years_list'):
            current_text = ""
            self.years_list.clear()
            for y in available_years:
                year_workouts = sum(1 for date_str in self.data['workouts'].keys() 
                                  if int(date_str.split('-')[0]) == y)
                item = QListWidgetItem(f"📆 Rok {y} ({year_workouts} dnů s cvičením)")
                item.setData(Qt.UserRole, y)
                self.years_list.addItem(item)
    
    def create_about_tab(self):
        """Vytvoří záložku O aplikaci"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        version_frame = QFrame()
        version_frame.setStyleSheet("""
            QFrame {
                background-color: #2d2d2d;
                border: 2px solid #0d7377;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        version_layout = QVBoxLayout(version_frame)
        
        version_title = QLabel(f"🏋️ Fitness Tracker")
        version_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #14919b;")
        version_layout.addWidget(version_title)
        
        version_info = QLabel(f"Verze: {VERSION} ({VERSION_DATE})")
        version_info.setStyleSheet("font-size: 12px; color: #a0a0a0;")
        version_layout.addWidget(version_info)
        
        version_desc = QLabel("Aplikace pro sledování cvičení s progresivními cíli")
        version_desc.setStyleSheet("font-size: 11px; color: #a0a0a0; font-style: italic;")
        version_layout.addWidget(version_desc)
        
        layout.addWidget(version_frame)
        
        warning_label = QLabel(
            "⚠️ Poznámka: První týden je proporcionální podle počtu dní.\n\n"
            "Například: Start ve čtvrtek 24.10. znamená:\n"
            "  • 24.10. - 27.10. (4 dny) = základní cíl\n"
            "  • 28.10. - 3.11. (první celý týden) = základ + 1× přírůstek\n"
            "  • 4.11. - 10.11. (druhý celý týden) = základ + 2× přírůstek"
        )
        warning_label.setStyleSheet("""
            background-color: #3d2c00;
            color: #ffd700;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #5d4c20;
        """)
        warning_label.setWordWrap(True)
        layout.addWidget(warning_label)
        
        diag_btn = QPushButton("🔍 Zobrazit diagnostiku výpočtu cílů")
        diag_btn.clicked.connect(self.show_diagnostics)
        layout.addWidget(diag_btn)
        
        layout.addStretch()
        
        return widget
    
    def create_settings_tab(self):
        """Záložka s nastavením - nyní i se správou cvičení"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Titulek
        title_label = QLabel("⚙️ Nastavení aplikace")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #14919b; padding: 10px;")
        layout.addWidget(title_label)
        
        # ==================== SEKCE 1: SPRÁVA CVIČENÍ ====================
        exercises_group = QGroupBox("🏋️ Správa cvičení")
        exercises_group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                background-color: #1e1e1e;
                border: 2px solid #0d7377;
                border-radius: 5px;
                padding-top: 18px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 3px 8px;
                color: #14919b;
            }
        """)
        exercises_layout = QVBoxLayout()
        
        # Info text
        exercises_info = QLabel("📝 Přidávej, upravuj nebo mazej typy cvičení")
        exercises_info.setStyleSheet("font-size: 12px; color: #a0a0a0; padding: 5px;")
        exercises_layout.addWidget(exercises_info)
        
        # Seznam cvičení
        self.exercises_list = QListWidget()
        self.exercises_list.setMaximumHeight(150)
        self.exercises_list.setStyleSheet("""
            QListWidget {
                background-color: #2d2d2d;
                border: 1px solid #3d3d3d;
                border-radius: 5px;
            }
            QListWidget::item {
                padding: 8px;
            }
            QListWidget::item:selected {
                background-color: #0d7377;
            }
        """)
        
        # Načti cvičení
        self.refresh_exercises_list()
        exercises_layout.addWidget(self.exercises_list)
        
        # Tlačítka pro správu cvičení
        exercises_buttons = QHBoxLayout()
        
        add_exercise_btn = QPushButton("➕ Přidat cvičení")
        add_exercise_btn.setStyleSheet("padding: 8px; background-color: #0d7377;")
        add_exercise_btn.clicked.connect(self.add_exercise)
        exercises_buttons.addWidget(add_exercise_btn)
        
        edit_exercise_btn = QPushButton("✏️ Upravit cvičení")
        edit_exercise_btn.setStyleSheet("padding: 8px; background-color: #2a4d50;")
        edit_exercise_btn.clicked.connect(self.edit_selected_exercise)
        exercises_buttons.addWidget(edit_exercise_btn)
        
        delete_exercise_btn = QPushButton("🗑️ Smazat cvičení")
        delete_exercise_btn.setStyleSheet("padding: 8px; background-color: #dc3545;")
        delete_exercise_btn.clicked.connect(self.delete_selected_exercise)
        exercises_buttons.addWidget(delete_exercise_btn)
        
        exercises_layout.addLayout(exercises_buttons)
        exercises_group.setLayout(exercises_layout)
        layout.addWidget(exercises_group)
        
        # ==================== SEKCE 2: SPRÁVA ROKŮ ====================
        years_group = QGroupBox("📅 Správa roků")
        years_group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                background-color: #1e1e1e;
                border: 2px solid #0d7377;
                border-radius: 5px;
                padding-top: 18px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 3px 8px;
                color: #14919b;
            }
        """)
        years_layout = QVBoxLayout()
        
        # Seznam roků
        self.years_list = QListWidget()
        self.years_list.setMaximumHeight(150)
        self.years_list.itemClicked.connect(self.on_year_selected_for_settings)  # ← OPRAVENO
        self.years_list.setStyleSheet("""
            QListWidget {
                background-color: #2d2d2d;
                border: 1px solid #3d3d3d;
                border-radius: 5px;
            }
            QListWidget::item {
                padding: 8px;
            }
            QListWidget::item:selected {
                background-color: #0d7377;
            }
        """)

        
        # Načti roky
        for year in self.get_available_years():
            year_workouts = sum(1 for date_str in self.data["workouts"].keys() if int(date_str.split("-")[0]) == year)
            item = QListWidgetItem(f"📅 Rok {year} ({year_workouts} dní s cvičením)")
            item.setData(Qt.UserRole, year)
            self.years_list.addItem(item)
        
        years_layout.addWidget(self.years_list)
        
        # Tlačítka pro správu roků
        years_buttons = QHBoxLayout()
        
        add_year_btn = QPushButton("➕ Přidat rok")
        add_year_btn.clicked.connect(self.add_custom_year)
        years_buttons.addWidget(add_year_btn)
        
        delete_year_btn = QPushButton("🗑️ Smazat rok")
        delete_year_btn.clicked.connect(self.delete_year_from_list)  # ← OPRAVENO
        years_buttons.addWidget(delete_year_btn)
        
        reset_year_btn = QPushButton("🔄 Vynulovat záznamy")
        reset_year_btn.clicked.connect(self.reset_year_workouts)  # ← OPRAVENO
        years_buttons.addWidget(reset_year_btn)

        
        years_layout.addLayout(years_buttons)
        years_group.setLayout(years_layout)
        layout.addWidget(years_group)
        
        # ==================== SEKCE 3: NASTAVENÍ VYBRANÉHO ROKU ====================
        settings_group = QGroupBox("⚙️ Nastavení vybraného roku")
        settings_group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                background-color: #1e1e1e;
                border: 2px solid #0d7377;
                border-radius: 5px;
                padding-top: 18px;
            }
        """)
        settings_layout = QVBoxLayout()
        
        # Grid pro organizaci
        settings_grid = QGridLayout()
        settings_grid.setSpacing(10)
        
        # Startovní datum
        date_label = QLabel("📅 Datum zahájení")
        date_label.setStyleSheet("font-weight: bold; color: #14919b;")
        settings_grid.addWidget(date_label, 0, 0)
        
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDate(QDate.currentDate())
        settings_grid.addWidget(self.start_date_edit, 1, 0)
        
        # Základní cíle
        base_goals_label = QLabel("🎯 Základní cíle (1. týden)")
        base_goals_label.setStyleSheet("font-weight: bold; color: #14919b;")
        settings_grid.addWidget(base_goals_label, 0, 1)
        
        base_goals_widget = QWidget()
        base_goals_layout = QVBoxLayout(base_goals_widget)
        base_goals_layout.setContentsMargins(0, 0, 0, 0)
        self.base_goal_spins = {}
        
        for exercise_id in self.get_active_exercises():
            config = self.get_exercise_config(exercise_id)
            row = QHBoxLayout()
            row.addWidget(QLabel(f"{config['icon']} {config['name']}:"))
            spin = QSpinBox()
            spin.setRange(0, 1000)
            spin.setValue(50)
            self.base_goal_spins[exercise_id] = spin
            row.addWidget(spin)
            base_goals_layout.addLayout(row)
        
        settings_grid.addWidget(base_goals_widget, 1, 1)
        
        # Týdenní přírůstky
        increment_label = QLabel("📈 Týdenní přírůstky")
        increment_label.setStyleSheet("font-weight: bold; color: #14919b;")
        settings_grid.addWidget(increment_label, 0, 2)
        
        increment_widget = QWidget()
        increment_layout = QVBoxLayout(increment_widget)
        increment_layout.setContentsMargins(0, 0, 0, 0)
        self.increment_spins = {}
        
        for exercise_id in self.get_active_exercises():
            config = self.get_exercise_config(exercise_id)
            row = QHBoxLayout()
            row.addWidget(QLabel(f"{config['icon']} {config['name']}:"))
            spin = QSpinBox()
            spin.setRange(0, 100)
            spin.setValue(10)
            self.increment_spins[exercise_id] = spin
            row.addWidget(spin)
            increment_layout.addLayout(row)
        
        settings_grid.addWidget(increment_widget, 1, 2)
        
        settings_layout.addLayout(settings_grid)
        
        # Tlačítko Uložit
        save_settings_btn = QPushButton("💾 Uložit nastavení")
        save_settings_btn.clicked.connect(self.save_settings)  # ← OPRAVENO
        save_settings_btn.setStyleSheet("padding: 10px; font-size: 14px; background-color: #0d7377;")
        settings_layout.addWidget(save_settings_btn)


        
        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)
        
        # ==================== SEKCE 4: EXPORT/IMPORT ====================
        backup_group = QGroupBox("💾 Záloha dat")
        backup_layout = QHBoxLayout()
        
        export_btn = QPushButton("📤 Exportovat data")
        export_btn.clicked.connect(self.export_data)
        backup_layout.addWidget(export_btn)
        
        import_btn = QPushButton("📥 Importovat data")
        import_btn.clicked.connect(self.import_data)
        backup_layout.addWidget(import_btn)
        
        backup_group.setLayout(backup_layout)
        layout.addWidget(backup_group)
        
        layout.addStretch()
        return widget

    def refresh_exercises_list(self):
        """Obnoví seznam cvičení"""
        self.exercises_list.clear()
        
        if "exercises" not in self.data:
            return
        
        # Seřadit podle order
        exercises = sorted(
            self.data["exercises"].items(),
            key=lambda x: x[1].get("order", 999)
        )
        
        for exercise_id, config in exercises:
            status = "✅" if config.get("active", True) else "❌"
            item = QListWidgetItem(f"{status} {config['icon']} {config['name']} (ID: {exercise_id})")
            item.setData(Qt.UserRole, exercise_id)
            self.exercises_list.addItem(item)
    
    
    def edit_selected_exercise(self):
        """Upraví vybrané cvičení"""
        current_item = self.exercises_list.currentItem()
        if not current_item:
            self.show_message("Chyba", "Vyber cvičení k úpravě!", QMessageBox.Warning)
            return
        
        exercise_id = current_item.data(Qt.UserRole)
        self.edit_exercise(exercise_id)
        self.refresh_exercises_list()
    
    
    def delete_selected_exercise(self):
        """Smaže vybrané cvičení"""
        current_item = self.exercises_list.currentItem()
        if not current_item:
            self.show_message("Chyba", "Vyber cvičení ke smazání!", QMessageBox.Warning)
            return
        
        exercise_id = current_item.data(Qt.UserRole)
        self.delete_exercise(exercise_id)
        self.refresh_exercises_list()

    def reset_year_workouts(self):
        """Vynuluje všechny záznamy pro vybraný rok (ponechá nastavení)"""
        selected_items = self.years_list.selectedItems()
        if not selected_items:
            self.show_message("Chyba", "Vyber rok, jehož záznamy chceš vynulovat", QMessageBox.Warning)
            return
        
        year = selected_items[0].data(Qt.UserRole)
        
        msg = QMessageBox(self)
        msg.setWindowTitle("Potvrzení vynulování")
        msg.setText(
            f"Opravdu chceš vynulovat všechny záznamy pro rok {year}?\n\n"
            f"Nastavení roku (datum začátku, cíle, přírůstky) zůstanou zachovány.\n"
            f"Tato akce je nevratná!"
        )
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        
        yes_btn = msg.button(QMessageBox.Yes)
        yes_btn.setText("Ano, vynulovat")
        no_btn = msg.button(QMessageBox.No)
        no_btn.setText("Ne, zrušit")
        
        if msg.exec() == QMessageBox.Yes:
            dates_to_delete = []
            for date_str in self.data['workouts'].keys():
                if int(date_str.split('-')[0]) == year:
                    dates_to_delete.append(date_str)
            
            for date_str in dates_to_delete:
                del self.data['workouts'][date_str]
            
            self.save_data()
            self.update_all_year_selectors()
            
            self.show_message("Vynulováno", f"Všechny záznamy pro rok {year} byly smazány.\nNastavení roku bylo zachováno.")
            
            for exercise in ['kliky', 'dřepy', 'skrčky']:
                self.update_exercise_tab(exercise)
                self.refresh_exercise_calendar(exercise)
            
            # OPRAVA: Refresh cílů v záložce přidat
            self.refresh_add_tab_goals()
            
            # Refresh seznamu roků
            self.years_list.clear()
            for y in self.get_available_years():
                year_workouts = sum(1 for date_str in self.data['workouts'].keys() 
                                  if int(date_str.split('-')[0]) == y)
                item = QListWidgetItem(f"📆 Rok {y} ({year_workouts} dnů s cvičením)")
                item.setData(Qt.UserRole, y)
                self.years_list.addItem(item)

    def load_year_settings_to_ui(self, year):
        """Načte nastavení roku do UI"""
        settings = self.get_year_settings(year)
        
        # Datum
        start_date_str = settings.get("start_date", f"{year}-01-01")
        start_date = QDate.fromString(start_date_str, "yyyy-MM-dd")
        self.start_date_edit.setDate(start_date)
        
        # **DYNAMICKY NAČÍST CÍLE PRO VŠECHNA AKTIVNÍ CVIČENÍ**
        active_exercises = self.get_active_exercises()
        
        for exercise_id in active_exercises:
            # Základní cíl
            if exercise_id in self.base_goal_spins:
                base_goal = settings.get("base_goals", {}).get(exercise_id, 50)
                self.base_goal_spins[exercise_id].setValue(base_goal)
            
            # Týdenní přírůstek
            if exercise_id in self.increment_spins:
                increment = settings.get("weekly_increment", {}).get(exercise_id, 10)
                self.increment_spins[exercise_id].setValue(increment)

    
    def on_year_selected_for_settings(self, item):
        """Načte nastavení zvoleného roku do formuláře"""
        year = item.data(Qt.UserRole)
        if not year:
            return
        
        self.current_settings_year = year
        self.load_year_settings_to_ui(year)

    def save_settings(self):
        """Uloží nastavení pro aktuálně vybraný rok"""
        if not self.current_settings_year:
            self.show_message("Chyba", "Nejdřív vyber rok!", QMessageBox.Warning)
            return
        
        year_str = str(self.current_settings_year)
        
        if year_str not in self.data["year_settings"]:
            self.data["year_settings"][year_str] = {
                "base_goals": {},
                "weekly_increment": {}
            }
        
        # Uložit datum
        start_date_str = self.start_date_edit.date().toString("yyyy-MM-dd")
        self.data["year_settings"][year_str]["start_date"] = start_date_str
        
        # **DYNAMICKY ULOŽIT VŠECHNA AKTIVNÍ CVIČENÍ**
        active_exercises = self.get_active_exercises()
        
        for exercise_id in active_exercises:
            # Základní cíl
            if exercise_id in self.base_goal_spins:
                self.data["year_settings"][year_str]["base_goals"][exercise_id] = self.base_goal_spins[exercise_id].value()
            
            # Týdenní přírůstek
            if exercise_id in self.increment_spins:
                self.data["year_settings"][year_str]["weekly_increment"][exercise_id] = self.increment_spins[exercise_id].value()
        
        self.save_data()
        
        # Refresh všech záložek
        for exercise in active_exercises:
            self.update_exercise_tab(exercise)
            self.refresh_exercise_calendar(exercise)
        
        self.show_message("Uloženo", f"Nastavení pro rok {self.current_settings_year} bylo uloženo!", QMessageBox.Information)

    def add_custom_year(self):
        """Dialog pro přidání libovolného roku - nyní s wizardem"""
        current_year = datetime.now().year
        year, ok = QInputDialog.getInt(
            self,
            "Přidat rok",
            "Zadej rok, který chceš přidat do sledování:",
            current_year + 1,  # Defaultně příští rok
            2000,
            2100,
            1
        )
        
        if ok:
            year_str = str(year)
            
            # Zkontrolovat, zda rok již existuje
            if year_str in self.data["year_settings"]:
                self.show_message(
                    "Informace",
                    f"Rok {year} již existuje v nastavení.",
                    QMessageBox.Information
                )
                return
            
            # Spustit Smart Year Wizard
            wizard = NewYearWizardDialog(year, self)
            
            if wizard.exec():
                # Získat doporučení z wizardu
                recommendations = wizard.get_recommendations()
                
                # Vytvořit year_settings s doporučenými hodnotami
                self.data["year_settings"][year_str] = {
                    "start_date": f"{year}-01-01",
                    "base_goals": {},
                    "weekly_increment": {}
                }
                
                # Aplikovat doporučení pro každé cvičení
                for exercise_id, goals in recommendations.items():
                    self.data["year_settings"][year_str]["base_goals"][exercise_id] = goals["base_goal"]
                    self.data["year_settings"][year_str]["weekly_increment"][exercise_id] = goals["weekly_increment"]
                
                self.save_data()
                self.update_all_year_selectors()
                
                # Automaticky přepnout na nový rok ve všech záložkách
                for exercise in self.get_active_exercises():
                    if exercise in self.exercise_year_selectors:
                        self.exercise_year_selectors[exercise].setCurrentText(str(year))
                
                # Refresh VŠECH záložek, grafů a přehledů
                for exercise in self.get_active_exercises():
                    self.update_exercise_tab(exercise)
                    self.refresh_exercise_calendar(exercise)
                    # Refresh grafu
                    if exercise in self.chart_modes:
                        current_mode = self.chart_modes[exercise]
                        self.update_performance_chart(exercise, current_mode)
                
                # Refresh seznamu roků v nastavení
                self.years_list.clear()
                for y in self.get_available_years():
                    year_workouts = sum(1 for date_str in self.data["workouts"].keys() if int(date_str.split("-")[0]) == y)
                    item = QListWidgetItem(f"📅 Rok {y} ({year_workouts} dní s cvičením)")
                    item.setData(Qt.UserRole, y)
                    self.years_list.addItem(item)
                
                # Načíst nastavení nového roku do UI
                self.load_year_settings_to_ui(year)
                
                # Shrnutí
                summary_text = f"Rok {year} byl vytvořen s těmito cíly:\n\n"
                for exercise_id, goals in recommendations.items():
                    config = self.get_exercise_config(exercise_id)
                    summary_text += f"{config['icon']} {config['name']}:\n"
                    summary_text += f"  • Základní cíl: {goals['base_goal']}\n"
                    summary_text += f"  • Týdenní přírůstek: {goals['weekly_increment']}\n\n"
                
                self.show_message(
                    "🎉 Rok vytvořen!",
                    summary_text,
                    QMessageBox.Information
                )

    
    def delete_year_from_list(self):
        """Smaže vybraný rok ze seznamu"""
        selected_items = self.years_list.selectedItems()
        if not selected_items:
            self.show_message("Chyba", "Vyber rok, který chceš smazat", QMessageBox.Warning)
            return
        
        year = selected_items[0].data(Qt.UserRole)
        self.delete_year_data(year)
        
        self.years_list.clear()
        available_years = self.get_available_years()
        for y in available_years:
            year_workouts = sum(1 for date_str in self.data['workouts'].keys() 
                              if int(date_str.split('-')[0]) == y)
            item = QListWidgetItem(f"📆 Rok {y} ({year_workouts} dnů s cvičením)")
            item.setData(Qt.UserRole, y)
            self.years_list.addItem(item)
        
        if available_years:
            self.load_year_settings_to_ui(available_years[0])
    
    def show_diagnostics(self):
        """Zobrazí diagnostické okno"""
        diag_window = QWidget()
        diag_window.setWindowTitle("Diagnostika výpočtu cílů")
        diag_window.resize(800, 500)
        
        layout = QVBoxLayout(diag_window)
        
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        
        current_year = datetime.now().year
        settings = self.get_year_settings(current_year)
        
        start_date_str = settings['start_date']
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        
        diag_text = f"📊 DIAGNOSTIKA VÝPOČTU CÍLŮ\n{'='*70}\n\n"
        diag_text += f"Verze aplikace: {VERSION}\n"
        diag_text += f"Rok: {current_year}\n"
        diag_text += f"Startovní datum: {start_date_str} ({['Po', 'Út', 'St', 'Čt', 'Pá', 'So', 'Ne'][start_date.weekday()]})\n"
        
        days_to_sunday = 6 - start_date.weekday()
        first_week_end = start_date + timedelta(days=days_to_sunday)
        first_full_week_start = first_week_end + timedelta(days=1)
        
        diag_text += f"Konec prvního (neúplného) týdne: {first_week_end.strftime('%Y-%m-%d')}\n"
        diag_text += f"Začátek prvního celého týdne: {first_full_week_start.strftime('%Y-%m-%d')}\n\n"
        
        for exercise in ['kliky', 'dřepy', 'skrčky']:
            base = settings['base_goals'][exercise]
            increment = settings['weekly_increment'][exercise]
            
            diag_text += f"\n{exercise.upper()}:\n"
            diag_text += f"  Základní cíl: {base}\n"
            diag_text += f"  Týdenní nárůst: {increment}\n\n"
            
            test_dates = [
                start_date_str,
                (start_date + timedelta(days=3)).strftime('%Y-%m-%d'),
                first_week_end.strftime('%Y-%m-%d'),
                first_full_week_start.strftime('%Y-%m-%d'),
                (first_full_week_start + timedelta(days=7)).strftime('%Y-%m-%d'),
                '2025-10-25',
                (datetime(current_year, 12, 31)).strftime('%Y-%m-%d')
            ]
            
            for date_str in test_dates:
                target_date = datetime.strptime(date_str, '%Y-%m-%d')
                goal = self.calculate_goal(exercise, date_str)
                
                if target_date <= first_week_end:
                    diag_text += f"    {date_str}: První týden (základní cíl) = {goal}\n"
                else:
                    days_diff = (target_date - first_full_week_start).days
                    full_weeks = (days_diff // 7) + 1
                    diag_text += f"    {date_str}: {full_weeks} celých týdnů → "
                    diag_text += f"{base} + ({full_weeks} × {increment}) = {goal}\n"
        
        text_edit.setText(diag_text)
        layout.addWidget(text_edit)
        
        close_btn = QPushButton("Zavřít")
        close_btn.clicked.connect(diag_window.close)
        layout.addWidget(close_btn)
        
        diag_window.show()
        self.diag_window = diag_window
        
    def create_performance_chart(self, exercisetype, parent_layout):
        """Vytvoří sekci s grafem výkonu a přepínači zobrazení"""
        chart_group = QGroupBox(f"📊 Graf výkonu - {exercisetype.capitalize()}")
        chart_group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                background-color: #1e1e1e;
                border: 2px solid #0d7377;
                border-radius: 5px;
                padding-top: 18px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 3px 8px;
                color: #14919b;
            }
        """)
        
        chart_layout = QVBoxLayout()
        
        # Přepínače zobrazení
        mode_buttons_layout = QHBoxLayout()
        mode_buttons_layout.addStretch()
        
        weekly_btn = QPushButton("📅 Týden")
        weekly_btn.setCheckable(True)
        weekly_btn.setChecked(True)
        weekly_btn.setFixedWidth(100)
        weekly_btn.setStyleSheet("padding: 8px; font-size: 12px;")
        weekly_btn.clicked.connect(lambda: self.update_performance_chart(exercisetype, "weekly"))
        mode_buttons_layout.addWidget(weekly_btn)
        
        monthly_btn = QPushButton("📆 Měsíc")
        monthly_btn.setCheckable(True)
        monthly_btn.setFixedWidth(100)
        monthly_btn.setStyleSheet("padding: 8px; font-size: 12px;")
        monthly_btn.clicked.connect(lambda: self.update_performance_chart(exercisetype, "monthly"))
        mode_buttons_layout.addWidget(monthly_btn)
        
        yearly_btn = QPushButton("📊 Rok")
        yearly_btn.setCheckable(True)
        yearly_btn.setFixedWidth(100)
        yearly_btn.setStyleSheet("padding: 8px; font-size: 12px;")
        yearly_btn.clicked.connect(lambda: self.update_performance_chart(exercisetype, "yearly"))
        mode_buttons_layout.addWidget(yearly_btn)
        
        mode_buttons_layout.addStretch()
        chart_layout.addLayout(mode_buttons_layout)
        
        # Uložení tlačítek pro toggle
        if not hasattr(self, 'chart_mode_buttons'):
            self.chart_mode_buttons = {}
        self.chart_mode_buttons[exercisetype] = {
            'weekly': weekly_btn,
            'monthly': monthly_btn,
            'yearly': yearly_btn
        }
        
        # Matplotlib figure
        fig = Figure(figsize=(12, 4), facecolor='#1e1e1e')
        canvas = FigureCanvas(fig)
        canvas.setStyleSheet("background-color: #1e1e1e;")
        chart_layout.addWidget(canvas)
        
        # Uložení reference
        if not hasattr(self, 'chart_canvases'):
            self.chart_canvases = {}
        if not hasattr(self, 'chart_figures'):
            self.chart_figures = {}
        if not hasattr(self, 'chart_modes'):
            self.chart_modes = {}
        
        self.chart_canvases[exercisetype] = canvas
        self.chart_figures[exercisetype] = fig
        self.chart_modes[exercisetype] = "weekly"
        
        chart_group.setLayout(chart_layout)
        parent_layout.addWidget(chart_group)
        
        # Iniciální vykreslení
        self.update_performance_chart(exercisetype, "weekly")

    def update_performance_chart(self, exercise_type, mode):
        """Aktualizuje graf výkonu podle zvoleného módu"""
        if exercise_type not in self.chart_figures:
            return
        
        # Update módu a toggle tlačítek
        self.chart_modes[exercise_type] = mode
        if exercise_type in self.chart_mode_buttons:
            for btn_mode, btn in self.chart_mode_buttons[exercise_type].items():
                btn.setChecked(btn_mode == mode)
        
        fig = self.chart_figures[exercise_type]
        fig.clear()
        
        ax = fig.add_subplot(111)
        ax.set_facecolor('#2d2d2d')
        fig.patch.set_facecolor('#1e1e1e')
        
        # Získání dat podle módu
        today = datetime.now().date()
        
        # **OPRAVA: Získat vybraný rok z selektoru**
        if exercise_type in self.exercise_year_selectors:
            selector = self.exercise_year_selectors[exercise_type]
            if selector and selector.currentText():
                selected_year = int(selector.currentText())
            else:
                selected_year = today.year
        else:
            selected_year = today.year
        
        # **OPRAVA: Načíst start_date pro vybraný rok (ne jen aktuální)**
        year_settings = self.get_year_settings(selected_year)
        settings_start_date_str = year_settings.get("start_date", f"{selected_year}-01-01")
        settings_start_date = datetime.strptime(settings_start_date_str, "%Y-%m-%d").date()
        
        if mode == "weekly":
            # **OPRAVA: Pro vybraný rok != aktuální rok, zobraz poslední týden TOHOTO roku**
            if selected_year == today.year:
                end_date = today
                start_date = today - timedelta(days=6)
            else:
                # Pro starší/budoucí rok: zobraz poslední týden roku nebo od start_date
                end_date = datetime(selected_year, 12, 31).date()
                start_date = end_date - timedelta(days=6)
            
            # Respektovat start_date - pokud týden začíná před start_date
            if start_date < settings_start_date:
                start_date = settings_start_date
            
            # Zajistit, že end_date nepřesáhne dnešek
            if end_date > today:
                end_date = today
            
            date_range = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
            title = f"Poslední týden ({start_date.strftime('%d.%m.')} - {end_date.strftime('%d.%m.%Y')})"
            xlabel_format = "%a\n%d.%m"
        
        elif mode == "monthly":
            # **OPRAVA: Pro vybraný rok != aktuální rok, zobraz poslední měsíc TOHOTO roku**
            if selected_year == today.year:
                current_month = today.month
                current_year = today.year
            else:
                # Pro starší/budoucí rok: zobraz prosinec nebo poslední měsíc se záznamy
                current_month = 12
                current_year = selected_year
            
            start_date = datetime(current_year, current_month, 1).date()
            if current_month == 12:
                next_month = datetime(current_year + 1, 1, 1).date()
            else:
                next_month = datetime(current_year, current_month + 1, 1).date()
            end_date = next_month - timedelta(days=1)
            
            # Respektovat start_date
            if start_date < settings_start_date:
                start_date = settings_start_date
            
            # Zajistit, že end_date nepřesáhne dnešek
            if end_date > today:
                end_date = today
            
            date_range = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
            title = f"{start_date.strftime('%B %Y')} (od {start_date.strftime('%d.%m.')})"
            xlabel_format = "%d.%m"
        
        else:  # yearly
            # Pokud je start_date v daném roce, použij ho; jinak 1.1.
            if settings_start_date.year == selected_year:
                start_date = settings_start_date
            else:
                start_date = datetime(selected_year, 1, 1).date()
            
            end_date = datetime(selected_year, 12, 31).date()
            
            # Omezení na dnešek, pokud je selected_year aktuální rok
            if selected_year == today.year and today < end_date:
                end_date = today
            
            date_range = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
            title = f"Celý rok {selected_year} (od {start_date.strftime('%d.%m.')})"
            xlabel_format = "%m/%y"
        
        # Sbírat data
        dates = []
        performed = []
        goals = []
        
        for date in date_range:
            if date > today:  # Nezobrazovat budoucnost
                continue
                
            date_str = date.strftime("%Y-%m-%d")
            dates.append(date)
            
            # Výkon
            perf = 0
            if date_str in self.data["workouts"] and exercise_type in self.data["workouts"][date_str]:
                records = self.data["workouts"][date_str][exercise_type]
                if isinstance(records, list):
                    perf = sum(r["value"] for r in records)
                elif isinstance(records, dict):
                    perf = records.get("value", 0)
            performed.append(perf)
            
            # Cíl
            goal = self.calculate_goal(exercise_type, date_str)
            goals.append(goal if isinstance(goal, int) else 0)
        
        if not dates:
            ax.text(0.5, 0.5, 'Žádná data k zobrazení', 
                    horizontalalignment='center', verticalalignment='center',
                    transform=ax.transAxes, fontsize=14, color='#a0a0a0')
        else:
            # Sloupcový graf pro výkon
            bar_width = 0.8 if mode == "weekly" else 0.6
            bars = ax.bar(dates, performed, width=bar_width, label='Výkon', color='#0d7377', alpha=0.8)
            
            # Čárový graf pro cíle
            ax.plot(dates, goals, label='Cíl', color='#FFD700', linewidth=2, marker='o', markersize=3)
            
            # **Označení začátku cvičení (pokud je v zobrazeném rozsahu)**
            if settings_start_date in dates:
                ax.axvline(x=settings_start_date, color='#32c766', linestyle='--', linewidth=2, alpha=0.7, label='Začátek cvičení')
                
                # Popisek u čáry
                y_max = max(max(performed) if performed else 0, max(goals) if goals else 0)
                if y_max > 0:
                    ax.text(settings_start_date, y_max * 1.05, 
                           f'Start {settings_start_date.strftime("%d.%m.")}',
                           rotation=90, verticalalignment='bottom', horizontalalignment='right',
                           fontsize=9, color='#32c766', weight='bold')
            
            # Styling
            ax.set_title(title, fontsize=14, color='#e0e0e0', pad=10)
            ax.set_xlabel('Datum', fontsize=10, color='#a0a0a0')
            ax.set_ylabel('Počet opakování', fontsize=10, color='#a0a0a0')
            ax.tick_params(colors='#a0a0a0', labelsize=8)
            ax.spines['bottom'].set_color('#3d3d3d')
            ax.spines['top'].set_color('#3d3d3d')
            ax.spines['left'].set_color('#3d3d3d')
            ax.spines['right'].set_color('#3d3d3d')
            ax.grid(True, alpha=0.2, color='#4d4d4d', linestyle='--')
            
            # Formátování X osy
            if mode == "yearly":
                # Pro rok - zobrazit jen některé měsíce
                num_dates = len(dates)
                step = max(1, num_dates // 12)
                ax.set_xticks([dates[i] for i in range(0, num_dates, step)])
                ax.set_xticklabels([dates[i].strftime(xlabel_format) for i in range(0, num_dates, step)], rotation=0)
            else:
                ax.set_xticks(dates)
                ax.set_xticklabels([d.strftime(xlabel_format) for d in dates], rotation=45 if mode == "monthly" else 0)
            
            # Legenda
            legend = ax.legend(loc='upper left', fontsize=9, facecolor='#2d2d2d', edgecolor='#3d3d3d')
            for text in legend.get_texts():
                text.set_color('#e0e0e0')
        
        fig.tight_layout()
        self.chart_canvases[exercise_type].draw()

    
    def create_exercise_tab(self, exercise_type, icon):
        """Vytvoří záložku pro konkrétní cvičení - BEZ přidávání"""
        widget = QWidget()
        main_layout = QHBoxLayout(widget)
        
        # ==================== LEVÝ PANEL ====================
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        # Year selector layout
        year_selector_layout = QHBoxLayout()
        year_selector_layout.addWidget(QLabel(f"📅 Zobrazit rok:"))
        year_selector = QComboBox()
        year_selector.setMinimumWidth(80)  # **NOVĚ: Minimální šířka pro viditelnost roků**
        
        available_years = self.get_available_years()
        if available_years:
            for year in available_years:
                year_selector.addItem(str(year))
            year_selector.setCurrentText(str(datetime.now().year))
        
        year_selector.currentTextChanged.connect(lambda: self.update_exercise_tab_and_calendar(exercise_type))
        self.exercise_year_selectors[exercise_type] = year_selector
        year_selector_layout.addWidget(year_selector)
        year_selector_layout.addStretch()
        left_layout.addLayout(year_selector_layout)
        # Cíle frame (den, týden, měsíc, zbytek roku)
        goals_frame = QFrame()
        goals_frame.setStyleSheet("""
            QFrame {
                background-color: #2d2d2d;
                border: 2px solid #0d7377;
                border-radius: 5px;
            }
        """)
        goals_layout = QVBoxLayout(goals_frame)
        
        # Dnešní sekce
        today_section = QLabel()
        today_section.setObjectName(f"today_section_{exercise_type}")
        today_section.setStyleSheet("font-size: 14px; font-weight: bold; color: #14919b; padding: 5px;")
        today_section.setWordWrap(True)
        goals_layout.addWidget(today_section)
        
        # Týdenní sekce
        week_section = QLabel()
        week_section.setObjectName(f"week_section_{exercise_type}")
        week_section.setStyleSheet("font-size: 12px; color: #FFD700; padding: 5px;")
        week_section.setWordWrap(True)
        goals_layout.addWidget(week_section)
        
        # Měsíční sekce
        month_section = QLabel()
        month_section.setObjectName(f"month_section_{exercise_type}")
        month_section.setStyleSheet("font-size: 12px; color: #90EE90; padding: 5px;")
        month_section.setWordWrap(True)
        goals_layout.addWidget(month_section)
        
        # Roční sekce (zbytek)
        year_rest_section = QLabel()
        year_rest_section.setObjectName(f"year_rest_section_{exercise_type}")
        year_rest_section.setStyleSheet("font-size: 12px; color: #87CEEB; padding: 5px;")
        year_rest_section.setWordWrap(True)
        goals_layout.addWidget(year_rest_section)
        
        # Progress bar
        progress_bar = QProgressBar()
        progress_bar.setObjectName(f"progress_bar_{exercise_type}")
        progress_bar.setTextVisible(True)
        goals_layout.addWidget(progress_bar)
        
        left_layout.addWidget(goals_frame)
        
        # Bulk actions
        bulk_actions_layout = QHBoxLayout()
        delete_selected_btn = QPushButton("🗑️ Smazat vybrané")
        delete_selected_btn.setObjectName(f"delete_selected_{exercise_type}")
        delete_selected_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        delete_selected_btn.clicked.connect(lambda: self.delete_selected_records(exercise_type))
        bulk_actions_layout.addWidget(delete_selected_btn)
        bulk_actions_layout.addStretch()
        left_layout.addLayout(bulk_actions_layout)
        
        # TreeWidget pro záznamy
        tree = QTreeWidget()
        tree.setObjectName(f"tree_{exercise_type}")
        tree.setColumnCount(4)  # Datum, Čas, Výkon, Data (hidden)
        tree.setHeaderLabels(["Datum / Záznam", "Čas / Výkon", "% cíle", "Data"])
        tree.setColumnHidden(3, True)
        
        header = tree.header()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        
        tree.setIndentation(20)
        tree.setContextMenuPolicy(Qt.CustomContextMenu)
        tree.customContextMenuRequested.connect(lambda pos: self.show_tree_context_menu(pos, exercise_type))
        tree.setStyleSheet("""
            QTreeWidget {
                background-color: #1e1e1e;
                border: 1px solid #3d3d3d;
            }
            QTreeWidget::item {
                padding: 5px;
            }
            QTreeWidget::item:selected {
                background-color: #0d7377;
            }
        """)
        
        left_layout.addWidget(tree)
        
        main_layout.addWidget(left_panel, 1)
        
        # ==================== PRAVÁ STRANA (SCROLLOVACÍ OBLAST) ====================
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        # Roční přehled - nadpis
        overview_label = QLabel(f"📊 Roční přehled - {exercise_type.capitalize()}")
        overview_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #14919b; padding: 5px;")
        right_layout.addWidget(overview_label)
        
        # JEDNODUCHÁ LEGENDA - jeden řádek
        legend_layout = QHBoxLayout()
        legend_layout.setSpacing(15)
        legend_layout.setContentsMargins(10, 5, 10, 5)
        
        def add_legend_item(color, text):
            color_box = QLabel()
            color_box.setFixedSize(18, 18)
            color_box.setStyleSheet(f"background-color: {color}; border: 1px solid #3d3d3d;")
            text_label = QLabel(text)
            text_label.setStyleSheet("font-size: 10px; color: #e0e0e0;")
            legend_layout.addWidget(color_box)
            legend_layout.addWidget(text_label)
        
        add_legend_item("#000000", "Před začátkem")
        add_legend_item("#006400", "Velký náskok")
        add_legend_item("#90EE90", "Mírný náskok")
        add_legend_item("#FFD700", "Akorát")
        add_legend_item("#FF6B6B", "Mírný skluz")
        add_legend_item("#8B0000", "Velký skluz")
        legend_layout.addStretch()
        right_layout.addLayout(legend_layout)
        
        # Scrollovací oblast pro kalendář a graf
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: #1e1e1e; }")
        
        scroll_content = QWidget()
        calendar_layout = QVBoxLayout(scroll_content)
        calendar_layout.setContentsMargins(0, 0, 0, 0)
        
        # Kalendář widget
        calendar_widget = QWidget()
        calendar_widget.setStyleSheet("background-color: #1e1e1e;")
        calendar_inner_layout = QVBoxLayout(calendar_widget)
        calendar_inner_layout.setContentsMargins(0, 0, 0, 0)
        self.exercise_calendar_widgets[exercise_type] = calendar_inner_layout
        calendar_layout.addWidget(calendar_widget)
        
        # Statistiky pod kalendářem
        stats_year_label = QLabel()
        stats_year_label.setObjectName(f"stats_year_label_{exercise_type}")
        stats_year_label.setStyleSheet("font-size: 11px; padding: 5px; background-color: #2d2d2d; color: #e0e0e0; border-radius: 5px;")
        calendar_layout.addWidget(stats_year_label)
        
        # ==================== NOVĚ: PŘIDÁNÍ GRAFU POD KALENDÁŘ ====================
        self.create_performance_chart(exercise_type, calendar_layout)
        
        calendar_layout.addStretch()
        
        scroll.setWidget(scroll_content)
        right_layout.addWidget(scroll)
        
        main_layout.addWidget(right_panel, 1)
        
        # Refresh kalendáře a detailního přehledu
        self.update_exercise_tab(exercise_type)
        self.refresh_exercise_calendar(exercise_type)
        
        return widget


    def show_tree_context_menu(self, position, exercise_type):
        """Zobrazí kontextové menu pro tree položky"""
        tree = self.findChild(QTreeWidget, f"tree_{exercise_type}")
        if not tree:
            return
        
        item = tree.itemAt(position)
        if not item:
            return
        
        from PySide6.QtWidgets import QMenu
        from PySide6.QtGui import QAction
        
        menu = QMenu()
        menu.setStyleSheet("""
            QMenu {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #3d3d3d;
            }
            QMenu::item:selected {
                background-color: #0d7377;
            }
        """)
        
        # Zjisti, zda je to parent (den) nebo child (záznam)
        is_parent = item.parent() is None
        
        if is_parent:
            # Menu pro den - pouze smazat
            delete_day_action = QAction("🗑️ Smazat všechny záznamy dne", self)
            delete_day_action.triggered.connect(lambda: self.delete_day_records(exercise_type, item))
            menu.addAction(delete_day_action)
        else:
            # Menu pro záznam - edit a smazat
            edit_action = QAction("✏️ Upravit záznam", self)
            data = item.data(3, Qt.UserRole)
            if data:
                edit_action.triggered.connect(lambda: self.edit_workout(data['exercise'], data['date'], data['record_id']))
            menu.addAction(edit_action)
            
            menu.addSeparator()
            
            delete_action = QAction("🗑️ Smazat záznam", self)
            delete_action.triggered.connect(lambda: self.delete_single_record(exercise_type, item))
            menu.addAction(delete_action)
        
        menu.exec(tree.viewport().mapToGlobal(position))

    def delete_day_records(self, exercise_type, day_item):
        """Smaže všechny záznamy pro daný den"""
        # Získej datum z textu
        date_text = day_item.text(0)
        # Odstranění ikony a získání data
        date_str = date_text.split(' ', 1)[1] if ' ' in date_text else date_text
        
        msg = QMessageBox(self)
        msg.setWindowTitle("Potvrzení smazání")
        msg.setText(f"Opravdu chceš smazat všechny záznamy pro {date_str}?")
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        
        yes_btn = msg.button(QMessageBox.Yes)
        yes_btn.setText("Ano, smazat")
        no_btn = msg.button(QMessageBox.No)
        no_btn.setText("Ne, zrušit")
        
        if msg.exec() == QMessageBox.Yes:
            if date_str in self.data['workouts'] and exercise_type in self.data['workouts'][date_str]:
                del self.data['workouts'][date_str][exercise_type]
                
                if not self.data['workouts'][date_str]:
                    del self.data['workouts'][date_str]
                
                self.save_data()
                self.update_exercise_tab(exercise_type)
                self.refresh_exercise_calendar(exercise_type)
                self.refresh_add_tab_goals()
                
                self.show_message("Smazáno", f"Všechny záznamy pro {date_str} byly smazány")

    def delete_single_record(self, exercise_type, record_item):
        """Smaže jeden záznam"""
        data = record_item.data(3, Qt.UserRole)
        if not data:
            return
        
        date_str = data['date']
        record_id = data['record_id']
        
        msg = QMessageBox(self)
        msg.setWindowTitle("Potvrzení smazání")
        msg.setText(f"Opravdu chceš smazat tento záznam?")
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        
        yes_btn = msg.button(QMessageBox.Yes)
        yes_btn.setText("Ano, smazat")
        no_btn = msg.button(QMessageBox.No)
        no_btn.setText("Ne, zrušit")
        
        if msg.exec() == QMessageBox.Yes:
            if date_str in self.data['workouts'] and exercise_type in self.data['workouts'][date_str]:
                records = self.data['workouts'][date_str][exercise_type]
                
                if isinstance(records, list):
                    self.data['workouts'][date_str][exercise_type] = [r for r in records if r['id'] != record_id]
                    
                    if not self.data['workouts'][date_str][exercise_type]:
                        del self.data['workouts'][date_str][exercise_type]
                    
                    if not self.data['workouts'][date_str]:
                        del self.data['workouts'][date_str]
                
                self.save_data()
                self.update_exercise_tab(exercise_type)
                self.refresh_exercise_calendar(exercise_type)
                self.refresh_add_tab_goals()
                
                self.show_message("Smazáno", "Záznam byl smazán")

    def delete_selected_records(self, exercise_type):
        """Smaže vybrané záznamy"""
        table = self.findChild(QTableWidget, f"table_{exercise_type}")
        if not table:
            return
        
        selected_ids = []
        for row in range(table.rowCount()):
            checkbox_widget = table.cellWidget(row, 0)
            if checkbox_widget:
                checkbox = checkbox_widget.findChild(QCheckBox)
                if checkbox and checkbox.isChecked():
                    record_id = table.item(row, 1).data(Qt.UserRole)
                    date_str = table.item(row, 1).text()
                    selected_ids.append((date_str, record_id))
        
        if not selected_ids:
            self.show_message("Chyba", "Nevybral jsi žádné záznamy!", QMessageBox.Warning)
            return
        
        msg = QMessageBox(self)
        msg.setWindowTitle("Potvrzení smazání")
        msg.setText(f"Opravdu chceš smazat {len(selected_ids)} záznamů?")
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        
        yes_btn = msg.button(QMessageBox.Yes)
        yes_btn.setText("Ano, smazat")
        no_btn = msg.button(QMessageBox.No)
        no_btn.setText("Ne, zrušit")
        
        if msg.exec() == QMessageBox.Yes:
            for date_str, record_id in selected_ids:
                if date_str in self.data['workouts'] and exercise_type in self.data['workouts'][date_str]:
                    records = self.data['workouts'][date_str][exercise_type]
                    if isinstance(records, list):
                        self.data['workouts'][date_str][exercise_type] = [r for r in records if r['id'] != record_id]
                        
                        if not self.data['workouts'][date_str][exercise_type]:
                            del self.data['workouts'][date_str][exercise_type]
                        
                        if not self.data['workouts'][date_str]:
                            del self.data['workouts'][date_str]
            
            self.save_data()
            self.update_exercise_tab(exercise_type)
            self.refresh_exercise_calendar(exercise_type)
            self.refresh_add_tab_goals()
            
            self.show_message("Smazáno", f"{len(selected_ids)} záznamů bylo smazáno")

    def update_exercise_tab_and_calendar(self, exercise_type):
        """Bezpečná aktualizace"""
        try:
            if exercise_type in self.exercise_year_selectors:
                selector = self.exercise_year_selectors[exercise_type]
                if selector and selector.currentText():
                    self.update_exercise_tab(exercise_type)
                    self.refresh_exercise_calendar(exercise_type)
                    
                    # **NOVĚ: Refresh grafu při změně roku**
                    if exercise_type in self.chart_modes:
                        current_mode = self.chart_modes[exercise_type]
                        self.update_performance_chart(exercise_type, current_mode)
        except Exception as e:
            print(f"Chyba při aktualizaci záložky {exercise_type}: {e}")

    def calculate_goal(self, exercise_type, date_str):
        """Vypočítá cíl pro dané datum"""
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            year = date.year
            settings = self.get_year_settings(year)
            
            # **FALLBACK: Pokud klíč neexistuje, zkus s diakritikou**
            if exercise_type not in settings['base_goals']:
                # Zkus starý formát s diakritikou
                old_mapping = {
                    "drepy": "dřepy",
                    "skrcky": "skrčky"
                }
                old_key = old_mapping.get(exercise_type, exercise_type)
                if old_key in settings['base_goals']:
                    exercise_type = old_key
                else:
                    # Pokud stále neexistuje, vrať výchozí
                    return 50
            
            base_goal = settings['base_goals'][exercise_type]
            weekly_increment = settings['weekly_increment'][exercise_type]
            start_date = datetime.strptime(settings['start_date'], "%Y-%m-%d").date()
            
            if date < start_date:
                return 0
            
            days_diff = (date - start_date).days
            
            # První neúplný týden
            first_week_days = 7 - start_date.weekday()
            
            if days_diff < first_week_days:
                return base_goal
            
            # Počet úplných týdnů
            days_after_first_week = days_diff - first_week_days
            full_weeks = days_after_first_week // 7
            
            return base_goal + (full_weeks + 1) * weekly_increment
        
        except Exception as e:
            print(f"Chyba v calculate_goal pro {exercise_type}, {date_str}: {e}")
            return 50

    def get_goal_calculation_text(self, exercise_type, date_str):
        """Vrátí text s vysvětlením výpočtu"""
        target_date = datetime.strptime(date_str, '%Y-%m-%d')
        year = target_date.year
        
        settings = self.get_year_settings(year)
        
        start_date = datetime.strptime(settings['start_date'], '%Y-%m-%d')
        base = settings['base_goals'][exercise_type]
        increment = settings['weekly_increment'][exercise_type]
        
        days_to_sunday = 6 - start_date.weekday()
        first_week_end = start_date + timedelta(days=days_to_sunday)
        
        if target_date <= first_week_end:
            return f"První týden: {base}"
        
        first_full_week_start = first_week_end + timedelta(days=1)
        days_since = (target_date - first_full_week_start).days
        full_weeks = (days_since // 7) + 1
        
        return f"{base} + {full_weeks} týdnů × {increment} = {base + full_weeks * increment}"
    
    def calculate_yearly_goal(self, exercise_type, year):
        """Vypočítá celkový roční cíl"""
        start_date = datetime(year, 1, 1)
        end_date = datetime(year, 12, 31)
        
        total_goal = 0
        current_date = start_date
        
        while current_date <= end_date:
            date_str = current_date.strftime('%Y-%m-%d')
            daily_goal = self.calculate_goal(exercise_type, date_str)
            total_goal += daily_goal
            current_date += timedelta(days=1)
        
        return total_goal
    
    def calculate_yearly_progress(self, exercise_type, year):
        """Vypočítá aktuální progress"""
        total_goal = self.calculate_yearly_goal(exercise_type, year)
        
        total_performed = 0
        for date_str, workouts in self.data['workouts'].items():
            workout_year = int(date_str.split('-')[0])
            if workout_year == year and exercise_type in workouts:
                records = workouts[exercise_type]
                
                if isinstance(records, list):
                    total_performed += sum(r['value'] for r in records)
                elif isinstance(records, dict):
                    total_performed += records.get('value', 0)
        
        today = datetime.now()
        if year == today.year:
            goal_to_date = 0
            start_date = datetime(year, 1, 1)
            current_date = start_date
            
            while current_date <= today:
                date_str = current_date.strftime('%Y-%m-%d')
                daily_goal = self.calculate_goal(exercise_type, date_str)
                goal_to_date += daily_goal
                current_date += timedelta(days=1)
        elif year < today.year:
            goal_to_date = total_goal
        else:
            goal_to_date = 0
        
        return total_performed, total_goal, goal_to_date

    def edit_workout(self, exercise_type, date_str, record_id):
        """Upraví konkrétní záznam"""
        if date_str not in self.data['workouts'] or exercise_type not in self.data['workouts'][date_str]:
            self.show_message("Chyba", "Záznam nenalezen!", QMessageBox.Critical)
            return
        
        records = self.data['workouts'][date_str][exercise_type]
        
        if isinstance(records, list):
            record = next((r for r in records if r['id'] == record_id), None)
        elif isinstance(records, dict) and records.get('id') == record_id:
            record = records
        else:
            record = None
        
        if not record:
            self.show_message("Chyba", "Záznam nenalezen!", QMessageBox.Critical)
            return
        
        old_value = record['value']
        
        new_value, ok = QInputDialog.getInt(
            self,
            "Upravit výkon",
            f"Nový výkon pro {exercise_type} ({date_str}):",
            old_value,
            0,
            10000,  # OPRAVA: Maximum 10000
            1
        )
        
        if ok and new_value != old_value:
            record['value'] = new_value
            record['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            self.save_data()
            self.update_exercise_tab(exercise_type)
            self.refresh_exercise_calendar(exercise_type)
            self.refresh_add_tab_goals()
            
            self.show_message("Upraveno", f"Výkon upraven z {old_value} na {new_value}")

    def update_exercise_tab(self, exercise_type):
        """Aktualizuje statistiky a tree se sbalovacími dny"""
        try:
            if exercise_type not in self.exercise_year_selectors:
                return
            
            selector = self.exercise_year_selectors[exercise_type]
            if not selector or not selector.currentText():
                return
            
            selected_year = int(selector.currentText())
            
            self.update_detailed_overview(exercise_type, selected_year)
            
            tree = self.findChild(QTreeWidget, f"tree_{exercise_type}")
            if tree:
                # NOVÉ: Uložit stav rozbalení
                expanded_dates = set()
                for i in range(tree.topLevelItemCount()):
                    item = tree.topLevelItem(i)
                    if item.isExpanded():
                        date_text = item.text(0)
                        date_str = date_text.split(' ', 1)[1] if ' ' in date_text else date_text
                        expanded_dates.add(date_str)
                
                tree.clear()
                
                days_data = {}
                for date_str in self.data['workouts'].keys():
                    workout_year = int(date_str.split('-')[0])
                    if workout_year == selected_year and exercise_type in self.data['workouts'][date_str]:
                        records = self.data['workouts'][date_str][exercise_type]
                        
                        if date_str not in days_data:
                            days_data[date_str] = []
                        
                        if isinstance(records, list):
                            days_data[date_str].extend(records)
                        elif isinstance(records, dict):
                            days_data[date_str].append(records)
                
                sorted_dates = sorted(days_data.keys(), reverse=True)
                
                for date_str in sorted_dates:
                    records = days_data[date_str]
                    
                    day_item = QTreeWidgetItem(tree)
                    
                    total_day_value = sum(r['value'] for r in records)
                    record_count = len(records)
                    
                    goal = self.calculate_goal(exercise_type, date_str)
                    if not isinstance(goal, int):
                        goal = int(goal) if goal else 0
                    
                    percent = (total_day_value / goal * 100) if goal > 0 else 0
                    
                    if percent >= 100:
                        status_icon = "✅"
                        color = QColor(0, 100, 0)
                    elif percent >= 50:
                        status_icon = "⏳"
                        color = QColor(255, 215, 0)
                    else:
                        status_icon = "❌"
                        color = QColor(255, 0, 0)
                    
                    day_item.setText(0, f"{status_icon} {date_str}")
                    day_item.setText(1, f"{total_day_value} ({record_count}×)")
                    day_item.setText(2, f"{percent:.0f}%")
                    day_item.setForeground(0, QColor(255, 255, 255))
                    day_item.setForeground(1, QColor(200, 200, 200))
                    day_item.setBackground(2, color)
                    day_item.setForeground(2, QColor(255, 255, 255))
                    
                    # NOVÉ: Obnovit stav rozbalení
                    day_item.setExpanded(date_str in expanded_dates)
                    
                    records_sorted = sorted(records, key=lambda x: x.get('timestamp', ''))
                    
                    for record in records_sorted:
                        value = record['value']
                        timestamp = record.get('timestamp', 'N/A')
                        time_only = timestamp.split(' ')[1] if ' ' in timestamp else timestamp
                        record_id = record.get('id', str(uuid.uuid4()))
                        
                        record_item = QTreeWidgetItem(day_item)
                        
                        record_item.setText(0, f"  📝 Záznam")
                        record_item.setText(1, f"{time_only} | {value}")
                        
                        record_percent = (value / goal * 100) if goal > 0 else 0
                        record_item.setText(2, f"{record_percent:.0f}%")
                        
                        if record_percent >= 100:
                            record_item.setBackground(2, QColor(0, 100, 0))
                        elif record_percent >= 75:
                            record_item.setBackground(2, QColor(144, 238, 144))
                        elif record_percent >= 50:
                            record_item.setBackground(2, QColor(255, 215, 0))
                        elif record_percent >= 25:
                            record_item.setBackground(2, QColor(255, 140, 0))
                        else:
                            record_item.setBackground(2, QColor(255, 0, 0))
                        
                        record_item.setForeground(2, QColor(255, 255, 255))
                        
                        record_item.setData(3, Qt.UserRole, {'date': date_str, 'record_id': record_id, 'exercise': exercise_type})
        
        except Exception as e:
            print(f"Chyba při update_exercise_tab pro {exercise_type}: {e}")
            import traceback
            traceback.print_exc()

    def update_detailed_overview(self, exercise_type, selected_year):
        """Aktualizuje detailní přehled: Den, Týden, Měsíc, Zbytek roku (pro aktuální rok) nebo Roční souhrn (pro jiné roky)"""
        try:
            today = datetime.now().date()
            today_str = today.strftime("%Y-%m-%d")
            current_year = today.year
            
            # **NOVĚ: Pro jiný rok než aktuální zobraz ROČNÍ SOUHRN**
            if selected_year != current_year:
                self.show_yearly_summary(exercise_type, selected_year, today)
                return
            
            # **PRO AKTUÁLNÍ ROK: Zobraz normální DNES/TÝDEN/MĚSÍC/ZBYTEK ROKU**
            current_date = today
            current_date_str = today_str
            
            # ====================  DNES ====================
            day_goal = self.calculate_goal(exercise_type, current_date_str)
            day_performed = 0
            
            if current_date_str in self.data["workouts"] and exercise_type in self.data["workouts"][current_date_str]:
                records = self.data["workouts"][current_date_str][exercise_type]
                if isinstance(records, list):
                    day_performed = sum(r["value"] for r in records)
                elif isinstance(records, dict):
                    day_performed = records.get("value", 0)
            
            day_diff = day_performed - day_goal
            day_status = f"(+{day_diff})" if day_diff >= 0 else str(day_diff)
            day_color = "#32c766" if day_diff >= 0 else "#ff6b6b"
            
            today_section = self.findChild(QLabel, f"today_section_{exercise_type}")
            if today_section:
                today_section.setText(f"📅 DNES ({current_date.strftime('%d.%m.%Y')}): {day_performed}/{day_goal} {day_status}")
                today_section.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {day_color}; padding: 5px;")
            
            # ==================== TÝDEN ====================
            week_start = current_date - timedelta(days=current_date.weekday())
            week_end = week_start + timedelta(days=6)
            
            # Respektovat start_date
            settings = self.get_year_settings(selected_year)
            settings_start_date = datetime.strptime(settings.get("start_date", f"{selected_year}-01-01"), "%Y-%m-%d").date()
            if week_start < settings_start_date:
                week_start = settings_start_date
            
            # Nepřekračovat dnešek
            if week_end > today:
                week_end = today
            
            week_goal = 0
            week_performed = 0
            current = week_start
            
            while current <= week_end:
                date_str = current.strftime("%Y-%m-%d")
                goal = self.calculate_goal(exercise_type, date_str)
                if isinstance(goal, int):
                    week_goal += goal
                
                if date_str in self.data["workouts"] and exercise_type in self.data["workouts"][date_str]:
                    records = self.data["workouts"][date_str][exercise_type]
                    if isinstance(records, list):
                        week_performed += sum(r["value"] for r in records)
                    elif isinstance(records, dict):
                        week_performed += records.get("value", 0)
                
                current += timedelta(days=1)
            
            week_diff = week_performed - week_goal
            week_status = f"(+{week_diff})" if week_diff >= 0 else str(week_diff)
            
            week_section = self.findChild(QLabel, f"week_section_{exercise_type}")
            if week_section:
                week_section.setText(f"📆 TÝDEN ({week_start.strftime('%d.%m.')} - {week_end.strftime('%d.%m.')}): {week_performed}/{week_goal} {week_status}")
                week_section.setStyleSheet("font-size: 12px; color: #FFD700; padding: 5px;")
            
            # ==================== MĚSÍC ====================
            month_start = datetime(current_date.year, current_date.month, 1).date()
            if current_date.month == 12:
                next_month = datetime(current_date.year + 1, 1, 1).date()
            else:
                next_month = datetime(current_date.year, current_date.month + 1, 1).date()
            month_end = next_month - timedelta(days=1)
            
            # Respektovat start_date
            if month_start < settings_start_date:
                month_start = settings_start_date
            
            # Nepřekračovat dnešek
            if month_end > today:
                month_end = today
            
            month_goal = 0
            month_performed = 0
            current = month_start
            
            while current <= month_end:
                date_str = current.strftime("%Y-%m-%d")
                goal = self.calculate_goal(exercise_type, date_str)
                if isinstance(goal, int):
                    month_goal += goal
                
                if date_str in self.data["workouts"] and exercise_type in self.data["workouts"][date_str]:
                    records = self.data["workouts"][date_str][exercise_type]
                    if isinstance(records, list):
                        month_performed += sum(r["value"] for r in records)
                    elif isinstance(records, dict):
                        month_performed += records.get("value", 0)
                
                current += timedelta(days=1)
            
            month_diff = month_performed - month_goal
            month_status = f"(+{month_diff})" if month_diff >= 0 else str(month_diff)
            
            month_section = self.findChild(QLabel, f"month_section_{exercise_type}")
            if month_section:
                month_section.setText(f"📊 MĚSÍC ({current_date.strftime('%B %Y')}): {month_performed}/{month_goal} {month_status}")
                month_section.setStyleSheet("font-size: 12px; color: #90EE90; padding: 5px;")
            
            # ==================== ZBYTEK ROKU ====================
            year_end = datetime(selected_year, 12, 31).date()
            tomorrow = current_date + timedelta(days=1)
            rest_start = tomorrow if tomorrow <= year_end else year_end
            
            rest_goal = 0
            current = rest_start
            
            while current <= year_end:
                date_str = current.strftime("%Y-%m-%d")
                goal = self.calculate_goal(exercise_type, date_str)
                if isinstance(goal, int):
                    rest_goal += goal
                current += timedelta(days=1)
            
            days_left = (year_end - current_date).days
            
            year_rest_section = self.findChild(QLabel, f"year_rest_section_{exercise_type}")
            if year_rest_section:
                year_rest_section.setText(f"⏳ ZBYTEK ROKU: {rest_goal} ({days_left} dní do {year_end.strftime('%d.%m.%Y')})")
                year_rest_section.setStyleSheet("font-size: 12px; color: #87CEEB; padding: 5px;")
            
            # ==================== PROGRESS BAR ====================
            total_performed, total_yearly_goal, goal_to_date = self.calculate_yearly_progress(exercise_type, selected_year)
            
            progress_bar = self.findChild(QProgressBar, f"progress_bar_{exercise_type}")
            if progress_bar and goal_to_date > 0:
                percentage = int((total_performed / goal_to_date) * 100)
                
                # **NOVĚ: Povolit hodnoty nad 100% a zobrazit náskok**
                progress_bar.setMaximum(max(100, percentage))  # Dynamické maximum
                progress_bar.setValue(percentage)
                
                # Formát s náskopem/skluzem
                diff = total_performed - goal_to_date
                if diff > 0:
                    progress_bar.setFormat(f"{total_performed}/{goal_to_date} ({percentage}%, +{diff})")
                    # Zelená barva pro náskok
                    progress_bar.setStyleSheet("""
                        QProgressBar {
                            text-align: center;
                            border: 2px solid #0d7377;
                            border-radius: 5px;
                            background-color: #2d2d2d;
                        }
                        QProgressBar::chunk {
                            background-color: #32c766;
                        }
                    """)
                elif diff < 0:
                    progress_bar.setFormat(f"{total_performed}/{goal_to_date} ({percentage}%, {diff})")
                    # Červená barva pro skluz
                    progress_bar.setStyleSheet("""
                        QProgressBar {
                            text-align: center;
                            border: 2px solid #0d7377;
                            border-radius: 5px;
                            background-color: #2d2d2d;
                        }
                        QProgressBar::chunk {
                            background-color: #ff6b6b;
                        }
                    """)
                else:
                    progress_bar.setFormat(f"{total_performed}/{goal_to_date} ({percentage}%)")
                    # Žlutá barva pro přesné splnění
                    progress_bar.setStyleSheet("""
                        QProgressBar {
                            text-align: center;
                            border: 2px solid #0d7377;
                            border-radius: 5px;
                            background-color: #2d2d2d;
                        }
                        QProgressBar::chunk {
                            background-color: #FFD700;
                        }
                    """)
            elif progress_bar:
                progress_bar.setValue(0)
                progress_bar.setFormat("Žádný cíl")
                progress_bar.setStyleSheet("""
                    QProgressBar {
                        text-align: center;
                        border: 2px solid #0d7377;
                        border-radius: 5px;
                        background-color: #2d2d2d;
                    }
                    QProgressBar::chunk {
                        background-color: #3d3d3d;
                    }
                """)
        
        except Exception as e:
            print(f"Chyba v update_detailed_overview pro {exercise_type}: {e}")
            import traceback
            traceback.print_exc()

    
    def show_yearly_summary(self, exercise_type, selected_year, today):
        """Zobrazí roční souhrn pro jiný rok než aktuální"""
        try:
            # Získat nastavení roku
            settings = self.get_year_settings(selected_year)
            settings_start_date = datetime.strptime(settings.get("start_date", f"{selected_year}-01-01"), "%Y-%m-%d").date()
            year_end = datetime(selected_year, 12, 31).date()
            
            # Pro budoucí rok omezit na dnešek
            if year_end > today:
                year_end = today
            
            # Spočítat celkové statistiky
            total_performed = 0
            total_goal = 0
            days_with_workout = 0
            
            current = settings_start_date
            while current <= year_end:
                date_str = current.strftime("%Y-%m-%d")
                
                # Cíl
                goal = self.calculate_goal(exercise_type, date_str)
                if isinstance(goal, int):
                    total_goal += goal
                
                # Výkon
                if date_str in self.data["workouts"] and exercise_type in self.data["workouts"][date_str]:
                    records = self.data["workouts"][date_str][exercise_type]
                    if isinstance(records, list):
                        perf = sum(r["value"] for r in records)
                        if perf > 0:
                            days_with_workout += 1
                        total_performed += perf
                    elif isinstance(records, dict):
                        perf = records.get("value", 0)
                        if perf > 0:
                            days_with_workout += 1
                        total_performed += perf
                
                current += timedelta(days=1)
            
            # Vypočítat průměr
            total_days = (year_end - settings_start_date).days + 1
            avg_per_day = total_performed / total_days if total_days > 0 else 0
            
            # Procento splnění
            percentage = int((total_performed / total_goal) * 100) if total_goal > 0 else 0
            diff = total_performed - total_goal
            diff_status = f"(+{diff})" if diff >= 0 else str(diff)
            diff_color = "#32c766" if diff >= 0 else "#ff6b6b"
            
            # Status podle roku
            if selected_year < today.year:
                year_status = "🏁 UZAVŘENÝ ROK"
                year_color = "#87CEEB"
            elif selected_year > today.year:
                year_status = "🔮 BUDOUCÍ ROK"
                year_color = "#FFD700"
            else:
                year_status = "📊 AKTUÁLNÍ ROK"
                year_color = "#32c766"
            
            # Aktualizovat UI
            today_section = self.findChild(QLabel, f"today_section_{exercise_type}")
            if today_section:
                today_section.setText(f"{year_status} {selected_year}")
                today_section.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {year_color}; padding: 5px;")
            
            week_section = self.findChild(QLabel, f"week_section_{exercise_type}")
            if week_section:
                week_section.setText(f"📈 Celkový výkon: {total_performed}/{total_goal} {diff_status}")
                week_section.setStyleSheet(f"font-size: 12px; color: {diff_color}; padding: 5px;")
            
            month_section = self.findChild(QLabel, f"month_section_{exercise_type}")
            if month_section:
                month_section.setText(f"📅 Dní s cvičením: {days_with_workout} / {total_days} (průměr: {avg_per_day:.1f}/den)")
                month_section.setStyleSheet("font-size: 12px; color: #90EE90; padding: 5px;")
            
            year_rest_section = self.findChild(QLabel, f"year_rest_section_{exercise_type}")
            if year_rest_section:
                year_rest_section.setText(f"✅ Splnění cíle: {percentage}% ({settings_start_date.strftime('%d.%m.')} - {year_end.strftime('%d.%m.%Y')})")
                year_rest_section.setStyleSheet("font-size: 12px; color: #FFD700; padding: 5px;")
            
            # Progress bar
            progress_bar = self.findChild(QProgressBar, f"progress_bar_{exercise_type}")
            if progress_bar:
                # **NOVĚ: Povolit hodnoty nad 100%**
                progress_bar.setMaximum(max(100, percentage))
                progress_bar.setValue(percentage)
                
                # Formát s náskopem/skluzem
                if diff > 0:
                    progress_bar.setFormat(f"{total_performed}/{total_goal} ({percentage}%, +{diff})")
                    progress_bar.setStyleSheet("""
                        QProgressBar {
                            text-align: center;
                            border: 2px solid #0d7377;
                            border-radius: 5px;
                            background-color: #2d2d2d;
                        }
                        QProgressBar::chunk {
                            background-color: #32c766;
                        }
                    """)
                elif diff < 0:
                    progress_bar.setFormat(f"{total_performed}/{total_goal} ({percentage}%, {diff})")
                    progress_bar.setStyleSheet("""
                        QProgressBar {
                            text-align: center;
                            border: 2px solid #0d7377;
                            border-radius: 5px;
                            background-color: #2d2d2d;
                        }
                        QProgressBar::chunk {
                            background-color: #ff6b6b;
                        }
                    """)
                else:
                    progress_bar.setFormat(f"{total_performed}/{total_goal} ({percentage}%)")
                    progress_bar.setStyleSheet("""
                        QProgressBar {
                            text-align: center;
                            border: 2px solid #0d7377;
                            border-radius: 5px;
                            background-color: #2d2d2d;
                        }
                        QProgressBar::chunk {
                            background-color: #FFD700;
                        }
                    """)
        
        except Exception as e:
            print(f"Chyba v show_yearly_summary pro {exercise_type}: {e}")
            import traceback
            traceback.print_exc()


    def refresh_exercise_calendar(self, exercise_type):
        """Vytvoří roční kalendář"""
        try:
            if exercise_type not in self.exercise_calendar_widgets:
                return
            
            calendar_layout = self.exercise_calendar_widgets[exercise_type]
            
            # OPRAVA: Vyčisti všechny children včetně layoutů
            while calendar_layout.count():
                child = calendar_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
                elif child.layout():
                    # Vyčisti vnořený layout
                    while child.layout().count():
                        sub_child = child.layout().takeAt(0)
                        if sub_child.widget():
                            sub_child.widget().deleteLater()
            
            if exercise_type not in self.exercise_year_selectors:
                return
            
            selector = self.exercise_year_selectors[exercise_type]
            if not selector or not selector.currentText():
                return
            
            selected_year = int(selector.currentText())
            
            months = ['Leden', 'Únor', 'Březen', 'Duben', 'Květen', 'Červen',
                      'Červenec', 'Srpen', 'Září', 'Říjen', 'Listopad', 'Prosinec']
            
            months_grid = QGridLayout()
            months_grid.setSpacing(10)
            months_grid.setContentsMargins(5, 5, 5, 5)
            
            for month_num in range(1, 13):
                month_widget = self.create_month_calendar_for_exercise(selected_year, month_num, months[month_num-1], exercise_type)
                row = (month_num - 1) // 4
                col = (month_num - 1) % 4
                months_grid.addWidget(month_widget, row, col)
            
            calendar_layout.addLayout(months_grid)
            calendar_layout.addStretch()
            
            self.update_year_statistics(exercise_type, selected_year)
        except Exception as e:
            print(f"Chyba při refresh_exercise_calendar pro {exercise_type}: {e}")
            import traceback
            traceback.print_exc()

    def create_month_calendar_for_exercise(self, year, month, month_name, exercise_type):
        """Vytvoří kalendář měsíce s GRADIENTNÍMI BARVAMI - VĚTŠÍ"""
        group = QGroupBox(f"{month_name}")
        group.setStyleSheet("""
            QGroupBox { 
                font-size: 16px;
                font-weight: bold;
                background-color: #1e1e1e;
                border: 2px solid #0d7377;
                border-radius: 5px;
                padding-top: 18px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 3px 8px;
                color: #14919b;
            }
        """)
        group.setFixedSize(330, 300)  # OPRAVA: 50% větší (220→330, 200→300)
        
        layout = QGridLayout()
        layout.setSpacing(4)
        layout.setContentsMargins(10, 10, 10, 10)
        
        days = ['Po', 'Út', 'St', 'Čt', 'Pá', 'So', 'Ne']
        for col, day in enumerate(days):
            label = QLabel(day)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("font-weight: bold; padding: 3px; color: #a0a0a0; font-size: 13px;")
            label.setFixedHeight(20)
            layout.addWidget(label, 0, col)
        
        first_day = datetime(year, month, 1)
        first_weekday = first_day.weekday()
        
        if month == 12:
            last_day = datetime(year + 1, 1, 1) - timedelta(days=1)
        else:
            last_day = datetime(year, month + 1, 1) - timedelta(days=1)
        days_in_month = last_day.day
        
        today = datetime.now().date()
        
        settings = self.get_year_settings(year)
        start_date = datetime.strptime(settings['start_date'], '%Y-%m-%d').date()
        
        row = 1
        col = first_weekday
        
        for day in range(1, days_in_month + 1):
            date = datetime(year, month, day)
            date_str = date.strftime('%Y-%m-%d')
            
            day_label = QLabel(str(day))
            day_label.setAlignment(Qt.AlignCenter)
            day_label.setFixedSize(42, 36)  # OPRAVA: 50% větší (28→42, 24→36)
            day_label.setFrameStyle(QFrame.Box)
            
            color, tooltip_text = self.get_day_color_gradient(date_str, date.date(), today, start_date, exercise_type)
            
            border_style = "border: 2px solid #87CEEB;" if date.date() == today else "border: 1px solid #3d3d3d;"
            
            day_label.setStyleSheet(
                f"background-color: {color}; font-weight: bold; color: #ffffff; {border_style} font-size: 16px;"  # OPRAVA: 50% větší font (11→16)
            )
            day_label.setToolTip(tooltip_text)
            
            layout.addWidget(day_label, row, col)
            
            col += 1
            if col > 6:
                col = 0
                row += 1
        
        group.setLayout(layout)
        return group

    def get_day_color_gradient(self, date_str, date, today, start_date, exercise_type):
        """Vrátí gradientní barvu podle výkonu a tooltip"""
        if date < start_date:
            return '#000000', "Před začátkem cvičení"
        
        # OPRAVA: Budoucnost - spočítej skluz
        if date > today:
            goal = self.calculate_goal(exercise_type, date_str)
            
            if not isinstance(goal, int):
                goal = int(goal) if goal else 0
            
            # OPRAVA: Výpočet skluzu do konce roku i pro budoucnost
            year = date.year
            end_of_year = datetime(year, 12, 31).date()
            total_diff = self.calculate_total_difference_to_date(exercise_type, date, end_of_year)
            
            if total_diff > 0:
                total_status = f"\n📊 Celkový náskok k 31.12.: +{total_diff}"
            elif total_diff < 0:
                total_status = f"\n📊 Celkový skluz k 31.12.: {total_diff}"
            else:
                total_status = f"\n📊 Celkový stav k 31.12.: Přesně"
            
            return '#8B0000', f"Budoucí den\nCíl: {goal}{total_status}"
        
        goal = self.calculate_goal(exercise_type, date_str)
        
        if not isinstance(goal, int):
            goal = int(goal) if goal else 0
        
        if date_str in self.data['workouts']:
            workout = self.data['workouts'][date_str]
            if exercise_type in workout:
                records = workout[exercise_type]
                
                if isinstance(records, list):
                    value = sum(r['value'] for r in records)
                    count = len(records)
                elif isinstance(records, dict):
                    value = records.get('value', 0)
                    count = 1
                else:
                    value = 0
                    count = 0
                
                difference = value - goal
                
                if difference >= goal:
                    color = '#006400'
                    status = "Velký náskok"
                elif difference > 0:
                    intensity = min(difference / goal, 1.0) if goal > 0 else 0
                    green_val = int(144 + (100 - 144) * intensity)
                    color = f'#{0:02x}{green_val:02x}{0:02x}'
                    status = f"Náskok +{difference}"
                elif difference == 0:
                    color = '#FFD700'
                    status = "Přesně podle plánu"
                elif difference >= -goal * 0.5:
                    intensity = abs(difference) / (goal * 0.5) if goal > 0 else 0
                    red_val = int(107 + (255 - 107) * (1 - intensity))
                    color = f'#ff{red_val:02x}{red_val:02x}'
                    status = f"Skluz {difference}"
                else:
                    color = '#8B0000'
                    status = f"Velký skluz {difference}"
                
                year = date.year
                end_of_year = datetime(year, 12, 31).date()
                
                total_diff = self.calculate_total_difference_to_date(exercise_type, date, end_of_year)
                
                if total_diff > 0:
                    total_status = f"\n📊 Celkový náskok k 31.12.: +{total_diff}"
                elif total_diff < 0:
                    total_status = f"\n📊 Celkový skluz k 31.12.: {total_diff}"
                else:
                    total_status = f"\n📊 Celkový stav k 31.12.: Přesně"
                
                tooltip = f"{date_str}\nVýkon: {value} ({count}× zápis)\nCíl: {goal}\n{status}{total_status}"
                return color, tooltip
        
        year = date.year
        end_of_year = datetime(year, 12, 31).date()
        total_diff = self.calculate_total_difference_to_date(exercise_type, date, end_of_year)
        
        if total_diff > 0:
            total_status = f"\n📊 Celkový náskok k 31.12.: +{total_diff}"
        elif total_diff < 0:
            total_status = f"\n📊 Celkový skluz k 31.12.: {total_diff}"
        else:
            total_status = f"\n📊 Celkový stav k 31.12.: Přesně"
        
        color = '#FF6B6B'
        tooltip = f"{date_str}\nNecvičil\nCíl: {goal}\nSkluz: -{goal}{total_status}"
        return color, tooltip

    def calculate_total_difference_to_date(self, exercise_type, from_date, to_date):
        """Vypočítá celkový skluz/náskok od daného data do zadaného data"""
        total_performed = 0
        total_goal = 0
        
        today = datetime.now().date()
        
        current_date = from_date
        while current_date <= to_date:
            date_str = current_date.strftime('%Y-%m-%d')
            
            goal = self.calculate_goal(exercise_type, date_str)
            
            # OPRAVA: Ujisti se že goal je int
            if not isinstance(goal, int):
                goal = int(goal) if goal else 0
            
            total_goal += goal
            
            # Výkon pouze do dnešního dne (budoucnost = 0)
            if current_date <= today:
                if date_str in self.data['workouts'] and exercise_type in self.data['workouts'][date_str]:
                    records = self.data['workouts'][date_str][exercise_type]
                    
                    if isinstance(records, list):
                        total_performed += sum(r['value'] for r in records)
                    elif isinstance(records, dict):
                        total_performed += records.get('value', 0)
            
            current_date += timedelta(days=1)
        
        return total_performed - total_goal

    def update_year_statistics(self, exercise_type, selected_year):
        """Aktualizuje statistiky pod kalendářem"""
        try:
            stats_label = self.findChild(QLabel, f"stats_year_label_{exercise_type}")
            if not stats_label:
                return
            
            total_days = 0
            days_met = 0
            days_partial = 0
            days_missed = 0
            
            start_date = datetime(selected_year, 1, 1).date()
            end_date = datetime(selected_year, 12, 31).date()
            today = datetime.now().date()
            
            settings = self.get_year_settings(selected_year)
            settings_start_date = datetime.strptime(settings['start_date'], '%Y-%m-%d').date()
            
            current_date = max(start_date, settings_start_date)
            end_calc_date = min(end_date, today)
            
            while current_date <= end_calc_date:
                date_str = current_date.strftime('%Y-%m-%d')
                goal = self.calculate_goal(exercise_type, date_str)
                
                # OPRAVA: Ujisti se že goal je int
                if not isinstance(goal, int):
                    goal = int(goal) if goal else 0
                
                total_days += 1
                
                if date_str in self.data['workouts'] and exercise_type in self.data['workouts'][date_str]:
                    workout_data = self.data['workouts'][date_str][exercise_type]
                    
                    # OPRAVA: Správné zpracování value
                    if isinstance(workout_data, list):
                        value = sum(r['value'] for r in workout_data)
                    elif isinstance(workout_data, dict):
                        value = workout_data.get('value', 0)
                    else:
                        value = 0
                    
                    if value >= goal:
                        days_met += 1
                    elif value > 0:
                        days_partial += 1
                    else:
                        days_missed += 1
                else:
                    days_missed += 1
                
                current_date += timedelta(days=1)
            
            met_pct = (days_met / total_days * 100) if total_days > 0 else 0
            partial_pct = (days_partial / total_days * 100) if total_days > 0 else 0
            missed_pct = (days_missed / total_days * 100) if total_days > 0 else 0
            
            stats_text = (
                f"📊 Statistiky roku {selected_year} (do {end_calc_date.strftime('%d.%m.')}): "
                f"✅ Splněno: {days_met} ({met_pct:.1f}%) | "
                f"⏳ Částečně: {days_partial} ({partial_pct:.1f}%) | "
                f"❌ Nesplněno: {days_missed} ({missed_pct:.1f}%)"
            )
            
            stats_label.setText(stats_text)
        except Exception as e:
            print(f"Chyba v update_year_statistics pro {exercise_type}: {e}")
            import traceback
            traceback.print_exc()

    def export_data(self):
        """Export celého cvičení do JSON souboru"""
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Exportovat cvičení",
            f"fitness_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            "JSON soubory (*.json)"
        )
        
        if filename:
            try:
                export_data = {
                    'version': VERSION,
                    'export_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'year_settings': self.data['year_settings'],
                    'workouts': self.data['workouts'],
                    'app_state': self.data['app_state']
                }
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, ensure_ascii=False, indent=2)
                
                years = list(self.data['year_settings'].keys())
                total_workouts = len(self.data['workouts'])
                
                self.show_message(
                    "Export úspěšný",
                    f"Cvičení bylo exportováno!\n\n"
                    f"Roky: {', '.join(years)}\n"
                    f"Celkem dnů: {total_workouts}\n"
                    f"Soubor: {Path(filename).name}"
                )
            except Exception as e:
                self.show_message("Chyba", f"Export selhal: {e}", QMessageBox.Critical)

    def import_data(self):
        """Import cvičení z JSON souboru"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Importovat cvičení",
            "",
            "JSON soubory (*.json)"
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    imported_data = json.load(f)
                
                # Ověř strukturu
                if 'year_settings' not in imported_data or 'workouts' not in imported_data:
                    self.show_message("Chyba", "Neplatný formát souboru!", QMessageBox.Critical)
                    return
                
                # Dialog pro výběr režimu
                msg = QMessageBox(self)
                msg.setWindowTitle("Režim importu")
                msg.setText(
                    "Jak chceš importovat data?\n\n"
                    "Sloučit: Přidá nová data k existujícím\n"
                    "Přepsat: Smaže všechna současná data a nahradí je importovanými"
                )
                msg.setIcon(QMessageBox.Question)
                
                merge_btn = msg.addButton("Sloučit", QMessageBox.ActionRole)
                overwrite_btn = msg.addButton("Přepsat", QMessageBox.DestructiveRole)
                cancel_btn = msg.addButton("Zrušit", QMessageBox.RejectRole)
                
                msg.exec()
                
                if msg.clickedButton() == cancel_btn:
                    return
                
                if msg.clickedButton() == overwrite_btn:
                    # Přepsat vše
                    confirm = QMessageBox(self)
                    confirm.setWindowTitle("Potvrzení přepsání")
                    confirm.setText(
                        "VAROVÁNÍ: Všechna současná data budou smazána!\n\n"
                        "Tato akce je nevratná. Pokračovat?"
                    )
                    confirm.setIcon(QMessageBox.Warning)
                    confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                    
                    yes_btn = confirm.button(QMessageBox.Yes)
                    yes_btn.setText("Ano, přepsat")
                    no_btn = confirm.button(QMessageBox.No)
                    no_btn.setText("Ne, zrušit")
                    
                    if confirm.exec() == QMessageBox.Yes:
                        self.data['year_settings'] = imported_data['year_settings']
                        self.data['workouts'] = imported_data['workouts']
                        if 'app_state' in imported_data:
                            self.data['app_state'] = imported_data['app_state']
                        
                        self.save_data()
                        self.update_all_year_selectors()
                        
                        # OPRAVA: Refresh všech záložek místo quit
                        for exercise in ['kliky', 'dřepy', 'skrčky']:
                            self.update_exercise_tab(exercise)
                            self.refresh_exercise_calendar(exercise)
                        
                        self.refresh_add_tab_goals()
                        
                        # Refresh seznamu roků v nastavení
                        self.years_list.clear()
                        for y in self.get_available_years():
                            year_workouts = sum(1 for date_str in self.data['workouts'].keys() 
                                              if int(date_str.split('-')[0]) == y)
                            item = QListWidgetItem(f"📆 Rok {y} ({year_workouts} dnů s cvičením)")
                            item.setData(Qt.UserRole, y)
                            self.years_list.addItem(item)
                        
                        self.show_message(
                            "Import dokončen",
                            "Data byla přepsána importovanými daty.\n\n"
                            "Aplikace byla obnovena s novými daty."
                        )
                        return
                
                elif msg.clickedButton() == merge_btn:
                    # Sloučit
                    merged_years = []
                    merged_workouts = 0
                    
                    # Sloučit year_settings
                    for year, settings in imported_data['year_settings'].items():
                        if year not in self.data['year_settings']:
                            self.data['year_settings'][year] = settings
                            merged_years.append(year)
                    
                    # Sloučit workouts
                    for date_str, workouts in imported_data['workouts'].items():
                        if date_str not in self.data['workouts']:
                            self.data['workouts'][date_str] = workouts
                            merged_workouts += 1
                        else:
                            # Sloučit záznamy pro stejný den
                            for exercise, records in workouts.items():
                                if exercise not in self.data['workouts'][date_str]:
                                    self.data['workouts'][date_str][exercise] = records
                                else:
                                    # Přidej záznamy
                                    if isinstance(records, list):
                                        if isinstance(self.data['workouts'][date_str][exercise], list):
                                            self.data['workouts'][date_str][exercise].extend(records)
                                        else:
                                            self.data['workouts'][date_str][exercise] = [
                                                self.data['workouts'][date_str][exercise],
                                                *records
                                            ]
                    
                    self.save_data()
                    self.update_all_year_selectors()
                    
                    for exercise in ['kliky', 'dřepy', 'skrčky']:
                        self.update_exercise_tab(exercise)
                        self.refresh_exercise_calendar(exercise)
                    
                    self.refresh_add_tab_goals()
                    
                    # Refresh seznamu roků v nastavení
                    self.years_list.clear()
                    for y in self.get_available_years():
                        year_workouts = sum(1 for date_str in self.data['workouts'].keys() 
                                          if int(date_str.split('-')[0]) == y)
                        item = QListWidgetItem(f"📆 Rok {y} ({year_workouts} dnů s cvičením)")
                        item.setData(Qt.UserRole, y)
                        self.years_list.addItem(item)
                    
                    self.show_message(
                        "Import dokončen",
                        f"Data byla sloučena!\n\n"
                        f"Nové roky: {', '.join(merged_years) if merged_years else 'žádné'}\n"
                        f"Nové dny: {merged_workouts}"
                    )
            
            except Exception as e:
                self.show_message("Chyba", f"Import selhal: {e}", QMessageBox.Critical)
                import traceback
                traceback.print_exc()

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_THEME)
    window = FitnessTrackerApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
