#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
import json
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QDoubleSpinBox, 
    QTabWidget, QLabel, QSpinBox, QPushButton, QDateEdit, QTableWidget, QMenu,
    QTableWidgetItem, QGroupBox, QFormLayout, QHeaderView, QMessageBox,
    QGridLayout, QComboBox, QScrollArea, QFrame, QProgressBar, QTextEdit, QTreeWidgetItemIterator, 
    QDialog, QListWidget, QListWidgetItem, QInputDialog, QCheckBox, QFileDialog, QSizePolicy,
    QTreeWidget, QTreeWidgetItem, QLineEdit, QTextBrowser, QAbstractItemView, QRadioButton, QTimeEdit
)
from PySide6.QtCore import Qt, QDate, QTime, QTimer, QSize
from PySide6.QtGui import QColor, QAction, QBrush

# Matplotlib imports
import matplotlib
matplotlib.use('Qt5Agg')
try:
    from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
except ImportError:
    # fallback pro starší Matplotlib/back-end
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.collections import LineCollection
import matplotlib.pyplot as plt

TITLE = "Fitness Tracker"
VERSION = "4.4.2"
APP_VERSION = VERSION
VERSION_DATE = "13.12.2025"

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
    """Dialog pro editaci existujícího záznamu (počet a čas)"""
    def __init__(self, exercise_type, date_str, current_value, timestamp, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Upravit záznam - {exercise_type}")
        self.delete_requested = False
        
        layout = QVBoxLayout(self)
        
        info_label = QLabel(f"Úprava záznamu pro {date_str}")
        info_label.setStyleSheet("font-weight: bold; font-size: 13px; padding: 5px; color: #14919b;")
        layout.addWidget(info_label)
        
        if timestamp:
            time_label = QLabel(f"Původní čas: {timestamp}")
            time_label.setStyleSheet("font-size: 10px; color: #a0a0a0; padding: 2px;")
            layout.addWidget(time_label)
        
        form_layout = QFormLayout()
        
        # Počet
        self.value_spin = QSpinBox()
        self.value_spin.setRange(0, 10000)
        self.value_spin.setValue(int(current_value))
        form_layout.addRow("Počet:", self.value_spin)
        
        # Čas
        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("HH:mm:ss")
        
        # Parse timestamp pro nastavení času (očekává "YYYY-MM-DD HH:MM:SS")
        t = QTime.currentTime()
        if timestamp and " " in timestamp:
            try:
                time_part = timestamp.split(' ')[1]
                t = QTime.fromString(time_part, "HH:mm:ss")
            except:
                pass
        self.time_edit.setTime(t)
        
        form_layout.addRow("Čas:", self.time_edit)
        
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
    
    def get_data(self):
        """Vrátí (nová_hodnota, nový_čas_string)"""
        return self.value_spin.value(), self.time_edit.time().toString("HH:mm:ss")
    
    def delete_record(self):
        self.delete_requested = True
        self.accept()


class FitnessTrackerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{TITLE} v{VERSION} - Sledování cvičení")
        
        # macOS/HiDPI & FullHD fix:
        # Původně 1680x1000, což je na FullHD (1080p) s taskbarem moc.
        # Snižuji minimum, aby šlo okno zmenšit/přizpůsobit.
        self.setMinimumSize(1280, 800)
        self.resize(1440, 900)

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
        self.ensure_body_metrics()

        self.setup_ui()
        self.restore_app_state()

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.auto_refresh)
        self.update_timer.start(5000)

        
    def ensure_body_metrics(self):
        """Zajistí existenci sekce body_metrics pro BMI/váhu."""
        if "body_metrics" not in self.data or not isinstance(self.data["body_metrics"], dict):
            self.data["body_metrics"] = {}
        body = self.data["body_metrics"]

        # Výchozí výška (cm)
        height = body.get("height_cm")
        if not isinstance(height, (int, float)) or height <= 0:
            body["height_cm"] = 180

        # Historie měření váhy
        history = body.get("weight_history")
        if not isinstance(history, list):
            body["weight_history"] = []

    def backup_data_file(self):
        """Vytvoří časovou zálohu JSON dat (do složky backup, udržuje max. 10 posledních)."""
        try:
            if not self.data_file.exists():
                return

            backup_dir = self.data_file.parent / "backup"
            backup_dir.mkdir(parents=True, exist_ok=True)

            ts = datetime.now().strftime("%Y%m%d-%H%M%S")
            backup_path = backup_dir / f"{self.data_file.stem}-{ts}{self.data_file.suffix}"

            with open(self.data_file, "rb") as src, open(backup_path, "wb") as dst:
                dst.write(src.read())

            # ponechat max 10 posledních záloh pro tento soubor
            backups = sorted(
                backup_dir.glob(f"{self.data_file.stem}-*{self.data_file.suffix}"),
                key=lambda p: p.stat().st_mtime,
                reverse=True
            )
            for old in backups[10:]:
                try:
                    old.unlink()
                except Exception:
                    pass

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

        try:
            self.save_data()
        except Exception as e:
            print(f"Chyba při ukládání dat: {e}")

        try:
            # Úplně na závěr: záloha do složky backup/
            self.backup_data_file()
        except Exception as e:
            print(f"Chyba při zálohování dat: {e}")

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
        """Vytvoří UI - dynamické záložky s fixním scrollováním pro cvičení."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
    
        self.tabs = QTabWidget()
        self.tabs.currentChanged.connect(self.on_tab_changed)
        layout.addWidget(self.tabs)
    
        # TabBar chování
        try:
            from PySide6.QtCore import Qt
            from PySide6.QtWidgets import QFrame, QSizePolicy
    
            tb = self.tabs.tabBar()
            tb.setExpanding(False)
            tb.setElideMode(Qt.ElideNone)
            self.tabs.setUsesScrollButtons(True)
            self.tabs.setTabBarAutoHide(False)
        except Exception:
            pass
    
        # ==================== ZÁLOŽKA „Přidat výkon" ====================
        add_widget = self.create_add_workout_tab()
        add_scroll = QScrollArea()
        add_scroll.setWidgetResizable(True)
        add_scroll.setFrameShape(QFrame.NoFrame)
        add_scroll.setStyleSheet("QScrollArea { border: none; background-color: #1e1e1e; }")
        add_scroll.setWidget(add_widget)
        self.tabs.addTab(add_scroll, "Přidat výkon")
    
        # ==================== DYNAMICKÉ ZÁLOŽKY PRO CVIČENÍ (FIX) ====================
        active_exercises = self.get_active_exercises()
        for exercise_id in active_exercises:
            config = self.get_exercise_config(exercise_id)
            icon = config.get("icon", "")
            name = config.get("name", exercise_id.capitalize())
            tab_label = f"{icon} {name}".strip()
    
            # 1. Vytvoříme obsah záložky (layout s kalendářem a grafem)
            ex_widget = self.create_exercise_tab(exercise_id, icon)
            
            # 2. ZÁSADNÍ FIX: Nastavíme PEVNOU MINIMÁLNÍ VELIKOST obsahu.
            #    Tím zabráníme deformaci ("zcvrknutí") kalendáře a grafů.
            #    Pokud je okno menší než toto, objeví se scrollbary.
            #    Hodnoty 1600x900 zajistí, že layout vypadá jako na velkém monitoru.
            ex_widget.setMinimumSize(1600, 900) 
            
            # 3. Vytvoříme ScrollArea
            ex_scroll = QScrollArea()
            # widgetResizable=True dovolí roztažení na VĚTŠÍCH monitorech...
            # ...ale díky setMinimumSize se nikdy nezmenší pod 1600x900 na MENŠÍCH.
            ex_scroll.setWidgetResizable(True) 
            ex_scroll.setFrameShape(QFrame.NoFrame)
            ex_scroll.setStyleSheet("QScrollArea { border: none; background-color: #1e1e1e; }")
            
            ex_scroll.setWidget(ex_widget)
    
            self.tabs.addTab(ex_scroll, tab_label)
    
        # ==================== OSTATNÍ ZÁLOŽKY (beze změny) ====================
        self.tabs.addTab(self.create_bmi_tab(), "BMI + váha")
        self.tabs.addTab(self.create_settings_tab(), "Nastavení")
        self.tabs.addTab(self.create_about_tab(), "O aplikaci")
    
        self.inject_about_updates()


    def create_bmi_tab(self):
        """Záložka pro sledování váhy a výpočet BMI."""
        tab = QWidget()
        main_layout = QHBoxLayout(tab)

        # Levý panel – osobní údaje, nové měření, historie
        left_layout = QVBoxLayout()

        # 📏 Osobní údaje
        personal_group = QGroupBox("📏 Osobní údaje")
        personal_form = QFormLayout()

        self.bmi_height_spin = QSpinBox()
        self.bmi_height_spin.setRange(120, 230)
        body = self.data.get("body_metrics", {})
        height_cm = int(body.get("height_cm", 180))
        if height_cm < 120 or height_cm > 230:
            height_cm = 180
        self.bmi_height_spin.setValue(height_cm)
        personal_form.addRow("Výška (cm):", self.bmi_height_spin)
        personal_group.setLayout(personal_form)
        left_layout.addWidget(personal_group)

        # ⚖️ Nové měření
        measurement_group = QGroupBox("⚖️ Nové měření")
        measurement_layout = QGridLayout()

        # Datum a čas měření
        measurement_layout.addWidget(QLabel("Datum:"), 0, 0)
        self.bmi_date_edit = QDateEdit()
        self.bmi_date_edit.setDate(QDate.currentDate())
        self.bmi_date_edit.setCalendarPopup(True)
        measurement_layout.addWidget(self.bmi_date_edit, 0, 1)

        measurement_layout.addWidget(QLabel("Čas:"), 0, 2)
        self.bmi_time_edit = QTimeEdit()
        self.bmi_time_edit.setTime(QTime.currentTime())
        measurement_layout.addWidget(self.bmi_time_edit, 0, 3)

        # Váha
        measurement_layout.addWidget(QLabel("Váha (kg):"), 1, 0)
        self.bmi_weight_spin = QDoubleSpinBox()
        self.bmi_weight_spin.setRange(40.0, 200.0)
        self.bmi_weight_spin.setSingleStep(0.1)
        self.bmi_weight_spin.setDecimals(1)
        self.bmi_weight_spin.setValue(80.0)
        measurement_layout.addWidget(self.bmi_weight_spin, 1, 1)

        # Aktuální BMI náhled
        self.bmi_current_label = QLabel("BMI: -")
        self.bmi_current_label.setStyleSheet("font-weight: bold;")
        measurement_layout.addWidget(self.bmi_current_label, 1, 2, 1, 2)

        # Uložit měření
        self.bmi_save_button = QPushButton("💾 Uložit měření")
        measurement_layout.addWidget(self.bmi_save_button, 2, 0, 1, 4)

        measurement_group.setLayout(measurement_layout)
        left_layout.addWidget(measurement_group)

        # 📜 Historie měření
        history_group = QGroupBox("📜 Historie měření")
        history_layout = QVBoxLayout()

        self.bmi_history_tree = QTreeWidget()
        self.bmi_history_tree.setColumnCount(5)
        self.bmi_history_tree.setHeaderLabels(["Datum", "Čas", "Váha [kg]", "BMI", "Kategorie"])
        self.bmi_history_tree.setRootIsDecorated(False)
        self.bmi_history_tree.setAlternatingRowColors(True)
        self.bmi_history_tree.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.bmi_history_tree.setEditTriggers(QAbstractItemView.NoEditTriggers)
        header = self.bmi_history_tree.header()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.ResizeToContents)

        # Kontextové menu pro editaci / smazání
        self.bmi_history_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.bmi_history_tree.customContextMenuRequested.connect(self.on_bmi_history_context_menu)

        history_layout.addWidget(self.bmi_history_tree)
        history_group.setLayout(history_layout)
        left_layout.addWidget(history_group, 1)

        main_layout.addLayout(left_layout, 1)

        # Pravý panel – grafy
        right_layout = QVBoxLayout()

        # 📈 Časový graf
        time_group = QGroupBox("📈 Vývoj váhy a BMI")
        time_layout = QVBoxLayout()

        mode_row = QHBoxLayout()
        mode_row.addWidget(QLabel("Režim:"))

        self.bmi_chart_mode_combo = QComboBox()
        self.bmi_chart_mode_combo.addItems(["Váha", "BMI", "Obojí"])
        self.bmi_chart_mode_combo.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.bmi_chart_mode_combo.setMinimumContentsLength(10)
        self.bmi_chart_mode_combo.setMinimumWidth(150)
        # výchozí režim: BMI (požadavek)
        self.bmi_chart_mode_combo.setCurrentText("Obojí")
        mode_row.addWidget(self.bmi_chart_mode_combo)

        mode_row.addSpacing(16)
        mode_row.addWidget(QLabel("Období:"))

        # Přepínání období – Týden / Měsíc / Rok
        self.bmi_period_buttons = {}

        week_btn = QPushButton("📅 Týden")
        week_btn.setCheckable(True)
        week_btn.setFixedWidth(100)
        week_btn.clicked.connect(lambda: self.set_bmi_period_mode("week"))
        mode_row.addWidget(week_btn)
        self.bmi_period_buttons["week"] = week_btn

        month_btn = QPushButton("📆 Měsíc")
        month_btn.setCheckable(True)
        month_btn.setFixedWidth(100)
        month_btn.clicked.connect(lambda: self.set_bmi_period_mode("month"))
        mode_row.addWidget(month_btn)
        self.bmi_period_buttons["month"] = month_btn

        year_btn = QPushButton("📊 Rok")
        year_btn.setCheckable(True)
        year_btn.setFixedWidth(100)
        year_btn.clicked.connect(lambda: self.set_bmi_period_mode("year"))
        mode_row.addWidget(year_btn)
        self.bmi_period_buttons["year"] = year_btn

        mode_row.addStretch()
        time_layout.addLayout(mode_row)

        # Vlastní rozsah Od–Do
        custom_row = QHBoxLayout()
        custom_row.addWidget(QLabel("Vlastní rozsah:"))
        
        # Defaultně posledních 30 dní
        today = QDate.currentDate()
        last_30 = today.addDays(-30)

        self.bmi_custom_from_edit = QDateEdit()
        self.bmi_custom_from_edit.setCalendarPopup(True)
        self.bmi_custom_from_edit.setDate(last_30)
        custom_row.addWidget(self.bmi_custom_from_edit)

        custom_row.addWidget(QLabel("–"))

        self.bmi_custom_to_edit = QDateEdit()
        self.bmi_custom_to_edit.setCalendarPopup(True)
        self.bmi_custom_to_edit.setDate(today)
        custom_row.addWidget(self.bmi_custom_to_edit)

        self.bmi_custom_apply_button = QPushButton("Použít")
        self.bmi_custom_apply_button.clicked.connect(self.apply_bmi_custom_range)
        custom_row.addWidget(self.bmi_custom_apply_button)

        custom_row.addStretch()
        time_layout.addLayout(custom_row)

        # Výchozí mód období: Custom (30 dní)
        self.bmi_period_mode = "custom"
        # Uložíme si proměnné pro custom range, aby update_bmi_time_chart měl co číst
        self.bmi_custom_from_date = last_30
        self.bmi_custom_to_date = today
        
        # Buttons jsou unchecked, protože je to custom
        week_btn.setChecked(False)
        month_btn.setChecked(False)
        year_btn.setChecked(False)

        self.bmi_time_fig = Figure(figsize=(8, 3), facecolor="#121212")
        self.bmi_time_canvas = FigureCanvas(self.bmi_time_fig)
        self.bmi_time_canvas.setStyleSheet("background-color: #121212;")
        time_layout.addWidget(self.bmi_time_canvas)

        time_group.setLayout(time_layout)
        right_layout.addWidget(time_group, 2)

        # 🧪 BMI zóny
        zones_group = QGroupBox("🧪 BMI zóny – přehled")
        zones_layout = QVBoxLayout()\

        self.bmi_zones_fig = Figure(figsize=(8, 2), facecolor="#121212")
        self.bmi_zones_canvas = FigureCanvas(self.bmi_zones_fig)
        self.bmi_zones_canvas.setStyleSheet("background-color: #121212;")
        zones_layout.addWidget(self.bmi_zones_canvas)

        zones_group.setLayout(zones_layout)
        right_layout.addWidget(zones_group, 1)

        main_layout.addLayout(right_layout, 1)

        # Signály
        self.bmi_height_spin.valueChanged.connect(self.on_bmi_height_changed)
        self.bmi_weight_spin.valueChanged.connect(self.update_bmi_current_display)
        self.bmi_date_edit.dateChanged.connect(self.update_bmi_current_display)
        self.bmi_time_edit.timeChanged.connect(self.update_bmi_current_display)
        self.bmi_save_button.clicked.connect(self.add_weight_measurement)
        self.bmi_chart_mode_combo.currentIndexChanged.connect(self.update_bmi_charts)

        # Inicializace
        self.refresh_bmi_history()
        self.update_bmi_current_display()
        self.update_bmi_charts()
        self.update_bmi_time_chart()

        return tab


    def set_bmi_period_mode(self, mode: str):
        """Nastaví období grafu (week/month/year) a přepne tlačítka."""
        if not hasattr(self, "bmi_period_buttons"):
            return

        if mode not in ("week", "month", "year"):
            mode = "month"

        self.bmi_period_mode = mode

        for key, btn in self.bmi_period_buttons.items():
            try:
                btn.setChecked(key == mode)
            except Exception:
                pass

        self.update_bmi_charts()

    def apply_bmi_custom_range(self):
        """Nastaví vlastní datumový rozsah pro graf váhy/BMI."""
        if not hasattr(self, "bmi_custom_from_edit") or not hasattr(self, "bmi_custom_to_edit"):
            return

        d_from = self.bmi_custom_from_edit.date()
        d_to = self.bmi_custom_to_edit.date()

        if d_to < d_from:
            self.show_message(
                "Neplatný rozsah",
                "Datum 'od' nesmí být větší než datum 'do'.",
                QMessageBox.Warning,
            )
            return

        # Ulož rozsah jako QDate, režim 'custom', tlačítka odškrtni
        self.bmi_custom_from_date = d_from
        self.bmi_custom_to_date = d_to
        self.bmi_period_mode = "custom"

        if hasattr(self, "bmi_period_buttons"):
            for btn in self.bmi_period_buttons.values():
                try:
                    btn.setChecked(False)
                except Exception:
                    pass

        self.update_bmi_charts()

    def on_bmi_height_changed(self, value: int):
        """Uložení výšky a aktualizace BMI výpočtů."""
        try:
            if "body_metrics" not in self.data or not isinstance(self.data["body_metrics"], dict):
                self.data["body_metrics"] = {}
            self.data["body_metrics"]["height_cm"] = int(value)
            self.save_data()
        except Exception as e:
            print(f"Chyba při ukládání výšky: {e}")
        self.update_bmi_current_display()
        self.update_bmi_charts()

    def add_weight_measurement(self):
        """Přidá nebo aktualizuje večerní měření váhy (max. jedno na den)."""
        if not hasattr(self, "bmi_weight_spin"):
            return

        body = self.data.get("body_metrics", {})
        height_cm = float(body.get("height_cm", 0))
        weight = float(self.bmi_weight_spin.value())

        if height_cm <= 0 or weight <= 0:
            self.show_message(
                "Neplatné hodnoty",
                "Nastav prosím výšku a váhu větší než 0.",
                QMessageBox.Warning,
            )
            return

        date = self.bmi_date_edit.date()
        time = self.bmi_time_edit.time()

        from datetime import datetime

        dt = datetime(date.year(), date.month(), date.day(), time.hour(), time.minute(), 0)
        date_str = dt.strftime("%Y-%m-%d")
        timestamp_str = dt.strftime("%Y-%m-%d %H:%M:%S")

        if "body_metrics" not in self.data or not isinstance(self.data["body_metrics"], dict):
            self.data["body_metrics"] = {}
        if "weight_history" not in self.data["body_metrics"] or not isinstance(self.data["body_metrics"]["weight_history"], list):
            self.data["body_metrics"]["weight_history"] = []

        history = self.data["body_metrics"]["weight_history"]

        # Max. jedno měření za den – pokud existuje, přepiš
        updated = False
        for entry in history:
            if entry.get("date") == date_str:
                entry["timestamp"] = timestamp_str
                entry["value"] = float(weight)
                updated = True
                break

        if not updated:
            new_entry = {
                "id": str(uuid.uuid4()),
                "timestamp": timestamp_str,
                "date": date_str,
                "value": float(weight),
            }
            history.append(new_entry)

        self.save_data()

        self.refresh_bmi_history()
        self.update_bmi_current_display()
        self.update_bmi_charts()

    def refresh_bmi_history(self):
        """Obnoví strom historie měření BMI/váhy."""
        if not hasattr(self, "bmi_history_tree"):
            return

        self.bmi_history_tree.clear()
        body = self.data.get("body_metrics", {})
        history = body.get("weight_history", [])
        height_cm = float(body.get("height_cm", 0))

        # Setřídit podle timestampu
        try:
            sorted_history = sorted(history, key=lambda e: e.get("timestamp", ""), reverse=True)
        except Exception:
            sorted_history = history

        from datetime import datetime

        for entry in sorted_history:
            ts = entry.get("timestamp")
            try:
                dt = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
            except Exception:
                # Fallback jen na datum
                dt = None

            if dt:
                date_str = dt.strftime("%d.%m.%Y")
                time_str = dt.strftime("%H:%M")
            else:
                date_str = entry.get("date", "")
                time_str = ""

            weight = float(entry.get("value", 0.0))
            bmi = self.calculate_bmi(weight, height_cm) if height_cm > 0 else 0.0
            cat_name, color = self.get_bmi_category(bmi) if bmi > 0 else ("-", None)

            item = QTreeWidgetItem([
                date_str,
                time_str,
                f"{weight:.1f}" if weight > 0 else "-",
                f"{bmi:.1f}" if bmi > 0 else "-",
                cat_name,
            ])

            # Ulož ID záznamu do UserRole (pro edit / delete)
            item.setData(0, Qt.UserRole, entry.get("id"))

            # Zarovnání čas / váha / BMI na střed
            for col in (1, 2, 3):
                item.setTextAlignment(col, Qt.AlignCenter)

            # Barevné označení podle BMI kategorie
            if bmi > 0 and color:
                brush = QBrush(QColor(color))
                for col in range(item.columnCount()):
                    item.setForeground(col, brush)

            self.bmi_history_tree.addTopLevelItem(item)

        self.bmi_history_tree.scrollToBottom()

    def on_bmi_history_context_menu(self, pos):
        """Kontextové menu pro editaci / smazání měření váhy."""
        if not hasattr(self, "bmi_history_tree"):
            return

        # Pozice je ve viewport souřadnicích
        item = self.bmi_history_tree.itemAt(pos)
        if item is None:
            return

        menu = QMenu(self)
        edit_action = menu.addAction("Upravit měření…")
        delete_action = menu.addAction("Smazat měření")

        global_pos = self.bmi_history_tree.viewport().mapToGlobal(pos)
        action = menu.exec_(global_pos)
        if action == edit_action:
            self.edit_weight_measurement(item)
        elif action == delete_action:
            self.delete_weight_measurement(item)

    def edit_weight_measurement(self, item: QTreeWidgetItem):
        """Upraví hodnotu váhy pro daný záznam."""
        entry_id = item.data(0, Qt.UserRole)
        if not entry_id:
            return

        body = self.data.get("body_metrics", {})
        history = body.get("weight_history", [])
        target = None
        for entry in history:
            if entry.get("id") == entry_id:
                target = entry
                break

        if target is None:
            return

        current_weight = float(target.get("value", 0.0))
        new_weight, ok = QInputDialog.getDouble(
            self,
            "Upravit měření",
            "Nová váha (kg):",
            current_weight,
            40.0,
            200.0,
            1,
        )
        if not ok:
            return

        target["value"] = float(new_weight)
        self.save_data()
        self.refresh_bmi_history()
        self.update_bmi_charts()
        self.update_bmi_current_display()

    def delete_weight_measurement(self, item: QTreeWidgetItem):
        """Smaže vybraný záznam měření váhy."""
        entry_id = item.data(0, Qt.UserRole)
        if not entry_id:
            return

        reply = QMessageBox.question(
            self,
            "Smazat měření",
            "Opravdu chceš smazat toto měření váhy?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply != QMessageBox.Yes:
            return

        body = self.data.get("body_metrics", {})
        history = body.get("weight_history", [])
        history = [e for e in history if e.get("id") != entry_id]
        self.data["body_metrics"]["weight_history"] = history
        self.save_data()
        self.refresh_bmi_history()
        self.update_bmi_charts()
        self.update_bmi_current_display()

    def update_bmi_current_display(self):
        """Aktualizuje náhled aktuálního BMI podle zadané váhy a výšky."""
        if not hasattr(self, "bmi_current_label"):
            return

        body = self.data.get("body_metrics", {})
        height_cm = float(body.get("height_cm", 0))
        weight = float(self.bmi_weight_spin.value()) if hasattr(self, "bmi_weight_spin") else 0.0

        if height_cm <= 0 or weight <= 0:
            self.bmi_current_label.setText("BMI: -")
            self.bmi_current_label.setStyleSheet("font-weight: bold; color: #e0e0e0;")
            return

        bmi = self.calculate_bmi(weight, height_cm)
        category, color = self.get_bmi_category(bmi)
        self.bmi_current_label.setText(f"BMI: {bmi:.1f} – {category}")
        self.bmi_current_label.setStyleSheet(f"font-weight: bold; color: {color};")

    def calculate_bmi(self, weight_kg: float, height_cm: float) -> float:
        """Výpočet BMI (kg / m^2), výsledek zaokrouhlený na jedno desetinné místo."""
        if height_cm <= 0:
            return 0.0
        height_m = height_cm / 100.0
        if height_m <= 0:
            return 0.0
        return round(weight_kg / (height_m * height_m), 1)

    def get_bmi_category(self, bmi: float):
        """Vrátí (název, barva) BMI kategorie pro dané BMI."""
        if bmi <= 0:
            return "Nedefinováno", "#e0e0e0"
        if bmi < 18.5:
            return "Podváha", "#4ea5ff"
        if bmi < 25.0:
            return "Normální hmotnost", "#32c766"
        if bmi < 30.0:
            return "Nadváha", "#ffc107"
        if bmi < 35.0:
            return "Obezita I", "#ff7043"
        return "Obezita II+", "#ff1744"

    def get_latest_bmi(self) -> float:
        """Vrátí BMI z posledního měření (nebo 0.0, pokud není k dispozici)."""
        body = self.data.get("body_metrics", {})
        height_cm = float(body.get("height_cm", 0))
        history = body.get("weight_history", [])
        if height_cm <= 0 or not history:
            return 0.0
        try:
            latest = max(history, key=lambda e: e.get("timestamp", ""))
        except Exception:
            latest = history[-1]
        weight = float(latest.get("value", 0.0))
        return self.calculate_bmi(weight, height_cm)

    def update_bmi_charts(self):
        """Aktualizuje oba BMI grafy (časový i zónový)."""
        self.update_bmi_time_chart()
        self.update_bmi_zones_chart()

    def update_bmi_time_chart(self):
        """Časový graf pro váhu a BMI s kalendářním týdnem/měsícem/rokem a vlastním rozsahem.

        Období:
            - 'week'   => pondělí–neděle aktuálního týdne
            - 'month'  => 1. den–poslední den aktuálního měsíce
            - 'year'   => 1.1.–31.12. aktuálního roku
            - 'custom' => rozsah Od–Do nastavený v UI

        Budoucí měření se ignorují.
        Váha = modrá hladká křivka (Catmull-Rom spline).
        BMI = hladká křivka (Catmull-Rom spline), rozdělená na barevné úseky podle BMI zón.
        Horizontální BMI pásy zůstávají.
        Legenda je uvnitř grafu vlevo nahoře.
        """
        if not hasattr(self, "bmi_time_fig") or not hasattr(self, "bmi_time_canvas"):
            return

        # Režim (Váha / BMI / Oba)
        mode = "Váha"
        if hasattr(self, "bmi_chart_mode_combo"):
            mode = self.bmi_chart_mode_combo.currentText()

        from datetime import datetime
        import matplotlib.dates as mdates
        from matplotlib.collections import LineCollection
        import numpy as np
        import matplotlib.pyplot as plt # Potřeba pro Normalize

        today = QDate.currentDate()
        period_mode = getattr(self, "bmi_period_mode", "week")

        # Výpočet kalendářního období (QDate)
        if period_mode == "week":
            # pondělí až neděle aktuálního týdne
            dow = today.dayOfWeek()  # 1 = pondělí
            start_q = today.addDays(-(dow - 1))
            end_q = start_q.addDays(6)
            period_label = f"týden {start_q.toString('dd.MM.yyyy')} – {end_q.toString('dd.MM.yyyy')}"
        elif period_mode == "year":
            start_q = QDate(today.year(), 1, 1)
            end_q = QDate(today.year(), 12, 31)
            period_label = f"rok {today.year()}"
        elif period_mode == "custom" and hasattr(self, "bmi_custom_from_date") and hasattr(self, "bmi_custom_to_date"):
            start_q = self.bmi_custom_from_date
            end_q = self.bmi_custom_to_date
            period_label = f"období {start_q.toString('dd.MM.yyyy')} – {end_q.toString('dd.MM.yyyy')}"
        else:
            # default: měsíc aktuálního dne
            start_q = QDate(today.year(), today.month(), 1)
            end_q = start_q.addMonths(1).addDays(-1)
            period_label = f"měsíc {start_q.toString('MM.yyyy')}"
            period_mode = "month"

        # Konverze na datetime (start 00:00, end 23:59:59)
        start_dt = datetime(start_q.year(), start_q.month(), start_q.day(), 0, 0, 0)
        end_dt = datetime(end_q.year(), end_q.month(), end_q.day(), 23, 59, 59)

        body = self.data.get("body_metrics", {})
        history = body.get("weight_history", [])
        height_cm = float(body.get("height_cm", 0))

        fig = self.bmi_time_fig
        fig.clear()
        fig.patch.set_facecolor("#121212")

        ax_weight = fig.add_subplot(111)
        ax_weight.set_facecolor("#121212")

        # Styling pro dark theme
        def style_axes(ax):
            ax.tick_params(colors="#e0e0e0")
            ax.xaxis.label.set_color("#e0e0e0")
            ax.yaxis.label.set_color("#e0e0e0")
            ax.title.set_color("#e0e0e0")
            for spine in ax.spines.values():
                spine.set_color("#e0e0e0")

        style_axes(ax_weight)

        if not history or height_cm <= 0:
            ax_weight.set_title("Zatím nejsou žádná měření nebo není nastavena výška.")
            ax_weight.set_xlabel("Datum")
            ax_weight.set_ylabel("Hodnota")
            self.bmi_time_canvas.draw()
            return

        now = datetime.now()

        # Připrav platná měření (bez budoucnosti, pouze v daném období)
        all_times: list[datetime] = []
        all_weights: list[float] = []
        all_bmis: list[float] = []

        for entry in sorted(history, key=lambda e: e.get("timestamp", "") or e.get("date", "")):
            ts = entry.get("timestamp")
            dt = None
            if ts:
                try:
                    dt = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
                except Exception:
                    dt = None
            if dt is None:
                date_str = entry.get("date", "")
                try:
                    dt = datetime.strptime(date_str, "%Y-%m-%d")
                except Exception:
                    continue

            if dt > now:
                continue
            if dt < start_dt or dt > end_dt:
                continue

            w = float(entry.get("value", 0.0))
            bmi_val = self.calculate_bmi(w, height_cm)

            all_times.append(dt)
            all_weights.append(w)
            all_bmis.append(bmi_val)

        if not all_times:
            ax_weight.set_title(f"V období {period_label} nejsou žádná měření.")
            ax_weight.set_xlabel("Datum")
            ax_weight.set_ylabel("Hodnota")
            self.bmi_time_canvas.draw()
            return

        ax_weight.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m.%Y"))
        ax_weight.xaxis.set_label_position("bottom")
        ax_weight.xaxis.tick_bottom()
        fig.autofmt_xdate(rotation=30)

        # Osa X přesně na dané období
        ax_weight.set_xlim(start_dt, end_dt)

        times = all_times
        weights = all_weights
        bmis = all_bmis

        # Původní x v číslech (datenum) – použijeme pro váhu i BMI
        xs_raw = [mdates.date2num(t) for t in times]

        # Pomocná funkce pro hladkou křivku (Catmull-Rom spline)
        def smooth_curve(xs_num: list[float], ys_vals: list[float], points_per_segment: int = 20):
            """Vrátí zahuštěné (x,y) body hladké křivky přes zadané body."""
            n = len(xs_num)
            if n < 3:
                # Příliš málo bodů – vrať jen původní data (bez vyhlazení)
                xs_arr = np.array(xs_num, dtype=float)
                ys_arr = np.array(ys_vals, dtype=float)
                return xs_arr, ys_arr

            xs_arr = np.array(xs_num, dtype=float)
            ys_arr = np.array(ys_vals, dtype=float)

            # Body P = (x,y)
            P = np.stack([xs_arr, ys_arr], axis=1)

            result_points = []

            for i in range(n - 1):
                # P0,P1,P2,P3 pro segment mezi P1 a P2
                P1 = P[i]
                P2 = P[i + 1]
                P0 = P[i - 1] if i - 1 >= 0 else P1
                P3 = P[i + 2] if i + 2 < n else P2

                # Parametr t v [0,1]
                if i < n - 2:
                    ts = np.linspace(0.0, 1.0, points_per_segment, endpoint=False)
                else:
                    # poslední segment včetně konce
                    ts = np.linspace(0.0, 1.0, points_per_segment, endpoint=True)

                for t in ts:
                    t2 = t * t
                    t3 = t2 * t
                    # Catmull-Rom: 0.5 * (2P1 + (-P0+P2)t + (2P0-5P1+4P2-P3)t^2 + (-P0+3P1-3P2+P3)t^3)
                    term1 = 2.0 * P1
                    term2 = (-P0 + P2) * t
                    term3 = (2.0 * P0 - 5.0 * P1 + 4.0 * P2 - P3) * t2
                    term4 = (-P0 + 3.0 * P1 - 3.0 * P2 + P3) * t3
                    point = 0.5 * (term1 + term2 + term3 + term4)
                    result_points.append(point)

            result_points = np.array(result_points)
            xs_s = result_points[:, 0]
            ys_s = result_points[:, 1]
            return xs_s, ys_s

        weight_line = None
        bmi_line = None
        ax_bmi = None

        # Váha – hladká křivka (modrá)
        if mode in ("Váha", "Obojí"):
            xs_weight_smooth, weights_smooth = smooth_curve(xs_raw, weights, points_per_segment=20)
            times_weight_smooth = [mdates.num2date(x) for x in xs_weight_smooth]

            (weight_line,) = ax_weight.plot(
                times_weight_smooth,
                weights_smooth,
                linestyle="-",
                linewidth=1.8,
                label="Váha [kg]",
                color="#4ea5ff",
            )
            ax_weight.set_ylabel("Váha [kg]")
            
            # Nastavení limitů osy pro váhu
            min_w = min(weights)
            max_w = max(weights)
            margin_w = max(1.0, (max_w - min_w) * 0.1)
            ax_weight.set_ylim(min_w - margin_w, max_w + margin_w)

        # BMI – hladká křivka, barevné úseky podle BMI zón
        if mode in ("BMI", "Obojí"):
            if mode == "Obojí":
                ax_bmi = ax_weight.twinx()
                ax_bmi.set_facecolor("#121212")
                style_axes(ax_bmi)
                ax_for_bmi = ax_bmi
            else:
                ax_for_bmi = ax_weight

            # Hladká křivka BMI
            xs_bmi_smooth, bmis_smooth = smooth_curve(xs_raw, bmis, points_per_segment=20)

            # Hraniční BMI hodnoty mezi zónami
            zone_thresholds = [18.5, 25.0, 30.0, 35.0]

            segments: list[list[list[float]]] = []
            seg_colors: list[str] = []

            if len(xs_bmi_smooth) > 1:
                for i in range(len(xs_bmi_smooth) - 1):
                    x0, y0 = float(xs_bmi_smooth[i]), float(bmis_smooth[i])
                    x1, y1 = float(xs_bmi_smooth[i + 1]), float(bmis_smooth[i + 1])

                    if y0 == y1:
                        mid_bmi = y0
                        _, col = self.get_bmi_category(mid_bmi)
                        segments.append([[x0, y0], [x1, y1]])
                        seg_colors.append(col)
                        continue

                    # Najdi průsečíky s prahy mezi y0 a y1
                    crossings = []
                    for thr in zone_thresholds:
                        if (y0 < thr < y1) or (y1 < thr < y0):
                            t = (thr - y0) / (y1 - y0)
                            x_thr = x0 + t * (x1 - x0)
                            crossings.append((t, x_thr, thr))

                    crossings.sort(key=lambda c: c[0])

                    points = [(x0, y0)]
                    for _, x_thr, y_thr in crossings:
                        points.append((x_thr, y_thr))
                    points.append((x1, y1))

                    for j in range(len(points) - 1):
                        xa, ya = points[j]
                        xb, yb = points[j + 1]
                        mid_bmi = (ya + yb) / 2.0
                        _, col = self.get_bmi_category(mid_bmi)
                        segments.append([[xa, ya], [xb, yb]])
                        seg_colors.append(col)

                bmi_collection = LineCollection(
                    segments,
                    colors=seg_colors,
                    linewidths=1.6,
                    linestyles="--",
                )
                ax_for_bmi.add_collection(bmi_collection)
                bmi_line = bmi_collection
            else:
                # Jen jeden bod – žádný úsek, BMI čára bude jen bod
                (bmi_line,) = ax_for_bmi.plot(
                    times,
                    bmis,
                    linestyle="--",
                    linewidth=1.6,
                    label="BMI",
                )

            ax_for_bmi.set_ylabel("BMI")

            # Fixní osa Y pro BMI: 20-35 (nebo širší dle dat)
            if len(bmis) > 0:
                real_min = min(bmis)
                real_max = max(bmis)
                target_min = min(20.0, real_min - 0.5)
                target_max = max(35.0, real_max + 0.5)
                ax_for_bmi.set_ylim(target_min, target_max)
        else:
            ax_bmi = None

        # Barevné body podle BMI kategorie (na původních měřeních)
        for t, w, bmi_val in zip(times, weights, bmis):
            _, color = self.get_bmi_category(bmi_val)
            if mode in ("Váha", "Obojí") and weight_line is not None:
                ax_weight.scatter([t], [w], color=color, s=30, zorder=5)
            if mode in ("BMI", "Obojí") and bmi_line is not None:
                target_ax = ax_bmi if ax_bmi is not None else ax_weight
                target_ax.scatter([t], [bmi_val], color=color, s=30, zorder=6)

        # BMI zóny – horizontální pásy
        if mode in ("BMI", "Obojí"):
            target_ax = ax_bmi if ax_bmi is not None else ax_weight
            bmi_zones = [
                (0.0, 18.5, "Podváha", "#4ea5ff"),
                (18.5, 25.0, "Normální", "#32c766"),
                (25.0, 30.0, "Nadváha", "#ffc107"),
                (30.0, 35.0, "Obezita I", "#ff7043"),
                (35.0, 50.0, "Obezita II+", "#ff1744"),
            ]
            for start_b, end_b, label_b, color_b in bmi_zones:
                target_ax.axhspan(start_b, end_b, alpha=0.08, color=color_b)

        # Titulek podle režimu + období
        if mode == "Váha":
            title = "Vývoj váhy"
        elif mode == "BMI":
            title = "Vývoj BMI"
        else:
            title = "Vývoj váhy a BMI"

        title = f"{title} – {period_label}"
        ax_weight.set_title(title)

        # Legenda – jen to, co je skutečně zobrazeno
        legend_handles = []
        legend_labels = []

        if mode in ("Váha", "Obojí") and weight_line is not None:
            legend_handles.append(weight_line)
            legend_labels.append("Váha [kg]")

        if mode in ("BMI", "Obojí") and bmi_line is not None:
            target_ax = ax_bmi if ax_bmi is not None else ax_weight
            dummy_bmi_line, = target_ax.plot(
                [], [],
                linestyle="--",
                linewidth=1.6,
                color="#e0e0e0",
            )
            legend_handles.append(dummy_bmi_line)
            legend_labels.append("BMI")

        if legend_handles:
            # Umístění legendy vlevo nahoře uvnitř grafu (stejně jako v grafu plnění plánu)
            legend = ax_weight.legend(
                legend_handles,
                legend_labels,
                loc="upper right",
                fontsize=8,
                facecolor="#1e1e1e",
                edgecolor="#3d3d3d",
                labelcolor="#e0e0e0"
            )
            legend.get_frame().set_alpha(0.9)

        # Překreslení
        fig.tight_layout()
        self.bmi_time_canvas.draw()

    def update_bmi_zones_chart(self):
        """„Vědecký“ graf BMI zón s vyznačením aktuálního BMI."""
        if not hasattr(self, "bmi_zones_fig") or not hasattr(self, "bmi_zones_canvas"):
            return

        fig = self.bmi_zones_fig
        fig.clear()
        fig.patch.set_facecolor("#121212")

        ax = fig.add_subplot(111)
        ax.set_facecolor("#121212")

        # Rozsah BMI osy
        min_bmi = 10
        max_bmi = 40
        ax.set_xlim(min_bmi, max_bmi)
        ax.set_ylim(0, 1)
        ax.set_yticks([])
        ax.set_xlabel("BMI")
        ax.xaxis.label.set_color("#e0e0e0")
        ax.tick_params(colors="#e0e0e0")
        for spine in ax.spines.values():
            spine.set_color("#e0e0e0")

        zones = [
            (10.0, 18.5, "Podváha", "#4ea5ff"),
            (18.5, 25.0, "Normální", "#32c766"),
            (25.0, 30.0, "Nadváha", "#ffc107"),
            (30.0, 35.0, "Obezita I", "#ff7043"),
            (35.0, 40.0, "Obezita II+", "#ff1744"),
        ]

        for start, end, label, color in zones:
            ax.axvspan(start, end, color=color, alpha=0.4)
            ax.text(
                (start + end) / 2.0,
                0.5,
                label,
                ha="center",
                va="center",
                fontsize=9,
                color="#000000",  # na barevném pruhu černý text je dobře vidět
                fontweight="bold"
            )

        current_bmi = self.get_latest_bmi()
        if current_bmi > 0:
            category, color = self.get_bmi_category(current_bmi)
            x = max(min(current_bmi, max_bmi), min_bmi)
            ax.axvline(x, color=color, linewidth=2)
            ax.text(
                x,
                0.9,
                f"{current_bmi:.1f}",
                ha="center",
                va="bottom",
                fontsize=9,
                color=color,
                fontweight="bold"
            )
            title = f"Poslední BMI: {current_bmi:.1f} – {category}"
        else:
            title = "BMI zóny (zatím žádné měření)"

        ax.set_title(title, color="#e0e0e0")

        self.bmi_zones_canvas.draw()
        
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
            "note": ""
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
        self.apply_add_tab_goals_gradient()
        self.apply_weekly_plan_gradient()

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
                "note": ""
            })

            config = self.get_exercise_config(exercise_id)
            added.append(f"{val}× {config['name']}")

        self.save_data()

        # Aktualizuj všechny záložky + GRAFY
        for exercise in active_exercises:
            self.update_exercise_tab(exercise)
            self.refresh_exercise_calendar(exercise)
            mode = self.chart_modes.get(exercise, "weekly") if hasattr(self, "chart_modes") else "weekly"
            self.update_performance_chart(exercise, mode)

        self.refresh_add_tab_goals()
        self.apply_add_tab_goals_gradient()
        self.apply_weekly_plan_gradient()
        self.show_message("Přidáno", f"Výkony zaznamenány:\n" + "\n".join(added))

        # Reset všech SpinBoxů
        for exercise_id in active_exercises:
            if exercise_id in self.exercise_spinboxes:
                self.exercise_spinboxes[exercise_id].setValue(0)
                
    def _calendar_percent_bg_hex(self, percent: float) -> str:
        """Stejný gradient jako v kalendáři (červená/žlutá/zelená) – mapováno přes % splnění."""
        try:
            p = float(percent)
        except Exception:
            p = 0.0

        # stejné prahy jako kalendář (přesně 100 -> žlutá)
        if p >= 200.0:
            return "#006400"
        if p > 100.0:
            intensity = min((p / 100.0) - 1.0, 1.0)
            green_val = int(144 + (100 - 144) * intensity)  # 144 -> 100
            return f"#{0:02x}{green_val:02x}{0:02x}"
        if abs(p - 100.0) < 1e-9:
            return "#FFD700"
        if p >= 50.0:
            intensity = abs(p - 100.0) / 50.0  # 100..50 => 0..1
            red_val = int(107 + (255 - 107) * (1 - intensity))
            return f"#ff{red_val:02x}{red_val:02x}"
        return "#8B0000"

    def _contrast_text_hex_for_bg(self, bg_hex: str) -> str:
        """Vrátí #000000 / #ffffff podle světlosti pozadí."""
        try:
            from PySide6.QtGui import QColor
            c = QColor(bg_hex)
            if not c.isValid():
                return "#ffffff"
            r = c.red()
            g = c.green()
            b = c.blue()
            # relativní jas (sRGB aproximace)
            lum = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255.0
            return "#000000" if lum > 0.6 else "#ffffff"
        except Exception:
            return "#ffffff"

    def apply_weekly_plan_gradient(self) -> None:
        """Dobarví týdenní rozpis + řádky cviků stejným gradientem jako kalendář (celé řádky)."""
        if not hasattr(self, "bmi_plan_weeks_tree"):
            return

        from PySide6.QtCore import Qt
        from PySide6.QtGui import QColor
        import re
        from datetime import datetime

        tree = self.bmi_plan_weeks_tree
        today = datetime.now().date()
        col_count = tree.columnCount()

        def _apply_row_colors(item, bg_hex: str, fg_hex: str) -> None:
            try:
                bg = QColor(bg_hex)
                fg = QColor(fg_hex)
                for c in range(col_count):
                    item.setBackground(c, bg)
                    item.setForeground(c, fg)
            except Exception:
                pass

        def _parse_percent(txt: str) -> float:
            if not isinstance(txt, str):
                return 0.0
            t = txt.replace("%", "").replace("％", "").strip()
            try:
                return float(t)
            except Exception:
                m = re.search(r"(-?\d+(?:[\.,]\d+)?)", t)
                if not m:
                    return 0.0
                try:
                    return float(m.group(1).replace(",", "."))
                except Exception:
                    return 0.0

        def _week_start_from_label(lbl: str):
            # "Týden X: dd.mm.yyyy – dd.mm.yyyy"
            try:
                m = re.search(r":\s*(\d{2}\.\d{2}\.\d{4})\s*[–-]", lbl)
                if not m:
                    return None
                return datetime.strptime(m.group(1), "%d.%m.%Y").date()
            except Exception:
                return None

        for i in range(tree.topLevelItemCount()):
            week_item = tree.topLevelItem(i)
            if not week_item:
                continue

            week_start = _week_start_from_label(week_item.text(0))
            colorize = (week_start is None) or (week_start <= today)

            percents = []
            for j in range(week_item.childCount()):
                child = week_item.child(j)
                if not child:
                    continue
                p = _parse_percent(child.text(4))
                percents.append(p)

                if colorize:
                    bg_hex = self._calendar_percent_bg_hex(p)
                    fg_hex = self._contrast_text_hex_for_bg(bg_hex)
                    _apply_row_colors(child, bg_hex, fg_hex)

            avg = (sum(percents) / len(percents)) if percents else 0.0

            try:
                week_item.setText(4, f"{avg:.0f} %")
                week_item.setTextAlignment(4, Qt.AlignCenter)
            except Exception:
                pass

            if colorize:
                bg_hex = self._calendar_percent_bg_hex(avg)
                fg_hex = self._contrast_text_hex_for_bg(bg_hex)
                _apply_row_colors(week_item, bg_hex, fg_hex)

    def apply_add_tab_goals_gradient(self) -> None:
        """Gradientní obarvení textu plnění v sekci 'Cíle pro zvolené datum' (stejně jako kalendář)."""
        if not hasattr(self, "add_goals_labels") or not hasattr(self, "add_date_edit"):
            return

        selected_date_str = self.add_date_edit.date().toString("yyyy-MM-dd")

        for exercise_id, label in (self.add_goals_labels or {}).items():
            if not label:
                continue

            goal = self.calculate_goal(exercise_id, selected_date_str)
            try:
                goal_val = float(goal) if goal else 0.0
            except Exception:
                goal_val = 0.0

            current_value = 0.0
            try:
                if selected_date_str in self.data.get("workouts", {}) and exercise_id in self.data["workouts"][selected_date_str]:
                    records = self.data["workouts"][selected_date_str][exercise_id]
                    if isinstance(records, list):
                        current_value = sum(float(r.get("value", 0) or 0) for r in records)
                    elif isinstance(records, dict):
                        current_value = float(records.get("value", 0) or 0)
            except Exception:
                current_value = 0.0

            percent = (current_value / goal_val * 100.0) if goal_val > 0 else 0.0
            color_hex = self._calendar_percent_bg_hex(percent)

            try:
                label.setStyleSheet(
                    f"font-size: 13px; padding: 5px; color: {color_hex}; font-weight: bold;"
                )
            except Exception:
                pass

    def create_add_workout_tab(self):
        """Záložka pro přidávání výkonů - dynamická podle aktivních cvičení + plán k dosažení BMI."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Titulek
        title_label = QLabel("📝 Přidání výkonů")
        layout.addWidget(title_label)

        # Výběr data
        date_row = QHBoxLayout()
        date_row.addWidget(QLabel("Datum:"))
        self.add_date_edit = QDateEdit()
        self.add_date_edit.setDate(QDate.currentDate())
        self.add_date_edit.setCalendarPopup(True)
        self.add_date_edit.dateChanged.connect(self.refresh_add_tab_goals)
        self.add_date_edit.dateChanged.connect(self.apply_add_tab_goals_gradient)
        date_row.addWidget(self.add_date_edit)
        date_row.addStretch()
        layout.addLayout(date_row)

        # ==================== HORNÍ SEKCE (3 sloupce) ====================
        top_sections = QHBoxLayout()

        # ---------- LEVÝ SLOUPEC: Cíle + Zadání výkonu ----------
        left_col_widget = QWidget()
        left_col_layout = QVBoxLayout(left_col_widget)
        left_col_layout.setContentsMargins(0, 0, 0, 0)

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
            if (
                selected_date_str in self.data["workouts"]
                and exercise_id in self.data["workouts"][selected_date_str]
            ):
                records = self.data["workouts"][selected_date_str][exercise_id]
                if isinstance(records, list):
                    current_value = sum(r.get("value", 0) for r in records)
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
        left_col_layout.addWidget(goals_group)

        # Přidávání výkonů - dynamické řádky
        add_group = QGroupBox("➕ Zadat výkon")
        add_layout = QVBoxLayout()
        add_layout.setSpacing(5)  # Menší mezery mezi řádky
        add_layout.setContentsMargins(10, 10, 10, 10)

        # Dynamicky vytvořit řádek pro každé cvičení
        self.exercise_spinboxes = {}

        for exercise_id in active_exercises:
            config = self.get_exercise_config(exercise_id)

            exercise_row = QHBoxLayout()
            exercise_row.setSpacing(8)  # Menší mezery mezi prvky v řádku

            # Label (bez fixní šířky, aby se vešel text)
            label = QLabel(f"{config['icon']} {config['name']}:")
            label.setMinimumWidth(80)  # Místo fixed width
            exercise_row.addWidget(label)

            # SpinBox
            spinbox = QSpinBox()
            spinbox.setRange(0, 10000)
            spinbox.setValue(0)
            spinbox.setFixedWidth(90)
            exercise_row.addWidget(spinbox)
            self.exercise_spinboxes[exercise_id] = spinbox

            # Hlavní tlačítko "Přidat"
            main_btn = QPushButton("Přidat")
            main_btn.setFixedWidth(70)
            main_btn.clicked.connect(
                lambda checked, ex_id=exercise_id: self.add_single_workout(
                    ex_id,
                    self.exercise_spinboxes[ex_id].value(),
                )
            )
            exercise_row.addWidget(main_btn)

            # Rychlá tlačítka
            quick_buttons = config.get("quick_buttons", [10, 20, 30])
            for quick_val in quick_buttons:
                quick_btn = QPushButton(str(quick_val))
                quick_btn.setFixedWidth(40)  # Trochu užší
                quick_btn.clicked.connect(
                    lambda checked, ex_id=exercise_id, val=quick_val: self.add_single_workout(
                        ex_id,
                        val,
                    )
                )
                exercise_row.addWidget(quick_btn)

            exercise_row.addStretch()
            add_layout.addLayout(exercise_row)

        add_group.setLayout(add_layout)
        left_col_layout.addWidget(add_group)

        # Tlačítko pro přidání všeho najednou
        add_all_btn = QPushButton("➕ Přidat všechny výkony najednou")
        add_all_btn.clicked.connect(self.add_all_workouts)
        left_col_layout.addWidget(add_all_btn)

        top_sections.addWidget(left_col_widget)

        # ---------- STŘEDNÍ SLOUPEC: Plán k dosažení BMI ----------
        plan_group = QGroupBox("🎯 Plán k dosažení cílového BMI")
        plan_layout = QVBoxLayout()

        params_row = QHBoxLayout()

        # Začátek plánu – MUSÍ být před „Cílové BMI“
        params_row.addWidget(QLabel("Začátek plánu:"))
        self.bmi_plan_start_date_edit = QDateEdit()
        self.bmi_plan_start_date_edit.setCalendarPopup(True)
        self.bmi_plan_start_date_edit.setDate(QDate.currentDate())

        # Načti uložené datum z app_state (pokud existuje)
        try:
            ds = (self.data.get('app_state', {}) or {}).get('plan_start_date')
            if isinstance(ds, str) and len(ds) >= 10:
                qd = QDate.fromString(ds[:10], "yyyy-MM-dd")
                if qd.isValid():
                    self.bmi_plan_start_date_edit.setDate(qd)
        except Exception:
            pass

        # Signály: auto přepočet + uložení do JSON
        try:
            self.bmi_plan_start_date_edit.dateChanged.connect(self.recompute_bmi_plan)
            self.bmi_plan_start_date_edit.dateChanged.connect(self._persist_plan_start_date)
        except Exception:
            pass

        params_row.addWidget(self.bmi_plan_start_date_edit)

        params_row.addWidget(QLabel("Cílové BMI:"))
        self.bmi_plan_target_spin = QDoubleSpinBox()
        self.bmi_plan_target_spin.setRange(18.5, 25.0)
        self.bmi_plan_target_spin.setSingleStep(0.1)
        self.bmi_plan_target_spin.setDecimals(1)
        self.bmi_plan_target_spin.setValue(22.0)
        params_row.addWidget(self.bmi_plan_target_spin)

        params_row.addSpacing(12)
        params_row.addWidget(QLabel("Horizont:"))
        self.bmi_plan_horizon_combo = QComboBox()
        self.bmi_plan_horizon_combo.addItems(["3 měsíce", "6 měsíců", "12 měsíců"])
        self.bmi_plan_horizon_combo.setCurrentIndex(1)
        params_row.addWidget(self.bmi_plan_horizon_combo)

        params_row.addSpacing(12)
        params_row.addWidget(QLabel("Režim:"))
        self.bmi_plan_mode_combo = QComboBox()
        self.bmi_plan_mode_combo.addItems(["Opatrný", "Střední", "Agresivnější"])
        self.bmi_plan_mode_combo.setCurrentText("Střední")
        params_row.addWidget(self.bmi_plan_mode_combo)

        # === OBNOVENÍ uložených hodnot plánu ===
        try:
            plan_state = (self.data.get('app_state', {}) or {}).get('bmi_plan', {})

            # Cílové BMI
            tb = plan_state.get('target_bmi')
            if isinstance(tb, (int, float)):
                tb = float(tb)
                tb = max(self.bmi_plan_target_spin.minimum(),
                         min(self.bmi_plan_target_spin.maximum(), tb))
                self.bmi_plan_target_spin.setValue(tb)

            # Horizont (podle textu položky)
            hz = plan_state.get('horizon')
            if isinstance(hz, str):
                idx = self.bmi_plan_horizon_combo.findText(hz)
                if idx >= 0:
                    self.bmi_plan_horizon_combo.setCurrentIndex(idx)

            # Režim (podle textu položky)
            md = plan_state.get('mode')
            if isinstance(md, str):
                idx = self.bmi_plan_mode_combo.findText(md)
                if idx >= 0:
                    self.bmi_plan_mode_combo.setCurrentIndex(idx)
        except Exception:
            pass

        # === PERZISTENCE při změně hodnot ===
        try:
            self.bmi_plan_target_spin.valueChanged.connect(self._persist_bmi_plan_settings)
            self.bmi_plan_horizon_combo.currentIndexChanged.connect(self._persist_bmi_plan_settings)
            self.bmi_plan_mode_combo.currentIndexChanged.connect(self._persist_bmi_plan_settings)
        except Exception:
            pass

        params_row.addStretch()

        self.bmi_plan_recompute_button = QPushButton("Přepočítat plán")
        params_row.addWidget(self.bmi_plan_recompute_button)

        plan_layout.addLayout(params_row)

        self.bmi_plan_summary_label = QLabel("")
        self.bmi_plan_summary_label.setWordWrap(True)
        self.bmi_plan_summary_label.setStyleSheet("font-size: 12px; color: #dddddd;")
        plan_layout.addWidget(self.bmi_plan_summary_label)

        # Hlavní tabulka plánu (po cvicích)
        self.bmi_plan_tree = QTreeWidget()
        self.bmi_plan_tree.setColumnCount(4)
        self.bmi_plan_tree.setHeaderLabels(["Cvik", "Doporučeno týdně", "Celkem v období", "Poznámka"])
        self.bmi_plan_tree.setRootIsDecorated(False)
        self.bmi_plan_tree.setAlternatingRowColors(True)
        self.bmi_plan_tree.setMinimumHeight(40)
        header = self.bmi_plan_tree.header()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        plan_layout.addWidget(self.bmi_plan_tree)

        plan_group.setLayout(plan_layout)
        top_sections.addWidget(plan_group)

        # ---------- PRAVÝ SLOUPEC: Týdenní rozpis ----------
        weekly_group = QGroupBox("📅 Týdenní rozpis a plnění plánu")
        weekly_layout = QVBoxLayout()

        self.bmi_plan_weeks_tree = QTreeWidget()
        self.bmi_plan_weeks_tree.setColumnCount(5)
        self.bmi_plan_weeks_tree.setHeaderLabels(
            ["Týden", "Cvik", "Plán (k týdnu)", "Skutečnost (k týdnu)", "Plnění"]
        )
        self.bmi_plan_weeks_tree.setRootIsDecorated(True)
        self.bmi_plan_weeks_tree.setAlternatingRowColors(True)
        self.bmi_plan_weeks_tree.setMinimumHeight(150)
        w_header = self.bmi_plan_weeks_tree.header()
        w_header.setStretchLastSection(False)
        w_header.setSectionResizeMode(0, QHeaderView.Stretch)
        w_header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        w_header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        w_header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        w_header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        weekly_layout.addWidget(self.bmi_plan_weeks_tree)

        weekly_group.setLayout(weekly_layout)
        top_sections.addWidget(weekly_group)

        # Rozdělení šířky 3 sloupců (minimální zásah)
        top_sections.setStretch(0, 2)
        top_sections.setStretch(1, 2)
        top_sections.setStretch(2, 3)

        # Přidat horní sekce do layoutu
        layout.addLayout(top_sections)

        # ==================== GRAF (dole přes celou šířku) ====================
        self.bmi_plan_fig = Figure(figsize=(10, 4), facecolor="#121212")
        self.bmi_plan_canvas = FigureCanvas(self.bmi_plan_fig)
        self.bmi_plan_canvas.setStyleSheet("background-color: #121212;")
        self.bmi_plan_canvas.setMinimumHeight(350)
        self.bmi_plan_canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.bmi_plan_canvas, 1)

        # Signály pro plán
        self.bmi_plan_recompute_button.clicked.connect(self.recompute_bmi_plan)
        self.bmi_plan_target_spin.valueChanged.connect(self.recompute_bmi_plan)
        self.bmi_plan_horizon_combo.currentIndexChanged.connect(self.recompute_bmi_plan)
        self.bmi_plan_mode_combo.currentIndexChanged.connect(self.recompute_bmi_plan)

        self.bmi_plan_target_spin.valueChanged.connect(self.apply_weekly_plan_gradient)
        self.bmi_plan_horizon_combo.currentIndexChanged.connect(self.apply_weekly_plan_gradient)
        self.bmi_plan_mode_combo.currentIndexChanged.connect(self.apply_weekly_plan_gradient)

        # Inicializace plánu (při otevření záložky / aplikace)
        self.recompute_bmi_plan()
        self.apply_weekly_plan_gradient()
        self.apply_add_tab_goals_gradient()

        return widget

    def _persist_bmi_plan_settings(self, *_) -> None:
        """
        Uloží hodnoty Cílové BMI, Horizont a Režim do self.data['app_state']['bmi_plan']
        a hned zapíše na disk přes save_data().
        """
        try:
            self.ensure_app_state()
            plan = dict(self.data.get('app_state', {}).get('bmi_plan', {}))
    
            # Bezpečný odběr hodnot z UI
            target_bmi = float(self.bmi_plan_target_spin.value()) if hasattr(self, 'bmi_plan_target_spin') else None
            horizon = self.bmi_plan_horizon_combo.currentText() if hasattr(self, 'bmi_plan_horizon_combo') else None
            mode = self.bmi_plan_mode_combo.currentText() if hasattr(self, 'bmi_plan_mode_combo') else None
    
            if target_bmi is not None:
                plan['target_bmi'] = target_bmi
            if isinstance(horizon, str) and horizon:
                plan['horizon'] = horizon
            if isinstance(mode, str) and mode:
                plan['mode'] = mode
    
            if 'app_state' not in self.data or not isinstance(self.data['app_state'], dict):
                self.data['app_state'] = {}
            self.data['app_state']['bmi_plan'] = plan
    
            self.save_data()
        except Exception as e:
            # Nechceme blokovat UI kvůli perzistenci
            print(f"_persist_bmi_plan_settings: {e}")

    def _persist_plan_start_date(self, qdate) -> None:
        """
        Uloží vybrané datum 'Začátek plánu' do self.data['app_state']['plan_start_date']
        ve formátu YYYY-MM-DD a okamžitě zapíše do JSON.
        """
        try:
            self.ensure_app_state()
            ds = qdate.toString("yyyy-MM-dd")
            if 'app_state' not in self.data or not isinstance(self.data['app_state'], dict):
                self.data['app_state'] = {}
            self.data['app_state']['plan_start_date'] = ds
            self.save_data()
        except Exception as e:
            # Nechceme brzdit UI kvůli perzistenci
            print(f"_persist_plan_start_date: {e}")
    
    def get_current_weight_and_bmi(self) -> tuple[float | None, float | None, float | None]:
        """Vrátí aktuální váhu, výšku a BMI z posledního měření, nebo (None, None, None).

        Očekává uložení v self.data["body_metrics"] se strukturou:
            {
                "height_cm": float,
                "weight_history": [
                    {"value": kg, "timestamp": "YYYY-MM-DD HH:MM:SS", ...},
                    ...
                ]
            }
        """
        body = self.data.get("body_metrics", {})
        height_cm_raw = body.get("height_cm", 0)
        try:
            height_cm = float(height_cm_raw)
        except (TypeError, ValueError):
            height_cm = 0.0

        if height_cm <= 0:
            return None, None, None

        history = body.get("weight_history", [])
        if not history:
            return None, height_cm, None

        # Najdi poslední záznam podle timestampu (nebo date)
        try:
            latest = max(
                history,
                key=lambda e: e.get("timestamp", "") or e.get("date", ""),
            )
            weight_raw = latest.get("value", 0.0)
            weight = float(weight_raw)
        except Exception:
            return None, height_cm, None

        if weight <= 0:
            return None, height_cm, None

        height_m = height_cm / 100.0
        bmi = weight / (height_m * height_m) if height_m > 0 else None
        return weight, height_cm, bmi

    def get_weekly_exercise_baseline(self, weeks: int = 8) -> dict[str, float]:
        """Spočítá průměrný týdenní objem cvičení podle historie za posledních `weeks` týdnů.

        Vrací mapu:
            {exercise_id: průměrná hodnota za týden}
        """
        workouts = self.data.get("workouts", {})
        if not workouts:
            return {}

        all_dates: list[datetime.date] = []
        for date_str in workouts.keys():
            try:
                d = datetime.strptime(date_str, "%Y-%m-%d").date()
                all_dates.append(d)
            except ValueError:
                continue

        if not all_dates:
            return {}

        max_date = max(all_dates)
        min_date = max_date - timedelta(days=weeks * 7 - 1)

        totals: dict[str, float] = {}

        current = min_date
        while current <= max_date:
            date_key = current.strftime("%Y-%m-%d")
            day_data = workouts.get(date_key)
            if day_data:
                for exercise_id, records in day_data.items():
                    value = 0.0
                    if isinstance(records, list):
                        value = sum(float(r.get("value", 0.0)) for r in records)
                    elif isinstance(records, dict):
                        value = float(records.get("value", 0.0))
                    if value:
                        totals[exercise_id] = totals.get(exercise_id, 0.0) + value
            current += timedelta(days=1)

        period_days = (max_date - min_date).days + 1
        if period_days <= 0:
            return {}

        weeks_effective = max(1.0, period_days / 7.0)

        baseline: dict[str, float] = {
            exercise_id: total / weeks_effective for exercise_id, total in totals.items()
        }
        return baseline

    def recompute_bmi_plan(self, *_):
        """Spočítá a zobrazí plán cvičení k dosažení cílového BMI v záložce „Přidat výkon“."""
        if not hasattr(self, "bmi_plan_tree"):
            return
    
        # Vyčisti předchozí řádky
        self.bmi_plan_tree.clear()
        if hasattr(self, "bmi_plan_weeks_tree"):
            self.bmi_plan_weeks_tree.clear()
        if hasattr(self, "bmi_plan_fig"):
            self.bmi_plan_fig.clear()
    
        weight_now, height_cm, bmi_now = self.get_current_weight_and_bmi()
        if height_cm is None or weight_now is None or bmi_now is None:
            self.bmi_plan_summary_label.setText(
                "Pro výpočet plánu je potřeba mít nastavenou výšku "
                "a alespoň jedno měření váhy v záložce „BMI & váha“."
            )
            if hasattr(self, "bmi_plan_canvas"):
                self.bmi_plan_canvas.draw()
            return
    
        target_bmi = float(self.bmi_plan_target_spin.value())
        height_m = height_cm / 100.0
        weight_target = target_bmi * (height_m * height_m)
        delta_weight = max(0.0, weight_now - weight_target)
    
        # Horizont v týdnech (orientačně)
        horizon_text = self.bmi_plan_horizon_combo.currentText()
        if "3" in horizon_text:
            horizon_weeks = 12
        elif "6" in horizon_text:
            horizon_weeks = 26
        else:
            horizon_weeks = 52
    
        mode_text = self.bmi_plan_mode_combo.currentText()
        # Tohle používáme pro odhad času (text) a pro navýšení objemu
        if mode_text == "Opatrný":
            weekly_loss = 0.35   # kg/týden
            mode_volume_factor = 0.15
        elif mode_text == "Agresivnější":
            weekly_loss = 0.75
            mode_volume_factor = 0.35
        else:
            weekly_loss = 0.5
            mode_volume_factor = 0.25
    
        # Intenzita: porovnání s "referenčním" středním tempem 0.5 kg/týden
        if delta_weight <= 0:
            weeks_needed = 0.0
            loss_in_horizon = 0.0
            intensity_factor = 1.0  # udržovací
        else:
            # Odhad času při zvoleném režimu (pro text)
            weeks_needed = delta_weight / weekly_loss if weekly_loss > 0 else horizon_weeks
            loss_in_horizon = min(delta_weight, weekly_loss * horizon_weeks)
    
            # Referenční doba při středním tempu 0.5 kg/týden
            moderate_loss = 0.5
            if moderate_loss > 0:
                weeks_needed_moderate = delta_weight / moderate_loss
            else:
                weeks_needed_moderate = weeks_needed
    
            # Intenzita = kolikrát rychlejší/pomalejší je zvolený režim vs. střední
            base_intensity = weeks_needed_moderate / weeks_needed if weeks_needed > 0 else 1.0
    
            # Omezit, aby plán nebyl úplně mimo (0.5× až 2×)
            intensity_factor = max(0.5, min(2.0, base_intensity))
    
        predicted_weight = weight_now - loss_in_horizon
        predicted_bmi = predicted_weight / (height_m * height_m) if height_m > 0 else bmi_now
    
        # Textový souhrn
        if delta_weight <= 0:
            summary = (
                f"Aktuální BMI: {bmi_now:.1f} (≈ {weight_now:.1f} kg). "
                f"Nacházíš se v cílové zóně nebo pod ní. Plán je nastaven jako udržovací "
                f"pro horizont {horizon_weeks} týdnů."
            )
        else:
            summary = (
                f"Aktuální BMI: {bmi_now:.1f} (≈ {weight_now:.1f} kg). "
                f"Cílové BMI: {target_bmi:.1f} (≈ {weight_target:.1f} kg).\n"
                f"Při režimu „{mode_text}“ by bylo potřeba přibližně {weeks_needed:.1f} týdne/týdnů "
                f"pro dosažení cíle.\n"
                f"V zvoleném horizontu {horizon_weeks} týdnů se odhaduje, "
                f"že bys mohl/a dosáhnout cca {predicted_weight:.1f} kg (BMI ≈ {predicted_bmi:.1f})."
            )
    
            if intensity_factor > 1.05:
                summary += (
                    f"\nZvolený horizont je kratší než doporučený – plán navyšuje objem cvičení "
                    f"zhruba o {(intensity_factor - 1.0) * 100:.0f} % oproti běžnému režimu."
                )
            elif intensity_factor < 0.95:
                summary += (
                    f"\nZvolený horizont je delší než doporučený – plán volí mírnější tempo "
                    f"(cca {intensity_factor * 100:.0f} % běžného objemu)."
                )
    
        self.bmi_plan_summary_label.setText(summary)
    
        # Základní objem cvičení z historie
        baseline = self.get_weekly_exercise_baseline(weeks=8)
        active_exercises = self.get_active_exercises()
    
        if not baseline and delta_weight > 0:
            self.bmi_plan_summary_label.setText(
                summary
                + "\n\n"
                + "Nebyla nalezena historie výkonů, plán proto používá konzervativní výchozí hodnoty."
            )
    
        # Plánované týdenní hodnoty pro jednotlivé cviky
        planned_weekly: dict[str, float] = {}
    
        for exercise_id in active_exercises:
            config = self.get_exercise_config(exercise_id)
            base_weekly = baseline.get(exercise_id, 0.0)
    
            if base_weekly <= 0:
                # Žádná historie – jemný start, ale škálujeme režimem i intenzitou
                base_value = 1.0 if delta_weight > 0 else 0.5
                weekly_value = base_value * (1.0 + mode_volume_factor) * intensity_factor
                note = "Žádná historie, navrženo jako jemný start."
            else:
                # Základ * (1 + režim) * intenzita (horizont, cílové BMI)
                weekly_value = base_weekly * (1.0 + mode_volume_factor) * intensity_factor
                note = (
                    f"Průměrně {base_weekly:.1f}/týden → režim +{int(mode_volume_factor * 100)} %, "
                    f"intenzita ×{intensity_factor:.2f}."
                )
    
            planned_weekly[exercise_id] = weekly_value
            total_value = weekly_value * horizon_weeks
    
            item = QTreeWidgetItem([
                f"{config['icon']} {config['name']}",
                f"{weekly_value:.1f}",
                f"{total_value:.1f}",
                note,
            ])
            item.setTextAlignment(1, Qt.AlignCenter)
            item.setTextAlignment(2, Qt.AlignCenter)
    
            self.bmi_plan_tree.addTopLevelItem(item)
    
        # Vygenerovat týdenní rozpis a graf plnění plánu
        self.recompute_bmi_weekly_breakdown(active_exercises, planned_weekly, horizon_weeks)

    def recompute_bmi_weekly_breakdown(
        self,
        active_exercises: list[str],
        planned_weekly: dict[str, float],
        horizon_weeks: int,
    ):
        """Vytvoří týdenní rozpis plánu a graf plnění (kumulativně do jednotlivých týdnů)."""
        if not hasattr(self, "bmi_plan_weeks_tree"):
            return

        from datetime import datetime, timedelta
        import matplotlib.dates as mdates
        import matplotlib.pyplot as plt
        from PySide6.QtGui import QColor

        self.bmi_plan_weeks_tree.clear()

        workouts = self.data.get("workouts", {})

        today = datetime.now().date()
        # pondělí aktuálního týdne (nebo start plánu)
        try:
            ds = self.bmi_plan_start_date_edit.date().toString("yyyy-MM-dd")
            week0 = datetime.strptime(ds, "%Y-%m-%d").date()
        except Exception:
            week0 = datetime.now().date()
        monday0 = week0  # Start plánu (nemusí být pondělí, ale pro účely plánu je to "den 0")

        # Pro tabulku chceme "týdenní" pohled (reset každý týden), aby seděl s grafem.
        # Odstraněna kumulace přes celou historii.
        
        weekly_compliance: list[tuple[datetime.date, float]] = []

        for week_idx in range(horizon_weeks):
            week_start = monday0 + timedelta(days=7 * week_idx)
            week_end = week_start + timedelta(days=6)

            # Číslo týdne v plánu
            plan_week_num = week_idx + 1
            week_label = f"Týden {plan_week_num}: {week_start.strftime('%d.%m.%Y')} – {week_end.strftime('%d.%m.%Y')}"
            
            week_item = QTreeWidgetItem([week_label, "", "", "", ""])
            self.bmi_plan_weeks_tree.addTopLevelItem(week_item)

            # Rozbalit, pokud je to aktuální týden
            is_current = (week_start <= today <= week_end)
            week_item.setExpanded(is_current)

            week_percent_sum = 0.0
            week_percent_count = 0

            for exercise_id in active_exercises:
                plan_week = planned_weekly.get(exercise_id, 0.0)

                # Skutečná hodnota v tomto týdnu
                actual_week = 0.0
                day = week_start
                while day <= week_end:
                    key = day.strftime("%Y-%m-%d")
                    day_data = workouts.get(key)
                    if day_data and exercise_id in day_data:
                        # Ošetření proti vnořeným dictům
                        raw_rec = day_data[exercise_id]
                        records = raw_rec
                        if isinstance(raw_rec, dict) and exercise_id in raw_rec:
                             records = raw_rec[exercise_id]

                        if isinstance(records, list):
                            actual_week += sum(float(r.get("value", 0.0)) for r in records)
                        elif isinstance(records, dict):
                            actual_week += float(records.get("value", 0.0))
                    day += timedelta(days=1)

                # Výpočet procenta pro tento týden (nikoliv kumulativně z historie)
                if plan_week > 0:
                    percent = (actual_week / plan_week) * 100.0
                    week_percent_sum += percent
                    week_percent_count += 1
                else:
                    percent = 0.0

                config = self.get_exercise_config(exercise_id)

                child = QTreeWidgetItem([
                    "",
                    f"{config['icon']} {config['name']}",
                    f"{plan_week:.1f}",     # Zobrazení plánu pro tento týden
                    f"{actual_week:.1f}",   # Zobrazení skutečnosti pro tento týden
                    f"{percent:.0f} %",
                ])
                child.setTextAlignment(2, Qt.AlignCenter)
                child.setTextAlignment(3, Qt.AlignCenter)
                child.setTextAlignment(4, Qt.AlignCenter)
                week_item.addChild(child)

            if week_percent_count > 0:
                avg_percent = week_percent_sum / week_percent_count
            else:
                avg_percent = 0.0

            weekly_compliance.append((week_start, avg_percent))

            # Barevné podbarvení týdne (Gradient: Červená -> Zelená)
            # Pokud je týden v budoucnu (celý), nepodbarvujeme, nebo jen šedě.
            # Pokud už začal (week_start <= today), barvíme.
            if week_start <= today:
                p = min(100.0, max(0.0, avg_percent)) / 100.0
                
                if p < 0.5:
                    # Červená (tmavá) -> Žlutá (tmavá)
                    ratio = p / 0.5
                    r = 77
                    g = int(77 * ratio)
                    b = 0
                else:
                    # Žlutá (tmavá) -> Zelená (tmavá)
                    ratio = (p - 0.5) / 0.5
                    r = int(77 * (1 - ratio))
                    g = int(77 - (27 * ratio)) # 77 -> 50 (tmavě zelená)
                    b = 0
                
                bg_color = QColor(r, g, b)
                for c in range(5):
                    week_item.setBackground(c, bg_color)

        # Graf plnění plánu
        if not hasattr(self, "bmi_plan_fig") or not hasattr(self, "bmi_plan_canvas"):
            return

        fig = self.bmi_plan_fig
        fig.clear()
        ax = fig.add_subplot(111)
        ax.set_facecolor("#121212")
        ax.tick_params(colors="#e0e0e0")
        ax.xaxis.label.set_color("#e0e0e0")
        ax.yaxis.label.set_color("#e0e0e0")
        ax.title.set_color("#e0e0e0")
        for spine in ax.spines.values():
            spine.set_color("#e0e0e0")

        if True:
            # === Denní průběh plnění ===
            from collections import defaultdict
            import numpy as _np
            from scipy.interpolate import PchipInterpolator
        
            # 1) Data preparation (same as before)
            daily_totals_by_ex: dict[str, dict[str, float]] = {}
            for exercise_id in active_exercises:
                m: dict[str, float] = defaultdict(float)
                for ds, perday in (workouts or {}).items():
                    recs = perday.get(exercise_id)
                    if isinstance(recs, list):
                        for r in recs:
                            try:
                                m[ds] += float(r.get("value", 0) or 0.0)
                            except Exception:
                                pass
                    elif isinstance(recs, dict):
                        try:
                            m[ds] += float(recs.get("value", 0) or 0.0)
                        except Exception:
                            pass
                daily_totals_by_ex[exercise_id] = m
        
            horizon_days = max(1, int(horizon_weeks) * 7)
            xs_days: list[datetime.date] = []
            ys_days: list[float] = []
        
            start_d = monday0
            end_d = monday0 + timedelta(days=horizon_days - 1)
        
            current_week_start = start_d
            while current_week_start <= end_d:
                current_week_end = min(current_week_start + timedelta(days=6), end_d)
                running_by_ex = {ex: 0.0 for ex in active_exercises}
        
                d = current_week_start
                while d <= current_week_end:
                    ds = d.strftime("%Y-%m-%d")
                    for ex in active_exercises:
                        running_by_ex[ex] += daily_totals_by_ex.get(ex, {}).get(ds, 0.0)
        
                    day_percent_sum = 0.0
                    day_percent_count = 0
                    for ex in active_exercises:
                        plan_week = float(planned_weekly.get(ex, 0.0) or 0.0)
                        if plan_week <= 0.0:
                            percent = 0.0
                        else:
                            percent = (running_by_ex[ex] / plan_week) * 100.0
                        percent = max(0.0, min(200.0, percent))
                        day_percent_sum += percent
                        day_percent_count += 1
        
                    avg_percent = (day_percent_sum / day_percent_count) if day_percent_count else 0.0
                    xs_days.append(d)
                    ys_days.append(avg_percent)
        
                    d += timedelta(days=1)
                current_week_start = current_week_start + timedelta(days=7)
        
            # 2) Plotting
            if xs_days and len(xs_days) > 1:
                xs_nums = mdates.date2num(xs_days)
                ys_nums = _np.array(ys_days)

                x_smooth = _np.linspace(xs_nums.min(), xs_nums.max(), len(xs_nums) * 5)
                try:
                    interpolator = PchipInterpolator(xs_nums, ys_nums)
                    y_smooth = interpolator(x_smooth)
                    line, = ax.plot(x_smooth, y_smooth, color="#14919b", linewidth=2, alpha=0.8, label="Průběh plnění")
                except Exception:
                     line, = ax.plot(xs_nums, ys_nums, color="#14919b", linewidth=2, alpha=0.8, label="Průběh plnění")

                sc = ax.scatter(xs_nums, ys_nums, color="#00e5ff", s=15, zorder=3)

                # === ZVÝRAZNĚNÍ ZAČÁTKŮ TÝDNŮ DLE ROZPISU ===
                # Vykreslíme vertikální čáru pro každý začátek týdne (monday0, monday0+7, ...)
                # Bez ohledu na to, jestli je to kalendářní pondělí.
                week_starts = [monday0 + timedelta(days=7*i) for i in range(horizon_weeks + 1)]
                
                for ws in week_starts:
                    if ws > end_d: break
                    ax.axvline(x=mdates.date2num(ws), color='#555555', linestyle='-', linewidth=1.5, alpha=0.8)
                
                # === ZOBRAZIT KAŽDÝ DEN NA OSE X ===
                ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.'))

                # Pokud je dnů hodně, zmenšíme font nebo proředíme popisky, 
                # ale grid/tiky necháme pro každý den
                if len(xs_days) > 30:
                     # Ponecháme major locator na každý den pro grid, ale formatter jen občas?
                     # Matplotlib to dělá těžko odděleně. 
                     # Uděláme kompromis: Locator každý den, ale popisky rotované a menší font.
                     pass

                # Jemná mřížka pro každý den
                ax.grid(True, which='major', axis='x', color='#2d2d2d', linestyle=':', alpha=0.3)
                
                plt.setp(ax.get_xticklabels(), rotation=90, ha='center', fontsize=8)
                
                # Anotace pro hover
                annot = ax.annotate("", xy=(0,0), xytext=(10,10),textcoords="offset points",
                                    bbox=dict(boxstyle="round", fc="#1e1e1e", ec="#14919b", alpha=0.9),
                                    color="#ffffff", fontsize=9)
                annot.set_visible(False)

                def update_annot(ind):
                    pos = sc.get_offsets()[ind["ind"][0]]
                    annot.xy = pos
                    date_num = pos[0]
                    val = pos[1]
                    date_val = mdates.num2date(date_num)
                    cz_days = ["Po", "Út", "St", "Čt", "Pá", "So", "Ne"]
                    day_name = cz_days[date_val.weekday()]
                    text = f"{day_name} {date_val.strftime('%d.%m.%Y')}\nPlnění: {val:.1f} %"
                    annot.set_text(text)
                    annot.get_bbox_patch().set_alpha(0.9)

                def hover(event):
                    vis = annot.get_visible()
                    if event.inaxes == ax:
                        cont, ind = sc.contains(event)
                        if cont:
                            update_annot(ind)
                            annot.set_visible(True)
                            fig.canvas.draw_idle()
                        else:
                            if vis:
                                annot.set_visible(False)
                                fig.canvas.draw_idle()
                
                fig.canvas.mpl_connect("motion_notify_event", hover)

        ax.axhline(y=100.0, color="#32CD32", linestyle="--", linewidth=1, alpha=0.5, label="Cíl 100 %")
        ax.set_title("Denní průběh plnění plánu (v rámci týdnů)")
        ax.set_ylabel("Plnění [%]")
        # Rozšíření limitů osy X, aby graf vyplnil celý prostor
        if xs_days:
            ax.set_xlim(left=mdates.date2num(start_d), right=mdates.date2num(end_d))
            
        ax.set_ylim(bottom=0, top=max(110, max(ys_days) + 10) if 'ys_days' in locals() and ys_days else 120)
        ax.legend(loc="upper right", fontsize=8, facecolor="#1e1e1e", edgecolor="#3d3d3d", labelcolor="#e0e0e0")
        
        fig.tight_layout()
        self.bmi_plan_canvas.draw()

    def refresh_add_tab_goals(self):
        """Aktualizuje přehled cílů (labels) v záložce Přidat výkon podle vybraného data a přepočítá BMI plán."""
        if not hasattr(self, "add_goals_labels") or not hasattr(self, "add_date_edit"):
            return

        selected_date_str = self.add_date_edit.date().toString("yyyy-MM-dd")

        # 1. Aktualizace cílů pro den (horní box)
        active_exercises = self.get_active_exercises()
        for exercise_id in active_exercises:
            if exercise_id not in self.add_goals_labels:
                continue

            config = self.get_exercise_config(exercise_id)
            goal = self.calculate_goal(exercise_id, selected_date_str)

            current_value = 0
            if (
                selected_date_str in self.data["workouts"]
                and exercise_id in self.data["workouts"][selected_date_str]
            ):
                records = self.data["workouts"][selected_date_str][exercise_id]
                if isinstance(records, list):
                    current_value = sum(r.get("value", 0) for r in records)
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

            lbl = self.add_goals_labels[exercise_id]
            lbl.setText(f"{config['icon']} {config['name']}: {status}")
            lbl.setStyleSheet(f"font-size: 13px; padding: 5px; color: {color}; font-weight: bold;")

        # 2. Automatický refresh BMI plánu a grafu
        self.recompute_bmi_plan()
        
    def expand_today_in_exercise_tree(self, exercise_type):
        """Rozbalí v seznamu záznamů dnešní den (pokud v tree existuje) pro dané cvičení."""
        try:
            tree = self.findChild(QTreeWidget, f"tree_{exercise_type}")
            if not tree:
                return

            today_str = datetime.now().strftime("%Y-%m-%d")

            for i in range(tree.topLevelItemCount()):
                month_item = tree.topLevelItem(i)
                if not month_item:
                    continue

                for j in range(month_item.childCount()):
                    day_item = month_item.child(j)
                    if not day_item:
                        continue

                    payload = day_item.data(3, Qt.UserRole)
                    if isinstance(payload, dict) and payload.get("type") == "day" and payload.get("date") == today_str:
                        month_item.setExpanded(True)
                        day_item.setExpanded(True)
                        try:
                            tree.setCurrentItem(day_item)
                            tree.scrollToItem(day_item)
                        except Exception:
                            pass
                        return
        except Exception as e:
            print(f"Chyba při rozbalení dne v seznamu záznamů: {e}")

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

                    # Nově: při přepnutí na záložku vždy rozbal dnešní den (pokud existuje)
                    self.expand_today_in_exercise_tree(exercise_id)
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
        """Záložka O aplikaci s kompletním helpem a manuálem (rozšířená, podrobnější verze)"""
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
        description = QTextBrowser()
        description.setReadOnly(True)
        description.setStyleSheet("background-color: #2d2d2d; border: 1px solid #3d3d3d; border-radius: 5px; padding: 15px;")
        description.setOpenExternalLinks(True)
    
        about_html = f"""
        <div style='font-size: 13px; line-height: 1.6;'>
          <h2 style='color: #14919b;'>📋 O aplikaci</h2>
          <p>
            <b>Fitness Tracker</b> je desktopová aplikace pro sledování pokroku v&nbsp;cvičení
            s inteligentním doporučením cílů. Umožňuje zaznamenávat denní výkony,
            průběžně hodnotit splnění cílů a vizualizovat výsledky v přehledech.
          </p>
    
          <h3 style='color: #32c766;'>✨ Hlavní funkce</h3>
          <ul>
            <li><b>🧙‍♂️ Smart Year Wizard</b> — průvodce vytvořením roku (analýza historie / level-based režim).</li>
            <li><b>🏋️ Vlastní cvičení</b> — přidávání typů cvičení (název, ikona, rychlá tlačítka).</li>
            <li><b>🗓️ Individuální start</b> — každé cvičení má <i>vlastní datum zahájení</i>, promítá se do grafů i kalendáře.</li>
            <li><b>📈 Grafy výkonu</b> — <i>🕒 Den</i> (kumulativně), 📅 Týden, 📆 Měsíc, 📊 Rok; <i>titulek dynamický</i> dle módu.</li>
            <li><b>📍 Start v grafech</b> — svislá čára „Start“ přesně podle zvoleného cvičení.</li>
            <li><b>↔️ Legenda vpravo</b> — umístěná mimo plochu grafu (žádné překrytí dat).</li>
            <li><b>🧩 Přehled záznamů</b> — strom po dnech, <i>multi-select</i> mazání, kumulativní % vůči dennímu cíli.</li>
            <li><b>📅 Kalendář</b> — barevné značení splnění, adaptivní barva textu při hoveru (čitelná na gradientu).</li>
            <li><b>💾 Export/Import</b> — JSON, migrace se <i>zálohou</i> před úpravou struktury.</li>
          </ul>
    
          <h3 style='color: #32c766;'>🆕 Co je nového</h3>
          <ul>
            <li><b>🕒 Denní graf</b> s kumulativním průběhem dne a čarou <i>Denní cíl</i>.</li>
            <li><b>↔️ Legenda mimo graf</b> — vpravo vedle os; přidána rezerva pravého okraje.</li>
            <li><b>🗓️ Start per-cvičení</b> — nezávislé starty pro cvičení (grafy, kalendář, přehledy).</li>
            <li><b>🧭 Titulek grafu</b> — Den (název dne + datum), Týden (číslo), Měsíc (název + rok), Rok (rok).</li>
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
    
          <h2 style='color: #32c766;'>1) Nastavení roku & startů</h2>
          <ol>
            <li>Otevři <b>⚙️ Nastavení</b> a vyber <b>rok</b> (výchozí je aktuální).</li>
            <li>Pro <b>každé cvičení</b> nastav <b>datum zahájení</b> (volitelné). Grafy i kalendář se dle něj přepočítají.</li>
            <li>Ulož – změny se projeví ihned.</li>
          </ol>
    
          <h2 style='color: #32c766;'>2) Přidávání výkonu</h2>
          <ul>
            <li>V záložce cvičení klikni <b>„Přidat výkon“</b> (pro dnešek) nebo vyber jiné datum.</li>
            <li>Využij <b>rychlá tlačítka</b> (např. +10 / +15 / +20) pro okamžité přidání bez psaní.</li>
            <li>Záznamy se obratem projeví v přehledech, kalendáři i grafu.</li>
          </ul>
    
          <h2 style='color: #32c766;'>3) Přehled, kalendář a graf</h2>
          <ul>
            <li><b>Strom záznamů</b> – seskupeno po dnech; výběr <i>celého dne</i> označí všechny vnitřní záznamy.</li>
            <li><b>Kalendář</b> – barvy splnění; při hoveru se barva textu přizpůsobí pozadí pro čitelnost.</li>
            <li><b>Graf</b> – přepínej tlačítky: <b>🕒 Den</b> / <b>📅 Týden</b> / <b>📆 Měsíc</b> / <b>📊 Rok</b>.</li>
          </ul>
    
          <div style='background-color: #1e1e1e; border: 2px solid #14919b; border-radius: 5px; padding: 12px; margin: 12px 0;'>
            <b>Tip:</b> Denní graf preferuje <i>vybraný den</i> ve stromu. Bez výběru ukáže dnešek (nebo poslední den s daty).
          </div>
    
          <h2 style='color: #32c766;'>4) Export & Import</h2>
          <ul>
            <li><b>Export</b> – uloží JSON (záloha).</li>
            <li><b>Import</b> – načte data; před migrací se vytváří <b>automatická záloha</b>.</li>
          </ul>
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
    
          <h2>Grafy</h2>
          <ul>
            <li><b>🕒 Den</b> – kumulativní křivka v rámci dne; horizontála <i>Denní cíl</i>; osa X v HH:MM; titulek „Název dne + datum“.</li>
            <li><b>📅 Týden</b> – posledních 7 dní; titulek „Týden &lt;číslo&gt;“.</li>
            <li><b>📆 Měsíc</b> – aktuální měsíc (respektuje <i>start cvičení</i>); titulek „Název měsíce + rok“.</li>
            <li><b>📊 Rok</b> – celý rok; svislá čára <i>Start</i> v rozsahu grafu; titulek „Rok &lt;rok&gt;“.</li>
            <li><b>Legenda</b> – vpravo vedle grafu; je vyhrazen pravý okraj (žádné překrytí dat).</li>
          </ul>
    
          <h2>Přehled záznamů (strom)</h2>
          <ul>
            <li><b>Nadpis dne</b> – top-level uzel; kliknutím rozbalíš/sbalíš; výběr označí všechny vnitřní záznamy.</li>
            <li><b>Vnitřní položky</b> – jednotlivé záznamy; multi-select (Shift/Cmd) a hromadné mazání.</li>
            <li><b>% vůči cíli</b> – u vnitřních položek vidíš procento vůči <i>dennímu cíli</i> (může být &gt; 100%).</li>
            <li><b>Kumulativně</b> – součet od první položky dne; barvou zvýrazněno překročení cíle.</li>
          </ul>
    
          <h2>Kalendář</h2>
          <ul>
            <li><b>Barvy</b> – zelená (splněno), žlutá (50–99%), červená (1–49%), šedá (0%).</li>
            <li><b>Hover text</b> – adaptivní barva (na světlém pozadí tmavý text, na tmavém světlý) pro lepší čitelnost.</li>
            <li><b>Začátky</b> – respektuje <i>individuální start</i> cvičení; dny před startem jsou „mimo“.</li>
          </ul>
    
          <h2>Nastavení</h2>
          <ul>
            <li><b>Rok</b> – seznam roků; výběr = filtrace přehledů.</li>
            <li><b>Starty cvičení</b> – nastavíš pro každý typ zvlášť (DatePicker v Nastavení).</li>
            <li><b>Export/Import</b> – JSON záloha/obnova; před migrací se dělá automatická záloha.</li>
          </ul>
    
          <h2>Klávesové zkratky</h2>
          <ul>
            <li><b>Tab</b> – přesun fokusů / záložek</li>
            <li><b>Enter</b> – potvrzení dialogů</li>
            <li><b>Esc</b> – zavření dialogu</li>
            <li><b>Cmd/Ctrl + Click</b> – multi-select položek ve stromu</li>
            <li><b>Shift + Click</b> – souvislý výběr ve stromu</li>
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
    
          <div style='background-color: #1e1e1e; border-left: 4px solid #14919b; padding: 12px; margin: 10px 0;'>
            <h3 style='color: #14919b; margin-top: 0;'>Denní graf mi ukazuje jiný den – proč?</h3>
            <p>Denní graf upřednostní <b>vybraný den</b> ve stromu. Pokud není vybrán, zobrazí <b>dnešek</b> nebo poslední den s daty.</p>
          </div>
    
          <div style='background-color: #1e1e1e; border-left: 4px solid #14919b; padding: 12px; margin: 10px 0;'>
            <h3 style='color: #14919b; margin-top: 0;'>Proč je v ročním/měsíčním grafu svislá čára?</h3>
            <p>Označuje <b>začátek cvičení</b> pro daný typ (nastavíš v Nastavení). Díky tomu vidíš reálný „start“ i při posunutém začátku.</p>
          </div>
    
          <div style='background-color: #1e1e1e; border-left: 4px solid #14919b; padding: 12px; margin: 10px 0;'>
            <h3 style='color: #14919b; margin-top: 0;'>Legenda mi někdy překrývala graf – je to opraveno?</h3>
            <p>Ano. Legenda je nyní <b>vpravo mimo graf</b> a je vyhrazen <b>pravý okraj</b>, takže data nic nepřekrývá.</p>
          </div>
    
          <div style='background-color: #1e1e1e; border-left: 4px solid #14919b; padding: 12px; margin: 10px 0;'>
            <h3 style='color: #14919b; margin-top: 0;'>Jak hromadně smazat záznamy?</h3>
            <p>Ve stromu označ <b>více položek</b> (Cmd/Ctrl + Click nebo Shift + Click) a použij <b>„Smazat vybrané“</b>. Lze označit i <b>celý den</b> (top-level).</p>
          </div>
    
          <div style='background-color: #1e1e1e; border-left: 4px solid #14919b; padding: 12px; margin: 10px 0;'>
            <h3 style='color: #14919b; margin-top: 0;'>Kde jsou data a jak je zálohovat?</h3>
            <p>V souboru <b>fitness_data.json</b>. Použij <b>Export</b> v Nastavení pro zálohu a <b>Import</b> pro obnovu/migraci. Před změnou struktury se dělá automatická záloha.</p>
          </div>
        </div>
        """
        faq_content.setHtml(faq_html)
        faq_scroll.setWidget(faq_content)
        faq_layout.addWidget(faq_scroll)
    
        help_tabs.addTab(faq_widget, "❓ FAQ")
        
        # ==================== TAB: BMI ====================
        bmi_widget = QWidget()
        bmi_layout = QVBoxLayout(bmi_widget)
        
        bmi_scroll = QScrollArea()
        bmi_scroll.setWidgetResizable(True)
        bmi_scroll.setStyleSheet("QScrollArea { border: none; }")
        
        bmi_content = QTextBrowser()
        bmi_content.setOpenExternalLinks(True)
        bmi_content.setStyleSheet("background: #121212; color: #e0e0e0; font-size: 13px;")
        bmi_html = """
        <h2 style='color:#14919b;'>🧮 BMI</h2>
        <p>V této záložce zadáváte <b>měření váhy</b> (datum, hmotnost). Aplikace spočítá <b>BMI</b> podle zadané <b>výšky</b>.</p>
        <ul>
          <li><b>Výška (cm)</b> – nastavte pro korektní BMI.</li>
          <li><b>Nové měření</b> – datum + váha; přidá se do historie.</li>
          <li><b>Graf</b> – přepínač <i>Váha/BMI/Obojí</i>, období <i>Týden/Měsíc/Rok</i>.</li>
          <li><b>Kategorie BMI</b> – informativní, zobrazená vedle hodnot.</li>
        </ul>
        """
        bmi_content.setHtml(bmi_html)
        bmi_scroll.setWidget(bmi_content)
        bmi_layout.addWidget(bmi_scroll)
        
        help_tabs.addTab(bmi_widget, "🧮 BMI")
        
        # ============== TAB: Plán k dosažení cílového BMI ==============
        plan2_widget = QWidget()
        plan2_layout = QVBoxLayout(plan2_widget)
        
        plan2_scroll = QScrollArea()
        plan2_scroll.setWidgetResizable(True)
        plan2_scroll.setStyleSheet("QScrollArea { border: none; }")
        
        plan2_content = QTextBrowser()
        plan2_content.setOpenExternalLinks(True)
        plan2_content.setStyleSheet("background: #121212; color: #e0e0e0; font-size: 13px;")
        plan2_html = """
        <h2 style='color:#14919b;'>🎯 Plán k dosažení cílového BMI</h2>
        <p>Plán sestaví doporučené <b>týdenní objemy</b> pro aktivní cviky.</p>
        <ul>
          <li><b>Začátek plánu</b> – vybírá <b>počáteční den</b>; plán od něj <i>spojitě</i> běží. Hodnota je <b>perzistentní</b>.</li>
          <li><b>Cílové BMI</b>, <b>Horizont</b>, <b>Režim</b> – perzistentní nastavení, změna vyvolá přepočet.</li>
          <li><b>Týdenní rozpis</b> – tabulka po týdnech a cvicích (plán/skutečnost/%).</li>
          <li><b>Graf plnění</b> – <b>denní body</b> v průběhu týdnů + <i>monotónní</i> hladká křivka (stejně jako denní graf výkonu).</li>
        </ul>
        """
        plan2_content.setHtml(plan2_html)
        plan2_scroll.setWidget(plan2_content)
        plan2_layout.addWidget(plan2_scroll)
        
        help_tabs.addTab(plan2_widget, "🎯 Plán k BMI")
    
        # Přidání sub-tabs do hlavního layoutu
        layout.addWidget(help_tabs)
    
        return widget

    def create_settings_tab(self):
        """Záložka s nastavením – per-cvičení startovní data, cíle, přírůstky, správa let + Export/Import."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
    
        # Titulek
        title_label = QLabel("⚙️ Nastavení aplikace")
        layout.addWidget(title_label)
    
        # ==================== SPRÁVA CVIČENÍ ====================
        exercises_group = QGroupBox("🏋️ Správa cvičení")
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
        settings_layout = QVBoxLayout()
    
        grid = QGridLayout()
        grid.setSpacing(10)
    
        # Per-exercise startovní data
        lbl_dates = QLabel("📅 Datum zahájení (pro každé cvičení)")
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
        from PySide6.QtWidgets import QSizePolicy  # lokální import

        chart_group = QGroupBox(f"📊 Graf výkonu - {exercisetype.capitalize()}")
        chart_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # NOVÉ
        chart_layout = QVBoxLayout()

        # Přepínače zobrazení
        mode_buttons_layout = QHBoxLayout()
        mode_buttons_layout.addStretch()

        # Den jako první
        daily_btn = QPushButton("🗓️ Den")
        daily_btn.setCheckable(True)
        daily_btn.setChecked(True)
        daily_btn.setFixedWidth(100)
        daily_btn.clicked.connect(lambda: self.update_performance_chart(exercisetype, "daily"))
        mode_buttons_layout.addWidget(daily_btn)

        weekly_btn = QPushButton("📅 Týden")
        weekly_btn.setCheckable(True)
        weekly_btn.setChecked(False)
        weekly_btn.setFixedWidth(100)
        weekly_btn.clicked.connect(lambda: self.update_performance_chart(exercisetype, "weekly"))
        mode_buttons_layout.addWidget(weekly_btn)

        monthly_btn = QPushButton("📆 Měsíc")
        monthly_btn.setCheckable(True)
        monthly_btn.setFixedWidth(100)
        monthly_btn.clicked.connect(lambda: self.update_performance_chart(exercisetype, "monthly"))
        mode_buttons_layout.addWidget(monthly_btn)

        yearly_btn = QPushButton("📊 Rok")
        yearly_btn.setCheckable(True)
        yearly_btn.setFixedWidth(100)
        yearly_btn.clicked.connect(lambda: self.update_performance_chart(exercisetype, "yearly"))
        mode_buttons_layout.addWidget(yearly_btn)

        mode_buttons_layout.addStretch()
        chart_layout.addLayout(mode_buttons_layout)

        # Celkový součet za zvolené období (aktualizuje se při překreslení grafu)
        total_label = QLabel()
        total_label.setObjectName(f"chart_total_label_{exercisetype}")
        total_label.setStyleSheet("font-size: 12px; color: #e0e0e0; padding: 2px 4px;")
        total_label.setText("Σ Nacvičeno za období: 0")
        total_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)  # NOVÉ
        chart_layout.addWidget(total_label)

        if not hasattr(self, 'chart_total_labels'):
            self.chart_total_labels = {}
        self.chart_total_labels[exercisetype] = total_label

        # Registrace tlačítek
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
        canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # NOVÉ
        chart_layout.addWidget(canvas)
        chart_layout.setStretch(chart_layout.count() - 1, 1)  # NOVÉ: canvas dostane veškerou výšku navíc

        # Uložení reference
        if not hasattr(self, 'chart_canvases'):
            self.chart_canvases = {}
        if not hasattr(self, 'chart_figures'):
            self.chart_figures = {}
        if not hasattr(self, 'chart_modes'):
            self.chart_modes = {}

        self.chart_canvases[exercisetype] = canvas
        self.chart_figures[exercisetype] = fig
        self.chart_modes[exercisetype] = "daily"

        chart_group.setLayout(chart_layout)
        parent_layout.addWidget(chart_group)

        # Iniciální vykreslení
        self.update_performance_chart(exercisetype, "daily")

    def on_calendar_day_clicked(self, exercise_type: str, date_str: str) -> None:
        """Klik na den v kalendáři: uloží vybraný den, sesynchronizuje rok a zobrazí denní graf."""
        try:
            # Pamatuj si vybraný den pro dané cvičení
            if not hasattr(self, "chart_selected_days"):
                self.chart_selected_days = {}
            self.chart_selected_days[exercise_type] = date_str
    
            # Přepni combobox roku (pokud existuje) na rok vybraného dne
            try:
                sel_year = int(date_str[:4])
                combo = None
                if hasattr(self, "exercise_year_selectors"):
                    combo = self.exercise_year_selectors.get(exercise_type)
                if combo is not None:
                    idx = combo.findText(str(sel_year))
                    if idx != -1 and combo.currentIndex() != idx:
                        combo.setCurrentIndex(idx)
            except Exception:
                pass
    
            # Přepni graf do režimu 'daily'
            self.update_performance_chart(exercise_type, "daily")
    
            # (volitelné) obnova kalendáře – pokud máte zvýraznění posledně kliknutého dne
            try:
                if hasattr(self, "refresh_exercise_calendar"):
                    self.refresh_exercise_calendar(exercise_type)
            except Exception:
                pass
        except Exception as e:
            print(f"on_calendar_day_clicked error: {e}")

    def update_performance_chart(self, exercise_type: str, mode: str) -> None:
        """Aktualizuje graf výkonu pro daný typ cvičení a režim (daily/weekly/monthly/yearly)."""
        from datetime import datetime, timedelta
        import matplotlib.dates as mdates

        # Ověření figure/canvas struktur
        if not hasattr(self, "chart_figures") or exercise_type not in self.chart_figures:
            return
        if not hasattr(self, "chart_canvases") or exercise_type not in self.chart_canvases:
            return

        if not hasattr(self, "chart_modes"):
            self.chart_modes = {}
        self.chart_modes[exercise_type] = mode

        # Pomocná funkce pro update sumy nad grafem
        total_label = None
        try:
            if hasattr(self, "chart_total_labels") and exercise_type in self.chart_total_labels:
                total_label = self.chart_total_labels[exercise_type]
        except Exception:
            total_label = None

        def _set_total(val: float) -> None:
            if not total_label:
                return
            try:
                if abs(val - round(val)) < 1e-9:
                    txt_val = str(int(round(val)))
                else:
                    txt_val = f"{val:.2f}"
                total_label.setText(f"Σ Nacvičeno za období: {txt_val}")
            except Exception:
                pass

        # Přepnout stav tlačítek (pokud existují)
        if hasattr(self, "chart_mode_buttons") and exercise_type in self.chart_mode_buttons:
            for btn_mode, btn in self.chart_mode_buttons[exercise_type].items():
                try:
                    btn.setChecked(btn_mode == mode)
                except Exception:
                    pass

        fig = self.chart_figures[exercise_type]
        canvas = self.chart_canvases[exercise_type]
        fig.clear()
        ax = fig.add_subplot(111)
        fig.patch.set_facecolor("#121212")
        ax.set_facecolor("#1e1e1e")

        # Tmavé osy
        ax.tick_params(axis="x", colors="#e0e0e0")
        ax.tick_params(axis="y", colors="#e0e0e0")
        ax.xaxis.label.set_color("#e0e0e0")
        ax.yaxis.label.set_color("#e0e0e0")
        ax.title.set_color("#e0e0e0")
        for spine in ax.spines.values():
            spine.set_color("#e0e0e0")

        today = datetime.now().date()

        # Rok pro dané cvičení (per-exercise combobox)
        if hasattr(self, "exercise_year_selectors") and exercise_type in self.exercise_year_selectors \
                and self.exercise_year_selectors[exercise_type].currentText():
            try:
                selected_year = int(self.exercise_year_selectors[exercise_type].currentText())
            except Exception:
                selected_year = today.year
        else:
            selected_year = today.year

        # CZ popisky
        _CZ_WEEKDAY = {
            0: "Pondělí", 1: "Úterý", 2: "Středa",
            3: "Čtvrtek", 4: "Pátek", 5: "Sobota", 6: "Neděle",
        }
        _CZ_MONTH = {
            1: "Leden", 2: "Únor", 3: "Březen", 4: "Duben", 5: "Květen", 6: "Červen",
            7: "Červenec", 8: "Srpen", 9: "Září", 10: "Říjen", 11: "Listopad", 12: "Prosinec",
        }

        # Začátek cvičení pro „start“ značku
        ys = self.get_year_settings(selected_year) if hasattr(self, "get_year_settings") else {}
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
            from PySide6.QtWidgets import QTreeWidget
            from PySide6.QtCore import Qt

            # 1) Zkusit vybraný den ze stromu / kalendáře
            day_date = None

            # Preferuj den vybraný klikem v kalendáři (pokud existuje)
            try:
                if not hasattr(self, "chart_selected_days"):
                    self.chart_selected_days = {}
                _ds = self.chart_selected_days.get(exercise_type)
                if isinstance(_ds, str) and len(_ds) == 10 and _ds[4] == "-" and _ds[7] == "-":
                    day_date = datetime.strptime(_ds, "%Y-%m-%d").date()
            except Exception:
                pass

            try:
                tree = self.findChild(QTreeWidget, f"tree_{exercise_type}")
                if day_date is None and tree:
                    for it in tree.selectedItems():
                        payload = it.data(3, Qt.UserRole)
                        if isinstance(payload, dict) and "record_id" in payload:
                            continue  # tohle je řádek výkonu, ne den
                        txt = it.text(0) if it is not None else ""
                        ds = txt.split(" ", 1)[1] if " " in txt else txt
                        if len(ds) == 10 and ds[4] == "-" and ds[7] == "-":
                            day_date = datetime.strptime(ds, "%Y-%m-%d").date()
                            break
            except Exception:
                day_date = None

            # 2) Fallback – dnešek nebo poslední den s daty v daném roce
            if day_date is None:
                if selected_year == today.year:
                    day_date = today
                else:
                    days_with_data: list[str] = []
                    for ds, perday in (self.data.get("workouts", {}) or {}).items():
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
                        last_ds = sorted(days_with_data)[-1]
                        try:
                            day_date = datetime.strptime(last_ds, "%Y-%m-%d").date()
                        except Exception:
                            day_date = datetime(selected_year, 1, 1).date()
                    else:
                        day_date = datetime(selected_year, 1, 1).date()

            day_str = day_date.strftime("%Y-%m-%d")

            # Vytahni záznamy pro daný den
            recs: list[dict] = []
            workouts = self.data.get("workouts", {})
            if day_str in workouts and exercise_type in workouts[day_str]:
                raw = workouts[day_str][exercise_type]
                if isinstance(raw, list):
                    recs = raw[:]
                elif isinstance(raw, dict):
                    recs = [raw]

            # (FIX) suma pro den
            try:
                _set_total(sum(float(r.get("value", 0) or 0) for r in recs))
            except Exception:
                _set_total(0.0)

            def _ts_to_dt(ts: str) -> datetime:
                try:
                    if len(ts) >= 19:
                        return datetime.strptime(ts[:19], "%Y-%m-%d %H:%M:%S")
                    if len(ts) >= 16:
                        return datetime.strptime(ts[:16], "%Y-%m-%d %H:%M")
                except Exception:
                    pass
                return datetime.strptime(day_str + " 12:00", "%Y-%m-%d %H:%M")

            recs_sorted = sorted(recs, key=lambda r: _ts_to_dt(r.get("timestamp", f"{day_str} 12:00")))

            # Kumulativní průběh
            times: list[datetime] = []
            cumul: list[float] = []
            running = 0.0
            for r in recs_sorted:
                dt = _ts_to_dt(r.get("timestamp", f"{day_str} 12:00"))
                running += float(r.get("value", 0) or 0)
                times.append(dt)
                cumul.append(running)

            # === NOVÉ: kotva na začátek dne (00:00 -> 0) a plochý úsek do prvního záznamu ===
            if times:
                start_of_day = datetime(day_date.year, day_date.month, day_date.day, 0, 0, 0)
                first_t = times[0]
                if first_t > start_of_day:
                    # vlož 00:00 s 0 a ještě bod těsně před první měřením, aby úsek byl vodorovný
                    t_before = max(start_of_day, first_t - timedelta(seconds=1))
                    times = [start_of_day, t_before] + times
                    cumul = [0.0, 0.0] + cumul

            # Denní cíl
            daily_goal = self.calculate_goal(exercise_type, day_str)
            if not isinstance(daily_goal, (int, float)):
                daily_goal = float(daily_goal) if daily_goal else 0.0

            # --- Monotónní kubická Hermitova interpolace (Fritsch–Carlson) ---
            def smooth_monotone_curve_x(xs_num: list[float], ys_vals: list[float], points_per_segment: int = 30):
                """Hladká křivka Y(X) bez smyček; shape-preserving, monotónní v X."""
                import numpy as _np

                n = len(xs_num)
                if n < 3:
                    return _np.array(xs_num, dtype=float), _np.array(ys_vals, dtype=float)

                x = _np.asarray(xs_num, dtype=float)
                y = _np.asarray(ys_vals, dtype=float)

                # Deduplikace shodných X (ponechá poslední Y)
                xx = [x[0]]
                yy = [y[0]]
                for i in range(1, len(x)):
                    if x[i] == xx[-1]:
                        yy[-1] = y[i]
                    else:
                        xx.append(x[i])
                        yy.append(y[i])
                x = _np.asarray(xx, dtype=float)
                y = _np.asarray(yy, dtype=float)
                n = len(x)
                if n < 3:
                    return x, y

                h = _np.diff(x)
                d = _np.diff(y) / h

                m = _np.empty(n, dtype=float)
                m[0] = d[0]
                m[-1] = d[-1]
                for i in range(1, n - 1):
                    if d[i - 1] == 0.0 or d[i] == 0.0 or (d[i - 1] > 0 and d[i] < 0) or (d[i - 1] < 0 and d[i] > 0):
                        m[i] = 0.0
                    else:
                        w1 = 2.0 * h[i] + h[i - 1]
                        w2 = h[i] + 2.0 * h[i - 1]
                        m[i] = (w1 + w2) / (w1 / d[i - 1] + w2 / d[i])  # vážený harmonický průměr

                for i in range(n - 1):
                    if d[i] == 0.0:
                        m[i] = 0.0
                        m[i + 1] = 0.0
                    else:
                        a = m[i] / d[i]
                        b = m[i + 1] / d[i]
                        if a < 0.0:
                            m[i] = 0.0
                            a = 0.0
                        if b < 0.0:
                            m[i + 1] = 0.0
                            b = 0.0
                        s = a * a + b * b
                        if s > 9.0:
                            t = 3.0 / _np.sqrt(s)
                            m[i] = t * a * d[i]
                            m[i + 1] = t * b * d[i]

                xs_out = []
                ys_out = []
                for i in range(n - 1):
                    xi, xi1 = x[i], x[i + 1]
                    hi = xi1 - xi
                    yi, yi1 = y[i], y[i + 1]
                    mi, mi1 = m[i], m[i + 1]
                    ts = _np.linspace(0.0, 1.0, points_per_segment, endpoint=(i == n - 2))
                    for t in ts:
                        t2 = t * t
                        t3 = t2 * t
                        h00 = 2 * t3 - 3 * t2 + 1
                        h10 = t3 - 2 * t2 + t
                        h01 = -2 * t3 + 3 * t2
                        h11 = t3 - t2
                        xs_out.append(xi + t * hi)
                        ys_out.append(h00 * yi + h10 * hi * mi + h01 * yi1 + h11 * hi * mi1)

                return _np.array(xs_out, dtype=float), _np.array(ys_out, dtype=float)

            if not times:
                ax.text(
                    0.5,
                    0.5,
                    "Žádné záznamy v tomto dni",
                    ha="center",
                    va="center",
                    transform=ax.transAxes,
                    fontsize=14,
                    color="#a0a0a0",
                )
            else:
                xs_raw = [mdates.date2num(dt) for dt in times]
                xs_smooth, cumul_smooth = smooth_monotone_curve_x(xs_raw, cumul, points_per_segment=30)
                times_smooth = [mdates.num2date(x) for x in xs_smooth]

                ax.plot(
                    times_smooth,
                    cumul_smooth,
                    label="Kumulativně (den)",
                    linewidth=2.0,
                    color="#0d7377",
                )
                ax.scatter(times, cumul, color="#0d7377", s=30, zorder=5)

                if daily_goal > 0:
                    ax.axhline(
                        daily_goal,
                        linestyle="--",
                        linewidth=1.8,
                        color="#FFD700",
                        label="Denní cíl",
                    )

                ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
                ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
                ax.xaxis.set_minor_locator(mdates.HourLocator(interval=1))

                start_view = datetime(day_date.year, day_date.month, day_date.day, 0, 0)
                end_view = datetime(day_date.year, day_date.month, day_date.day, 23, 59, 59)
                ax.set_xlim(start_view, end_view)

            dw = _CZ_WEEKDAY[day_date.weekday()]
            ax.set_title(f"Denní vývoj - {exercise_type.capitalize()} ({dw} {day_date.strftime('%Y-%m-%d')})")
            ax.set_xlabel("Čas")
            ax.set_ylabel("Hodnota")

            canvas.draw()
            return

        # =================================================================
        #                 WEEKLY / MONTHLY / YEARLY (BEZE ZMĚNY)
        # =================================================================
        workouts = self.data.get("workouts", {})
        if not workouts:
            _set_total(0.0)
            ax.text(
                0.5,
                0.5,
                "Žádná data",
                ha="center",
                va="center",
                transform=ax.transAxes,
                fontsize=14,
                color="#a0a0a0",
            )
            canvas.draw()
            return

        # Akumulace denních hodnot pro daný rok + cvičení
        from datetime import date as _date  # typová nápověda
        daily_values: dict[_date, float] = {}
        for date_str, perday in workouts.items():
            if not isinstance(date_str, str) or len(date_str) < 10:
                continue
            try:
                dt = datetime.strptime(date_str[:10], "%Y-%m-%d").date()
            except Exception:
                continue
            if dt.year != selected_year:
                continue
            if exercise_type not in perday:
                continue
            records = perday[exercise_type]
            if isinstance(records, list):
                total = sum(float(r.get("value", 0) or 0) for r in records)
            elif isinstance(records, dict):
                total = float(records.get("value", 0) or 0)
            else:
                continue
            daily_values[dt] = daily_values.get(dt, 0.0) + total

        if not daily_values:
            _set_total(0.0)
            ax.text(
                0.5,
                0.5,
                "Žádná data pro zvolený rok",
                ha="center",
                va="center",
                transform=ax.transAxes,
                fontsize=14,
                color="#a0a0a0",
            )
            canvas.draw()
            return

        dates_sorted = sorted(daily_values.keys())

        # Rozsah podle režimu
        if mode == "weekly":
            end_date = today if selected_year == today.year else min(
                datetime(selected_year, 12, 31).date(),
                today,
            )
            start_r = max(end_date - timedelta(days=6), datetime(selected_year, 1, 1).date(), start_date)
            range_start, range_end = start_r, end_date
            xlabel_format = "%d.%m"
        elif mode == "monthly":
            month = today.month if selected_year == today.year else 12
            month_start = datetime(selected_year, month, 1).date()
            next_month = datetime(
                selected_year + (1 if month == 12 else 0),
                1 if month == 12 else month + 1,
                1,
            ).date()
            month_end = next_month - timedelta(days=1)
            month_start = max(month_start, start_date)
            month_end = min(month_end, today)
            range_start, range_end = month_start, month_end
            xlabel_format = "%d.%m"
        else:  # yearly
            year_start = max(datetime(selected_year, 1, 1).date(), start_date)
            year_end = min(datetime(selected_year, 12, 31).date(), today)
            range_start, range_end = year_start, year_end
            xlabel_format = "%d.%m."

        if range_end < range_start:
            _set_total(0.0)
            ax.text(
                0.5,
                0.5,
                "Žádná data k zobrazení",
                ha="center",
                va="center",
                transform=ax.transAxes,
                fontsize=14,
                color="#a0a0a0",
            )
            canvas.draw()
            return

        dates = [range_start + timedelta(days=i) for i in range((range_end - range_start).days + 1)]
        performed: list[float] = []
        goals: list[float] = []
        for d in dates:
            ds = d.strftime("%Y-%m-%d")
            v = 0.0
            if ds in workouts and exercise_type in workouts[ds]:
                recs = workouts[ds][exercise_type]
                if isinstance(recs, list):
                    v = sum(float(r.get("value", 0) or 0) for r in recs)
                elif isinstance(recs, dict):
                    v = float(recs.get("value", 0) or 0)
            g = self.calculate_goal(exercise_type, ds)
            if not isinstance(g, (int, float)):
                g = float(g) if g else 0.0
            performed.append(v)
            goals.append(g)

        # (FIX) suma pro týden/měsíc/rok podle aktuálního rozsahu
        _set_total(sum(performed))

        bar_w = 0.8 if mode == "weekly" else 0.6
        ax.bar(dates, performed, width=bar_w, label="Výkon", color="#0d7377", alpha=0.8)
        ax.plot(dates, goals, label="Cíl", color="#FFD700", linewidth=2, marker="o", markersize=3)

        # Svislá čára začátku cvičení
        if start_date >= dates[0] and start_date <= dates[-1]:
            ax.axvline(
                x=start_date,
                color="#32c766",
                linestyle="--",
                linewidth=2,
                alpha=0.7,
                label="Začátek cvičení",
            )

        # X osa
        if mode == "yearly":
            num_dates = len(dates)
            step = max(1, num_dates // 12)
            ax.set_xticks([dates[i] for i in range(0, num_dates, step)])
            ax.set_xticklabels(
                [dates[i].strftime(xlabel_format) for i in range(0, num_dates, step)],
                rotation=0,
            )
        else:
            ax.set_xticks(dates)
            ax.set_xticklabels(
                [d.strftime(xlabel_format) for d in dates],
                rotation=45 if mode == "monthly" else 0,
            )

        # Titulek
        if mode == "weekly":
            week_no = range_end.isocalendar().week
            ax.set_title(f"Týden {week_no}", fontsize=14)
        elif mode == "monthly":
            month_name = _CZ_MONTH[range_start.month]
            ax.set_title(f"{month_name} {range_start.year}", fontsize=14)
        else:
            ax.set_title(f"Rok {selected_year}", fontsize=14)

        canvas.draw()

    def create_exercise_tab(self, exercise_type, icon):
        """Vytvoří záložku pro konkrétní cvičení - BEZ přidávání (jen layout a tabulka záznamů)."""
        from PySide6.QtWidgets import QHeaderView, QSizePolicy  # lokální import
        widget = QWidget()

        # hlavní layout vertikální (nahoře obsah, dole graf přes celou šířku)
        main_layout = QVBoxLayout(widget)

        # Horní část: dvousloupec (levý panel + pravý panel)
        top_container = QWidget()
        top_layout = QHBoxLayout(top_container)
        top_layout.setContentsMargins(0, 0, 0, 0)

        # ==================== LEVÝ PANEL ====================
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)

        # Year selector layout
        year_selector_layout = QHBoxLayout()
        year_selector_layout.addWidget(QLabel("📅 Zobrazit rok:"))
        year_selector = QComboBox()
        year_selector.setMinimumWidth(80)

        # Naplnění roků
        years = set()
        today = datetime.now().date()
        for k in self.data.get("workouts", {}).keys():
            try:
                d = datetime.strptime(k[:10], "%Y-%m-%d").date()
                years.add(d.year)
            except Exception:
                pass
        if not years:
            years = {today.year}
        years = sorted(years)
        for y in years:
            year_selector.addItem(str(y))

        if not hasattr(self, "exercise_year_selectors"):
            self.exercise_year_selectors = {}
        self.exercise_year_selectors[exercise_type] = year_selector

        year_selector_layout.addWidget(year_selector)
        year_selector_layout.addStretch()
        left_layout.addLayout(year_selector_layout)

        # Přehledové sekce
        goals_frame = QFrame()
        goals_frame.setObjectName(f"goals_frame_{exercise_type}")
        goals_frame.setStyleSheet(
            "QFrame { background-color: #1e1e1e; border: 1px solid #0d7377; border-radius: 5px; }"
        )
        goals_layout = QVBoxLayout(goals_frame)

        today_section = QLabel()
        today_section.setObjectName(f"today_section_{exercise_type}")
        today_section.setStyleSheet("font-size: 12px; color: #87CEEB; padding: 5px;")
        today_section.setWordWrap(True)
        goals_layout.addWidget(today_section)

        week_section = QLabel()
        week_section.setObjectName(f"week_section_{exercise_type}")
        week_section.setStyleSheet("font-size: 12px; color: #87CEEB; padding: 5px;")
        week_section.setWordWrap(True)
        goals_layout.addWidget(week_section)

        month_section = QLabel()
        month_section.setObjectName(f"month_section_{exercise_type}")
        month_section.setStyleSheet("font-size: 12px; color: #87CEEB; padding: 5px;")
        month_section.setWordWrap(True)
        goals_layout.addWidget(month_section)

        # Roční sekce
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

        # Bulk akce
        bulk_actions_layout = QHBoxLayout()
        delete_selected_btn = QPushButton("🗑️ Smazat vybrané")
        delete_selected_btn.clicked.connect(lambda: self.delete_selected_records(exercise_type))
        bulk_actions_layout.addWidget(delete_selected_btn)
        bulk_actions_layout.addStretch()
        left_layout.addLayout(bulk_actions_layout)

        # ==================== TABULKA ZÁZNAMŮ ====================
        tree = QTreeWidget()
        tree.setObjectName(f"tree_{exercise_type}")
        tree.setColumnCount(4)
        tree.setHeaderLabels(["📅 Den", "⏱️ Čas", "💪 Hodnota", "Poznámka"])
        tree.setSelectionMode(QTreeWidget.ExtendedSelection)
        tree.setSortingEnabled(False)

        header = tree.header()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Fixed)
        tree.setColumnHidden(3, True)

        tree.setColumnWidth(0, max(80, tree.columnWidth(0)))
        tree.setColumnWidth(1, max(70, tree.columnWidth(1)))

        tree.setContextMenuPolicy(Qt.CustomContextMenu)
        tree.customContextMenuRequested.connect(
            lambda pos: self.on_exercise_tree_context_menu(pos, tree, exercise_type)
        )

        left_layout.addWidget(tree)
        top_layout.addWidget(left_panel, 1)

        # ==================== PRAVÁ STRANA ====================
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)

        overview_label = QLabel(f"📊 Roční přehled - {exercise_type.capitalize()}")
        overview_label.setStyleSheet(
            "font-size: 14px; font-weight: bold; color: #14919b; padding: 5px;"
        )
        right_layout.addWidget(overview_label)

        legend_layout = QHBoxLayout()
        legend_layout.setSpacing(15)
        legend_layout.setContentsMargins(10, 5, 10, 5)

        def add_legend_item(color: str, text: str) -> None:
            color_box = QLabel()
            color_box.setFixedSize(18, 18)
            color_box.setStyleSheet(
                f"background-color: {color}; border: 1px solid #3d3d3d;"
            )
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
        add_legend_item("#555555", "Necvičil")
        legend_layout.addStretch()
        right_layout.addLayout(legend_layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: #1e1e1e; }")

        scroll_content = QWidget()
        calendar_layout = QVBoxLayout(scroll_content)
        calendar_layout.setContentsMargins(0, 0, 0, 0)
        scroll_content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        calendar_widget = QWidget()
        calendar_widget.setStyleSheet("background-color: #1e1e1e;")
        calendar_inner_layout = QVBoxLayout(calendar_widget)
        calendar_inner_layout.setContentsMargins(0, 0, 0, 0)
        if not hasattr(self, "exercise_calendar_widgets"):
            self.exercise_calendar_widgets = {}
        self.exercise_calendar_widgets[exercise_type] = calendar_inner_layout
        calendar_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        calendar_layout.addWidget(calendar_widget)

        stats_year_label = QLabel()
        stats_year_label.setObjectName(f"stats_year_label_{exercise_type}")
        stats_year_label.setStyleSheet(
            "font-size: 11px; padding: 6px; background-color: #2d2d2d; "
            "color: #e0e0e0; border-radius: 5px;"
        )
        calendar_layout.addWidget(stats_year_label)

        # Graf je pod top_container (přes celou šířku), ne ve scrollu
        scroll.setWidget(scroll_content)
        right_layout.addWidget(scroll, 1)

        top_layout.addWidget(right_panel, 1)

        # původní poměr šířek
        top_layout.setStretch(0, 1)
        top_layout.setStretch(1, 3)

        # přidat horní část do hlavního layoutu
        main_layout.addWidget(top_container, 1)

        # Graf přes celou šířku (pod horními panely)
        self.create_performance_chart(exercise_type, main_layout)

        # Vynucení minimální výšky grafu (Canvasu)
        if hasattr(self, "chart_canvases") and exercise_type in self.chart_canvases:
            canvas = self.chart_canvases[exercise_type]
            canvas.setMinimumHeight(350)

        # ZMĚNA: bezpečný kompromis – graf může růst, ale horní část se nezhroutí
        main_layout.setStretch(0, 1)
        main_layout.setStretch(1, 1)

        # Refresh záložky a kalendáře
        self.update_exercise_tab(exercise_type)
        self.refresh_exercise_calendar(exercise_type)

        return widget
    
    def on_exercise_tree_context_menu(self, pos, tree, exercise_type):
        """Zobrazí kontextové menu pro záznamy ve stromu cvičení."""
        item = tree.itemAt(pos)
        if not item:
            return

        menu = QMenu(self)
        
        # Načti metadata pro identifikaci
        payload = item.data(3, Qt.UserRole)
        
        # Zjistíme typ
        item_type = "unknown"
        if isinstance(payload, dict):
            item_type = payload.get("type", "unknown")
        
        if item_type == "record":
            # == MENU PRO ZÁZNAM ==
            edit_action = menu.addAction("✏️ Upravit záznam")
            delete_action = menu.addAction("🗑️ Smazat záznam")
            
            action = menu.exec_(tree.viewport().mapToGlobal(pos))
            
            if action == edit_action:
                self.edit_workout(exercise_type, payload["date"], payload["record_id"])
            elif action == delete_action:
                reply = QMessageBox.question(
                    self, "Smazat záznam", "Opravdu smazat tento záznam?",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    date_str = payload["date"]
                    rec_id = payload["record_id"]
                    if date_str in self.data["workouts"] and exercise_type in self.data["workouts"][date_str]:
                        recs = self.data["workouts"][date_str][exercise_type]
                        if isinstance(recs, list):
                            self.data["workouts"][date_str][exercise_type] = [r for r in recs if r["id"] != rec_id]
                            # Clean up
                            if not self.data["workouts"][date_str][exercise_type]:
                                del self.data["workouts"][date_str][exercise_type]
                            if not self.data["workouts"][date_str]:
                                del self.data["workouts"][date_str]
                                
                            self.save_data()
                            self.update_exercise_tab(exercise_type)
                            self.refresh_exercise_calendar(exercise_type)
                            if exercise_type in self.chart_modes:
                                self.update_performance_chart(exercise_type, self.chart_modes[exercise_type])
                            self.show_message("Smazáno", "Záznam byl odstraněn.")
        
        elif item_type == "day":
            # == MENU PRO DEN ==
            delete_day_action = menu.addAction("🗑️ Smazat všechny záznamy dne")
            
            action = menu.exec_(tree.viewport().mapToGlobal(pos))
            
            if action == delete_day_action:
                date_str = payload.get("date")
                if not date_str: 
                    # Fallback parsing z textu, kdyby payload chyběl
                    txt = item.text(0)
                    date_str = txt.split(" ", 1)[1] if " " in txt else txt

                reply = QMessageBox.question(
                    self, "Smazat den", f"Opravdu smazat všechny záznamy z {date_str}?",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    if date_str in self.data["workouts"] and exercise_type in self.data["workouts"][date_str]:
                        del self.data["workouts"][date_str][exercise_type]
                        if not self.data["workouts"][date_str]:
                            del self.data["workouts"][date_str]
                            
                        self.save_data()
                        self.update_exercise_tab(exercise_type)
                        self.refresh_exercise_calendar(exercise_type)
                        if exercise_type in self.chart_modes:
                            self.update_performance_chart(exercise_type, self.chart_modes[exercise_type])
                        self.show_message("Smazáno", "Záznamy dne byly odstraněny.")
                        
        else:
            # Měsíc nebo jiné - zatím nic
            pass

    def ensure_exercise_chart_expands(self, exercise_type: str) -> None:
        """
        Zajistí, aby 'Graf výkonu' (FigureCanvas) pro dané cvičení vertikálně vyplnil zbývající prostor.
        Nemění architekturu ani vzhled; pouze nastaví SizePolicy a stretch v existujících layoutech.
        Bezpečně (try/except) – pokud něco nenajde, UI to nerozbije.
        """
        try:
            from PySide6.QtWidgets import QWidget, QSizePolicy, QBoxLayout, QGridLayout
    
            canvas = None
            try:
                canvas = self.chart_canvases.get(exercise_type) if hasattr(self, "chart_canvases") else None
            except Exception:
                canvas = None
            if canvas is None or not isinstance(canvas, QWidget):
                return
    
            # 1) Canvas a jeho rodiče musí být Expanding (V i H)
            def set_expanding(w: QWidget) -> None:
                try:
                    sp = w.sizePolicy()
                    sp.setVerticalPolicy(QSizePolicy.Expanding)
                    sp.setHorizontalPolicy(QSizePolicy.Expanding)
                    w.setSizePolicy(sp)
                except Exception:
                    pass
    
            set_expanding(canvas)
            parent = canvas.parentWidget()
            if parent:
                set_expanding(parent)
                gparent = parent.parentWidget()
                if gparent:
                    set_expanding(gparent)
    
            # 2) Zvýšit stretch řádku/polohy, kde canvas leží, v nejbližším rodičovském layoutu
            lay = parent.layout() if (parent and parent.layout()) else None
            if lay is not None:
                try:
                    idx = lay.indexOf(canvas)
                    if idx != -1:
                        if isinstance(lay, QBoxLayout):
                            lay.setStretch(idx, 1)  # graf = “elastic”
                        elif isinstance(lay, QGridLayout):
                            r, c, rs, cs = lay.getItemPosition(idx)
                            lay.setRowStretch(r, 1)
                except Exception:
                    pass
    
            # 3) (Volitelné) Snížit stretch u kalendářové části, pokud sdílí stejný layout
            #    Tohle nechávám vypnuté – bez znalosti konkrétní hierarchie by to bylo moc odvážné.
            #    Pokud mi pošlete přesně funkci s layoutem, nastavím i okolní streče “na míru”.
    
        except Exception as e:
            print(f"ensure_exercise_chart_expands error: {e}")

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
        tree = self.findChild(QTreeWidget, f"tree_{exercise_type}")
        if not tree:
            self.show_message("Chyba", "Strom záznamů nebyl nalezen.", QMessageBox.Warning)
            return
    
        selected_items = tree.selectedItems()
        if not selected_items:
            self.show_message("Informace", "Nejprve vyber záznam(y) ke smazání.", QMessageBox.Information)
            return
    
        # Pomocná funkce pro sběr ID z itemu (a jeho dětí)
        to_delete = []  # list[(date_str, record_id)]
        
        def collect_records(item):
            payload = item.data(3, Qt.UserRole)
            if isinstance(payload, dict):
                itype = payload.get("type")
                if itype == "record":
                    to_delete.append((payload["date"], payload["record_id"]))
                elif itype == "day" or itype == "month":
                    # Je to kontejner, projdi děti
                    for i in range(item.childCount()):
                        collect_records(item.child(i))
            else:
                # Fallback kdyby payload chyběl, zkus děti
                for i in range(item.childCount()):
                    collect_records(item.child(i))

        for item in selected_items:
            collect_records(item)
    
        # Dedup
        to_delete = list({(d, r) for (d, r) in to_delete})
    
        if not to_delete:
            self.show_message("Informace", "Nebyly nalezeny žádné záznamy ke smazání.", QMessageBox.Information)
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
            if date_str in self.data["workouts"] and exercise_type in self.data["workouts"][date_str]:
                records = self.data["workouts"][date_str][exercise_type]
                if isinstance(records, list):
                    self.data["workouts"][date_str][exercise_type] = [r for r in records if r.get("id") != record_id]
                    if not self.data["workouts"][date_str][exercise_type]:
                        del self.data["workouts"][date_str][exercise_type]
                    if not self.data["workouts"][date_str]:
                        del self.data["workouts"][date_str]
                elif isinstance(records, dict):
                    if records.get("id") == record_id:
                        del self.data["workouts"][date_str][exercise_type]
                        if not self.data["workouts"][date_str]:
                            del self.data["workouts"][date_str]
    
        self.save_data()
    
        # Refresh UI
        self.update_exercise_tab(exercise_type)
        self.refresh_exercise_calendar(exercise_type)
        if exercise_type in self.chart_modes:
            self.update_performance_chart(exercise_type, self.chart_modes[exercise_type])
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
        """Upraví konkrétní záznam (počet i čas) pomocí dialogu"""
        if date_str not in self.data['workouts'] or exercise_type not in self.data['workouts'][date_str]:
            self.show_message("Chyba", "Záznam nenalezen!", QMessageBox.Critical)
            return
        
        records = self.data['workouts'][date_str][exercise_type]
        
        target_record = None
        if isinstance(records, list):
            target_record = next((r for r in records if r['id'] == record_id), None)
        elif isinstance(records, dict) and records.get('id') == record_id:
            target_record = records
        
        if not target_record:
            self.show_message("Chyba", "Záznam nenalezen!", QMessageBox.Critical)
            return
        
        old_value = target_record.get('value', 0)
        current_timestamp = target_record.get('timestamp', f"{date_str} 12:00:00")
        
        # Otevření dialogu
        dialog = EditWorkoutDialog(exercise_type, date_str, old_value, current_timestamp, self)
        if dialog.exec():
            # 1. Pokud uživatel zvolil "Smazat" uvnitř dialogu
            if dialog.delete_requested:
                reply = QMessageBox.question(
                    self, "Smazat záznam", "Opravdu smazat tento záznam?",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    if isinstance(records, list):
                        self.data['workouts'][date_str][exercise_type] = [r for r in records if r['id'] != record_id]
                    elif isinstance(records, dict):
                        del self.data['workouts'][date_str][exercise_type]
                    
                    self.save_data()
                    self.update_exercise_tab(exercise_type)
                    self.refresh_exercise_calendar(exercise_type)
                    self.refresh_add_tab_goals()
                    if exercise_type in self.chart_modes:
                        self.update_performance_chart(exercise_type, self.chart_modes[exercise_type])
                    
                    self.show_message("Smazáno", "Záznam byl odstraněn.")
                return

            # 2. Uložení změn (Počet + Čas)
            new_value, new_time_str = dialog.get_data()
            
            # Aktualizace hodnoty
            target_record['value'] = new_value
            
            # Aktualizace času (zachováme datum, změníme čas)
            try:
                date_part = current_timestamp.split(' ')[0]
                target_record['timestamp'] = f"{date_part} {new_time_str}"
            except:
                # Fallback kdyby byl timestamp poškozený
                target_record['timestamp'] = f"{date_str} {new_time_str}"
            
            self.save_data()
            
            # Refresh UI
            self.update_exercise_tab(exercise_type)
            self.refresh_exercise_calendar(exercise_type)
            self.refresh_add_tab_goals()
            
            # Refresh grafu
            if exercise_type in self.chart_modes:
                self.update_performance_chart(exercise_type, self.chart_modes[exercise_type])
            
            self.show_message("Upraveno", f"Záznam upraven na: {new_value} ks ({new_time_str})")

            
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
        """
        Aktualizuje statistiky a strom záznamů daného cvičení.
        Struktura: Měsíc (YYYY-MM) -> Týden (ISO) -> Den (YYYY-MM-DD) -> Záznamy.
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

            # --- UCHOVÁNÍ VÝBĚRU + ROZBALENÍ (unikátní klíče, aby se netloukly týdny) ---
            preserved = set()             # {(date_str, record_id)}
            expanded_items = set()

            iterator = QTreeWidgetItemIterator(tree)
            while iterator.value():
                item = iterator.value()

                if item.isExpanded():
                    payload = item.data(3, Qt.UserRole)
                    if isinstance(payload, dict):
                        t = payload.get("type")
                        if t == "month":
                            expanded_items.add(("month", payload.get("key")))
                        elif t == "week":
                            expanded_items.add(("week", payload.get("month_key"), payload.get("week")))
                        elif t == "day":
                            expanded_items.add(("day", payload.get("date")))
                        else:
                            expanded_items.add(("text", item.text(0)))
                    else:
                        expanded_items.add(("text", item.text(0)))

                if item.isSelected():
                    payload = item.data(3, Qt.UserRole)
                    if isinstance(payload, dict) and "date" in payload and "record_id" in payload:
                        preserved.add((payload["date"], payload["record_id"]))

                iterator += 1

            first_population = (tree.property("_ever_populated") is not True)

            tree.blockSignals(True)
            tree.clear()

            # Multi-select a výkon
            tree.setSelectionMode(QAbstractItemView.ExtendedSelection)
            tree.setSelectionBehavior(QAbstractItemView.SelectItems)
            tree.setAlternatingRowColors(False)
            tree.setUniformRowHeights(True)

            # --- Data po dnech (jen zvolený rok) ---
            days_data: dict[str, list[dict]] = {}
            for ds, perday in self.data.get("workouts", {}).items():
                year_here = int(ds.split("-")[0]) if "-" in ds else None
                if year_here != selected_year:
                    continue
                if exercise_type in perday:
                    recs = perday[exercise_type]
                    if isinstance(recs, list):
                        days_data.setdefault(ds, []).extend(recs)
                    elif isinstance(recs, dict):
                        days_data.setdefault(ds, []).append(recs)

            # Dny: nejnovější datum první
            sorted_dates = sorted(days_data.keys(), reverse=True)

            # Seskupení do měsíců
            from collections import defaultdict
            months_map = defaultdict(list)
            for d in sorted_dates:
                month_key = d[:7]  # YYYY-MM
                months_map[month_key].append(d)

            sorted_months = sorted(months_map.keys(), reverse=True)

            # Připrav fonty
            try:
                from PySide6.QtGui import QFont
                child_val_font = QFont()
                child_val_font.setBold(True)
                child_time_font = QFont("Menlo")
                base_size = tree.font().pointSize() if tree.font().pointSize() > 0 else 11
                child_time_font.setPointSize(max(base_size - 1, 9))

                month_font = QFont()
                month_font.setBold(True)
                month_font.setPointSize(base_size + 1)

                week_font = QFont()
                week_font.setBold(True)
            except Exception:
                child_val_font = None
                child_time_font = None
                month_font = None
                week_font = None

            # Pomocná funkce barvy (přesně dle zadání)
            def _pct_color(p: int) -> QColor:
                if p >= 200:
                    return QColor("#006400")
                elif p > 100:
                    intensity = min((p / 100.0) - 1.0, 1.0)
                    green_val = int(144 + (100 - 144) * intensity)
                    return QColor(0, green_val, 0)
                elif p == 100:
                    return QColor("#FFD700")
                elif p >= 50:
                    intensity = (1.0 - (p / 100.0)) * 2.0
                    val = int(107 + (255 - 107) * (1.0 - intensity))
                    return QColor(255, val, val)
                else:
                    return QColor("#8B0000")

            current_month_str = datetime.now().strftime("%Y-%m")
            today_str = datetime.now().strftime("%Y-%m-%d")

            cz_months = {
                "01": "Leden", "02": "Únor", "03": "Březen", "04": "Duben", "05": "Květen", "06": "Červen",
                "07": "Červenec", "08": "Srpen", "09": "Září", "10": "Říjen", "11": "Listopad", "12": "Prosinec"
            }

            for m_key in sorted_months:
                y_str, m_str = m_key.split("-")
                m_name = cz_months.get(m_str, m_str)
                month_label = f"{m_name} {y_str}"

                # (1) měsíční suma (suma hodnot)
                month_total_value = 0
                for date_str in months_map[m_key]:
                    records = days_data.get(date_str, [])
                    try:
                        month_total_value += sum(r.get("value", 0) for r in records)
                    except Exception:
                        pass

                month_item = QTreeWidgetItem(tree)
                month_item.setText(0, month_label)
                month_item.setText(1, f"Σ {month_total_value}")
                month_item.setData(3, Qt.UserRole, {"type": "month", "key": m_key})

                if month_font:
                    month_item.setFont(0, month_font)
                    month_item.setFont(1, month_font)

                # (2) barevné odlišení řádků pro měsíce
                month_bg = QColor(36, 52, 71)  # odlišené od týdnů
                for c in range(tree.columnCount()):
                    month_item.setBackground(c, month_bg)

                month_item.setTextAlignment(1, Qt.AlignCenter)

                is_current = (m_key == current_month_str)
                if first_population:
                    month_item.setExpanded(is_current)
                else:
                    if ("month", m_key) in expanded_items:
                        month_item.setExpanded(True)

                # (2) týdenní seskupení uvnitř měsíce
                week_map: dict[int, list[str]] = {}
                week_order: list[int] = []
                for date_str in months_map[m_key]:
                    try:
                        ddt = datetime.strptime(date_str, "%Y-%m-%d").date()
                        wno = int(ddt.isocalendar().week)
                    except Exception:
                        continue
                    if wno not in week_map:
                        week_map[wno] = []
                        week_order.append(wno)
                    week_map[wno].append(date_str)

                for wno in week_order:
                    # (1) týdenní suma (suma hodnot za týden)
                    week_total_value = 0
                    for date_str in week_map.get(wno, []):
                        records = days_data.get(date_str, [])
                        try:
                            week_total_value += sum(r.get("value", 0) for r in records)
                        except Exception:
                            pass

                    week_item = QTreeWidgetItem(month_item)
                    week_item.setText(0, f"📆 Týden {wno}")
                    week_item.setText(1, f"Σ {week_total_value}")
                    week_item.setTextAlignment(1, Qt.AlignCenter)
                    week_item.setData(3, Qt.UserRole, {"type": "week", "month_key": m_key, "week": wno})

                    if week_font:
                        week_item.setFont(0, week_font)
                        week_item.setFont(1, week_font)

                    # (2) barevné odlišení řádků pro týdny
                    week_bg = QColor(43, 43, 43)  # odlišené od měsíců
                    for c in range(tree.columnCount()):
                        week_item.setBackground(c, week_bg)

                    contains_today = (today_str in week_map.get(wno, []))
                    if first_population:
                        week_item.setExpanded(contains_today and (m_key == current_month_str))
                    else:
                        if ("week", m_key, wno) in expanded_items:
                            week_item.setExpanded(True)

                    for date_str in week_map[wno]:
                        records = days_data[date_str]

                        total_day_value = sum(r.get("value", 0) for r in records)
                        record_count = len(records)
                        goal = self.calculate_goal(exercise_type, date_str)
                        if not isinstance(goal, int):
                            goal = int(goal) if goal else 0
                        percent = (total_day_value / goal * 100) if goal > 0 else 0

                        # Barva podle logiky
                        color_status = _pct_color(int(percent))

                        if percent >= 100:
                            status_icon = "✅"
                        elif percent >= 50:
                            status_icon = "⏳"
                        else:
                            status_icon = "❌"

                        day_item = QTreeWidgetItem(week_item)
                        day_item.setText(0, f"{status_icon} {date_str}")
                        day_item.setText(1, f"{total_day_value} ({record_count}×)")
                        day_item.setText(2, f"{percent:.0f}%")

                        day_item.setData(3, Qt.UserRole, {"type": "day", "date": date_str})

                        # Standardní barvy pro sloupce 0 (datum) a 1 (hodnota)
                        day_item.setForeground(0, QColor(255, 255, 255))
                        day_item.setForeground(1, QColor(200, 200, 200))

                        # Kontrastní text pro barevný sloupec (2)
                        is_light = False
                        if percent == 100:
                            is_light = True  # Gold
                        elif 50 <= percent < 100:
                            is_light = True  # Light red/pink
                        text_col = QColor(0, 0, 0) if is_light else QColor(255, 255, 255)

                        day_item.setBackground(2, color_status)
                        day_item.setForeground(2, text_col)

                        day_item.setTextAlignment(1, Qt.AlignCenter)
                        day_item.setTextAlignment(2, Qt.AlignCenter)

                        if first_population:
                            day_item.setExpanded(date_str == today_str)
                            if date_str == today_str:
                                # při prvním naplnění rozbal i rodiče, aby byl dnešek opravdu vidět
                                try:
                                    week_item.setExpanded(True)
                                    month_item.setExpanded(True)
                                except Exception:
                                    pass
                        else:
                            if ("day", date_str) in expanded_items:
                                day_item.setExpanded(True)

                        # --- ZÁZNAMY ---
                        def _time_key(rec: dict) -> str:
                            ts = rec.get("timestamp", "")
                            if " " in ts:
                                return ts.split(" ", 1)[1]
                            return ts

                        records_sorted_asc = sorted(records, key=_time_key)
                        cumulative_pairs = []
                        running_total = 0
                        for rec in records_sorted_asc:
                            running_total += rec.get("value", 0)
                            cumulative_pairs.append((rec, running_total))

                        for idx, (record, running_total) in enumerate(reversed(cumulative_pairs)):
                            value = record.get("value", 0)
                            timestamp = record.get("timestamp", "N/A")
                            time_only = timestamp.split(" ")[1] if " " in timestamp else timestamp
                            record_id = record.get("id", "")

                            if goal > 0:
                                rec_cum_pct = int(round((running_total / goal) * 100))
                                pct_text = f"{rec_cum_pct} %"
                            else:
                                rec_cum_pct = None
                                pct_text = "—"

                            rec_item = QTreeWidgetItem(day_item)
                            rec_item.setText(0, pct_text)
                            rec_item.setText(1, str(value))
                            rec_item.setText(2, time_only)
                            rec_item.setText(3, record_id)

                            rec_item.setData(3, Qt.UserRole, {
                                "type": "record",
                                "date": date_str,
                                "record_id": record_id,
                                "exercise": exercise_type,
                            })

                            rec_item.setTextAlignment(0, Qt.AlignCenter)
                            rec_item.setTextAlignment(1, Qt.AlignCenter)
                            rec_item.setTextAlignment(2, Qt.AlignCenter)

                            if rec_cum_pct is None:
                                rec_item.setForeground(0, QColor(200, 200, 200))
                            else:
                                # Barva TEXTU procent u záznamu (pozadí ne)
                                rec_item.setForeground(0, _pct_color(rec_cum_pct))

                            rec_item.setForeground(1, QColor(240, 240, 240))
                            rec_item.setForeground(2, QColor(180, 180, 180))

                            if child_val_font:
                                rec_item.setFont(1, child_val_font)
                            if child_time_font:
                                rec_item.setFont(2, child_time_font)

                            if idx % 2 == 1:
                                shade = QColor(255, 255, 255, 14)
                                rec_item.setBackground(0, shade)
                                rec_item.setBackground(1, shade)
                                rec_item.setBackground(2, shade)

                            if (date_str, record_id) in preserved:
                                rec_item.setSelected(True)

            if first_population:
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
                    rest_goal -= g
                cur += timedelta(days=1)
            rest_goal += day_performed
    
            lbl_rest = self.findChild(QLabel, f"year_rest_section_{exercise_type}")
            if lbl_rest:
                lbl_rest.setText(f"🎯 ZBYTEK ROKU ({max(today, ex_start).strftime('%d.%m.')} – {year_end.strftime('%d.%m.%Y')}): {rest_goal}")
                if rest_goal < 0:
                    lbl_rest.setStyleSheet("font-size: 12px; color: #c50c0c; padding: 5px;")
                elif rest_goal == 0:
                    lbl_rest.setStyleSheet("font-size: 12px; color: #eede5b; padding: 5px;")
                else:
                    lbl_rest.setStyleSheet("font-size: 12px; color: #5bee63; padding: 5px;")
    
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

    def _calendar_text_color_for_bg_hex(self, bg_hex: str) -> str:
        """
        Vrátí vhodnou barvu textu podle světlosti barvy pozadí (hex).
        - Světlé pozadí  -> tmavý text
        - Tmavé pozadí   -> světlý text
        """
        try:
            if not isinstance(bg_hex, str) or not bg_hex.startswith("#") or len(bg_hex) < 7:
                # Bezpečný fallback – světlý text pro dark theme
                return "#f0f0f0"

            c = bg_hex.lstrip("#")
            r, g, b = int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)

            def _lin(v: float) -> float:
                v = v / 255.0
                return v/12.92 if v <= 0.04045 else ((v+0.055)/1.055)**2.4

            # Relativní luminance (sRGB)
            lum = 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)
            return "#111111" if lum >= 0.60 else "#f0f0f0"
        except Exception:
            # V nouzi ponech světlý text (dark theme)
            return "#f0f0f0"

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
            text_color = self._calendar_text_color_for_bg_hex(color)
            day_label.setStyleSheet(f"background-color: {color}; color: {text_color}; font-weight: bold; {border_style} font-size: 16px;")
            day_label.setToolTip(self._calendar_tooltip_with_contrast(tooltip_text, color))
    
            # <<< JEDINÉ DOPLNĚNÍ: klik na den -> přepni graf na 'Den' pro tento den
            try:
                day_label.setCursor(Qt.PointingHandCursor)
                day_label.mousePressEvent = (
                    lambda ev, _ds=date_str, _ex=exercise_type:
                        self.on_calendar_day_clicked(_ex, _ds) if ev.button() == Qt.LeftButton else None
                )
            except Exception:
                pass
            
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
        
        color = '#555555' # Změna barvy na šedou pro neaktivní dny
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

            today = datetime.now().date()
            year_start = datetime(selected_year, 1, 1).date()
            year_end = datetime(selected_year, 12, 31).date()

            if selected_year < today.year:
                end_calc_date = year_end
            elif selected_year == today.year:
                end_calc_date = today
            else:
                # budoucí rok -> zatím nic "do dneška"
                end_calc_date = year_start - timedelta(days=1)

            ex_start = self.get_exercise_start_date(exercise_type, selected_year)

            # --- Denní klasifikace do dneška (v rámci roku) ---
            days_exact_100 = 0
            days_over = 0
            days_partial_missed = 0
            days_not_exercised = 0
            irrelevant_days = 0

            relevant_days = 0
            sum_goal_to_date = 0
            sum_done_to_date = 0

            d = year_start
            while d <= end_calc_date:
                if d < ex_start:
                    irrelevant_days += 1
                    d += timedelta(days=1)
                    continue

                ds = d.strftime("%Y-%m-%d")
                goal = self.calculate_goal(exercise_type, ds)
                if not isinstance(goal, int):
                    goal = int(goal) if goal else 0

                if goal <= 0:
                    irrelevant_days += 1
                    d += timedelta(days=1)
                    continue

                relevant_days += 1
                sum_goal_to_date += goal

                done = 0
                if ds in self.data.get("workouts", {}) and exercise_type in self.data["workouts"][ds]:
                    recs = self.data["workouts"][ds][exercise_type]
                    try:
                        done = sum(r["value"] for r in (recs if isinstance(recs, list) else [recs]))
                    except Exception:
                        try:
                            done = recs.get("value", 0) if isinstance(recs, dict) else 0
                        except Exception:
                            done = 0

                sum_done_to_date += done

                if done <= 0:
                    days_not_exercised += 1
                elif done < goal:
                    days_partial_missed += 1
                elif done == goal:
                    days_exact_100 += 1
                else:
                    days_over += 1

                d += timedelta(days=1)

            avg_done_per_day = (sum_done_to_date / relevant_days) if relevant_days > 0 else 0
            avg_pct_to_date = (sum_done_to_date / sum_goal_to_date * 100) if sum_goal_to_date > 0 else 0

            # --- Plán do konce roku (od startu cvičení v daném roce) ---
            planned_total_to_year_end = 0
            d = max(year_start, ex_start)
            while d <= year_end:
                ds = d.strftime("%Y-%m-%d")
                g = self.calculate_goal(exercise_type, ds)
                if not isinstance(g, int):
                    g = int(g) if g else 0
                if g > 0:
                    planned_total_to_year_end += g
                d += timedelta(days=1)

            remaining_total_to_year_end = planned_total_to_year_end - sum_done_to_date
            if remaining_total_to_year_end < 0:
                remaining_total_to_year_end = 0

            # --- ZBYTEK ROKU: stejně jako v DEN/TÝDEN/MĚSÍC/ZBYTEK ---
            remaining_from_today = 0
            remaining_days = 0
            avg_needed_future = 0.0

            if selected_year == today.year:
                today_str = today.strftime("%Y-%m-%d")
                day_performed = 0
                if today_str in self.data.get("workouts", {}) and exercise_type in self.data["workouts"][today_str]:
                    recs = self.data["workouts"][today_str][exercise_type]
                    try:
                        day_performed = sum(r["value"] for r in (recs if isinstance(recs, list) else [recs]))
                    except Exception:
                        try:
                            day_performed = recs.get("value", 0) if isinstance(recs, dict) else 0
                        except Exception:
                            day_performed = 0

                cur = max(today, ex_start)
                while cur <= year_end:
                    ds = cur.strftime("%Y-%m-%d")
                    g = self.calculate_goal(exercise_type, ds)
                    if not isinstance(g, int):
                        g = int(g) if g else 0
                    if g > 0:
                        remaining_from_today += g
                        remaining_days += 1
                    cur += timedelta(days=1)

                # odečíst dnešní výkon (stejná logika jako rest_goal += day_performed v update_detailed_overview)
                if today >= ex_start:
                    g_today = self.calculate_goal(exercise_type, today_str)
                    if not isinstance(g_today, int):
                        g_today = int(g_today) if g_today else 0
                    if g_today > 0:
                        remaining_from_today -= day_performed

                if remaining_from_today < 0:
                    remaining_from_today = 0

                avg_needed_future = (remaining_from_today / remaining_days) if remaining_days > 0 else 0.0

            stats_text = (
                f"📊 Statistiky roku {selected_year} (do {end_calc_date.strftime('%d.%m.')}): "
                f"✅ Přesně 100%: {days_exact_100} | "
                f"🟢 Nad plán: {days_over} | "
                f"⚠️ Částečně nesplněno: {days_partial_missed} | "
                f"❌ Necvičil: {days_not_exercised} | "
                f"💤 Irelevantní: {irrelevant_days}"
                f"\n"
                f"📈 Průměrný výkon: {avg_done_per_day:.1f}/den ({avg_pct_to_date:.1f}% plánu dosud)"
                f"\n"
                f"📌 Od startu nacvičeno: {sum_done_to_date:.0f}"
            )

            if selected_year == today.year:
                stats_text += (
                    f"\n"
                    f"🎯 ZBYTEK ROKU ({max(today, ex_start).strftime('%d.%m.')} – {year_end.strftime('%d.%m.%Y')}): "
                    f"{remaining_from_today:.0f} (průměrně {avg_needed_future:.1f}/den, zbývá {remaining_days} dní)"
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

from PySide6.QtGui import QIcon

def main():
    app = QApplication(sys.argv)

    # Nastavení aplikační ikony (platí pro všechna okna)
    app_icon = QIcon()
    app_icon.addFile("resources/icons/app_icon_512.png", QSize(512, 512))
    app.setWindowIcon(app_icon)

    window = FitnessTrackerApp()
    # Na menších rozlišeních (FullHD) je lepší využít celou plochu, 
    # aby se prvky (kalendář/graf) nepřekrývaly.
    window.showMaximized()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()