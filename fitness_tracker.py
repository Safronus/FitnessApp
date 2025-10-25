#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fitness Tracker - Aplikace pro sledování cvičení s progresivními cíli
Verze 1.3

Changelog:
v1.3 (25.10.2025)
- Více záznamů za den (nepřepisování)
- Každý záznam má vlastní řádek v tabulce
- Checkboxy pro výběr záznamů
- Hromadné mazání vybraných záznamů
- Editace a mazání jednotlivých záznamů
- Migrace dat na nový formát s lists

v1.2b - v1.0.0
- Předchozí verze
"""

import sys
import json
import uuid  # NOVÝ IMPORT
from datetime import datetime, timedelta
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QLabel, QSpinBox, QPushButton, QDateEdit, QTableWidget,
    QTableWidgetItem, QGroupBox, QFormLayout, QHeaderView, QMessageBox,
    QGridLayout, QComboBox, QScrollArea, QFrame, QProgressBar, QTextEdit,
    QDialog, QListWidget, QListWidgetItem, QInputDialog
)
from PySide6.QtCore import Qt, QDate, QTimer
from PySide6.QtGui import QColor

# Verze aplikace
VERSION = "1.3"
VERSION_DATE = "26.10.2025"

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


class NewYearDialog(QDialog):
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
        self.setWindowTitle(f"Fitness Tracker v{VERSION} - Sledování cvičení")
        self.setMinimumSize(1400, 800)
        
        self.data_file = Path("fitness_data.json")
        self.exercise_year_selectors = {}
        self.exercise_calendar_widgets = {}
        self.current_settings_year = datetime.now().year
        
        self.load_data()
        self.ensure_app_state()
        self.migrate_data()
        self.migrate_to_year_settings()
        self.setup_ui()
        self.restore_app_state()
        
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.auto_refresh)
        self.update_timer.start(5000)
        
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
        
    def load_data(self):
        if self.data_file.exists():
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        else:
            current_year = datetime.now().year
            self.data = {
                'version': VERSION,
                'year_settings': {
                    str(current_year): {
                        'start_date': f'{current_year}-01-01',
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
                },
                'workouts': {},
                'app_state': {
                    'last_tab': 0,
                    'window_geometry': None,
                    'exercise_years': {
                        'kliky': datetime.now().year,
                        'dřepy': datetime.now().year,
                        'skrčky': datetime.now().year
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
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        self.tabs = QTabWidget()
        self.tabs.currentChanged.connect(self.on_tab_changed)
        layout.addWidget(self.tabs)
        
        self.tabs.addTab(self.create_add_workout_tab(), "➕ Přidat výkon")
        self.tabs.addTab(self.create_exercise_tab('kliky', '💪'), "💪 Kliky")
        self.tabs.addTab(self.create_exercise_tab('dřepy', '🦵'), "🦵 Dřepy")
        self.tabs.addTab(self.create_exercise_tab('skrčky', '🧘'), "🧘 Skrčky")
        self.tabs.addTab(self.create_settings_tab(), "⚙️ Nastavení")
        self.tabs.addTab(self.create_about_tab(), "ℹ️ O aplikaci")

    def add_single_workout(self, exercise_type, value):
        """Přidá výkon pro jednu kategorii"""
        if value == 0:
            self.show_message("Chyba", f"Zadej nenulovou hodnotu pro {exercise_type}!", QMessageBox.Warning)
            return
        
        selected_date_str = self.add_date_edit.date().toString('yyyy-MM-dd')
        
        if selected_date_str not in self.data['workouts']:
            self.data['workouts'][selected_date_str] = {}
        
        if exercise_type not in self.data['workouts'][selected_date_str]:
            self.data['workouts'][selected_date_str][exercise_type] = []
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        new_record = {
            'value': value,
            'timestamp': timestamp,
            'id': str(uuid.uuid4())
        }
        
        self.data['workouts'][selected_date_str][exercise_type].append(new_record)
        
        self.save_data()
        
        # Aktualizuj všechny záložky
        for exercise in ['kliky', 'dřepy', 'skrčky']:
            self.update_exercise_tab(exercise)
            self.refresh_exercise_calendar(exercise)
        
        # Refresh přehledu cílů
        self.refresh_add_tab_goals()
        
        self.show_message("Přidáno", f"Výkon byl zaznamenán: {value} {exercise_type}")
        
        # Reset hodnoty
        if exercise_type == 'kliky':
            self.kliky_spin.setValue(0)
        elif exercise_type == 'dřepy':
            self.drepy_spin.setValue(0)
        elif exercise_type == 'skrčky':
            self.skrcky_spin.setValue(0)

    def add_all_workouts(self):
        """Přidá všechny výkony najednou"""
        kliky_val = self.kliky_spin.value()
        drepy_val = self.drepy_spin.value()
        skrcky_val = self.skrcky_spin.value()
        
        if kliky_val == 0 and drepy_val == 0 and skrcky_val == 0:
            self.show_message("Chyba", "Zadej alespoň jednu nenulovou hodnotu!", QMessageBox.Warning)
            return
        
        selected_date_str = self.add_date_edit.date().toString('yyyy-MM-dd')
        
        if selected_date_str not in self.data['workouts']:
            self.data['workouts'][selected_date_str] = {}
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        added = []
        
        if kliky_val > 0:
            if 'kliky' not in self.data['workouts'][selected_date_str]:
                self.data['workouts'][selected_date_str]['kliky'] = []
            
            self.data['workouts'][selected_date_str]['kliky'].append({
                'value': kliky_val,
                'timestamp': timestamp,
                'id': str(uuid.uuid4())
            })
            added.append(f"kliky: {kliky_val}")
        
        if drepy_val > 0:
            if 'dřepy' not in self.data['workouts'][selected_date_str]:
                self.data['workouts'][selected_date_str]['dřepy'] = []
            
            self.data['workouts'][selected_date_str]['dřepy'].append({
                'value': drepy_val,
                'timestamp': timestamp,
                'id': str(uuid.uuid4())
            })
            added.append(f"dřepy: {drepy_val}")
        
        if skrcky_val > 0:
            if 'skrčky' not in self.data['workouts'][selected_date_str]:
                self.data['workouts'][selected_date_str]['skrčky'] = []
            
            self.data['workouts'][selected_date_str]['skrčky'].append({
                'value': skrcky_val,
                'timestamp': timestamp,
                'id': str(uuid.uuid4())
            })
            added.append(f"skrčky: {skrcky_val}")
        
        self.save_data()
        
        # Aktualizuj všechny záložky
        for exercise in ['kliky', 'dřepy', 'skrčky']:
            self.update_exercise_tab(exercise)
            self.refresh_exercise_calendar(exercise)
        
        # Refresh přehledu
        self.refresh_add_tab_goals()
        
        self.show_message("Přidáno", f"Výkony zaznamenány:\n" + "\n".join(added))
        
        # Reset hodnot
        self.kliky_spin.setValue(0)
        self.drepy_spin.setValue(0)
        self.skrcky_spin.setValue(0)

    def create_add_workout_tab(self):
        """Záložka pro přidávání výkonů - redesign"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        title_label = QLabel("➕ Přidání výkonu")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #14919b; padding: 10px;")
        layout.addWidget(title_label)
        
        # Výběr data
        date_row = QHBoxLayout()
        date_row.addWidget(QLabel("📅 Datum:"))
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
        
        selected_date_str = self.add_date_edit.date().toString('yyyy-MM-dd')
        
        for exercise in ['kliky', 'dřepy', 'skrčky']:
            goal = self.calculate_goal(exercise, selected_date_str)
            
            if selected_date_str in self.data['workouts'] and exercise in self.data['workouts'][selected_date_str]:
                workout_data = self.data['workouts'][selected_date_str][exercise]
                if isinstance(workout_data, dict):
                    current_value = workout_data['value']
                else:
                    current_value = workout_data
                
                if current_value >= goal:
                    status = f"✅ Splněno ({current_value}/{goal})"
                    color = "#32c766"
                elif current_value > 0:
                    status = f"⏳ Rozpracováno ({current_value}/{goal})"
                    color = "#FFD700"
                else:
                    status = f"❌ Nesplněno (0/{goal})"
                    color = "#ff6b6b"
            else:
                status = f"❌ Nesplněno (0/{goal})"
                color = "#ff6b6b"
            
            goal_label = QLabel(f"{exercise.capitalize()}: {status}")
            goal_label.setStyleSheet(f"font-size: 13px; padding: 5px; color: {color}; font-weight: bold;")
            goal_label.setObjectName(f"goal_label_{exercise}")
            self.add_goals_labels[exercise] = goal_label
            goals_layout.addWidget(goal_label)
        
        goals_group.setLayout(goals_layout)
        layout.addWidget(goals_group)
        
        # Přidávání výkonů - každá kategorie samostatně
        add_group = QGroupBox("➕ Zadat výkon")
        add_layout = QVBoxLayout()
        
        # Kliky
        kliky_row = QHBoxLayout()
        kliky_row.addWidget(QLabel("💪 Kliky:"))
        self.kliky_spin = QSpinBox()
        self.kliky_spin.setRange(0, 1000)
        self.kliky_spin.setValue(0)
        kliky_row.addWidget(self.kliky_spin)
        kliky_btn = QPushButton("✅ Přidat")
        kliky_btn.clicked.connect(lambda: self.add_single_workout('kliky', self.kliky_spin.value()))
        kliky_row.addWidget(kliky_btn)
        add_layout.addLayout(kliky_row)
        
        # Dřepy
        drepy_row = QHBoxLayout()
        drepy_row.addWidget(QLabel("🦵 Dřepy:"))
        self.drepy_spin = QSpinBox()
        self.drepy_spin.setRange(0, 1000)
        self.drepy_spin.setValue(0)
        drepy_row.addWidget(self.drepy_spin)
        drepy_btn = QPushButton("✅ Přidat")
        drepy_btn.clicked.connect(lambda: self.add_single_workout('dřepy', self.drepy_spin.value()))
        drepy_row.addWidget(drepy_btn)
        add_layout.addLayout(drepy_row)
        
        # Skrčky
        skrcky_row = QHBoxLayout()
        skrcky_row.addWidget(QLabel("🧘 Skrčky:"))
        self.skrcky_spin = QSpinBox()
        self.skrcky_spin.setRange(0, 1000)
        self.skrcky_spin.setValue(0)
        skrcky_row.addWidget(self.skrcky_spin)
        skrcky_btn = QPushButton("✅ Přidat")
        skrcky_btn.clicked.connect(lambda: self.add_single_workout('skrčky', self.skrcky_spin.value()))
        skrcky_row.addWidget(skrcky_btn)
        add_layout.addLayout(skrcky_row)
        
        add_group.setLayout(add_layout)
        layout.addWidget(add_group)
        
        # Tlačítko pro přidání všeho najednou
        add_all_btn = QPushButton("🚀 Přidat všechny výkony najednou")
        add_all_btn.setStyleSheet("font-size: 14px; padding: 12px; background-color: #0d7377;")
        add_all_btn.clicked.connect(self.add_all_workouts)
        layout.addWidget(add_all_btn)
        
        layout.addStretch()
        
        return widget

    def refresh_add_tab_goals(self):
        """Aktualizuje přehled cílů při změně data"""
        selected_date_str = self.add_date_edit.date().toString('yyyy-MM-dd')
        
        for exercise in ['kliky', 'dřepy', 'skrčky']:
            goal = self.calculate_goal(exercise, selected_date_str)
            
            current_value = 0
            if selected_date_str in self.data['workouts'] and exercise in self.data['workouts'][selected_date_str]:
                records = self.data['workouts'][selected_date_str][exercise]
                if isinstance(records, list):
                    current_value = sum(r['value'] for r in records)
                elif isinstance(records, dict):
                    current_value = records.get('value', 0)
            
            if current_value >= goal:
                status = f"✅ Splněno ({current_value}/{goal})"
                color = "#32c766"
            elif current_value > 0:
                status = f"⏳ Rozpracováno ({current_value}/{goal})"
                color = "#FFD700"
            else:
                status = f"❌ Nesplněno (0/{goal})"
                color = "#ff6b6b"
            
            if exercise in self.add_goals_labels:
                self.add_goals_labels[exercise].setText(f"{exercise.capitalize()}: {status}")
                self.add_goals_labels[exercise].setStyleSheet(f"font-size: 13px; padding: 5px; color: {color}; font-weight: bold;")

    def on_tab_changed(self, index):
        try:
            tab_name = self.tabs.tabText(index)
            if "💪" in tab_name:
                self.update_exercise_tab('kliky')
                self.refresh_exercise_calendar('kliky')
            elif "🦵" in tab_name:
                self.update_exercise_tab('dřepy')
                self.refresh_exercise_calendar('dřepy')
            elif "🧘" in tab_name:
                self.update_exercise_tab('skrčky')
                self.refresh_exercise_calendar('skrčky')
        except Exception as e:
            print(f"Chyba při přepnutí záložky: {e}")
    
    def auto_refresh(self):
        try:
            current_tab = self.tabs.currentIndex()
            tab_name = self.tabs.tabText(current_tab)
            
            if "💪" in tab_name:
                self.update_exercise_tab('kliky')
            elif "🦵" in tab_name:
                self.update_exercise_tab('dřepy')
            elif "🧘" in tab_name:
                self.update_exercise_tab('skrčky')
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
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        years_group = QGroupBox("📅 Správa roků")
        years_layout = QVBoxLayout()
        
        available_years = self.get_available_years()
        years_text = f"Dostupné roky: {', '.join(map(str, available_years))}"
        
        info_label = QLabel(years_text)
        info_label.setStyleSheet("padding: 10px; color: #14919b;")
        info_label.setWordWrap(True)
        years_layout.addWidget(info_label)
        
        hint_label = QLabel("💡 Tip: Klikni na rok pro úpravu jeho nastavení")
        hint_label.setStyleSheet("padding: 5px; color: #a0a0a0; font-size: 10px; font-style: italic;")
        years_layout.addWidget(hint_label)
        
        self.years_list = QListWidget()
        self.years_list.setMaximumHeight(150)
        self.years_list.itemClicked.connect(self.on_year_selected_for_settings)
        
        for year in available_years:
            year_workouts = sum(1 for date_str in self.data['workouts'].keys() 
                              if int(date_str.split('-')[0]) == year)
            
            item = QListWidgetItem(f"📆 Rok {year} ({year_workouts} dnů s cvičením)")
            item.setData(Qt.UserRole, year)
            self.years_list.addItem(item)
        
        years_layout.addWidget(self.years_list)
        
        years_buttons = QHBoxLayout()
        
        add_year_btn = QPushButton("➕ Přidat nový rok")
        add_year_btn.clicked.connect(self.add_custom_year)
        years_buttons.addWidget(add_year_btn)
        
        delete_year_btn = QPushButton("🗑️ Smazat vybraný rok")
        delete_year_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        delete_year_btn.clicked.connect(lambda: self.delete_year_from_list())
        years_buttons.addWidget(delete_year_btn)
        
        years_layout.addLayout(years_buttons)
        
        years_group.setLayout(years_layout)
        layout.addWidget(years_group)
        
        self.current_year_label = QLabel()
        self.current_year_label.setStyleSheet("""
            background-color: #0d7377;
            color: white;
            padding: 8px;
            border-radius: 5px;
            font-weight: bold;
            font-size: 13px;
        """)
        self.current_year_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.current_year_label)
        
        # SDRUŽENÁ SKUPINA: Nastavení cílů
        goals_settings_group = QGroupBox("🎯 Nastavení cílů pro vybraný rok")
        goals_settings_layout = QVBoxLayout()
        
        # Startovní datum
        date_layout = QFormLayout()
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setCalendarPopup(True)
        date_layout.addRow("📅 Datum zahájení:", self.start_date_edit)
        goals_settings_layout.addLayout(date_layout)
        
        # Základní cíle
        base_label = QLabel("Základní cíle (na startovní datum):")
        base_label.setStyleSheet("font-weight: bold; padding-top: 10px; color: #14919b;")
        goals_settings_layout.addWidget(base_label)
        
        base_goals_layout = QFormLayout()
        
        self.base_kliky = QSpinBox()
        self.base_kliky.setRange(0, 1000)
        base_goals_layout.addRow("💪 Kliky:", self.base_kliky)
        
        self.base_drepy = QSpinBox()
        self.base_drepy.setRange(0, 1000)
        base_goals_layout.addRow("🦵 Dřepy:", self.base_drepy)
        
        self.base_skrcky = QSpinBox()
        self.base_skrcky.setRange(0, 1000)
        base_goals_layout.addRow("🧘 Skrčky:", self.base_skrcky)
        
        goals_settings_layout.addLayout(base_goals_layout)
        
        # Týdenní přírůstky
        increment_label = QLabel("Týdenní přírůstky (za každý celý týden):")
        increment_label.setStyleSheet("font-weight: bold; padding-top: 10px; color: #14919b;")
        goals_settings_layout.addWidget(increment_label)
        
        increment_layout = QFormLayout()
        
        self.increment_kliky = QSpinBox()
        self.increment_kliky.setRange(0, 100)
        increment_layout.addRow("💪 Kliky (+týdně):", self.increment_kliky)
        
        self.increment_drepy = QSpinBox()
        self.increment_drepy.setRange(0, 100)
        increment_layout.addRow("🦵 Dřepy (+týdně):", self.increment_drepy)
        
        self.increment_skrcky = QSpinBox()
        self.increment_skrcky.setRange(0, 100)
        increment_layout.addRow("🧘 Skrčky (+týdně):", self.increment_skrcky)
        
        goals_settings_layout.addLayout(increment_layout)
        
        goals_settings_group.setLayout(goals_settings_layout)
        layout.addWidget(goals_settings_group)
        
        save_btn = QPushButton("💾 Uložit nastavení")
        save_btn.clicked.connect(self.save_settings)
        layout.addWidget(save_btn)
        
        layout.addStretch()
        
        self.load_year_settings_to_ui(self.current_settings_year)
        
        return widget

    def load_year_settings_to_ui(self, year):
        """Načte nastavení pro daný rok do UI"""
        self.current_settings_year = year
        settings = self.get_year_settings(year)
        
        self.current_year_label.setText(f"⚙️ Upravuješ nastavení pro rok: {year}")
        
        start_date = QDate.fromString(settings['start_date'], 'yyyy-MM-dd')
        self.start_date_edit.setDate(start_date)
        
        self.base_kliky.setValue(settings['base_goals']['kliky'])
        self.base_drepy.setValue(settings['base_goals']['dřepy'])
        self.base_skrcky.setValue(settings['base_goals']['skrčky'])
        
        self.increment_kliky.setValue(settings['weekly_increment']['kliky'])
        self.increment_drepy.setValue(settings['weekly_increment']['dřepy'])
        self.increment_skrcky.setValue(settings['weekly_increment']['skrčky'])
    
    def on_year_selected_for_settings(self, item):
        """Při kliknutí na rok v nastavení načte jeho konfiguraci"""
        selected_year = item.data(Qt.UserRole)
        self.load_year_settings_to_ui(selected_year)
        
        for exercise in ['kliky', 'dřepy', 'skrčky']:
            if exercise in self.exercise_year_selectors:
                self.exercise_year_selectors[exercise].setCurrentText(str(selected_year))
        
        for exercise in ['kliky', 'dřepy', 'skrčky']:
            self.update_exercise_tab(exercise)
            self.refresh_exercise_calendar(exercise)
    
    def save_settings(self):
        year_str = str(self.current_settings_year)
        
        self.data['year_settings'][year_str]['start_date'] = self.start_date_edit.date().toString('yyyy-MM-dd')
        self.data['year_settings'][year_str]['base_goals']['kliky'] = self.base_kliky.value()
        self.data['year_settings'][year_str]['base_goals']['dřepy'] = self.base_drepy.value()
        self.data['year_settings'][year_str]['base_goals']['skrčky'] = self.base_skrcky.value()
        self.data['year_settings'][year_str]['weekly_increment']['kliky'] = self.increment_kliky.value()
        self.data['year_settings'][year_str]['weekly_increment']['dřepy'] = self.increment_drepy.value()
        self.data['year_settings'][year_str]['weekly_increment']['skrčky'] = self.increment_skrcky.value()
        
        self.save_data()
        self.show_message("Uloženo", f"Nastavení pro rok {self.current_settings_year} bylo úspěšně uloženo!")
        
        for exercise in ['kliky', 'dřepy', 'skrčky']:
            self.update_exercise_tab(exercise)
            if exercise in self.exercise_calendar_widgets:
                self.refresh_exercise_calendar(exercise)
    
    def add_custom_year(self):
        """Dialog pro přidání libovolného roku"""
        current_year = datetime.now().year
        
        year, ok = QInputDialog.getInt(
            self,
            "Přidat rok",
            "Zadej rok, který chceš přidat do sledování:",
            current_year,
            2000,
            2100,
            1
        )
        
        if ok:
            dialog = NewYearDialog(year, self)
            
            if dialog.exec():
                if not dialog.use_current:
                    self.show_message(
                        "Informace",
                        f"Rok {year} byl přidán s výchozím nastavením.\n"
                        "Můžeš ho upravit kliknutím na rok v seznamu.",
                        QMessageBox.Information
                    )
                
                first_day_of_year = f"{year}-01-01"
                if first_day_of_year not in self.data['workouts']:
                    self.data['workouts'][first_day_of_year] = {}
                
                self.get_year_settings(year)
                
                self.save_data()
                self.update_all_year_selectors()
                
                for exercise in ['kliky', 'dřepy', 'skrčky']:
                    if exercise in self.exercise_year_selectors:
                        self.exercise_year_selectors[exercise].setCurrentText(str(year))
                
                self.years_list.clear()
                for y in self.get_available_years():
                    year_workouts = sum(1 for date_str in self.data['workouts'].keys() 
                                      if int(date_str.split('-')[0]) == y)
                    item = QListWidgetItem(f"📆 Rok {y} ({year_workouts} dnů s cvičením)")
                    item.setData(Qt.UserRole, y)
                    self.years_list.addItem(item)
                
                self.load_year_settings_to_ui(year)
                
                self.show_message(
                    "Úspěch",
                    f"Rok {year} byl přidán do sledování!\nMůžeš začít zaznamenávat svá cvičení.",
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
    
    def create_exercise_tab(self, exercise_type, icon):
        """Vytvoří záložku pro konkrétní cvičení - BEZ přidávání"""
        widget = QWidget()
        main_layout = QHBoxLayout(widget)
        
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        year_selector_layout = QHBoxLayout()
        year_selector_layout.addWidget(QLabel(f"📅 Zobrazit rok:"))
        
        year_selector = QComboBox()
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
        
        goals_frame = QFrame()
        goals_frame.setStyleSheet("""
            QFrame {
                background-color: #2d2d2d;
                border: 2px solid #0d7377;
                border-radius: 5px;
            }
        """)
        goals_layout = QVBoxLayout(goals_frame)
        
        today_goal_label = QLabel()
        today_goal_label.setObjectName(f"today_goal_label_{exercise_type}")
        today_goal_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #14919b; padding: 5px;")
        goals_layout.addWidget(today_goal_label)
        
        calc_label = QLabel()
        calc_label.setObjectName(f"calc_label_{exercise_type}")
        calc_label.setStyleSheet("font-size: 10px; color: #a0a0a0; padding: 2px; font-style: italic;")
        goals_layout.addWidget(calc_label)
        
        performance_label = QLabel()
        performance_label.setObjectName(f"performance_label_{exercise_type}")
        performance_label.setStyleSheet("font-size: 13px; font-weight: bold; padding: 5px;")
        goals_layout.addWidget(performance_label)
        
        year_goal_label = QLabel()
        year_goal_label.setObjectName(f"year_goal_label_{exercise_type}")
        year_goal_label.setStyleSheet("font-size: 12px; font-weight: bold; color: #32c766; padding: 5px;")
        goals_layout.addWidget(year_goal_label)
        
        progress_bar = QProgressBar()
        progress_bar.setObjectName(f"progress_bar_{exercise_type}")
        progress_bar.setTextVisible(True)
        goals_layout.addWidget(progress_bar)
        
        stats_label = QLabel()
        stats_label.setObjectName(f"stats_label_{exercise_type}")
        stats_label.setStyleSheet("font-size: 11px; color: #a0a0a0; padding: 5px;")
        goals_layout.addWidget(stats_label)
        
        left_layout.addWidget(goals_frame)
        
        # Tlačítka pro hromadné akce
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
        
        # TABULKA s checkboxy
        table = QTableWidget()
        table.setObjectName(f"table_{exercise_type}")
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["☑️", "Datum", "Čas", "Výkon"])
        
        table.verticalHeader().setDefaultSectionSize(30)
        table.verticalHeader().setMinimumSectionSize(30)
        
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        
        left_layout.addWidget(table)
        
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        overview_label = QLabel(f"📊 Roční přehled - {exercise_type.capitalize()}")
        overview_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #14919b; padding: 5px;")
        right_layout.addWidget(overview_label)
        
        legend_frame = QFrame()
        legend_frame.setStyleSheet("background-color: #2d2d2d; border: 1px solid #3d3d3d; padding: 5px;")
        legend_layout = QGridLayout(legend_frame)
        legend_layout.setSpacing(5)
        
        def create_color_sample(color, text):
            h_layout = QHBoxLayout()
            h_layout.setSpacing(3)
            color_box = QLabel()
            color_box.setFixedSize(15, 15)
            color_box.setStyleSheet(f"background-color: {color}; border: 1px solid #3d3d3d;")
            h_layout.addWidget(color_box)
            text_label = QLabel(text)
            text_label.setStyleSheet("font-size: 10px;")
            h_layout.addWidget(text_label)
            h_layout.addStretch()
            return h_layout
        
        legend_layout.addLayout(create_color_sample("#000000", "Před začátkem"), 0, 0)
        legend_layout.addLayout(create_color_sample("#006400", "Velký náskok"), 0, 1)
        legend_layout.addLayout(create_color_sample("#90EE90", "Mírný náskok"), 0, 2)
        legend_layout.addLayout(create_color_sample("#FFD700", "Akorát"), 1, 0)
        legend_layout.addLayout(create_color_sample("#FF6B6B", "Mírný skluz"), 1, 1)
        legend_layout.addLayout(create_color_sample("#8B0000", "Velký skluz"), 1, 2)
        
        right_layout.addWidget(legend_frame)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        calendar_widget = QWidget()
        calendar_layout = QVBoxLayout(calendar_widget)
        
        self.exercise_calendar_widgets[exercise_type] = calendar_layout
        
        scroll.setWidget(calendar_widget)
        right_layout.addWidget(scroll)
        
        stats_year_label = QLabel()
        stats_year_label.setObjectName(f"stats_year_label_{exercise_type}")
        stats_year_label.setStyleSheet("font-size: 11px; padding: 5px; background-color: #2d2d2d; color: #e0e0e0; border-radius: 5px;")
        right_layout.addWidget(stats_year_label)
        
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 1)
        
        self.update_exercise_tab(exercise_type)
        self.refresh_exercise_calendar(exercise_type)
        
        return widget

    def delete_selected_records(self, exercise_type):
        """Smaže vybrané záznamy"""
        table = self.findChild(QTableWidget, f"table_{exercise_type}")
        if not table:
            return
        
        selected_ids = []
        for row in range(table.rowCount()):
            checkbox = table.cellWidget(row, 0)
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
            self.show_message("Smazáno", f"{len(selected_ids)} záznamů bylo smazáno")

    def update_exercise_tab_and_calendar(self, exercise_type):
        """Bezpečná aktualizace"""
        try:
            if exercise_type in self.exercise_year_selectors:
                selector = self.exercise_year_selectors[exercise_type]
                if selector and selector.currentText():
                    self.update_exercise_tab(exercise_type)
                    self.refresh_exercise_calendar(exercise_type)
        except Exception as e:
            print(f"Chyba při aktualizaci záložky {exercise_type}: {e}")
    
    def calculate_goal(self, exercise_type, date_str):
        """Vypočítá cíl pro daný den"""
        target_date = datetime.strptime(date_str, '%Y-%m-%d')
        year = target_date.year
        
        settings = self.get_year_settings(year)
        
        start_date = datetime.strptime(settings['start_date'], '%Y-%m-%d')
        base_goal = settings['base_goals'][exercise_type]
        increment = settings['weekly_increment'][exercise_type]
        
        if target_date < start_date:
            return 0
        
        days_to_sunday = 6 - start_date.weekday()
        first_week_end = start_date + timedelta(days=days_to_sunday)
        
        if target_date <= first_week_end:
            return base_goal
        
        first_full_week_start = first_week_end + timedelta(days=1)
        days_since_first_full_week = (target_date - first_full_week_start).days
        
        full_weeks = (days_since_first_full_week // 7) + 1
        
        goal = base_goal + (full_weeks * increment)
        
        return max(0, goal)
    
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
        """Otevře dialog pro editaci záznamu"""
        records = self.data['workouts'][date_str][exercise_type]
        
        if not isinstance(records, list):
            records = [records]
        
        record = next((r for r in records if r['id'] == record_id), None)
        
        if not record:
            self.show_message("Chyba", "Záznam nebyl nalezen!", QMessageBox.Warning)
            return
        
        current_value = record['value']
        timestamp = record.get('timestamp', 'N/A')
        
        dialog = EditWorkoutDialog(exercise_type, date_str, current_value, timestamp, self)
        
        if dialog.exec():
            if dialog.delete_requested:
                self.data['workouts'][date_str][exercise_type] = [r for r in records if r['id'] != record_id]
                
                if not self.data['workouts'][date_str][exercise_type]:
                    del self.data['workouts'][date_str][exercise_type]
                
                if not self.data['workouts'][date_str]:
                    del self.data['workouts'][date_str]
                
                self.show_message("Smazáno", "Záznam byl smazán")
            else:
                new_value = dialog.get_value()
                edit_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                for r in records:
                    if r['id'] == record_id:
                        r['value'] = new_value
                        r['edited'] = edit_timestamp
                        break
                
                self.show_message("Upraveno", f"Záznam byl upraven na: {new_value} {exercise_type}")
            
            self.save_data()
            self.update_exercise_tab(exercise_type)
            self.refresh_exercise_calendar(exercise_type)

    def update_exercise_tab(self, exercise_type):
        """Aktualizuje statistiky a tabulku"""
        try:
            if exercise_type not in self.exercise_year_selectors:
                return
            
            selector = self.exercise_year_selectors[exercise_type]
            if not selector or not selector.currentText():
                return
            
            selected_year = int(selector.currentText())
            
            today = datetime.now()
            today_str = today.strftime('%Y-%m-%d')
            
            if selected_year > today.year:
                display_date_str = f"{selected_year}-01-01"
                today_goal = self.calculate_goal(exercise_type, display_date_str)
                today_goal_label = self.findChild(QLabel, f"today_goal_label_{exercise_type}")
                if today_goal_label:
                    today_goal_label.setText(f"🎯 Cíl pro {selected_year}: {today_goal}")
            elif selected_year < today.year:
                display_date_str = f"{selected_year}-12-31"
                today_goal = self.calculate_goal(exercise_type, display_date_str)
                today_goal_label = self.findChild(QLabel, f"today_goal_label_{exercise_type}")
                if today_goal_label:
                    today_goal_label.setText(f"🎯 Cíl {selected_year} (31.12.): {today_goal}")
            else:
                today_goal = self.calculate_goal(exercise_type, today_str)
                today_goal_label = self.findChild(QLabel, f"today_goal_label_{exercise_type}")
                if today_goal_label:
                    today_goal_label.setText(f"🎯 Dnešní cíl: {today_goal}")
                display_date_str = today_str
            
            calc_label = self.findChild(QLabel, f"calc_label_{exercise_type}")
            if calc_label:
                calc_text = self.get_goal_calculation_text(exercise_type, display_date_str)
                calc_label.setText(calc_text)
            
            total_performed, total_yearly_goal, goal_to_date = self.calculate_yearly_progress(exercise_type, selected_year)
            difference = total_performed - goal_to_date
            
            performance_label = self.findChild(QLabel, f"performance_label_{exercise_type}")
            if performance_label:
                if difference > 0:
                    performance_label.setText(f"📈 Náskok: +{difference:,}")
                    performance_label.setStyleSheet("font-size: 13px; font-weight: bold; color: #32c766; padding: 5px;")
                elif difference < 0:
                    performance_label.setText(f"📉 Skluz: {difference:,}")
                    performance_label.setStyleSheet("font-size: 13px; font-weight: bold; color: #ff6b6b; padding: 5px;")
                else:
                    performance_label.setText(f"✅ Podle plánu")
                    performance_label.setStyleSheet("font-size: 13px; font-weight: bold; color: #14919b; padding: 5px;")
            
            year_goal_label = self.findChild(QLabel, f"year_goal_label_{exercise_type}")
            if year_goal_label:
                year_goal_label.setText(f"📅 Roční cíl {selected_year}: {total_yearly_goal:,}")
            
            progress_bar = self.findChild(QProgressBar, f"progress_bar_{exercise_type}")
            if progress_bar and goal_to_date > 0:
                percentage = int((total_performed / goal_to_date) * 100)
                progress_bar.setValue(percentage)
                progress_bar.setFormat(f"{total_performed:,} / {goal_to_date:,} ({percentage}%)")
            elif progress_bar:
                progress_bar.setValue(0)
                progress_bar.setFormat("Žádný cíl")
            
            stats_label = self.findChild(QLabel, f"stats_label_{exercise_type}")
            if stats_label:
                remaining = max(0, goal_to_date - total_performed)
                
                days_trained = sum(1 for date_str, workouts in self.data['workouts'].items() 
                                 if int(date_str.split('-')[0]) == selected_year and exercise_type in workouts)
                
                stats_label.setText(
                    f"Splněno: {total_performed:,} | Zbývá: {remaining:,} | Dní: {days_trained}"
                )
            
            table = self.findChild(QTableWidget, f"table_{exercise_type}")
            if table:
                table.setRowCount(0)
                
                # Sesbírat všechny záznamy
                all_records = []
                for date_str in self.data['workouts'].keys():
                    workout_year = int(date_str.split('-')[0])
                    if workout_year == selected_year and exercise_type in self.data['workouts'][date_str]:
                        records = self.data['workouts'][date_str][exercise_type]
                        
                        if isinstance(records, list):
                            for record in records:
                                all_records.append((date_str, record))
                        elif isinstance(records, dict):
                            all_records.append((date_str, records))
                
                # Seřadit podle data a času
                all_records.sort(key=lambda x: (x[0], x[1].get('timestamp', '')), reverse=True)
                
                for date_str, record in all_records:
                    value = record['value']
                    timestamp = record.get('timestamp', 'N/A')
                    time_only = timestamp.split(' ')[1] if ' ' in timestamp else timestamp
                    record_id = record.get('id', str(uuid.uuid4()))
                    
                    row = table.rowCount()
                    table.insertRow(row)
                    
                    # Checkbox
                    checkbox = QCheckBox()
                    checkbox_widget = QWidget()
                    checkbox_layout = QHBoxLayout(checkbox_widget)
                    checkbox_layout.addWidget(checkbox)
                    checkbox_layout.setAlignment(Qt.AlignCenter)
                    checkbox_layout.setContentsMargins(0, 0, 0, 0)
                    table.setCellWidget(row, 0, checkbox_widget)
                    
                    # Datum (s ID v UserRole)
                    date_item = QTableWidgetItem(date_str)
                    date_item.setData(Qt.UserRole, record_id)
                    table.setItem(row, 1, date_item)
                    
                    table.setItem(row, 2, QTableWidgetItem(time_only))
                    table.setItem(row, 3, QTableWidgetItem(str(value)))
        except Exception as e:
            print(f"Chyba při update_exercise_tab pro {exercise_type}: {e}")

    def refresh_exercise_calendar(self, exercise_type):
        """Vytvoří roční kalendář"""
        try:
            if exercise_type not in self.exercise_calendar_widgets:
                return
            
            calendar_layout = self.exercise_calendar_widgets[exercise_type]
            
            while calendar_layout.count():
                child = calendar_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
            
            if exercise_type not in self.exercise_year_selectors:
                return
            
            selector = self.exercise_year_selectors[exercise_type]
            if not selector or not selector.currentText():
                return
            
            selected_year = int(selector.currentText())
            
            months = ['Leden', 'Únor', 'Březen', 'Duben', 'Květen', 'Červen',
                      'Červenec', 'Srpen', 'Září', 'Říjen', 'Listopad', 'Prosinec']
            
            months_grid = QGridLayout()
            months_grid.setSpacing(8)
            months_grid.setContentsMargins(5, 5, 5, 5)
            
            for month_num in range(1, 13):
                month_widget = self.create_month_calendar_for_exercise(selected_year, month_num, months[month_num-1], exercise_type)
                month_widget.setMinimumWidth(180)
                row = (month_num - 1) // 3
                col = (month_num - 1) % 3
                months_grid.addWidget(month_widget, row, col)
            
            # Responsive columns
            for col in range(3):
                months_grid.setColumnStretch(col, 1)
            
            calendar_layout.addLayout(months_grid)
            
            self.update_year_statistics(exercise_type, selected_year)
        except Exception as e:
            print(f"Chyba při refresh_exercise_calendar pro {exercise_type}: {e}")

    def create_month_calendar_for_exercise(self, year, month, month_name, exercise_type):
        """Vytvoří kalendář měsíce s GRADIENTNÍMI BARVAMI"""
        group = QGroupBox(f"{month_name}")
        group.setStyleSheet("""
            QGroupBox { 
                font-size: 11px; 
                background-color: #2d2d2d;
                border: 1px solid #3d3d3d;
            }
        """)
        layout = QGridLayout()
        layout.setSpacing(2)
        layout.setContentsMargins(5, 5, 5, 5)
        
        days = ['Po', 'Út', 'St', 'Čt', 'Pá', 'So', 'Ne']
        for col, day in enumerate(days):
            label = QLabel(day)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("font-weight: bold; padding: 2px; color: #e0e0e0; font-size: 9px;")
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
            day_label.setFixedSize(25, 25)
            day_label.setFrameStyle(QFrame.Box)
            
            # Gradientní barvy
            color, tooltip_text = self.get_day_color_gradient(date_str, date.date(), today, start_date, exercise_type)
            
            # Zvýraznění dnešního dne
            border_style = "border: 2px solid #87CEEB;" if date.date() == today else "border: 1px solid #3d3d3d;"
            
            day_label.setStyleSheet(
                f"background-color: {color}; font-weight: bold; color: #ffffff; {border_style} font-size: 9px;"
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
        
        if date > today:
            goal = self.calculate_goal(exercise_type, date_str)
            return '#8B0000', f"Budoucí den\nCíl: {goal}"
        
        goal = self.calculate_goal(exercise_type, date_str)
        
        if date_str in self.data['workouts']:
            workout = self.data['workouts'][date_str]
            if exercise_type in workout:
                records = workout[exercise_type]
                
                # Sečti všechny záznamy za den
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
                    intensity = min(difference / goal, 1.0)
                    green_val = int(144 + (100 - 144) * intensity)
                    color = f'#{0:02x}{green_val:02x}{0:02x}'
                    status = f"Náskok +{difference}"
                elif difference == 0:
                    color = '#FFD700'
                    status = "Přesně podle plánu"
                elif difference >= -goal * 0.5:
                    intensity = abs(difference) / (goal * 0.5)
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
        
        current_date = from_date
        while current_date <= to_date:
            date_str = current_date.strftime('%Y-%m-%d')
            
            goal = self.calculate_goal(exercise_type, date_str)
            total_goal += goal
            
            if date_str in self.data['workouts'] and exercise_type in self.data['workouts'][date_str]:
                records = self.data['workouts'][date_str][exercise_type]
                
                if isinstance(records, list):
                    total_performed += sum(r['value'] for r in records)
                elif isinstance(records, dict):
                    total_performed += records.get('value', 0)
            
            current_date += timedelta(days=1)
        
        return total_performed - total_goal

    def update_year_statistics(self, exercise_type, year):
        """Aktualizuje statistiky roku"""
        stats_label = self.findChild(QLabel, f"stats_year_label_{exercise_type}")
        if not stats_label:
            return
        
        year_workouts = {}
        for date_str, data in self.data['workouts'].items():
            workout_year = int(date_str.split('-')[0])
            if workout_year == year and exercise_type in data:
                year_workouts[date_str] = data
        
        total_days = len(year_workouts)
        
        days_achieved = 0
        for date_str in year_workouts.keys():
            workout_data = year_workouts[date_str][exercise_type]
            if isinstance(workout_data, dict):
                value = workout_data['value']
            else:
                value = workout_data
            
            goal = self.calculate_goal(exercise_type, date_str)
            if value >= goal:
                days_achieved += 1
        
        today = datetime.now()
        if year == today.year:
            days_in_year = (today - datetime(year, 1, 1)).days + 1
        elif year < today.year:
            days_in_year = 365 + (1 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 0)
        else:
            days_in_year = 0
        
        if days_in_year > 0:
            activity_percent = (total_days / days_in_year) * 100
            achievement_percent = (days_achieved / total_days * 100) if total_days > 0 else 0
        else:
            activity_percent = 0
            achievement_percent = 0
        
        stats_label.setText(
            f"📊 Rok {year}: {total_days} dnů s cvičením ({activity_percent:.1f}%) | "
            f"Splněno cílů: {days_achieved}/{total_days} ({achievement_percent:.1f}%)"
        )


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_THEME)
    window = FitnessTrackerApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
