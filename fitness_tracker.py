#!/usr/bin/env python3
# -*- coding: utf-8 -*-


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
    QTreeWidget, QTreeWidgetItem, QLineEdit, QTextBrowser, QAbstractItemView, QRadioButton  # ← PŘIDÁNO
)

from PySide6.QtCore import Qt, QDate, QTimer
from PySide6.QtGui import QColor, QAction

# Matplotlib imports
import matplotlib
matplotlib.use('Qt5Agg')
# Matplotlib canvas alias pro volání FigureCanvas(fig)
try:
    from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
except ImportError:
    # fallback pro starší Matplotlib/back-end
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

TITLE = "Fitness Tracker"
VERSION = "3.0.5"
VERSION_DATE = "15.11.2025"

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

class YearCreationModeDialog(QDialog):
    """Dialog pro výběr způsobu vytvoření roku"""
    
    def __init__(self, year, parent=None):
        super().__init__(parent)
        self.year = year
        self.mode = None  # "wizard", "classic", "copy"
        
        self.setWindowTitle(f"Vytvoření roku {year}")
        self.setMinimumWidth(500)
        
        layout = QVBoxLayout(self)
        
        # Titulek
        title = QLabel(f"🎯 Jak chceš vytvořit rok {year}?")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #14919b; padding: 15px;")
        layout.addWidget(title)
        
        # **OPTION 1: Smart Wizard**
        wizard_btn = QPushButton("🧙‍♂️ Smart Year Wizard (Doporučeno)")
        wizard_btn.setMinimumHeight(80)
        wizard_btn.setStyleSheet("""
            QPushButton {
                padding: 15px;
                font-size: 14px;
                text-align: left;
                background-color: #0d7377;
                border: 2px solid #14919b;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #14919b;
            }
        """)
        wizard_desc = QLabel("   💡 Inteligentní průvodce s analýzou historie a personalizovaným doporučením")
        wizard_desc.setStyleSheet("font-size: 11px; color: #a0a0a0; padding-left: 20px;")
        wizard_btn.clicked.connect(lambda: self.select_mode("wizard"))
        layout.addWidget(wizard_btn)
        layout.addWidget(wizard_desc)
        
        layout.addSpacing(10)
        
        # **OPTION 2: Zkopírovat minulý rok**
        copy_btn = QPushButton("📋 Zkopírovat z předchozího roku")
        copy_btn.setMinimumHeight(60)
        copy_btn.setStyleSheet("""
            QPushButton {
                padding: 12px;
                font-size: 13px;
                text-align: left;
                background-color: #2d2d2d;
                border: 2px solid #3d3d3d;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
            }
        """)
        copy_desc = QLabel("   Rychlé vytvoření s nastavením z minulého roku")
        copy_desc.setStyleSheet("font-size: 11px; color: #a0a0a0; padding-left: 20px;")
        copy_btn.clicked.connect(lambda: self.select_mode("copy"))
        layout.addWidget(copy_btn)
        layout.addWidget(copy_desc)
        
        layout.addSpacing(10)
        
        # **OPTION 3: Výchozí nastavení**
        classic_btn = QPushButton("🆕 Výchozí nastavení")
        classic_btn.setMinimumHeight(60)
        classic_btn.setStyleSheet("""
            QPushButton {
                padding: 12px;
                font-size: 13px;
                text-align: left;
                background-color: #2d2d2d;
                border: 2px solid #3d3d3d;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
            }
        """)
        classic_desc = QLabel("   Začít s defaultními cíli (50 kliků, 20 dřepů, 20 skrčků)")
        classic_desc.setStyleSheet("font-size: 11px; color: #a0a0a0; padding-left: 20px;")
        classic_btn.clicked.connect(lambda: self.select_mode("classic"))
        layout.addWidget(classic_btn)
        layout.addWidget(classic_desc)
        
        layout.addSpacing(20)
        
        # Tlačítko Zrušit
        cancel_btn = QPushButton("Zrušit")
        cancel_btn.clicked.connect(self.reject)
        layout.addWidget(cancel_btn)
    
    def select_mode(self, mode):
        """Vybere mód a zavře dialog"""
        self.mode = mode
        self.accept()
    
    def get_mode(self):
        """Vrátí vybraný mód"""
        return self.mode


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
        self.setMinimumSize(700, 750)  # ← OPRAVA: Zvýšeno z 500 na 600
        
        layout = QVBoxLayout(self)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)  # ← ZMĚNA: 100% místo 5
        self.progress_bar.setValue(0)      # ← Začíná na 0%
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
        
    def create_analysis_page(self):
        """Stránka 2: Analýza předchozího roku - vylepšená verze"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("📊 Analýza předchozího roku")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #14919b;")
        layout.addWidget(title)
        
        # Větší textové pole bez max výšky
        self.analysis_text = QTextBrowser()
        self.analysis_text.setReadOnly(True)
        self.analysis_text.setStyleSheet("""
            QTextBrowser {
                background-color: #2d2d2d;
                border: 2px solid #3d3d3d;
                border-radius: 5px;
                font-family: 'Courier New', monospace;
                font-size: 13px;
                padding: 10px;
            }
        """)
        self.analysis_text.setOpenExternalLinks(True)
        layout.addWidget(self.analysis_text)
        
        self.perform_analysis()
        
        return page
    
    def perform_analysis(self):
        """Provede analýzu předchozího roku - vylepšená s barevnými indikacemi"""
        previous_year = self.year - 1
        analysis_html = f"<div style='font-size: 14px;'>"
        analysis_html += f"<h2 style='color: #14919b;'>🔍 Analýza roku {previous_year}</h2><br>"
    
        found_data = False
    
        for exercise_id in self.parent_app.get_active_exercises():
            config = self.parent_app.get_exercise_config(exercise_id)
            analysis = self.calculator.analyze_previous_year(previous_year, exercise_id)
            
            if analysis and analysis["days_count"] > 0:
                found_data = True
                # Najít začátek a konec cvičení
                first_date = None
                last_date = None
    
                for date_str in sorted(self.parent_app.data.get("workouts", {}).keys()):
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
                    if date_obj.year != previous_year:
                        continue
                    if exercise_id in self.parent_app.data["workouts"][date_str]:
                        if not first_date:
                            first_date = date_obj
                        last_date = date_obj
    
                year_start = datetime(previous_year, 1, 1).date()
                year_end = datetime(previous_year, 12, 31).date()
                is_full_year = (first_date and first_date <= datetime(previous_year, 1, 15).date() and 
                                last_date and last_date >= datetime(previous_year, 12, 15).date())
    
                # Barevná indikace
                if is_full_year:
                    status_color = "#32c766"
                    status_icon = "✅"
                    status_text = "Celý rok"
                elif analysis["days_count"] >= 100:
                    status_color = "#FFD700"
                    status_icon = "🟡"
                    status_text = "Částečný rok"
                else:
                    status_color = "#ff6b6b"
                    status_icon = "🔴"
                    status_text = "Málo dat"
    
                analysis_html += f"<div style='border: 2px solid {status_color}; border-radius: 5px; padding: 15px; margin: 10px 0; background-color: #1e1e1e;'>"
                analysis_html += f"<h3 style='color: {status_color}; margin: 0;'>{status_icon} {config['icon']} {config['name']}</h3>"
    
                analysis_html += f"<table style='width: 100%; margin-top: 10px; color: #e0e0e0;'>"
                analysis_html += f"<tr><td style='padding: 5px;'><b>Status:</b></td><td style='color: {status_color};'>{status_text}</td></tr>"
    
                if first_date and last_date:
                    analysis_html += f"<tr><td style='padding: 5px;'><b>Začátek:</b></td><td>{first_date.strftime('%d.%m.%Y')}</td></tr>"
                    analysis_html += f"<tr><td style='padding: 5px;'><b>Konec:</b></td><td>{last_date.strftime('%d.%m.%Y')}</td></tr>"
                    training_days = (last_date - first_date).days
                    analysis_html += f"<tr><td style='padding: 5px;'><b>Délka:</b></td><td>{training_days} dní</td></tr>"
    
                analysis_html += f"<tr><td style='padding: 5px;'><b>Dní s tréninkem:</b></td><td><span style='color: #14919b; font-weight: bold;'>{analysis['days_count']}</span></td></tr>"
                analysis_html += f"<tr><td style='padding: 5px;'><b>Průměr/den:</b></td><td>{analysis['avg_daily']:.1f}</td></tr>"
                analysis_html += f"<tr><td style='padding: 5px;'><b>Průměr (posl. 3 měs.):</b></td><td><span style='color: #32c766; font-weight: bold;'>{analysis['avg_last_3_months']:.1f}</span></td></tr>"
                analysis_html += f"<tr><td style='padding: 5px;'><b>Finální cíl:</b></td><td>{analysis['final_goal']}</td></tr>"
                analysis_html += "</table>"
                analysis_html += "</div>"
    
        if not found_data:
            analysis_html += f"<div style='border: 2px solid #ff6b6b; border-radius: 5px; padding: 20px; margin: 10px 0; background-color: #1e1e1e; text-align: center;'>"
            analysis_html += f"<h3 style='color: #ff6b6b;'>❌ Nenašel jsem dostatek dat z roku {previous_year}</h3>"
            analysis_html += f"<p style='color: #a0a0a0; margin-top: 10px;'>💡 Cíle budou nastaveny podle tvého fitness levelu a preferencí.</p>"
            analysis_html += "</div>"
    
        analysis_html += "</div>"
        self.analysis_text.setHtml(analysis_html)

    
    def create_welcome_page(self):
        """Stránka 1: Uvítání - opravená verze s HTML"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # **TEXTOVÉ POLE S HTML místo QLabel**
        welcome_text = QTextEdit()
        welcome_text.setReadOnly(True)
        welcome_text.setStyleSheet("""
            QTextEdit {
                background-color: #2d2d2d;
                border: 2px solid #0d7377;
                border-radius: 5px;
                padding: 20px;
                font-size: 14px;
            }
        """)
        
        welcome_html = f"""
        <div style='line-height: 1.8;'>
        <h1 style='color: #14919b; text-align: center; margin-bottom: 20px;'>
        🎉 Vytvoření roku {self.year}
        </h1>
        
        <p style='font-size: 15px; margin-bottom: 20px;'>
        Vítej v průvodci vytvořením nového roku!
        </p>
        
        <p style='font-size: 14px; margin-bottom: 25px;'>
        Tento wizard ti pomůže nastavit <b style='color: #32c766;'>optimální cíle</b> pro rok {self.year} 
        na základě tvého fitness levelu, dostupného času a cílů.
        </p>
        
        <div style='background-color: #1e1e1e; border: 2px solid #14919b; border-radius: 5px; padding: 20px; margin: 20px 0;'>
        <h3 style='color: #14919b; margin-top: 0;'>📋 Proces má 5 kroků:</h3>
        
        <table style='width: 100%; border-collapse: collapse;'>
        <tr>
            <td style='padding: 8px; vertical-align: top;'><span style='font-size: 20px;'>1️⃣</span></td>
            <td style='padding: 8px;'><b>Uvítání a přehled</b><br><span style='color: #a0a0a0; font-size: 12px;'>Informace o wizardu</span></td>
        </tr>
        <tr>
            <td style='padding: 8px; vertical-align: top;'><span style='font-size: 20px;'>2️⃣</span></td>
            <td style='padding: 8px;'><b>Analýza předchozího roku</b><br><span style='color: #a0a0a0; font-size: 12px;'>Statistiky a trendy</span></td>
        </tr>
        <tr>
            <td style='padding: 8px; vertical-align: top;'><span style='font-size: 20px;'>3️⃣</span></td>
            <td style='padding: 8px;'><b>Výběr fitness levelu</b><br><span style='color: #a0a0a0; font-size: 12px;'>Začátečník / Intermediate / Pokročilý</span></td>
        </tr>
        <tr>
            <td style='padding: 8px; vertical-align: top;'><span style='font-size: 20px;'>4️⃣</span></td>
            <td style='padding: 8px;'><b>Nastavení preferencí</b><br><span style='color: #a0a0a0; font-size: 12px;'>Dostupný čas a hlavní cíl</span></td>
        </tr>
        <tr>
            <td style='padding: 8px; vertical-align: top;'><span style='font-size: 20px;'>5️⃣</span></td>
            <td style='padding: 8px;'><b>Chytré doporučení a potvrzení</b><br><span style='color: #a0a0a0; font-size: 12px;'>AI-powered výpočet cílů</span></td>
        </tr>
        </table>
        </div>
        
        <div style='background-color: #1e1e1e; border-left: 4px solid #32c766; padding: 15px; margin-top: 20px;'>
        <p style='margin: 0; color: #32c766;'>
        <b>💡 Tip:</b> Průvodce trvá přibližně <b>2-3 minuty</b>. Můžeš kdykoli kliknout na <b>"← Zpět"</b> 
        pro změnu předchozích odpovědí.
        </p>
        </div>
        
        <p style='text-align: center; margin-top: 30px; color: #a0a0a0; font-style: italic;'>
        Klikni na <b>"Další →"</b> pro pokračování
        </p>
        </div>
        """
        
        welcome_text.setHtml(welcome_html)
        layout.addWidget(welcome_text)
        
        return page

    
    def perform_analysis(self):
        """Provede analýzu předchozího roku - vylepšená s barevnými indikacemi"""
        previous_year = self.year - 1
        
        analysis_html = f"<div style='font-size: 14px;'>"
        analysis_html += f"<h2 style='color: #14919b;'>🔍 Analýza roku {previous_year}</h2><br>"
        
        found_data = False
        
        for exercise_id in self.parent_app.get_active_exercises():
            config = self.parent_app.get_exercise_config(exercise_id)
            analysis = self.calculator.analyze_previous_year(previous_year, exercise_id)
            
            if analysis and analysis["days_count"] > 0:
                found_data = True
                
                # **NOVĚ: Najít začátek a konec cvičení**
                first_date = None
                last_date = None
                
                for date_str in sorted(self.parent_app.data.get("workouts", {}).keys()):
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
                    if date_obj.year != previous_year:
                        continue
                    
                    if exercise_id in self.parent_app.data["workouts"][date_str]:
                        if not first_date:
                            first_date = date_obj
                        last_date = date_obj
                
                # **VÝPOČET: Celý rok?**
                year_start = datetime(previous_year, 1, 1).date()
                year_end = datetime(previous_year, 12, 31).date()
                
                is_full_year = (first_date and first_date <= datetime(previous_year, 1, 15).date() and 
                               last_date and last_date >= datetime(previous_year, 12, 15).date())
                
                # **BAREVNÁ INDIKACE**
                if is_full_year:
                    status_color = "#32c766"  # Zelená
                    status_icon = "✅"
                    status_text = "Celý rok"
                elif analysis["days_count"] >= 100:
                    status_color = "#FFD700"  # Žlutá
                    status_icon = "🟡"
                    status_text = "Částečný rok"
                else:
                    status_color = "#ff6b6b"  # Červená
                    status_icon = "🔴"
                    status_text = "Málo dat"
                
                # **FORMÁTOVÁNÍ VÝSTUPU**
                analysis_html += f"<div style='border: 2px solid {status_color}; border-radius: 5px; padding: 15px; margin: 10px 0; background-color: #1e1e1e;'>"
                analysis_html += f"<h3 style='color: {status_color}; margin: 0;'>{status_icon} {config['icon']} {config['name']}</h3>"
                
                analysis_html += f"<table style='width: 100%; margin-top: 10px; color: #e0e0e0;'>"
                analysis_html += f"<tr><td style='padding: 5px;'><b>Status:</b></td><td style='color: {status_color};'>{status_text}</td></tr>"
                
                if first_date and last_date:
                    analysis_html += f"<tr><td style='padding: 5px;'><b>Začátek:</b></td><td>{first_date.strftime('%d.%m.%Y')}</td></tr>"
                    analysis_html += f"<tr><td style='padding: 5px;'><b>Konec:</b></td><td>{last_date.strftime('%d.%m.%Y')}</td></tr>"
                    
                    # Délka tréninku
                    training_days = (last_date - first_date).days
                    analysis_html += f"<tr><td style='padding: 5px;'><b>Délka:</b></td><td>{training_days} dní</td></tr>"
                
                analysis_html += f"<tr><td style='padding: 5px;'><b>Dní s tréninkem:</b></td><td><span style='color: #14919b; font-weight: bold;'>{analysis['days_count']}</span></td></tr>"
                analysis_html += f"<tr><td style='padding: 5px;'><b>Průměr/den:</b></td><td>{analysis['avg_daily']:.1f}</td></tr>"
                analysis_html += f"<tr><td style='padding: 5px;'><b>Průměr (posl. 3 měs.):</b></td><td><span style='color: #32c766; font-weight: bold;'>{analysis['avg_last_3_months']:.1f}</span></td></tr>"
                analysis_html += f"<tr><td style='padding: 5px;'><b>Finální cíl:</b></td><td>{analysis['final_goal']}</td></tr>"
                analysis_html += "</table>"
                
                analysis_html += "</div>"
        
        if not found_data:
            analysis_html += f"<div style='border: 2px solid #ff6b6b; border-radius: 5px; padding: 20px; margin: 10px 0; background-color: #1e1e1e; text-align: center;'>"
            analysis_html += f"<h3 style='color: #ff6b6b;'>❌ Nenašel jsem dostatek dat z roku {previous_year}</h3>"
            analysis_html += f"<p style='color: #a0a0a0; margin-top: 10px;'>💡 Cíle budou nastaveny podle tvého fitness levelu a preferencí.</p>"
            analysis_html += "</div>"
        
        analysis_html += "</div>"
        
        self.analysis_text.setHtml(analysis_html)

    
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
        """Stránka 4: Preference (čás + cíl) - se scrollem"""
        page = QWidget()
        main_layout = QVBoxLayout(page)
        
        title = QLabel("⚙️ Tvoje preference")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #14919b; padding-bottom: 10px;")
        main_layout.addWidget(title)
        
        # **SCROLL AREA**
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; }")
        
        scroll_widget = QWidget()
        layout = QVBoxLayout(scroll_widget)
        
        # **SEKCE 1: ČAS**
        time_group = QGroupBox("⏰ Kolik času můžeš trénovat týdně?")
        time_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                background-color: #1e1e1e;
                border: 2px solid #0d7377;
                border-radius: 5px;
                padding-top: 15px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: #14919b;
            }
        """)
        time_group_layout = QVBoxLayout()
        
        self.time_buttons = QWidget()
        time_layout = QVBoxLayout(self.time_buttons)
        time_layout.setSpacing(8)
        
        for time_id, time_data in SmartGoalCalculator.TIME_AVAILABILITY.items():
            btn = QPushButton(time_data["name"])
            btn.setCheckable(True)
            btn.setMinimumHeight(45)
            btn.setStyleSheet("""
                QPushButton {
                    padding: 12px;
                    font-size: 13px;
                    text-align: left;
                    background-color: #2d2d2d;
                    border: 2px solid #3d3d3d;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #3d3d3d;
                }
                QPushButton:checked {
                    background-color: #0d7377;
                    border: 2px solid #14919b;
                    font-weight: bold;
                }
            """)
            btn.clicked.connect(lambda checked, t=time_id: self.set_time_availability(t))
            
            if time_id == "medium":
                btn.setChecked(True)
            
            time_layout.addWidget(btn)
        
        time_group_layout.addWidget(self.time_buttons)
        time_group.setLayout(time_group_layout)
        layout.addWidget(time_group)
        
        # **SEKCE 2: CÍL**
        goal_group = QGroupBox("🎯 Jaký je tvůj hlavní cíl?")
        goal_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                background-color: #1e1e1e;
                border: 2px solid #0d7377;
                border-radius: 5px;
                padding-top: 15px;
                margin-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: #14919b;
            }
        """)
        goal_group_layout = QVBoxLayout()
        
        self.goal_buttons = QWidget()
        goal_layout = QVBoxLayout(self.goal_buttons)
        goal_layout.setSpacing(8)
        
        for goal_id, goal_data in SmartGoalCalculator.GOAL_TYPES.items():
            btn = QPushButton(goal_data["name"])
            btn.setCheckable(True)
            btn.setMinimumHeight(45)
            btn.setStyleSheet("""
                QPushButton {
                    padding: 12px;
                    font-size: 13px;
                    text-align: left;
                    background-color: #2d2d2d;
                    border: 2px solid #3d3d3d;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #3d3d3d;
                }
                QPushButton:checked {
                    background-color: #0d7377;
                    border: 2px solid #14919b;
                    font-weight: bold;
                }
            """)
            btn.clicked.connect(lambda checked, g=goal_id: self.set_goal_type(g))
            
            if goal_id == "endurance":
                btn.setChecked(True)
            
            goal_layout.addWidget(btn)
        
        goal_group_layout.addWidget(self.goal_buttons)
        goal_group.setLayout(goal_group_layout)
        layout.addWidget(goal_group)
        
        layout.addStretch()
        
        # **Přidání scroll widgetu do scroll area**
        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area)
        
        return page

    def create_summary_page(self):
        """Stránka 5: Souhrn a doporučení - vylepšená verze"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel(f"✅ Tvé nové cíle pro rok {self.year}")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #14919b;")
        layout.addWidget(title)
        
        # **VYLEPŠENÍ: Větší textové pole, využije celou výšku**
        self.summary_text = QTextEdit()
        self.summary_text.setReadOnly(True)
        # Odstraněno: setMaximumHeight
        self.summary_text.setStyleSheet("""
            QTextEdit {
                background-color: #2d2d2d;
                border: 2px solid #0d7377;
                border-radius: 5px;
                font-family: 'Courier New', monospace;
                font-size: 13px;
                padding: 10px;
            }
        """)
        layout.addWidget(self.summary_text)
        
        return page
    
    
    def generate_summary(self):
        """Vygeneruje souhrn doporučení - vylepšená verze"""
        summary_html = f"<div style='font-size: 14px;'>"
        summary_html += f"<h2 style='color: #14919b;'>🎯 Doporučené cíle pro rok {self.year}</h2><br>"
        
        self.recommendations = {}
        
        # **Informace o zvolených parametrech**
        fitness_name = SmartGoalCalculator.FITNESS_LEVELS[self.answers["fitness_level"]]["name"]
        time_name = SmartGoalCalculator.TIME_AVAILABILITY[self.answers["time_availability"]]["name"]
        goal_name = SmartGoalCalculator.GOAL_TYPES[self.answers["goal_type"]]["name"]
        
        summary_html += f"<div style='border: 2px solid #14919b; border-radius: 5px; padding: 15px; margin-bottom: 20px; background-color: #1e1e1e;'>"
        summary_html += f"<h3 style='color: #14919b; margin: 0;'>📋 Tvůj profil</h3>"
        summary_html += f"<table style='width: 100%; margin-top: 10px; color: #e0e0e0;'>"
        summary_html += f"<tr><td style='padding: 5px;'><b>Fitness level:</b></td><td>{fitness_name}</td></tr>"
        summary_html += f"<tr><td style='padding: 5px;'><b>Dostupný čas:</b></td><td>{time_name}</td></tr>"
        summary_html += f"<tr><td style='padding: 5px;'><b>Hlavní cíl:</b></td><td>{goal_name}</td></tr>"
        summary_html += "</table>"
        summary_html += "</div>"
        
        # **Cíle pro každé cvičení**
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
            
            # Vypočti finální cíl
            final_goal = goals['base_goal'] + (52 * goals['weekly_increment'])
            
            # Barevná indikace podle metody
            if goals['method'] == "history_based":
                border_color = "#32c766"
                method_icon = "📊"
                method_text = "Založeno na historii"
            else:
                border_color = "#FFD700"
                method_icon = "⚙️"
                method_text = "Založeno na fitness levelu"
            
            summary_html += f"<div style='border: 2px solid {border_color}; border-radius: 5px; padding: 15px; margin: 10px 0; background-color: #1e1e1e;'>"
            summary_html += f"<h3 style='color: {border_color}; margin: 0;'>{config['icon']} {config['name']}</h3>"
            
            summary_html += f"<table style='width: 100%; margin-top: 10px; color: #e0e0e0;'>"
            summary_html += f"<tr><td style='padding: 5px; width: 50%;'><b>Základní cíl (1. týden):</b></td><td style='color: #32c766; font-weight: bold; font-size: 16px;'>{goals['base_goal']} opakování/den</td></tr>"
            summary_html += f"<tr><td style='padding: 5px;'><b>Týdenní přírůstek:</b></td><td style='color: #FFD700; font-weight: bold;'>+{goals['weekly_increment']} opakování</td></tr>"
            summary_html += f"<tr><td style='padding: 5px;'><b>Finální cíl (52. týden):</b></td><td style='color: #0d7377; font-weight: bold; font-size: 16px;'>{final_goal} opakování/den</td></tr>"
            summary_html += f"<tr><td style='padding: 5px;'><b>Metoda výpočtu:</b></td><td style='color: {border_color};'>{method_icon} {method_text}</td></tr>"
            summary_html += "</table>"
            
            summary_html += "</div>"
        
        summary_html += "<br><div style='text-align: center; color: #a0a0a0; font-style: italic;'>"
        summary_html += "💡 Tyto hodnoty můžeš kdykoliv upravit v Nastavení."
        summary_html += "</div>"
        
        summary_html += "</div>"
        
        self.summary_text.setHtml(summary_html)

    
    def set_fitness_level(self, level):
        """Nastaví fitness level"""
        self.answers["fitness_level"] = level
        # Uncheck všechny tlačítka
        for btn in self.fitness_buttons.findChildren(QPushButton):
            btn.setChecked(False)
        # Najdi a check správné tlačítko
        for btn in self.fitness_buttons.findChildren(QPushButton):
            # Lambda nemá sender(), musíme najít tlačítko jinak
            if btn.isCheckable():
                # Zkontroluj, které tlačítko odpovídá levelu
                if level == "beginner" and "🟢" in btn.text():
                    btn.setChecked(True)
                elif level == "intermediate" and "🟡" in btn.text():
                    btn.setChecked(True)
                elif level == "advanced" and "🔴" in btn.text():
                    btn.setChecked(True)
    
    def set_time_availability(self, time):
        """Nastaví dostupný čas"""
        self.answers["time_availability"] = time
        # Uncheck všechny
        for btn in self.time_buttons.findChildren(QPushButton):
            btn.setChecked(False)
        # Check správné tlačítko
        for btn in self.time_buttons.findChildren(QPushButton):
            if time == "low" and "3×" in btn.text():
                btn.setChecked(True)
            elif time == "medium" and "5×" in btn.text():
                btn.setChecked(True)
            elif time == "high" and "Každý den" in btn.text():
                btn.setChecked(True)
    
    def set_goal_type(self, goal):
        """Nastaví hlavní cíl"""
        self.answers["goal_type"] = goal
        # Uncheck všechny
        for btn in self.goal_buttons.findChildren(QPushButton):
            btn.setChecked(False)
        # Check správné tlačítko
        for btn in self.goal_buttons.findChildren(QPushButton):
            if goal == "muscle" and "🏋️" in btn.text():
                btn.setChecked(True)
            elif goal == "weight_loss" and "🔥" in btn.text():
                btn.setChecked(True)
            elif goal == "endurance" and "💪" in btn.text():
                btn.setChecked(True)

    
    def show_page(self, index):
        """Zobrazí stránku podle indexu"""
        # Skrytí všech stránek
        for page in self.pages:
            page.setVisible(False)
        
        # Zobraz aktuální stránku
        self.stack_layout.addWidget(self.pages[index])
        self.pages[index].setVisible(True)
        
        self.current_page = index
        
        # **OPRAVA: Progress bar 0% → 100%**
        progress_percent = int((index / (len(self.pages) - 1)) * 100) if len(self.pages) > 1 else 0
        self.progress_bar.setValue(progress_percent)
        
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
        # macOS/HiDPI: aby se pohodlně vešly graf + celý kalendář
        self.setMinimumSize(1680, 1000)
        self.resize(1680, 1050)
    
        self.data_file = Path("fitness_data.json")
        self.exercise_year_selectors = {}
        self.exercise_calendar_widgets = {}
        self.current_settings_year = datetime.now().year
    
        self.load_data()
        self.ensure_app_state()
        self.migrate_data()
        self.migrate_to_year_settings()
        self.migrate_to_exercises()
        self.migrate_exercise_keys()  # migrace klíčů (bez zásahu)
    
        self.setup_ui()
        self.restore_app_state()
    
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.auto_refresh)
        self.update_timer.start(5000)

    def backup_data_file(self):
        """Vytvoří časovou zálohu JSON dat před migračními zásahy."""
        try:
            ts = datetime.now().strftime("%Y%m%d-%H%M%S")
            backup_path = self.data_file.with_name(f"{self.data_file.stem}.backup-{ts}.json")
            with open(self.data_file, "rb") as src, open(backup_path, "wb") as dst:
                dst.write(src.read())
            print(f"Záloha dat vytvořena: {backup_path}")
        except Exception as e:
            print(f"Záloha dat selhala: {e}")
            
    def migrate_exercise_start_dates(self):
        """Doplní year_settings[year].exercise_start_dates pro všechna cvičení, pokud chybí.
        Vytvoří zálohu JSON před první změnou.
        """
        changed = False
        # Pro každý rok v year_settings
        for year_str, ys in self.data.get("year_settings", {}).items():
            if not isinstance(ys, dict):
                continue
            ex_map = ys.get("exercise_start_dates")
            if ex_map is None:
                ys["exercise_start_dates"] = {}
                ex_map = ys["exercise_start_dates"]
                changed = True
            # Pro všechna cvičení (i případně neaktivní kvůli historii)
            for ex_id, ex_conf in self.data.get("exercises", {}).items():
                if ex_id in ex_map and ex_map[ex_id]:
                    continue
                # 1) pokud je v exercises.start_dates[year], použij
                sd_map = ex_conf.get("start_dates", {}) if isinstance(ex_conf, dict) else {}
                if isinstance(sd_map, dict) and year_str in sd_map and sd_map[year_str]:
                    ex_map[ex_id] = sd_map[year_str]
                    changed = True
                    continue
                # 2) fallback na year_settings.start_date nebo 1.1.
                fallback = ys.get("start_date", f"{year_str}-01-01")
                ex_map[ex_id] = fallback
                changed = True
        if changed:
            # vytvoř zálohu a ulož
            self.backup_data_file()
            self.save_data()
            print("Migrace: doplněny exercise_start_dates pro roky v year_settings.")
            
    def get_exercise_start_date(self, exercise_id: str, year: int):
        """
        Vrátí startovní datum pro dané cvičení a rok (date).
        Priorita: year_settings[year].exercise_start_dates[exercise] → exercises[exercise].start_dates[year]
                  → year_settings[year].start_date → YYYY-01-01
        """
        try:
            ys = self.get_year_settings(year)
            # 1) Per-exercise v year_settings
            ex_map = ys.get("exercise_start_dates", {})
            if isinstance(ex_map, dict) and exercise_id in ex_map and ex_map[exercise_id]:
                ds = ex_map[exercise_id]
            else:
                # 2) Fallback na definici u daného cvičení
                ex_conf = self.data.get("exercises", {}).get(exercise_id, {})
                sd_map = ex_conf.get("start_dates", {}) if isinstance(ex_conf, dict) else {}
                if isinstance(sd_map, dict) and str(year) in sd_map and sd_map[str(year)]:
                    ds = sd_map[str(year)]
                else:
                    # 3) Fallback na globální start_date v daném roce
                    ds = ys.get("start_date", f"{year}-01-01")
            return datetime.strptime(ds, "%Y-%m-%d").date()
        except Exception:
            # Bezpečný fallback
            return datetime(year, 1, 1).date()

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
    
        # DYNAMICKÉ ZÁLOŽKY PRO CVIČENÍ
        active_exercises = self.get_active_exercises()
        for exercise_id in active_exercises:
            config = self.get_exercise_config(exercise_id)
            tab_label = f"{config['icon']} {config['name']}"
            self.tabs.addTab(self.create_exercise_tab(exercise_id, config['icon']), tab_label)
    
        # Záložka "Nastavení"
        self.tabs.addTab(self.create_settings_tab(), "⚙️ Nastavení")
    
        # Záložka "O aplikaci"
        self.tabs.addTab(self.create_about_tab(), "ℹ️ O aplikaci")
    
        # >>> Přidej nenarušující „Novinky“ do About (nová podzáložka)
        self.inject_about_updates()
        
    def inject_about_updates(self):
        """
        Najde záložku „ℹ️ O aplikaci“, uvnitř QTabWidget s helpem vytvoří NOVOU podzáložku '🆕 Novinky',
        aby změny byly jasně vidět bez zásahu do tvého původního obsahu.
        """
        try:
            if not hasattr(self, "tabs"):
                return
            about_idx = -1
            for i in range(self.tabs.count()):
                if "O aplikaci" in self.tabs.tabText(i):
                    about_idx = i
                    break
            if about_idx < 0:
                return
    
            about_root = self.tabs.widget(about_idx)
            help_tabs = about_root.findChild(QTabWidget)
            if not help_tabs:
                return
    
            # Zabraň duplicitě
            for i in range(help_tabs.count()):
                if "Novinky" in help_tabs.tabText(i):
                    return
    
            news = QWidget()
            v = QVBoxLayout(news)
    
            browser = QTextBrowser()
            browser.setReadOnly(True)
            browser.setStyleSheet("background-color: #2d2d2d; border: none; padding: 15px;")
            browser.setHtml(f"""
            <div style='font-size:13px; line-height:1.6;'>
                <h1 style='color:#14919b;'>🆕 Novinky</h1>
                <ul>
                    <li>📅 <b>Per-cvičení „Datum zahájení“</b> – přehledy, grafy, kalendář i statistiky to plně respektují.</li>
                    <li>⚡ <b>Nastavení se projeví ihned</b> po uložení (grafy/kalendáře/přehledy se přepočítají).</li>
                    <li>🗑️ <b>Smazat vybrané</b> v přehledu opět funguje (smazání z QTreeWidget).</li>
                    <li>📈 <b>Graf</b> se po „Přidat výkon“ automaticky aktualizuje.</li>
                    <li>🪟 <b>Větší okno</b> – komfortní zobrazení celého kalendáře i grafu.</li>
                </ul>
            </div>
            """)
            v.addWidget(browser)
    
            help_tabs.addTab(news, "🆕 Novinky")
        except Exception as e:
            print(f"inject_about_updates() selhalo: {e}")

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
        self.data["workouts"][selected_date_str][exercise_type].append({
            "value": value,
            "timestamp": timestamp,
            "id": str(uuid.uuid4())
        })
    
        self.save_data()
    
        # Aktualizuj všechny záložky
        active_exercises = self.get_active_exercises()
        for exercise in active_exercises:
            self.update_exercise_tab(exercise)
            self.refresh_exercise_calendar(exercise)
            # >>> DOPLNĚNO: hned přegeneruj i graf (zachová aktuální mód)
            mode = self.chart_modes.get(exercise, "weekly") if hasattr(self, "chart_modes") else "weekly"
            self.update_performance_chart(exercise, mode)
    
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
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
        if selected_date_str not in self.data["workouts"]:
            self.data["workouts"][selected_date_str] = {}
    
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
    
        # Aktualizuj všechny záložky + GRAFY
        for exercise in active_exercises:
            self.update_exercise_tab(exercise)
            self.refresh_exercise_calendar(exercise)
            mode = self.chart_modes.get(exercise, "weekly") if hasattr(self, "chart_modes") else "weekly"
            self.update_performance_chart(exercise, mode)
    
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
        """Záložka O aplikaci s kompletním helpm a manuálem"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # **SUB-TABS pro různé sekce helpu**
        help_tabs = QTabWidget()
        
        # ==================== TAB 1: O APLIKACI ====================
        about_widget = QWidget()
        about_layout = QVBoxLayout(about_widget)
        
        # Logo/Titulek
        title = QLabel(f"🏋️ {TITLE}")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #14919b; padding: 20px;")
        title.setAlignment(Qt.AlignCenter)
        about_layout.addWidget(title)
        
        # Verze a datum
        version_info = QLabel(f"<b>Verze:</b> {VERSION}<br><b>Datum:</b> {VERSION_DATE}")
        version_info.setStyleSheet("font-size: 13px; padding: 10px; text-align: center;")
        version_info.setAlignment(Qt.AlignCenter)
        about_layout.addWidget(version_info)
        
        # Popis
        description = QTextBrowser()  # ← ZMĚNA: QTextBrowser místo QTextEdit
        description.setReadOnly(True)
        description.setStyleSheet("background-color: #2d2d2d; border: 1px solid #3d3d3d; border-radius: 5px; padding: 15px;")
        description.setOpenExternalLinks(True)  # ← Nyní funguje!
        
        about_html = f"""
        <div style='font-size: 13px; line-height: 1.6;'>
        <h2 style='color: #14919b;'>📋 O aplikaci</h2>
        <p>
        <b>Fitness Tracker</b> je desktopová aplikace pro sledování pokroku v cvičení 
        s inteligentním doporučením cílů. Umožňuje zaznamenávat denní výkony, 
        sledovat splnění cílů a vizualizovat pokrok v ročním přehledu.
        </p>
        
        <h3 style='color: #32c766;'>✨ Hlavní funkce</h3>
        <ul>
            <li><b>🧙‍♂️ Smart Year Wizard</b> — AI-powered průvodce vytvořením roku</li>
            <li><b>🏋️ Dynamické cvičení</b> — přidávej vlastní typy cvičení</li>
            <li><b>📊 Sledování výkonu</b> — progresivní týdenní cíle</li>
            <li><b>📈 Grafy a vizualizace</b> — týden/měsíc/rok</li>
            <li><b>💾 Správa dat</b> — export/import, migrace</li>
        </ul>
        
        <h3 style='color: #32c766;'>👤 Autor</h3>
        <p>
        <b>Vytvořil:</b> safronus<br>
        <b>Licence:</b> MIT<br>
        <b>GitHub:</b> <a href='https://github.com/safronus/FitnessApp' style='color: #14919b; text-decoration: underline;'>https://github.com/safronus/FitnessApp</a>
        </p>
        
        <p style='margin-top: 20px; color: #a0a0a0; font-style: italic; text-align: center;'>
        💪 Vytvořeno s láskou pro fitness nadšence! 🏋️
        </p>
        </div>
        """
        
        description.setHtml(about_html)
        about_layout.addWidget(description)
        
        help_tabs.addTab(about_widget, "ℹ️ O aplikaci")
        
        # ==================== TAB 2: RYCHLÝ START ====================
        quickstart_widget = QWidget()
        quickstart_layout = QVBoxLayout(quickstart_widget)
        
        quickstart_scroll = QScrollArea()
        quickstart_scroll.setWidgetResizable(True)
        quickstart_scroll.setStyleSheet("QScrollArea { border: none; }")
        
        quickstart_content = QTextBrowser()
        quickstart_content.setReadOnly(True)
        quickstart_content.setStyleSheet("background-color: #2d2d2d; border: none; padding: 15px;")
        
        quickstart_html = """
        <div style='font-size: 13px; line-height: 1.6;'>
        <h1 style='color: #14919b;'>🚀 Rychlý start</h1>
        
        <h2 style='color: #32c766;'>Krok 1: První spuštění</h2>
        <p>
        Po prvním spuštění aplikace se automaticky vytvoří <b>aktuální rok</b> s výchozím nastavením:
        </p>
        <ul>
            <li>💪 Kliky: 50/den, +10/týden</li>
            <li>🦵 Dřepy: 20/den, +5/týden</li>
            <li>🧘 Skrčky: 20/den, +10/týden</li>
        </ul>
        
        <h2 style='color: #32c766;'>Krok 2: Přidání výkonu</h2>
        <ol>
            <li>Jdi do záložky <b>"➕ Přidat výkon"</b></li>
            <li>Vyber datum (defaultně dnes)</li>
            <li>Zadej počet opakování pro jednotlivá cvičení</li>
            <li>Klikni <b>"Přidat"</b> nebo použij rychlá tlačítka</li>
        </ol>
        
        <div style='background-color: #1e1e1e; border: 2px solid #14919b; border-radius: 5px; padding: 15px; margin: 10px 0;'>
        <b>💡 Tip:</b> Můžeš použít <b>rychlá tlačítka</b> (10, 15, 20) pro okamžité přidání výkonu bez psaní!
        </div>
        
        <h2 style='color: #32c766;'>Krok 3: Sledování pokroku</h2>
        <p>
        Přepni na záložku konkrétního cvičení (💪 Kliky, 🦵 Dřepy, 🧘 Skrčky) a sleduj:
        </p>
        <ul>
            <li><b>📊 Přehled DNES/TÝDEN/MĚSÍC</b> — aktuální status</li>
            <li><b>📈 Graf výkonu</b> — vizualizace pokroku</li>
            <li><b>📅 Kalendář</b> — barevný přehled splněných dní</li>
            <li><b>📝 TreeWidget</b> — seznam záznamů s možností editace</li>
        </ul>
        
        <h2 style='color: #32c766;'>Krok 4: Vytvoření nového roku (volitelné)</h2>
        <p>
        Pokud chceš vytvořit nový rok (např. 2026):
        </p>
        <ol>
            <li>Jdi do <b>⚙️ Nastavení</b></li>
            <li>Sekce <b>"Správa roků"</b> → klikni <b>"➕ Přidat rok"</b></li>
            <li>Vyber mód: <b>Smart Wizard</b> / Zkopírovat / Výchozí</li>
            <li>Projdi 5-krokovým průvodcem</li>
            <li>Rok je vytvořen s optimálními cíli!</li>
        </ol>
        
        <div style='background-color: #1e1e1e; border: 2px solid #32c766; border-radius: 5px; padding: 15px; margin: 10px 0;'>
        <b>🎉 Gratulujeme!</b> Nyní máš aplikaci připravenou k používání. Pokračuj do <b>Uživatelského manuálu</b> pro pokročilé funkce.
        </div>
        </div>
        """
        
        quickstart_content.setHtml(quickstart_html)
        quickstart_scroll.setWidget(quickstart_content)
        quickstart_layout.addWidget(quickstart_scroll)
        
        help_tabs.addTab(quickstart_widget, "🚀 Rychlý start")
        
        # ==================== TAB 3: UŽIVATELSKÝ MANUÁL ====================
        manual_widget = QWidget()
        manual_layout = QVBoxLayout(manual_widget)
        
        manual_scroll = QScrollArea()
        manual_scroll.setWidgetResizable(True)
        manual_scroll.setStyleSheet("QScrollArea { border: none; }")
        
        manual_content = QTextBrowser()
        manual_content.setReadOnly(True)
        manual_content.setStyleSheet("background-color: #2d2d2d; border: none; padding: 15px;")
        
        manual_html = """
        <div style='font-size: 13px; line-height: 1.6;'>
        <h1 style='color: #14919b;'>📖 Uživatelský manuál</h1>
        
        <h2 style='color: #32c766;'>1️⃣ Záložka "Přidat výkon"</h2>
        <h3>Základní přidání</h3>
        <ul>
            <li><b>Datum:</b> Vyber datum pro záznam (defaultně dnes)</li>
            <li><b>Cíle:</b> Vidíš přehled dnešních cílů a jejich splnění</li>
            <li><b>Zadání:</b> Zapiš počet opakování a klikni "Přidat"</li>
            <li><b>Rychlá tlačítka:</b> Okamžitě přidej přednastavené hodnoty</li>
        </ul>
        
        <h3>Přidání všech najednou</h3>
        <p>
        Použij tlačítko <b>"➕ Přidat všechny výkony najednou"</b> pro zadání více cvičení současně.
        </p>
        
        <div style='background-color: #1e1e1e; border-left: 4px solid #FFD700; padding: 10px; margin: 10px 0;'>
        <b>⚠️ Poznámka:</b> Záznamy můžeš kdykoli upravit nebo smazat v záložce konkrétního cvičení (TreeWidget).
        </div>
        
        <hr style='border: 1px solid #3d3d3d; margin: 20px 0;'>
        
        <h2 style='color: #32c766;'>2️⃣ Záložky cvičení (Kliky/Dřepy/Skrčky/...)</h2>
        
        <h3>Výběr roku</h3>
        <p>
        Nahoře najdeš <b>📅 Zobrazit rok</b> selector. Přepínej mezi roky pro zobrazení historie.
        </p>
        
        <h3>Sekce přehledů</h3>
        <ul>
            <li><b>DNES:</b> Dnešní výkon vs cíl (zelený = splněno, červený = nesplněno)</li>
            <li><b>TÝDEN:</b> Týdenní souhrn (aktuální týden)</li>
            <li><b>MĚSÍC:</b> Měsíční souhrn (aktuální měsíc)</li>
            <li><b>ZBYTEK ROKU:</b> Zbývající cíl do konce roku (jen pro aktuální rok)</li>
        </ul>
        
        <div style='background-color: #1e1e1e; border-left: 4px solid #32c766; padding: 10px; margin: 10px 0;'>
        <b>💡 Tip:</b> Pro <b>jiné roky</b> se zobrazuje <b>roční souhrn</b> místo denních/týdenních přehledů.
        </div>
        
        <h3>Progress bar</h3>
        <p>
        Progress bar ukazuje splnění cíle <b>k dnešnímu dni</b>:
        </p>
        <ul>
            <li>🟢 <b>Zelený:</b> Náskok (máš více než cíl) → např. 120/100 (+20%)</li>
            <li>🟡 <b>Žlutý:</b> Přesně splněno</li>
            <li>🔴 <b>Červený:</b> Skluz (máš méně než cíl)</li>
        </ul>
        
        <h3>Graf výkonu</h3>
        <p>
        Přepínej mezi třemi módy:
        </p>
        <ul>
            <li><b>📅 Týden:</b> Posledních 7 dní</li>
            <li><b>📅 Měsíc:</b> Posledních 30 dní</li>
            <li><b>📅 Rok:</b> Celý rok s vertikální čárou začátku</li>
        </ul>
        
        <h3>Barevný kalendář</h3>
        <p>
        Kalendář zobrazuje <b>splnění cílů</b> pro každý den:
        </p>
        <ul>
            <li><b style='color: #32c766;'>Zelený:</b> Cíl splněn</li>
            <li><b style='color: #FFD700;'>Žlutý:</b> Částečně splněno (50-99%)</li>
            <li><b style='color: #ff6b6b;'>Červený:</b> Nesplněno</li>
            <li><b style='color: #3d3d3d;'>Šedý:</b> Žádný trénink</li>
        </ul>
        
        <h3>TreeWidget - záznamy</h3>
        <p>
        Seznam všech záznamů s možnostmi:
        </p>
        <ul>
            <li><b>Editace:</b> Dvojklik na hodnotu → uprav počet opakování</li>
            <li><b>Smazání:</b> Pravý klik → "Smazat záznam"</li>
            <li><b>Filtrování:</b> Automaticky podle vybraného roku</li>
        </ul>
        
        <hr style='border: 1px solid #3d3d3d; margin: 20px 0;'>
        
        <h2 style='color: #32c766;'>3️⃣ Záložka "Nastavení"</h2>
        
        <h3>Správa cvičení</h3>
        <p>
        Přidávej, upravuj nebo mazej typy cvičení:
        </p>
        <ul>
            <li><b>➕ Přidat cvičení:</b> Vytvoř vlastní typ (shyby, běh, plank...)</li>
            <li><b>✏️ Upravit cvičení:</b> Změň název, ikonu nebo rychlá tlačítka</li>
            <li><b>🗑️ Smazat cvičení:</b> Odstraň včetně všech dat (nevratné!)</li>
        </ul>
        
        <div style='background-color: #1e1e1e; border-left: 4px solid #ff6b6b; padding: 10px; margin: 10px 0;'>
        <b>⚠️ Varování:</b> Smazání cvičení je <b>nevratné</b>! Všechna data pro toto cvičení budou smazána.
        </div>
        
        <h3>Správa roků</h3>
        <ul>
            <li><b>➕ Přidat rok:</b> Vytvoř nový rok pomocí Smart Wizardu</li>
            <li><b>🗑️ Smazat rok:</b> Odstraň rok včetně nastavení (data zůstanou)</li>
            <li><b>🔄 Vynulovat záznamy:</b> Smaž všechny výkony pro daný rok</li>
        </ul>
        
        <h3>Nastavení vybraného roku</h3>
        <p>
        Klikni na rok v seznamu a uprav:
        </p>
        <ul>
            <li><b>📅 Datum zahájení:</b> Od kdy počítat progresivní cíle</li>
            <li><b>🎯 Základní cíle:</b> Počet opakování v 1. týdnu</li>
            <li><b>📈 Týdenní přírůstky:</b> O kolik se zvyšuje každý týden</li>
        </ul>
        
        <h3>Záloha dat</h3>
        <ul>
            <li><b>📤 Exportovat data:</b> Ulož JSON soubor jako zálohu</li>
            <li><b>📥 Importovat data:</b> Načti zálohu nebo přenést mezi zařízeními</li>
        </ul>
        
        <hr style='border: 1px solid #3d3d3d; margin: 20px 0;'>
        
        <h2 style='color: #32c766;'>4️⃣ Smart Year Wizard (🧙‍♂️)</h2>
        
        <p>
        Inteligentní průvodce vytvořením roku s <b>5 kroky</b>:
        </p>
        
        <h3>Krok 1: Uvítání</h3>
        <p>Přehled procesu a informace o wizardu.</p>
        
        <h3>Krok 2: Analýza předchozího roku</h3>
        <p>
        Wizard analyzuje tvůj minulý rok a zobrazí:
        </p>
        <ul>
            <li>Počet dní s tréninkem</li>
            <li>Průměrný denní výkon</li>
            <li>Průměr posledních 3 měsíců (důležité!)</li>
            <li>Finální cíl minulého roku</li>
            <li>Status: Celý rok / Částečný / Málo dat</li>
        </ul>
        
        <h3>Krok 3: Fitness level</h3>
        <p>Vyber svou úroveň:</p>
        <ul>
            <li>🟢 <b>Začátečník:</b> Pro ty, kdo začínají (multiplier 0.5×)</li>
            <li>🟡 <b>Intermediate:</b> Pravidelný trénink (multiplier 1.0×)</li>
            <li>🔴 <b>Pokročilý:</b> Pokročilá kondice (multiplier 1.5×)</li>
        </ul>
        
        <h3>Krok 4: Preference</h3>
        <p><b>Dostupný čas:</b></p>
        <ul>
            <li>3× týdně (multiplier 0.7×)</li>
            <li>5× týdně (multiplier 1.0×)</li>
            <li>Každý den (multiplier 1.2×)</li>
        </ul>
        
        <p><b>Hlavní cíl:</b></p>
        <ul>
            <li>🔥 Hubnutí (multiplier 1.0×)</li>
            <li>💪 Kondice (multiplier 1.1×)</li>
            <li>🏋️ Svalová hmota (multiplier 1.2×)</li>
        </ul>
        
        <h3>Krok 5: Chytré doporučení</h3>
        <p>
        Wizard vypočítá optimální cíle pomocí <b>AI-powered algoritmu</b>:
        </p>
        
        <div style='background-color: #1e1e1e; border: 2px solid #14919b; border-radius: 5px; padding: 15px; margin: 10px 0;'>
        <h4 style='color: #32c766; margin: 0;'>Historie-based metoda (vysoká spolehlivost)</h4>
        <p>Pokud existují data z minulého roku (min. 30 dní):</p>
        <code style='display: block; background-color: #0d1117; padding: 10px; border-radius: 5px; margin: 5px 0;'>
        base = avg_last_3_months × fitness × time × goal × 0.9<br>
        increment = base × 0.10
        </code>
        </div>
        
        <div style='background-color: #1e1e1e; border: 2px solid #FFD700; border-radius: 5px; padding: 15px; margin: 10px 0;'>
        <h4 style='color: #FFD700; margin: 0;'>Level-based metoda (střední spolehlivost)</h4>
        <p>Pokud neexistují data z minulého roku:</p>
        <code style='display: block; background-color: #0d1117; padding: 10px; border-radius: 5px; margin: 5px 0;'>
        base = default × fitness × time × goal<br>
        increment = base × 0.10
        </code>
        </div>
        
        <p>
        Finální souhrn zobrazí doporučené cíle pro všechna cvičení s projekcí finálního cíle (52. týden).
        </p>
        
        <hr style='border: 1px solid #3d3d3d; margin: 20px 0;'>
        
        <h2 style='color: #32c766;'>5️⃣ Klávesové zkratky</h2>
        <ul>
            <li><b>Tab:</b> Přepíná mezi záložkami</li>
            <li><b>Enter:</b> Potvrzuje dialogy</li>
            <li><b>Esc:</b> Zavírá dialogy</li>
        </ul>
        
        </div>
        """
        
        manual_content.setHtml(manual_html)
        manual_scroll.setWidget(manual_content)
        manual_layout.addWidget(manual_scroll)
        
        help_tabs.addTab(manual_widget, "📖 Manuál")
        
        # ==================== TAB 4: FAQ ====================
        faq_widget = QWidget()
        faq_layout = QVBoxLayout(faq_widget)
        
        faq_scroll = QScrollArea()
        faq_scroll.setWidgetResizable(True)
        faq_scroll.setStyleSheet("QScrollArea { border: none; }")
        
        faq_content = QTextBrowser()
        faq_content.setReadOnly(True)
        faq_content.setStyleSheet("background-color: #2d2d2d; border: none; padding: 15px;")
        
        faq_html = """
        <div style='font-size: 13px; line-height: 1.6;'>
        <h1 style='color: #14919b;'>❓ Často kladené otázky (FAQ)</h1>
        
        <div style='background-color: #1e1e1e; border-left: 4px solid #14919b; padding: 15px; margin: 10px 0;'>
        <h3 style='color: #14919b; margin-top: 0;'>Q: Jak přidat vlastní typ cvičení?</h3>
        <p>
        <b>A:</b> Jdi do <b>⚙️ Nastavení</b> → <b>Správa cvičení</b> → <b>"➕ Přidat cvičení"</b>. 
        Zadej název (např. Shyby), ikonu (🤸), základní cíl (10) a týdenní přírůstek (5). 
        Po restartu aplikace se objeví nová záložka.
        </p>
        </div>
        
        <div style='background-color: #1e1e1e; border-left: 4px solid #14919b; padding: 15px; margin: 10px 0;'>
        <h3 style='color: #14919b; margin-top: 0;'>Q: Můžu upravit cíle pro aktuální rok?</h3>
        <p>
        <b>A:</b> Ano! V <b>Nastavení</b> vyber rok ze seznamu, uprav <b>základní cíle</b> nebo 
        <b>týdenní přírůstky</b> a klikni <b>"💾 Uložit nastavení"</b>. Změny se projeví okamžitě.
        </p>
        </div>
        
        <div style='background-color: #1e1e1e; border-left: 4px solid #14919b; padding: 15px; margin: 10px 0;'>
        <h3 style='color: #14919b; margin-top: 0;'>Q: Jak funguje progress bar nad 100%?</h3>
        <p>
        <b>A:</b> Pokud máš <b>náskok</b> oproti cíli, progress bar se zobrazí <b>zeleně</b> 
        a ukazuje, o kolik jsi před cílem. Např. 120/100 (+20%) znamená, že máš 20% náskok!
        </p>
        </div>
        
        <div style='background-color: #1e1e1e; border-left: 4px solid #14919b; padding: 15px; margin: 10px 0;'>
        <h3 style='color: #14919b; margin-top: 0;'>Q: Co dělat, když jsem přeskočil několik dní?</h3>
        <p>
        <b>A:</b> Žádný problém! Můžeš zpětně přidat výkony pro jakýkoliv minulý den. 
        V záložce <b>"Přidat výkon"</b> vyber datum a zaznamenuj výkon. 
        Všechny přehledy a grafy se automaticky aktualizují.
        </p>
        </div>
        
        <div style='background-color: #1e1e1e; border-left: 4px solid #14919b; padding: 15px; margin: 10px 0;'>
        <h3 style='color: #14919b; margin-top: 0;'>Q: Kde se ukládají data?</h3>
        <p>
        <b>A:</b> Všechna data se ukládají lokálně do souboru <b>fitness_data.json</b> 
        ve stejné složce jako aplikace. Můžeš tento soubor zálohovat nebo přenést mezi zařízeními.
        </p>
        </div>
        
        <div style='background-color: #1e1e1e; border-left: 4px solid #14919b; padding: 15px; margin: 10px 0;'>
        <h3 style='color: #14919b; margin-top: 0;'>Q: Můžu smazat cvičení?</h3>
        <p>
        <b>A:</b> Ano, ale <b>POZOR!</b> Smazání cvičení je <b>nevratné</b> a smaže 
        <b>všechna data</b> (záznamy, cíle) pro toto cvičení. Nejprve exportuj data jako zálohu!
        </p>
        </div>
        
        <div style='background-color: #1e1e1e; border-left: 4px solid #14919b; padding: 15px; margin: 10px 0;'>
        <h3 style='color: #14919b; margin-top: 0;'>Q: Jak funguje Smart Year Wizard?</h3>
        <p>
        <b>A:</b> Wizard analyzuje tvůj minulý rok (pokud existuje) a na základě 
        <b>průměru posledních 3 měsíců</b>, <b>fitness levelu</b>, <b>dostupného času</b> 
        a <b>hlavního cíle</b> vypočítá optimální cíle pro nový rok. Používá 
        <b>progressive overload princip</b> (10% růst/týden) pro bezpečnou progresi.
        </p>
        </div>
        
        <div style='background-color: #1e1e1e; border-left: 4px solid #14919b; padding: 15px; margin: 10px 0;'>
        <h3 style='color: #14919b; margin-top: 0;'>Q: Co znamenají barvy v kalendáři?</h3>
        <p>
        <b>A:</b><br>
        🟢 <b style='color: #32c766;'>Zelený</b> — Cíl splněn (100%+)<br>
        🟡 <b style='color: #FFD700;'>Žlutý</b> — Částečně splněno (50-99%)<br>
        🔴 <b style='color: #ff6b6b;'>Červený</b> — Nesplněno (1-49%)<br>
        ⚫ <b style='color: #3d3d3d;'>Šedý</b> — Žádný trénink (0%)
        </p>
        </div>
        
        <div style='background-color: #1e1e1e; border-left: 4px solid #14919b; padding: 15px; margin: 10px 0;'>
        <h3 style='color: #14919b; margin-top: 0;'>Q: Aplikace nespouští / graf se nezobrazuje</h3>
        <p>
        <b>A:</b> Zkontroluj, že máš nainstalované závislosti:<br>
        <code style='background-color: #0d1117; padding: 5px; border-radius: 3px;'>
        pip install PySide6 matplotlib
        </code><br>
        Pokud problém přetrvává, reinstaluj závislosti:<br>
        <code style='background-color: #0d1117; padding: 5px; border-radius: 3px;'>
        pip install --upgrade --force-reinstall PySide6 matplotlib
        </code>
        </p>
        </div>
        
        </div>
        """
        
        faq_content.setHtml(faq_html)
        faq_scroll.setWidget(faq_content)
        faq_layout.addWidget(faq_scroll)
        
        help_tabs.addTab(faq_widget, "❓ FAQ")
        
        # Přidání sub-tabs do hlavního layoutu
        layout.addWidget(help_tabs)
        
        return widget

    def create_settings_tab(self):
        """Záložka s nastavením – per-cvičení startovní data, cíle, přírůstky, správa let + Export/Import."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
    
        # Titulek
        title_label = QLabel("⚙️ Nastavení aplikace")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #14919b; padding: 10px;")
        layout.addWidget(title_label)
    
        # ==================== SPRÁVA CVIČENÍ ====================
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
        """)
        exercises_layout = QVBoxLayout()
        self.exercises_list = QListWidget()
        exercises_layout.addWidget(self.exercises_list)
    
        ex_buttons = QHBoxLayout()
        btn_add = QPushButton("➕ Přidat cvičení")
        btn_add.setObjectName("btn_add_exercise")
        btn_add.clicked.connect(self.add_exercise)
        ex_buttons.addWidget(btn_add)
    
        btn_edit = QPushButton("✏️ Upravit cvičení")
        btn_edit.setObjectName("btn_edit_exercise")
        btn_edit.clicked.connect(self.edit_selected_exercise)
        ex_buttons.addWidget(btn_edit)
    
        btn_del = QPushButton("🗑️ Smazat cvičení")
        btn_del.setObjectName("btn_delete_exercise")
        btn_del.clicked.connect(self.delete_selected_exercise)
        ex_buttons.addWidget(btn_del)
    
        exercises_layout.addLayout(ex_buttons)
        exercises_group.setLayout(exercises_layout)
        layout.addWidget(exercises_group)
    
        # ==================== SPRÁVA ROKŮ ====================
        years_group = QGroupBox("📆 Správa roků")
        years_group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                background-color: #1e1e1e;
                border: 2px solid #0d7377;
                border-radius: 5px;
                padding-top: 18px;
            }
        """)
        years_layout = QVBoxLayout()
    
        self.years_list = QListWidget()
        self.years_list.setObjectName("years_list")
        self.years_list.itemClicked.connect(self.on_year_selected_for_settings)
        years_layout.addWidget(self.years_list)
    
        y_buttons = QHBoxLayout()
        y_add = QPushButton("➕ Přidat rok")
        y_add.clicked.connect(self.add_custom_year)
        y_buttons.addWidget(y_add)
    
        y_del = QPushButton("🗑️ Smazat rok")
        y_del.clicked.connect(self.delete_year_from_list)
        y_buttons.addWidget(y_del)
    
        y_reset = QPushButton("🔄 Vynulovat záznamy")
        y_reset.clicked.connect(self.reset_year_workouts)
        y_buttons.addWidget(y_reset)
    
        years_layout.addLayout(y_buttons)
        years_group.setLayout(years_layout)
        layout.addWidget(years_group)
    
        # ==================== NASTAVENÍ VYBRANÉHO ROKU ====================
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
    
        grid = QGridLayout()
        grid.setSpacing(10)
    
        # Per-exercise startovní data
        lbl_dates = QLabel("📅 Datum zahájení (pro každé cvičení)")
        lbl_dates.setStyleSheet("font-weight: bold; color: #14919b;")
        grid.addWidget(lbl_dates, 0, 0)
    
        self.exercise_start_date_edits = {}
        dates_widget = QWidget()
        dates_layout = QVBoxLayout(dates_widget)
        dates_layout.setContentsMargins(0, 0, 0, 0)
    
        for exercise_id in self.get_active_exercises():
            cfg = self.get_exercise_config(exercise_id)
            row = QHBoxLayout()
            row.addWidget(QLabel(f"{cfg['icon']} {cfg['name']}:"))
            de = QDateEdit()
            de.setCalendarPopup(True)
            de.setDisplayFormat("dd.MM.yyyy")
            de.setDate(QDate.currentDate())
            de.setObjectName(f"date_edit_{exercise_id}")
            self.exercise_start_date_edits[exercise_id] = de
            row.addWidget(de)
            dates_layout.addLayout(row)
        grid.addWidget(dates_widget, 1, 0)
    
        # Základní cíle
        lbl_base = QLabel("🎯 Základní cíle (1. týden)")
        lbl_base.setStyleSheet("font-weight: bold; color: #14919b;")
        grid.addWidget(lbl_base, 0, 1)
    
        base_widget = QWidget()
        base_layout = QVBoxLayout(base_widget)
        base_layout.setContentsMargins(0, 0, 0, 0)
        self.base_goal_spins = {}
        for exercise_id in self.get_active_exercises():
            cfg = self.get_exercise_config(exercise_id)
            row = QHBoxLayout()
            row.addWidget(QLabel(f"{cfg['icon']} {cfg['name']}:"))
            spin = QSpinBox()
            spin.setRange(0, 10000)
            spin.setObjectName(f"spin_base_{exercise_id}")
            self.base_goal_spins[exercise_id] = spin
            row.addWidget(spin)
            base_layout.addLayout(row)
        grid.addWidget(base_widget, 1, 1)
    
        # Týdenní přírůstky
        lbl_inc = QLabel("📈 Týdenní přírůstky")
        lbl_inc.setStyleSheet("font-weight: bold; color: #14919b;")
        grid.addWidget(lbl_inc, 0, 2)
    
        inc_widget = QWidget()
        inc_layout = QVBoxLayout(inc_widget)
        inc_layout.setContentsMargins(0, 0, 0, 0)
        self.increment_spins = {}
        for exercise_id in self.get_active_exercises():
            cfg = self.get_exercise_config(exercise_id)
            row = QHBoxLayout()
            row.addWidget(QLabel(f"{cfg['icon']} {cfg['name']}:"))
            spin = QSpinBox()
            spin.setRange(0, 10000)
            spin.setObjectName(f"spin_inc_{exercise_id}")
            self.increment_spins[exercise_id] = spin
            row.addWidget(spin)
            inc_layout.addLayout(row)
        grid.addWidget(inc_widget, 1, 2)
    
        settings_layout.addLayout(grid)
    
        # Uložit
        btns = QHBoxLayout()
        btn_save = QPushButton("💾 Uložit nastavení")
        btn_save.setObjectName("btn_save_settings")
        btn_save.clicked.connect(self.save_settings)
        btns.addWidget(btn_save)
        settings_layout.addLayout(btns)
    
        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)
    
        # ==================== SPRÁVA DAT (Export/Import) – návrat ====================
        data_group = QGroupBox("💾 Správa dat")
        data_group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                background-color: #1e1e1e;
                border: 2px solid #0d7377;
                border-radius: 5px;
                padding-top: 18px;
            }
        """)
        data_layout = QHBoxLayout()
        btn_export = QPushButton("📤 Export dat")
        btn_export.setObjectName("btn_export_data")
        btn_export.clicked.connect(self.export_data)
        data_layout.addWidget(btn_export)
    
        btn_import = QPushButton("📥 Import dat")
        btn_import.setObjectName("btn_import_data")
        btn_import.clicked.connect(self.import_data)
        data_layout.addWidget(btn_import)
    
        data_group.setLayout(data_layout)
        layout.addWidget(data_group)
    
        # ==== Naplnění seznamů a AUTO-VÝBĚR AKTUÁLNÍHO ROKU ====
        self.refresh_exercises_list()
    
        self.years_list.clear()
        for y in self.get_available_years():
            year_workouts = sum(1 for ds in self.data.get('workouts', {}).keys()
                                if int(ds.split('-')[0]) == y)
            item = QListWidgetItem(f"📆 Rok {y} ({year_workouts} dnů s cvičením)")
            item.setData(Qt.UserRole, y)
            self.years_list.addItem(item)
    
        # Auto-výběr: aktuální rok
        current_year = datetime.now().year
        self.current_settings_year = current_year
        target_row = -1
        for i in range(self.years_list.count()):
            it = self.years_list.item(i)
            if it.data(Qt.UserRole) == current_year:
                target_row = i
                break
        if target_row >= 0:
            self.years_list.setCurrentRow(target_row)
        # Načíst hodnoty do UI pro aktuální rok
        self.load_year_settings_to_ui(current_year)
    
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
        """Načte nastavení daného roku do UI (per-exercise data, cíle, přírůstky) a označí rok v seznamu."""
        self.current_settings_year = int(year)
        year_str = str(year)
        settings = self.get_year_settings(year)
    
        # Nastavit výběr v listu roků vizuálně (pokud ještě není)
        for i in range(self.years_list.count()):
            it = self.years_list.item(i)
            if it and it.data(Qt.UserRole) == year:
                self.years_list.setCurrentRow(i)
                break
    
        # Per-exercise startovní data
        for exercise_id in self.get_active_exercises():
            dt = self.get_exercise_start_date(exercise_id, year)
            qd = QDate(dt.year, dt.month, dt.day)
            if exercise_id in self.exercise_start_date_edits:
                self.exercise_start_date_edits[exercise_id].setDate(qd)
    
        # Základní cíle a přírůstky
        for exercise_id in self.get_active_exercises():
            if exercise_id in self.base_goal_spins:
                base_goal = settings.get("base_goals", {}).get(exercise_id, 50)
                self.base_goal_spins[exercise_id].setValue(base_goal)
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
        """Uloží nastavení vybraného roku a OKAMŽITĚ promítne změny do všech záložek (grafy/přehledy/kalendáře)."""
        if not self.current_settings_year:
            self.show_message("Chyba", "Nejdřív vyber rok!", QMessageBox.Warning)
            return
    
        year_str = str(self.current_settings_year)
        self.data.setdefault("year_settings", {})
        self.data["year_settings"].setdefault(year_str, {
            "base_goals": {},
            "weekly_increment": {}
        })
    
        # Uložit startovní data pro každé cvičení
        active_exercises = self.get_active_exercises()
        ex_dates = {}
        min_date = None
        if hasattr(self, "exercise_start_date_edits"):
            for ex_id in active_exercises:
                if ex_id in self.exercise_start_date_edits:
                    ds = self.exercise_start_date_edits[ex_id].date().toString("yyyy-MM-dd")
                    ex_dates[ex_id] = ds
                    md = datetime.strptime(ds, "%Y-%m-%d").date()
                    if (min_date is None) or (md < min_date):
                        min_date = md
    
        ys = self.data["year_settings"][year_str]
        ys.setdefault("exercise_start_dates", {})
        ys["exercise_start_dates"].update(ex_dates)
        # Kompatibilitní globální start_date = nejmenší per-exercise
        ys["start_date"] = (min_date or datetime(int(year_str), 1, 1).date()).strftime("%Y-%m-%d")
    
        # Cíle & přírůstky
        for ex_id in active_exercises:
            if ex_id in self.base_goal_spins:
                ys.setdefault("base_goals", {})
                ys["base_goals"][ex_id] = self.base_goal_spins[ex_id].value()
            if ex_id in self.increment_spins:
                ys.setdefault("weekly_increment", {})
                ys["weekly_increment"][ex_id] = self.increment_spins[ex_id].value()
    
        # Uložit
        self.save_data()
    
        # ===== OKAMŽITÉ PROMÍTNUTÍ ZMĚN DO UI =====
        try:
            # 1) Přehledy (DEN/TÝDEN/MĚSÍC/ZBYTEK) pro každé cvičení
            for ex in active_exercises:
                # Zvolený rok z comboboxu cvičení (pokud existuje), jinak aktuální
                selected_year = datetime.now().year
                if ex in self.exercise_year_selectors and self.exercise_year_selectors[ex].currentText():
                    selected_year = int(self.exercise_year_selectors[ex].currentText())
                self.update_detailed_overview(ex, selected_year)
    
            # 2) Kalendáře
            for ex in active_exercises:
                self.refresh_exercise_calendar(ex)
    
            # 3) Grafy – zachovat aktuální mód
            for ex in active_exercises:
                mode = self.chart_modes.get(ex, "weekly")
                self.update_performance_chart(ex, mode)
    
            # 4) Statistiky pod kalendářem
            for ex in active_exercises:
                selected_year = datetime.now().year
                if ex in self.exercise_year_selectors and self.exercise_year_selectors[ex].currentText():
                    selected_year = int(self.exercise_year_selectors[ex].currentText())
                self.update_year_statistics(ex, selected_year)
    
            self.show_message("Uloženo", f"Nastavení pro rok {self.current_settings_year} bylo uloženo a okamžitě aplikováno.", QMessageBox.Information)
        except Exception as e:
            # V krajním případě upozorni na restart, ale nepadat
            print(f"Post-save refresh selhal: {e}")
            self.show_message("Poznámka", "Nastavení bylo uloženo. Pokud se změny hned neprojevily, prosím restartuj aplikaci.", QMessageBox.Information)

    def add_custom_year(self):
        """Dialog pro přidání libovolného roku - s výběrem módu"""
        current_year = datetime.now().year
        year, ok = QInputDialog.getInt(
            self,
            "Přidat rok",
            "Zadej rok, který chceš přidat do sledování:",
            current_year + 1,
            2000,
            2100,
            1
        )
        
        if not ok:
            return
        
        year_str = str(year)
        
        # Zkontrolovat, zda rok již existuje
        if year_str in self.data["year_settings"]:
            self.show_message(
                "Informace",
                f"Rok {year} již existuje v nastavení.",
                QMessageBox.Information
            )
            return
        
        # **NOVĚ: Dialog pro výběr módu**
        mode_dialog = YearCreationModeDialog(year, self)
        
        if not mode_dialog.exec():
            # **OPRAVA: Zrušení mode dialogu**
            return
        
        mode = mode_dialog.get_mode()
        
        if not mode:
            # **OPRAVA: Žádný mód nebyl vybrán**
            return
        
        # **INICIALIZACE success_message**
        success_message = ""
        year_created = False
        
        if mode == "wizard":
            # **SMART WIZARD**
            wizard = NewYearWizardDialog(year, self)
            
            if wizard.exec():
                recommendations = wizard.get_recommendations()
                
                self.data["year_settings"][year_str] = {
                    "start_date": f"{year}-01-01",
                    "base_goals": {},
                    "weekly_increment": {}
                }
                
                for exercise_id, goals in recommendations.items():
                    self.data["year_settings"][year_str]["base_goals"][exercise_id] = goals["base_goal"]
                    self.data["year_settings"][year_str]["weekly_increment"][exercise_id] = goals["weekly_increment"]
                
                # Inicializace per-exercise startovních dat
                ys = self.data["year_settings"][year_str]
                ys.setdefault("exercise_start_dates", {})
                for ex_id in self.data.get("exercises", {}).keys():
                    ys["exercise_start_dates"][ex_id] = ys.get("start_date", f"{year}-01-01")
                
                success_message = f"Rok {year} vytvořen pomocí Smart Wizardu!"
                year_created = True
            else:
                # **OPRAVA: Wizard byl zrušen, nic nevytvářej**
                return
        
        elif mode == "copy":
            # **ZKOPÍROVAT Z MINULÉHO ROKU**
            previous_year = year - 1
            previous_year_str = str(previous_year)
            
            if previous_year_str in self.data["year_settings"]:
                previous_settings = self.data["year_settings"][previous_year_str]
                
                self.data["year_settings"][year_str] = {
                    "start_date": f"{year}-01-01",
                    "base_goals": previous_settings["base_goals"].copy(),
                    "weekly_increment": previous_settings["weekly_increment"].copy()
                }
                
                # Inicializace per-exercise startovních dat
                ys = self.data["year_settings"][year_str]
                ys.setdefault("exercise_start_dates", {})
                for ex_id in self.data.get("exercises", {}).keys():
                    ys["exercise_start_dates"][ex_id] = ys.get("start_date", f"{year}-01-01")
                
                success_message = f"Rok {year} vytvořen zkopírováním z roku {previous_year}!"
                year_created = True
            else:
                # Fallback na výchozí
                self.data["year_settings"][year_str] = self.create_default_year_settings(year)
                # Inicializace per-exercise startovních dat
                ys = self.data["year_settings"][year_str]
                ys.setdefault("exercise_start_dates", {})
                for ex_id in self.data.get("exercises", {}).keys():
                    ys["exercise_start_dates"][ex_id] = ys.get("start_date", f"{year}-01-01")
                success_message = f"Rok {year} vytvořen s výchozím nastavením (minulý rok neexistuje)!"
                year_created = True
        
        else:  # mode == "classic"
            # **VÝCHOZÍ NASTAVENÍ**
            self.data["year_settings"][year_str] = self.create_default_year_settings(year)
            # Inicializace per-exercise startovních dat
            ys = self.data["year_settings"][year_str]
            ys.setdefault("exercise_start_dates", {})
            for ex_id in self.data.get("exercises", {}).keys():
                ys["exercise_start_dates"][ex_id] = ys.get("start_date", f"{year}-01-01")
            success_message = f"Rok {year} vytvořen s výchozím nastavením!"
            year_created = True
        
        # **KONTROLA: Pokud rok nebyl vytvořen, ukonči**
        if not year_created:
            return
        
        # **Společné kroky pro všechny módy**
        self.save_data()
        self.update_all_year_selectors()
        
        # Přepnout na nový rok
        for exercise in self.get_active_exercises():
            if exercise in self.exercise_year_selectors:
                self.exercise_year_selectors[exercise].setCurrentText(str(year))
        
        # Refresh všeho
        for exercise in self.get_active_exercises():
            self.update_exercise_tab(exercise)
            self.refresh_exercise_calendar(exercise)
            if exercise in self.chart_modes:
                current_mode = self.chart_modes[exercise]
                self.update_performance_chart(exercise, current_mode)
        
        # Refresh v nastavení
        self.years_list.clear()
        for y in self.get_available_years():
            year_workouts = sum(1 for date_str in self.data["workouts"].keys() if int(date_str.split("-")[0]) == y)
            item = QListWidgetItem(f"📅 Rok {y} ({year_workouts} dní s cvičením)")
            item.setData(Qt.UserRole, y)
            self.years_list.addItem(item)
        
        self.load_year_settings_to_ui(year)
        
        self.show_message("🎉 Úspěch!", success_message, QMessageBox.Information)

    
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
        
        # Globální start_date ponechán pro referenci
        start_date_str = settings.get('start_date', f"{current_year}-01-01")
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        days_to_sunday = 6 - start_date.weekday()
        first_week_end = start_date + timedelta(days=days_to_sunday)
        first_full_week_start = first_week_end + timedelta(days=1)
        
        diag_text = f"Nastavení pro rok {current_year}\n"
        for exercise in self.get_active_exercises():
            base = settings['base_goals'][exercise]
            increment = settings['weekly_increment'][exercise]
            
            ex_sd = self.get_exercise_start_date(exercise, current_year)
            diag_text += f"\n{exercise.upper()} (start {ex_sd.strftime('%Y-%m-%d')}):\n"
            diag_text += f"  Základní cíl: {base}\n"
            diag_text += f"  Týdenní nárůst: {increment}\n\n"
            
            test_dates = [
                start_date_str,
                (start_date + timedelta(days=3)).strftime('%Y-%m-%d'),
                first_week_end.strftime('%Y-%m-%d'),
                first_full_week_start.strftime('%Y-%m-%d'),
                (first_full_week_start + timedelta(days=7)).strftime('%Y-%m-%d'),
                '2025-10-25',
            ]
            for d in test_dates:
                diag_text += f"  {d}: {self.calculate_goal(exercise, d)}\n"
        
        text_edit.setPlainText(diag_text)
        layout.addWidget(text_edit)
        diag_window.show()
        
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
    
        # NOVĚ: tlačítko 'Den' – vložíme ho před 'Týden'
        daily_btn = QPushButton("🕒 Den")
        daily_btn.setCheckable(True)
        daily_btn.setFixedWidth(100)
        daily_btn.setStyleSheet("padding: 8px; font-size: 12px;")
        daily_btn.clicked.connect(lambda: self.update_performance_chart(exercisetype, "daily"))
        mode_buttons_layout.insertWidget(mode_buttons_layout.indexOf(weekly_btn), daily_btn)
    
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
    
        # Registrace tlačítek (doplněn 'daily')
        if not hasattr(self, 'chart_mode_buttons'):
            self.chart_mode_buttons = {}
        self.chart_mode_buttons[exercisetype] = {
            'daily': daily_btn,
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
        """Aktualizuje graf výkonu podle zvoleného módu (daily/weekly/monthly/yearly).
        - daily: průběh aktuálně zvoleného dne (čas → kumulativní výkon), + vodorovná čára denního cíle
        - ostatní módy beze změny (výkon vs. cíl; svislá čára startu cvičení, pokud spadá do rozsahu)
        """
        # Ověření figure/canvas struktur
        if not hasattr(self, 'chart_figures') or exercise_type not in self.chart_figures:
            return
        if not hasattr(self, 'chart_modes'):
            self.chart_modes = {}
        self.chart_modes[exercise_type] = mode
    
        # Přepnout stav tlačítek (pokud existují)
        if hasattr(self, 'chart_mode_buttons') and exercise_type in self.chart_mode_buttons:
            for btn_mode, btn in self.chart_mode_buttons[exercise_type].items():
                try:
                    btn.setChecked(btn_mode == mode)
                except Exception:
                    pass
    
        fig = self.chart_figures[exercise_type]
        fig.clear()
        ax = fig.add_subplot(111)
    
        # Tmavé pozadí a osy
        ax.set_facecolor('#1e1e1e')
        ax.tick_params(axis='x', colors='#e0e0e0')
        ax.tick_params(axis='y', colors='#e0e0e0')
    
        cfg = self.get_exercise_config(exercise_type) if hasattr(self, 'get_exercise_config') else {"name": exercise_type}
        ax.set_title(f"Výkon – {cfg.get('name', exercise_type)}", color='#e0e0e0', fontsize=14)
    
        today = datetime.now().date()
    
        # Zvolený rok z per-exercise comboboxu
        if hasattr(self, 'exercise_year_selectors') and exercise_type in self.exercise_year_selectors \
           and self.exercise_year_selectors[exercise_type].currentText():
            selected_year = int(self.exercise_year_selectors[exercise_type].currentText())
        else:
            selected_year = today.year
    
        # ---- Získání startu cvičení pro značku (pro non-daily módy) ----
        ys = self.get_year_settings(selected_year) if hasattr(self, 'get_year_settings') else {}
        ex_starts = (ys.get("exercise_start_dates") or {}) if isinstance(ys, dict) else {}
        ex_start_str = ex_starts.get(exercise_type)
    
        start_date = None
        if ex_start_str:
            try:
                start_date = datetime.strptime(ex_start_str, "%Y-%m-%d").date()
            except Exception:
                start_date = None
        if start_date is None:
            try:
                ex_def = (self.data.get("exercises", {}) or {}).get(exercise_type, {})
                per_year = (ex_def.get("start_dates") or {})
                ex2_str = per_year.get(str(selected_year))
                if ex2_str:
                    start_date = datetime.strptime(ex2_str, "%Y-%m-%d").date()
            except Exception:
                start_date = None
        if start_date is None:
            try:
                ys_start = (ys or {}).get("start_date")
                if ys_start:
                    start_date = datetime.strptime(ys_start, "%Y-%m-%d").date()
            except Exception:
                start_date = None
        if start_date is None:
            start_date = datetime(selected_year, 1, 1).date()
    
        # =================================================================
        #                          DAILY MODE
        # =================================================================
        if mode == "daily":
            # 1) Zkusit zjistit vybraný den z přehledového stromu (top-level výběr dne)
            day_date = None
            try:
                tree = self.findChild(QTreeWidget, f"tree_{exercise_type}")
                if tree:
                    for it in tree.selectedItems():
                        payload = it.data(3, Qt.UserRole)
                        # top-level den nemá payload s 'record_id'
                        if not (isinstance(payload, dict) and 'record_id' in payload):
                            txt = it.text(0) if it is not None else ""
                            ds = txt.split(' ', 1)[1] if ' ' in txt else txt
                            # očekáváme formát YYYY-MM-DD
                            if len(ds) == 10 and ds[4] == '-' and ds[7] == '-':
                                day_date = datetime.strptime(ds, "%Y-%m-%d").date()
                                break
            except Exception:
                day_date = None
    
            # 2) Fallback: dnešek (pokud ve zvoleném roce), případně poslední den v roce s daty pro dané cvičení
            if day_date is None:
                if selected_year == today.year:
                    day_date = today
                else:
                    # poslední den v roce s nějakým záznamem
                    days_with_data = []
                    for ds, perday in (self.data.get('workouts', {}) or {}).items():
                        if not isinstance(ds, str) or len(ds) < 10: 
                            continue
                        try:
                            y = int(ds[:4])
                        except Exception:
                            continue
                        if y != selected_year:
                            continue
                        if exercise_type in perday:
                            days_with_data.append(ds)
                    if days_with_data:
                        ds = sorted(days_with_data)[-1]
                        try:
                            day_date = datetime.strptime(ds, "%Y-%m-%d").date()
                        except Exception:
                            day_date = datetime(selected_year, 1, 1).date()
                    else:
                        day_date = datetime(selected_year, 1, 1).date()
    
            # Vytažení všech záznamů daného dne
            day_str = day_date.strftime("%Y-%m-%d")
            recs = []
            if day_str in self.data.get('workouts', {}) and exercise_type in self.data['workouts'][day_str]:
                raw = self.data['workouts'][day_str][exercise_type]
                if isinstance(raw, list):
                    recs = raw[:]
                elif isinstance(raw, dict):
                    recs = [raw]
    
            # Setřídění podle času
            def _ts_to_dt(ts: str) -> datetime:
                # očekávaný formát "YYYY-MM-DD HH:MM[:SS]"
                try:
                    if len(ts) >= 19:
                        return datetime.strptime(ts[:19], "%Y-%m-%d %H:%M:%S")
                    elif len(ts) >= 16:
                        return datetime.strptime(ts[:16], "%Y-%m-%d %H:%M")
                    else:
                        # bez času → 12:00
                        return datetime.strptime(day_str + " 12:00", "%Y-%m-%d %H:%M")
                except Exception:
                    return datetime.strptime(day_str + " 12:00", "%Y-%m-%d %H:%M")
    
            recs_sorted = sorted(recs, key=lambda r: _ts_to_dt(r.get("timestamp", f"{day_str} 12:00")))
    
            # Kumulativní výkon během dne
            times = []
            cumul = []
            running = 0
            for r in recs_sorted:
                dt = _ts_to_dt(r.get("timestamp", f"{day_str} 12:00"))
                running += int(r.get("value", 0))
                times.append(dt)
                cumul.append(running)
    
            # Denní cíl
            daily_goal = self.calculate_goal(exercise_type, day_str)
            if not isinstance(daily_goal, int):
                daily_goal = int(daily_goal) if daily_goal else 0
    
            # vykreslení
            import matplotlib.dates as mdates
            if not times:
                ax.text(0.5, 0.5, 'Žádné záznamy v tomto dni', ha='center', va='center',
                        transform=ax.transAxes, fontsize=14, color='#a0a0a0')
            else:
                # čára kumulativního výkonu + body v časech
                ax.plot(times, cumul, label='Kumulativně (den)', linewidth=2, marker='o', markersize=4, color='#0d7377')
                # denní cíl jako horizontála
                if daily_goal > 0:
                    ax.axhline(daily_goal, linestyle='--', linewidth=1.8, color='#FFD700', label='Denní cíl')
    
                # časová osa v HH:MM
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
                ax.set_xlim(datetime(day_date.year, day_date.month, day_date.day, 0, 0),
                            datetime(day_date.year, day_date.month, day_date.day, 23, 59, 59))
    
            ax.set_title(f"Den {day_date.strftime('%d.%m.%Y')}", color='#e0e0e0', fontsize=14)
            leg = ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0., fontsize=9, facecolor='#2d2d2d', edgecolor='#3d3d3d')
            for t in leg.get_texts():
                t.set_color('#e0e0e0')
    
            fig.tight_layout()
            if hasattr(self, 'chart_canvases') and exercise_type in self.chart_canvases:
                self.chart_canvases[exercise_type].draw()
            return  # daily zpracován; dál nepokračujeme
    
        # =================================================================
        #                WEEKLY / MONTHLY / YEARLY (beze změn)
        # =================================================================
        # Vypočet rozsahu dle módu + vykreslení jako dříve
        if mode == "weekly":
            end_date = today if selected_year == today.year else min(datetime(selected_year, 12, 31).date(), today)
            start_r = max(end_date - timedelta(days=6), datetime(selected_year, 1, 1).date(), start_date)
            range_start, range_end = start_r, end_date
            xlabel_format = "%d.%m"
    
        elif mode == "monthly":
            month = today.month if selected_year == today.year else 12
            month_start = datetime(selected_year, month, 1).date()
            next_month = datetime(selected_year + (1 if month == 12 else 0), 1 if month == 12 else month + 1, 1).date()
            month_end = next_month - timedelta(days=1)
            month_start = max(month_start, start_date)
            month_end = min(month_end, today)
            range_start, range_end = month_start, month_end
            xlabel_format = "%d.%m"
    
        else:  # "yearly"
            year_start = max(datetime(selected_year, 1, 1).date(), start_date)
            year_end = min(datetime(selected_year, 12, 31).date(), today)
            range_start, range_end = year_start, year_end
            xlabel_format = "%d.%m."
    
        if range_end < range_start:
            ax.text(0.5, 0.5, 'Žádná data k zobrazení', ha='center', va='center',
                    transform=ax.transAxes, fontsize=14, color='#a0a0a0')
            fig.tight_layout()
            if hasattr(self, 'chart_canvases') and exercise_type in self.chart_canvases:
                self.chart_canvases[exercise_type].draw()
            return
    
        dates = [range_start + timedelta(days=i) for i in range((range_end - range_start).days + 1)]
        performed, goals = [], []
        for d in dates:
            ds = d.strftime("%Y-%m-%d")
            v = 0
            if ds in self.data.get('workouts', {}) and exercise_type in self.data['workouts'][ds]:
                recs = self.data['workouts'][ds][exercise_type]
                if isinstance(recs, list):
                    v = sum(r.get("value", 0) for r in recs)
                elif isinstance(recs, dict):
                    v = recs.get("value", 0)
            g = self.calculate_goal(exercise_type, ds)
            if not isinstance(g, int):
                g = int(g) if g else 0
            performed.append(v)
            goals.append(g)
    
        bar_w = 0.8 if mode == "weekly" else 0.6
        ax.bar(dates, performed, width=bar_w, label='Výkon', color='#0d7377', alpha=0.8)
        ax.plot(dates, goals, label='Cíl', color='#FFD700', linewidth=2, marker='o', markersize=3)
    
        # Svislá čára dne zahájení (pokud spadá do rozsahu)
        if start_date >= dates[0] and start_date <= dates[-1]:
            ax.axvline(x=start_date, color='#32c766', linestyle='--', linewidth=2, alpha=0.7, label='Začátek cvičení')
            y_max = max(max(performed) if performed else 0, max(goals) if goals else 0)
            if y_max > 0:
                ax.text(start_date, y_max * 1.05, f"Start {start_date.strftime('%d.%m.')}",
                        rotation=90, va='bottom', ha='right', fontsize=9, color='#32c766', weight='bold')
    
        if mode == "yearly":
            num_dates = len(dates)
            step = max(1, num_dates // 12)
            ax.set_xticks([dates[i] for i in range(0, num_dates, step)])
            ax.set_xticklabels([dates[i].strftime(xlabel_format) for i in range(0, num_dates, step)], rotation=0)
        else:
            ax.set_xticks(dates)
            ax.set_xticklabels([d.strftime(xlabel_format) for d in dates],
                               rotation=45 if mode == "monthly" else 0)
    
        leg = ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0., fontsize=9, facecolor='#2d2d2d', edgecolor='#3d3d3d')
        for t in leg.get_texts():
            t.set_color('#e0e0e0')
    
        fig.tight_layout()
        if hasattr(self, 'chart_canvases') and exercise_type in self.chart_canvases:
            self.chart_canvases[exercise_type].draw()
        
    def create_exercise_tab(self, exercise_type, icon):
        """Vytvoří záložku pro konkrétní cvičení - BEZ přidávání (layout beze změny).
        MINIMAL-CHANGE: pouze přidán řádek s přepínači Den/Týden/Měsíc/Rok pod kalendář (nad graf),
        které volají update_performance_chart(...). Ničeho dalšího se nedotýkáme.
        """
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
    
        # ==================== JEN TOTO NAVÍC: přepínače režimu grafu ====================
        # (Malý vodorovný řádek s tlačítky Den/Týden/Měsíc/Rok; bez dopadu na zbytek layoutu)
        mode_row = QHBoxLayout()
        mode_row.setSpacing(8)
        btn_day = QRadioButton("Den")
        btn_week = QRadioButton("Týden")
        btn_month = QRadioButton("Měsíc")
        btn_year = QRadioButton("Rok")
        # výchozí režim necháme jako doposud – Týden
        btn_week.setChecked(True)
    
        # uložíme odkazy pro pozdější synchronizaci (bez dalších zásahů do app)
        if not hasattr(self, "chart_mode_buttons"):
            self.chart_mode_buttons = {}
        self.chart_mode_buttons[exercise_type] = {
            "daily": btn_day,
            "weekly": btn_week,
            "monthly": btn_month,
            "yearly": btn_year,
        }
    
        # signály: volají update_performance_chart se zvoleným módem
        for b in (btn_day, btn_week, btn_month, btn_year):
            b.toggled.connect(
                lambda _=None, m=b: m.isChecked()
                and self.update_performance_chart(
                    exercise_type,
                    "daily" if m is btn_day else "weekly" if m is btn_week else "monthly" if m is btn_month else "yearly"
                )
            )
    
        mode_row.addWidget(btn_day)
        mode_row.addWidget(btn_week)
        mode_row.addWidget(btn_month)
        mode_row.addWidget(btn_year)
        mode_row.addStretch()
        calendar_layout.addLayout(mode_row)
        # ==================== KONEC DOPLNĚNÍ ====================
    
        # ==================== GRAF POD KALENDÁŘEM (beze změny) ====================
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
        """Smaže vybrané záznamy v levém přehledu (QTreeWidget)."""
        # Cílíme na strom v záložce cvičení
        tree = self.findChild(QTreeWidget, f"tree_{exercise_type}")
        if not tree:
            self.show_message("Chyba", "Strom záznamů nebyl nalezen.", QMessageBox.Warning)
            return
    
        selected_items = tree.selectedItems()
        if not selected_items:
            self.show_message("Informace", "Nejprve vyber záznam(y) ke smazání.", QMessageBox.Information)
            return
    
        # Nasbírej konkrétní recordy (mohou být označené jednotlivé záznamy, nebo celé dny)
        to_delete = []  # list[(date_str, record_id)]
        for item in selected_items:
            payload = item.data(3, Qt.UserRole)  # v update_exercise_tab ukládáme dict do sloupce 3
            if isinstance(payload, dict) and 'date' in payload and 'record_id' in payload:
                to_delete.append((payload['date'], payload['record_id']))
            else:
                # Je to den -> vezmi všechny děti = záznamy
                for i in range(item.childCount()):
                    child = item.child(i)
                    p2 = child.data(3, Qt.UserRole)
                    if isinstance(p2, dict) and 'date' in p2 and 'record_id' in p2:
                        to_delete.append((p2['date'], p2['record_id']))
    
        # Dedup
        to_delete = list({(d, r) for (d, r) in to_delete})
    
        if not to_delete:
            self.show_message("Informace", "Nebyl vybrán žádný konkrétní záznam.", QMessageBox.Information)
            return
    
        # Potvrzení
        msg = QMessageBox(self)
        msg.setWindowTitle("Potvrdit smazání")
        msg.setIcon(QMessageBox.Warning)
        msg.setText(f"Opravdu smazat {len(to_delete)} záznamů?")
        yes_btn = msg.addButton("Ano, smazat", QMessageBox.YesRole)
        no_btn = msg.addButton("Ne, zrušit", QMessageBox.NoRole)
        msg.exec()
        if msg.clickedButton() is not yes_btn:
            return
    
        # Proveď smazání
        for date_str, record_id in to_delete:
            if date_str in self.data['workouts'] and exercise_type in self.data['workouts'][date_str]:
                records = self.data['workouts'][date_str][exercise_type]
                if isinstance(records, list):
                    self.data['workouts'][date_str][exercise_type] = [r for r in records if r.get('id') != record_id]
                    # Pokud už pro tento den není žádné cvičení, odstraň klíč
                    if not self.data['workouts'][date_str][exercise_type]:
                        del self.data['workouts'][date_str][exercise_type]
                    # Pokud je den prázdný, odstraň i datum
                    if not self.data['workouts'][date_str]:
                        del self.data['workouts'][date_str]
                elif isinstance(records, dict):
                    if records.get('id') == record_id:
                        del self.data['workouts'][date_str][exercise_type]
                        if not self.data['workouts'][date_str]:
                            del self.data['workouts'][date_str]
    
        self.save_data()
    
        # Refresh UI
        self.update_exercise_tab(exercise_type)
        self.refresh_exercise_calendar(exercise_type)
        mode = self.chart_modes.get(exercise_type, "weekly") if hasattr(self, "chart_modes") else "weekly"
        self.update_performance_chart(exercise_type, mode)
        self.refresh_add_tab_goals()
    
        self.show_message("Smazáno", f"{len(to_delete)} záznamů bylo smazáno.")

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
        """Vypočítá cíl pro dané datum s respektem k per-cvičení startu."""
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            year = date.year
            settings = self.get_year_settings(year)
    
            # Fallback klíčů s/bez diakritiky
            if exercise_type not in settings['base_goals']:
                old_mapping = {"drepy": "dřepy", "skrcky": "skrčky"}
                old_key = old_mapping.get(exercise_type, exercise_type)
                if old_key in settings['base_goals']:
                    exercise_type = old_key
                else:
                    return 50
    
            base_goal = settings['base_goals'][exercise_type]
            weekly_increment = settings['weekly_increment'][exercise_type]
    
            # PER-EXERCISE START
            ex_sd_map = settings.get("exercise_start_dates", {})
            if isinstance(ex_sd_map, dict) and exercise_type in ex_sd_map and ex_sd_map[exercise_type]:
                start_str = ex_sd_map[exercise_type]
            else:
                ex_conf = self.data.get("exercises", {}).get(exercise_type, {})
                sd_map = ex_conf.get("start_dates", {}) if isinstance(ex_conf, dict) else {}
                if isinstance(sd_map, dict) and str(year) in sd_map and sd_map[str(year)]:
                    start_str = sd_map[str(year)]
                else:
                    start_str = settings.get("start_date", f"{year}-01-01")
            start_date = datetime.strptime(start_str, "%Y-%m-%d").date()
    
            if date < start_date:
                return 0
    
            # Logika: první „zlomený“ týden → base_goal, pak každý další týden + increment
            days_diff = (date - start_date).days
            first_week_days = 7 - start_date.weekday()
            if days_diff < first_week_days:
                return base_goal
    
            days_after_first = days_diff - first_week_days
            full_weeks = days_after_first // 7
            return base_goal + (full_weeks + 1) * weekly_increment
    
        except Exception as e:
            print(f"Chyba v calculate_goal pro {exercise_type}, {date_str}: {e}")
            return 50

    def get_goal_calculation_text(self, exercise_type, date_str):
        """Vrátí text s vysvětlením výpočtu"""
        target_date = datetime.strptime(date_str, '%Y-%m-%d')
        year = target_date.year
        settings = self.get_year_settings(year)
        
        start_date = datetime.combine(self.get_exercise_start_date(exercise_type, year), datetime.min.time())
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
            
    def _calendar_tooltip_with_contrast(self, tooltip_text: str, bg_hex: str) -> str:
        """
        Vrátí HTML tooltip se správným kontrastem textu podle světlosti barvy pozadí (hex).
        - Světlé pozadí  -> tmavý text
        - Tmavé pozadí   -> světlý text
        Zachová původní řádky (\\n) pomocí white-space: pre-line.
        """
        try:
            if not isinstance(bg_hex, str) or not bg_hex.startswith("#") or len(bg_hex) < 7:
                # Bezpečný fallback – světlý text pro dark theme
                return f"<div style='color:#f0f0f0; white-space:pre-line'>{tooltip_text}</div>"
    
            c = bg_hex.lstrip("#")
            r, g, b = int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)
    
            def _lin(v: float) -> float:
                v = v / 255.0
                return v/12.92 if v <= 0.04045 else ((v+0.055)/1.055)**2.4
    
            # Relativní luminance (sRGB)
            lum = 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)
            text_color = "#111111" if lum >= 0.60 else "#f0f0f0"
    
            return f"<div style='color:{text_color}; white-space:pre-line'>{tooltip_text}</div>"
        except Exception:
            # V nouzi ponech světlý text (dark theme)
            return f"<div style='color:#f0f0f0; white-space:pre-line'>{tooltip_text}</div>"

    def update_exercise_tab(self, exercise_type):
        """Aktualizuje statistiky a strom záznamů daného cvičení.
    
        Styl top-level dne: beze změny (emoji + barevný % sloupec).
        Nově: child záznamy v 1. sloupci zobrazují KUMULATIVNÍ podíl vůči dennímu cíli
        (např. 20 %, 120 %, 180 % …) s barevným zvýrazněním. Funkčně zachován multi-select,
        uchování výběru i výchozí sbalení po prvním naplnění.
        """
        try:
            if exercise_type not in self.exercise_year_selectors:
                return
            selector = self.exercise_year_selectors[exercise_type]
            if not selector or not selector.currentText():
                return
    
            selected_year = int(selector.currentText())
    
            # Přehledové boxy / progress bar apod.
            self.update_detailed_overview(exercise_type, selected_year)
    
            tree = self.findChild(QTreeWidget, f"tree_{exercise_type}")
            if not tree:
                return
    
            # --- UCHOVÁNÍ VÝBĚRU ---
            preserved = set()             # {(date_str, record_id)}
            preserved_days = set()        # {date_str}
            preserved_children_by_day: dict[str, set] = {}
    
            for it in tree.selectedItems():
                payload = it.data(3, Qt.UserRole)
                if isinstance(payload, dict) and 'date' in payload and 'record_id' in payload:
                    date_str = payload['date']
                    rec_id = payload['record_id']
                    preserved.add((date_str, rec_id))
                    preserved_children_by_day.setdefault(date_str, set()).add(rec_id)
                else:
                    # Vybraný den (top-level) → ulož datum i děti
                    txt = it.text(0) if it is not None else ""
                    date_str = txt.split(' ', 1)[1] if ' ' in txt else txt
                    if date_str:
                        preserved_days.add(date_str)
                    for i in range(it.childCount()):
                        ch = it.child(i)
                        p2 = ch.data(3, Qt.UserRole)
                        if isinstance(p2, dict) and 'date' in p2 and 'record_id' in p2:
                            preserved.add((p2['date'], p2['record_id']))
                            preserved_children_by_day.setdefault(p2['date'], set()).add(p2['record_id'])
    
            # --- UCHOVÁNÍ ROZBALENÍ DNŮ ---
            expanded_dates = set()
            for i in range(tree.topLevelItemCount()):
                item = tree.topLevelItem(i)
                if item and item.isExpanded():
                    txt = item.text(0)
                    date_str = txt.split(' ', 1)[1] if ' ' in txt else txt
                    expanded_dates.add(date_str)
    
            first_population = (tree.property("_ever_populated") is not True)
    
            tree.blockSignals(True)
            tree.clear()
    
            # Multi-select a výkon
            tree.setSelectionMode(QAbstractItemView.ExtendedSelection)
            tree.setSelectionBehavior(QAbstractItemView.SelectItems)
            tree.setAlternatingRowColors(False)  # child řádky prokládáme ručně
            tree.setUniformRowHeights(True)
    
            # --- Data po dnech (jen zvolený rok) ---
            days_data: dict[str, list[dict]] = {}
            for ds, perday in self.data.get('workouts', {}).items():
                year_here = int(ds.split('-')[0]) if '-' in ds else None
                if year_here != selected_year:
                    continue
                if exercise_type in perday:
                    recs = perday[exercise_type]
                    if isinstance(recs, list):
                        days_data.setdefault(ds, []).extend(recs)
                    elif isinstance(recs, dict):
                        days_data.setdefault(ds, []).append(recs)
    
            # Seřazení dnů – nejnovější nahoře
            sorted_dates = sorted(days_data.keys(), reverse=True)
    
            # Připrav fonty pro child řádky
            try:
                from PySide6.QtGui import QFont
                child_val_font = QFont()
                child_val_font.setBold(True)
    
                # Monospace pro čas (macOS: Menlo; fallback funguje i jinde)
                child_time_font = QFont("Menlo")
                base_size = tree.font().pointSize() if tree.font().pointSize() > 0 else 11
                child_time_font.setPointSize(max(base_size - 1, 9))
            except Exception:
                child_val_font = None
                child_time_font = None
    
            # Pomocná funkce pro barvu kumulativního % v 1. sloupci (dark-friendly)
            def _pct_color(p: int) -> "QColor":
                # <50 % šedá, 50–99 % zlatá, 100–149 % zelená, 150 %+ tyrkys
                if p < 50:
                    return QColor(176, 176, 176)
                if p < 100:
                    return QColor(255, 215, 0)   # zlatá
                if p < 150:
                    return QColor(50, 199, 102)  # zelená
                return QColor(0, 188, 212)       # tyrkys
    
            for date_str in sorted_dates:
                records = days_data[date_str]
    
                # Souhrn dne
                total_day_value = sum(r.get('value', 0) for r in records)
                record_count = len(records)
                goal = self.calculate_goal(exercise_type, date_str)
                if not isinstance(goal, int):
                    goal = int(goal) if goal else 0
                percent = (total_day_value / goal * 100) if goal > 0 else 0
    
                # Top-level (den) – PŮVODNÍ vzhled (emoji + barevný %)
                if percent >= 100:
                    status_icon = "✅"
                    color = QColor(0, 100, 0)
                elif percent >= 50:
                    status_icon = "⏳"
                    color = QColor(255, 215, 0)
                else:
                    status_icon = "❌"
                    color = QColor(255, 0, 0)
    
                day_item = QTreeWidgetItem(tree)
                day_item.setText(0, f"{status_icon} {date_str}")
                day_item.setText(1, f"{total_day_value} ({record_count}×)")
                day_item.setText(2, f"{percent:.0f}%")
    
                day_item.setForeground(0, QColor(255, 255, 255))
                day_item.setForeground(1, QColor(200, 200, 200))
                day_item.setBackground(2, color)
                day_item.setForeground(2, QColor(255, 255, 255))
                day_item.setTextAlignment(1, Qt.AlignCenter)
                day_item.setTextAlignment(2, Qt.AlignCenter)
    
                # Respektuj stav rozbalení / výchozí sbalení
                day_item.setExpanded(date_str in expanded_dates if not first_population else False)
    
                # --- Child záznamy: 1. sloupec = KUMULATIVNÍ podíl vůči dennímu cíli ---
                running_total = 0
                for idx, record in enumerate(sorted(records, key=lambda x: x.get('timestamp', ''))):
                    value = record.get('value', 0)
                    timestamp = record.get('timestamp', 'N/A')
                    time_only = timestamp.split(' ')[1] if ' ' in timestamp else timestamp
                    record_id = record.get('id', '')
    
                    running_total += value
                    if goal > 0:
                        rec_cum_pct = int(round((running_total / goal) * 100))
                        pct_text = f"{rec_cum_pct} %"
                    else:
                        rec_cum_pct = None
                        pct_text = "—"
    
                    rec_item = QTreeWidgetItem(day_item)
    
                    # Sloupce: [kumulativní % vůči cíli] [hodnota] [čas] [id]
                    rec_item.setText(0, pct_text)
                    rec_item.setText(1, str(value))
                    rec_item.setText(2, time_only)
                    rec_item.setText(3, record_id)
    
                    # Zarovnání
                    rec_item.setTextAlignment(0, Qt.AlignCenter)
                    rec_item.setTextAlignment(1, Qt.AlignCenter)
                    rec_item.setTextAlignment(2, Qt.AlignCenter)
    
                    # Barvy textu (dark-friendly)
                    if rec_cum_pct is None:
                        rec_item.setForeground(0, QColor(200, 200, 200))  # neutrální, když goal=0
                    else:
                        rec_item.setForeground(0, _pct_color(rec_cum_pct))
                    rec_item.setForeground(1, QColor(240, 240, 240))   # hodnota výrazněji
                    rec_item.setForeground(2, QColor(180, 180, 180))   # čas jemněji
    
                    # Fonty
                    if child_val_font:
                        rec_item.setFont(1, child_val_font)
                    if child_time_font:
                        rec_item.setFont(2, child_time_font)
    
                    # Lehký „striping“ child řádků (jen uvnitř dne)
                    if idx % 2 == 1:
                        shade = QColor(255, 255, 255, 14)  # velmi jemné
                        rec_item.setBackground(0, shade)
                        rec_item.setBackground(1, shade)
                        rec_item.setBackground(2, shade)
    
                    # Malý spacing pro child řádky (vyšší řádek)
                    try:
                        from PySide6.QtCore import QSize
                        rec_item.setData(0, Qt.SizeHintRole, QSize(0, 22))
                    except Exception:
                        pass
    
                    # Tooltip s detaily včetně kumulativního podílu
                    if rec_cum_pct is None:
                        tt_pct = "n/a"
                    else:
                        tt_pct = f"{rec_cum_pct} %"
                    tt = f"Hodnota: {value}\nKumulativně: {running_total} ({tt_pct})\nČas: {time_only}\nID: {record_id}"
                    rec_item.setToolTip(0, tt)
                    rec_item.setToolTip(1, tt)
                    rec_item.setToolTip(2, tt)
    
                    # payload pro mazání / reselect
                    rec_item.setData(3, Qt.UserRole, {
                        'date': date_str,
                        'record_id': record_id,
                        'exercise': exercise_type
                    })
    
                    # Re-select po refreshi (pokud byl vybrán)
                    if (date_str, record_id) in preserved:
                        rec_item.setSelected(True)
    
                # Viditelné označení dne (když byl vybrán den, nebo všechny jeho děti)
                sel_children = preserved_children_by_day.get(date_str, set())
                if date_str in preserved_days or (record_count > 0 and len(sel_children) == record_count):
                    day_item.setSelected(True)
    
            # Výchozí chování po PRVNÍM naplnění: vše sbalené
            if first_population:
                tree.collapseAll()
                tree.setProperty("_ever_populated", True)
    
            tree.blockSignals(False)
    
        except Exception as e:
            print(f"Chyba při update_exercise_tab pro {exercise_type}: {e}")
            import traceback
            traceback.print_exc()

    def update_detailed_overview(self, exercise_type, selected_year):
        """Aktualizuje detailní přehled: Den, Týden, Měsíc, Zbytek roku (pro aktuální rok) nebo Roční souhrn (pro jiné roky)."""
        try:
            today = datetime.now().date()
            today_str = today.strftime("%Y-%m-%d")
            current_year = today.year
    
            # Jiný rok -> použij roční souhrn
            if selected_year != current_year:
                self.show_yearly_summary(exercise_type, selected_year, today)
                return
    
            current_date = today
            current_date_str = today_str
    
            # ===== DNES =====
            day_goal = self.calculate_goal(exercise_type, current_date_str)
            day_performed = 0
            if current_date_str in self.data["workouts"] and exercise_type in self.data["workouts"][current_date_str]:
                records = self.data["workouts"][current_date_str][exercise_type]
                if isinstance(records, list):
                    day_performed = sum(r["value"] for r in records)
                elif isinstance(records, dict):
                    day_performed = records.get("value", 0)
    
            day_diff = day_performed - (day_goal if isinstance(day_goal, int) else 0)
            day_status = f"(+{day_diff})" if day_diff >= 0 else str(day_diff)
            day_color = "#32c766" if day_diff >= 0 else "#ff6b6b"
    
            lbl_today = self.findChild(QLabel, f"today_section_{exercise_type}")
            if lbl_today:
                lbl_today.setText(f"📅 DNES ({current_date.strftime('%d.%m.%Y')}): {day_performed}/{day_goal} {day_status}")
                lbl_today.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {day_color}; padding: 5px;")
    
            # Zjisti per-exercise start pro řezání týden/měsíc
            settings = self.get_year_settings(selected_year)
            ex_sd_map = settings.get("exercise_start_dates", {})
            if isinstance(ex_sd_map, dict) and exercise_type in ex_sd_map and ex_sd_map[exercise_type]:
                start_str = ex_sd_map[exercise_type]
            else:
                ex_conf = self.data.get("exercises", {}).get(exercise_type, {})
                sd_map = ex_conf.get("start_dates", {}) if isinstance(ex_conf, dict) else {}
                if isinstance(sd_map, dict) and str(selected_year) in sd_map and sd_map[str(selected_year)]:
                    start_str = sd_map[str(selected_year)]
                else:
                    start_str = settings.get("start_date", f"{selected_year}-01-01")
            ex_start = datetime.strptime(start_str, "%Y-%m-%d").date()
    
            # ===== TÝDEN =====
            week_start = current_date - timedelta(days=current_date.weekday())
            week_end = week_start + timedelta(days=6)
            if week_start < ex_start:
                week_start = ex_start
            if week_end > today:
                week_end = today
    
            week_goal = 0
            week_performed = 0
            d = week_start
            while d <= week_end:
                ds = d.strftime("%Y-%m-%d")
                g = self.calculate_goal(exercise_type, ds)
                if isinstance(g, int):
                    week_goal += g
                if ds in self.data["workouts"] and exercise_type in self.data["workouts"][ds]:
                    recs = self.data["workouts"][ds][exercise_type]
                    week_performed += sum(r["value"] for r in (recs if isinstance(recs, list) else [recs]))
                d += timedelta(days=1)
    
            week_diff = week_performed - week_goal
            lbl_week = self.findChild(QLabel, f"week_section_{exercise_type}")
            if lbl_week:
                lbl_week.setText(f"📆 TÝDEN ({week_start.strftime('%d.%m.')}–{week_end.strftime('%d.%m.')}): {week_performed}/{week_goal} ({'+' if week_diff>=0 else ''}{week_diff})")
                lbl_week.setStyleSheet("font-size: 12px; color: #FFD700; padding: 5px;")
    
            # ===== MĚSÍC =====
            month_start = current_date.replace(day=1)
            next_month = (month_start + timedelta(days=32)).replace(day=1)
            month_end = next_month - timedelta(days=1)
            if month_start < ex_start:
                month_start = ex_start
            if month_end > today:
                month_end = today
    
            month_goal = 0
            month_performed = 0
            d = month_start
            while d <= month_end:
                ds = d.strftime("%Y-%m-%d")
                g = self.calculate_goal(exercise_type, ds)
                if isinstance(g, int):
                    month_goal += g
                if ds in self.data["workouts"] and exercise_type in self.data["workouts"][ds]:
                    recs = self.data["workouts"][ds][exercise_type]
                    month_performed += sum(r["value"] for r in (recs if isinstance(recs, list) else [recs]))
                d += timedelta(days=1)
    
            month_diff = month_performed - month_goal
            lbl_month = self.findChild(QLabel, f"month_section_{exercise_type}")
            if lbl_month:
                lbl_month.setText(f"🗓️ MĚSÍC ({month_start.strftime('%d.%m.')}–{month_end.strftime('%d.%m.')}): {month_performed}/{month_goal} ({'+' if month_diff>=0 else ''}{month_diff})")
                lbl_month.setStyleSheet("font-size: 12px; color: #87CEEB; padding: 5px;")
    
            # ===== ZBYTEK ROKU =====
            year_end = datetime(selected_year, 12, 31).date()
            cur = max(today, ex_start)
            rest_goal = 0
            while cur <= year_end:
                g = self.calculate_goal(exercise_type, cur.strftime("%Y-%m-%d"))
                if isinstance(g, int):
                    rest_goal += g
                cur += timedelta(days=1)
    
            lbl_rest = self.findChild(QLabel, f"year_rest_section_{exercise_type}")
            if lbl_rest:
                lbl_rest.setText(f"🎯 ZBYTEK ROKU ({max(today, ex_start).strftime('%d.%m.')} – {year_end.strftime('%d.%m.%Y')}): {rest_goal}")
                lbl_rest.setStyleSheet("font-size: 12px; color: #32c766; padding: 5px;")
    
            # ===== PROGRESS BAR (aktuální rok do dneška) =====
            total_performed, total_goal, goal_to_date = self.calculate_yearly_progress(exercise_type, selected_year)
            progress_bar = self.findChild(QProgressBar, f"progress_bar_{exercise_type}")
            if progress_bar:
                if goal_to_date > 0:
                    percentage = int((total_performed / goal_to_date) * 100)
                    diff = total_performed - goal_to_date
    
                    progress_bar.setMinimum(0)
                    progress_bar.setMaximum(max(100, percentage))
                    progress_bar.setValue(percentage)
    
                    if diff > 0:
                        progress_bar.setFormat(f"{total_performed}/{goal_to_date} ({percentage}%, +{diff})")
                        progress_bar.setStyleSheet("""
                            QProgressBar {
                                text-align: center;
                                border: 2px solid #0d7377;
                                border-radius: 5px;
                                background-color: #2d2d2d;
                            }
                            QProgressBar::chunk { background-color: #32c766; }
                        """)
                    elif diff == 0:
                        progress_bar.setFormat(f"{total_performed}/{goal_to_date} ({percentage}%)")
                        progress_bar.setStyleSheet("""
                            QProgressBar {
                                text-align: center;
                                border: 2px solid #0d7377;
                                border-radius: 5px;
                                background-color: #2d2d2d;
                            }
                            QProgressBar::chunk { background-color: #FFD700; }
                        """)
                    else:
                        progress_bar.setFormat(f"{total_performed}/{goal_to_date} ({percentage}%, {diff})")
                        progress_bar.setStyleSheet("""
                            QProgressBar {
                                text-align: center;
                                border: 2px solid #0d7377;
                                border-radius: 5px;
                                background-color: #2d2d2d;
                            }
                            QProgressBar::chunk { background-color: #3d3d3d; }
                        """)
                else:
                    progress_bar.setValue(0)
                    progress_bar.setFormat("Žádný cíl k dnešku")
                    progress_bar.setStyleSheet("""
                        QProgressBar {
                            text-align: center;
                            border: 2px solid #0d7377;
                            border-radius: 5px;
                            background-color: #2d2d2d;
                        }
                        QProgressBar::chunk { background-color: #3d3d3d; }
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
            # PER-EXERCISE start: prefer year_settings.exercise_start_dates[exercise_type],
            # then exercises[exercise_type].start_dates[selected_year], else fallback to global start_date
            ex_sd_map = settings.get("exercise_start_dates", {})
            if isinstance(ex_sd_map, dict) and exercise_type in ex_sd_map and ex_sd_map[exercise_type]:
                settings_start_date_str = ex_sd_map[exercise_type]
            else:
                ex_conf = self.data.get("exercises", {}).get(exercise_type, {})
                sd_map = ex_conf.get("start_dates", {}) if isinstance(ex_conf, dict) else {}
                if isinstance(sd_map, dict) and str(selected_year) in sd_map and sd_map[str(selected_year)]:
                    settings_start_date_str = sd_map[str(selected_year)]
                else:
                    settings_start_date_str = settings.get("start_date", f"{selected_year}-01-01")
            settings_start_date = datetime.strptime(settings_start_date_str, "%Y-%m-%d").date()
            year_end = datetime(selected_year, 12, 31).date()
            
            # Pro budoucí rok omezit na dnešek
            if year_end > today:
                year_end = today
            
            # Spočítat celkové statistiky
            total_performed = 0
            total_goal = 0
            days_with_workout = 0
            
            current = max(settings_start_date, datetime(selected_year, 1, 1).date())
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
            
            # Status roku
            if selected_year < today.year:
                year_status = "🕰️ UPLYNULÝ ROK"
                year_color = "#a0a0a0"
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
                year_rest_section.setText(
                    f"✅ Splnění cíle: {percentage}% ({'+' if diff>=0 else ''}{diff}) "
                    f"({settings_start_date.strftime('%d.%m.')} - {year_end.strftime('%d.%m.%Y')})"
                )
                year_rest_section.setStyleSheet("font-size: 12px; color: #FFD700; padding: 5px;")
            
            # Progress bar
            progress_bar = self.findChild(QProgressBar, f"progress_bar_{exercise_type}")
            if progress_bar:
                progress_bar.setMinimum(0)
                progress_bar.setMaximum(max(total_goal, 1))
                progress_bar.setValue(min(total_performed, total_goal))
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
            }
        """)
        layout = QGridLayout()
        layout.setSpacing(6)
        
        first_day = datetime(year, month, 1)
        first_weekday = (first_day.weekday())  # 0=Mon
        last_day = (first_day + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        days_in_month = last_day.day
        today = datetime.now().date()
        
        start_date = self.get_exercise_start_date(exercise_type, year)
        
        row = 1
        col = first_weekday
        for day in range(1, days_in_month + 1):
            date = datetime(year, month, day)
            date_str = date.strftime('%Y-%m-%d')
            
            day_label = QLabel(str(day))
            day_label.setAlignment(Qt.AlignCenter)
            day_label.setMinimumSize(42, 36)
            day_label.setFrameStyle(QFrame.Box)
            
            color, tooltip_text = self.get_day_color_gradient(date_str, date.date(), today, start_date, exercise_type)
            border_style = "border: 2px solid #87CEEB;" if date.date() == today else "border: 1px solid #3d3d3d;"
            day_label.setStyleSheet(f"background-color: {color}; font-weight: bold; {border_style} font-size: 16px;")
            day_label.setToolTip(self._calendar_tooltip_with_contrast(tooltip_text, color))
            
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
            
            settings_start_date = self.get_exercise_start_date(exercise_type, selected_year)
            
            current_date = max(start_date, settings_start_date)
            end_calc_date = min(end_date, today)
            
            while current_date <= end_calc_date:
                date_str = current_date.strftime('%Y-%m-%d')
                goal = self.calculate_goal(exercise_type, date_str)
                if not isinstance(goal, int):
                    goal = int(goal) if goal else 0
                total_days += 1
                
                if date_str in self.data['workouts'] and exercise_type in self.data['workouts'][date_str]:
                    workout_data = self.data['workouts'][date_str][exercise_type]
                    done = sum(r['value'] for r in (workout_data if isinstance(workout_data, list) else [workout_data]))
                    if done >= goal:
                        days_met += 1
                    elif done > 0:
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