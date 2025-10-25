#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fitness Tracker - Aplikace pro sledování cvičení s progresivními cíli
Verze 1.0.0

Changelog:
v1.0.0 (25.10.2025)
- Přidána správa roků v nastavení
- Časové značky pro všechny záznamy
- Verzování aplikace
- Plná podpora kalendářních roků
- Dark theme design
- Editace a mazání záznamů
- Náskok/skluz oproti plánu
- Proporcionální první týden
- Automatické ukládání stavu
"""

import sys
import json
from datetime import datetime, timedelta
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QLabel, QSpinBox, QPushButton, QDateEdit, QTableWidget,
    QTableWidgetItem, QGroupBox, QFormLayout, QHeaderView, QMessageBox,
    QGridLayout, QComboBox, QScrollArea, QFrame, QProgressBar, QTextEdit,
    QDialog, QListWidget, QListWidgetItem
)
from PySide6.QtCore import Qt, QDate, QTimer
from PySide6.QtGui import QColor, QPalette

# Verze aplikace
VERSION = "1.0.0"
VERSION_DATE = "25.10.2025"

# Dark Theme Stylesheet
DARK_THEME = """
/* Hlavní okno a základní widgety */
QMainWindow, QWidget {
    background-color: #1e1e1e;
    color: #e0e0e0;
}

/* Záložky */
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

/* GroupBox */
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

/* Labels */
QLabel {
    color: #e0e0e0;
    background-color: transparent;
}

/* SpinBox */
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

/* DateEdit */
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

/* Calendar Widget */
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

/* Buttons */
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

/* ComboBox */
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

/* ListWidget */
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

/* Table */
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

/* ScrollBar */
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

/* ScrollArea */
QScrollArea {
    background-color: #1e1e1e;
    border: 1px solid #3d3d3d;
}

/* TextEdit */
QTextEdit {
    background-color: #2d2d2d;
    color: #e0e0e0;
    border: 1px solid #3d3d3d;
    border-radius: 5px;
}

/* ProgressBar */
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

/* Frame */
QFrame {
    background-color: #2d2d2d;
    border: 1px solid #3d3d3d;
}

/* Dialog */
QDialog {
    background-color: #1e1e1e;
    color: #e0e0e0;
}

/* MessageBox */
QMessageBox {
    background-color: #1e1e1e;
    color: #e0e0e0;
}

QMessageBox QPushButton {
    min-width: 80px;
}
"""


class EditWorkoutDialog(QDialog):
    """Dialog pro editaci existujícího záznamu"""
    def __init__(self, exercise_type, date_str, current_value, timestamp, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Upravit záznam - {exercise_type}")
        self.exercise_type = exercise_type
        self.date_str = date_str
        
        layout = QVBoxLayout(self)
        
        info_label = QLabel(f"Upravit záznam pro {exercise_type} dne {date_str}")
        info_label.setStyleSheet("font-weight: bold; padding: 10px; color: #e0e0e0;")
        layout.addWidget(info_label)
        
        # Zobrazení času vytvoření
        if timestamp:
            time_label = QLabel(f"Přidáno: {timestamp}")
            time_label.setStyleSheet("font-size: 11px; color: #a0a0a0; padding: 5px;")
            layout.addWidget(time_label)
        
        form_layout = QFormLayout()
        
        self.value_spin = QSpinBox()
        self.value_spin.setRange(0, 1000)
        self.value_spin.setValue(current_value)
        form_layout.addRow(f"Nový počet {exercise_type}:", self.value_spin)
        
        layout.addLayout(form_layout)
        
        buttons_layout = QHBoxLayout()
        
        save_btn = QPushButton("💾 Uložit")
        save_btn.clicked.connect(self.accept)
        buttons_layout.addWidget(save_btn)
        
        delete_btn = QPushButton("🗑️ Smazat záznam")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
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
        
        self.delete_requested = False
    
    def delete_record(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Potvrzení smazání")
        msg.setText(f"Opravdu chceš smazat záznam pro {self.exercise_type} ze dne {self.date_str}?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        
        yes_btn = msg.button(QMessageBox.Yes)
        yes_btn.setText("Ano")
        no_btn = msg.button(QMessageBox.No)
        no_btn.setText("Ne")
        
        if msg.exec() == QMessageBox.Yes:
            self.delete_requested = True
            self.accept()
    
    def get_value(self):
        return self.value_spin.value()


class FitnessTrackerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"Fitness Tracker v{VERSION} - Sledování cvičení")
        self.setMinimumSize(1200, 700)
        
        self.data_file = Path("fitness_data.json")
        self.exercise_year_selectors = {}
        
        self.load_data()
        self.migrate_data()  # Migrace starých dat na nový formát s timestampy
        self.setup_ui()
        self.restore_app_state()
        
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.auto_refresh)
        self.update_timer.start(5000)
        
    def closeEvent(self, event):
        self.save_app_state()
        event.accept()
    
    def migrate_data(self):
        """Migrace starých dat na nový formát s timestampy"""
        migrated = False
        for date_str, workouts in self.data['workouts'].items():
            for exercise, value in workouts.items():
                # Pokud je hodnota jen číslo (starý formát), převedeme na nový formát
                if isinstance(value, (int, float)):
                    workouts[exercise] = {
                        'value': int(value),
                        'timestamp': f"{date_str} 12:00:00"  # Výchozí čas pro staré záznamy
                    }
                    migrated = True
        
        if migrated:
            self.save_data()
            print("Data byla migrována na nový formát s timestampy")
        
    def load_data(self):
        if self.data_file.exists():
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        else:
            current_year = datetime.now().year
            self.data = {
                'version': VERSION,
                'settings': {
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
                },
                'workouts': {},
                'app_state': {
                    'last_tab': 0,
                    'window_geometry': None,
                    'selected_year': datetime.now().year,
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
        self.data['app_state']['last_tab'] = self.tabs.currentIndex()
        self.data['app_state']['window_geometry'] = {
            'x': self.x(),
            'y': self.y(),
            'width': self.width(),
            'height': self.height()
        }
        
        if hasattr(self, 'overview_year_selector'):
            self.data['app_state']['selected_year'] = int(self.overview_year_selector.currentText())
        
        if 'exercise_years' not in self.data['app_state']:
            self.data['app_state']['exercise_years'] = {}
        
        for exercise, selector in self.exercise_year_selectors.items():
            self.data['app_state']['exercise_years'][exercise] = int(selector.currentText())
        
        self.save_data()
    
    def restore_app_state(self):
        if 'app_state' in self.data:
            if self.data['app_state']['window_geometry']:
                geom = self.data['app_state']['window_geometry']
                self.setGeometry(geom['x'], geom['y'], geom['width'], geom['height'])
            
            if 'last_tab' in self.data['app_state']:
                self.tabs.setCurrentIndex(self.data['app_state']['last_tab'])
            
            if 'exercise_years' in self.data['app_state']:
                for exercise, year in self.data['app_state']['exercise_years'].items():
                    if exercise in self.exercise_year_selectors:
                        selector = self.exercise_year_selectors[exercise]
                        index = selector.findText(str(year))
                        if index >= 0:
                            selector.setCurrentIndex(index)
            
            if hasattr(self, 'overview_year_selector') and 'selected_year' in self.data['app_state']:
                year = str(self.data['app_state']['selected_year'])
                index = self.overview_year_selector.findText(year)
                if index >= 0:
                    self.overview_year_selector.setCurrentIndex(index)
    
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        self.tabs = QTabWidget()
        self.tabs.currentChanged.connect(self.on_tab_changed)
        layout.addWidget(self.tabs)
        
        self.tabs.addTab(self.create_settings_tab(), "⚙️ Nastavení")
        self.tabs.addTab(self.create_exercise_tab('kliky', '💪'), "💪 Kliky")
        self.tabs.addTab(self.create_exercise_tab('dřepy', '🦵'), "🦵 Dřepy")
        self.tabs.addTab(self.create_exercise_tab('skrčky', '🧘'), "🧘 Skrčky")
        self.tabs.addTab(self.create_overview_tab(), "📊 Roční přehled")
        
    def on_tab_changed(self, index):
        tab_name = self.tabs.tabText(index)
        if tab_name == "📊 Roční přehled":
            self.refresh_overview()
        elif "💪" in tab_name:
            self.update_exercise_tab('kliky')
        elif "🦵" in tab_name:
            self.update_exercise_tab('dřepy')
        elif "🧘" in tab_name:
            self.update_exercise_tab('skrčky')
    
    def auto_refresh(self):
        current_tab = self.tabs.currentIndex()
        tab_name = self.tabs.tabText(current_tab)
        
        if tab_name == "📊 Roční přehled":
            self.refresh_overview()
        elif "💪" in tab_name:
            self.update_exercise_tab('kliky')
        elif "🦵" in tab_name:
            self.update_exercise_tab('dřepy')
        elif "🧘" in tab_name:
            self.update_exercise_tab('skrčky')
    
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
        """Vrátí seznam všech roků, ve kterých jsou záznamy nebo aktuální rok"""
        current_year = datetime.now().year
        years = set([current_year])
        
        for date_str in self.data['workouts'].keys():
            year = int(date_str.split('-')[0])
            years.add(year)
        
        start_year = int(self.data['settings']['start_date'].split('-')[0])
        years.add(start_year)
        
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
            # Smazání všech záznamů pro daný rok
            dates_to_delete = []
            for date_str in self.data['workouts'].keys():
                if int(date_str.split('-')[0]) == year:
                    dates_to_delete.append(date_str)
            
            for date_str in dates_to_delete:
                del self.data['workouts'][date_str]
            
            self.save_data()
            
            # Aktualizace všech selectorů roků
            for exercise in ['kliky', 'dřepy', 'skrčky']:
                if exercise in self.exercise_year_selectors:
                    selector = self.exercise_year_selectors[exercise]
                    selector.clear()
                    for y in self.get_available_years():
                        selector.addItem(str(y))
                    selector.setCurrentText(str(datetime.now().year))
            
            if hasattr(self, 'overview_year_selector'):
                self.overview_year_selector.clear()
                for y in self.get_available_years():
                    self.overview_year_selector.addItem(str(y))
                self.overview_year_selector.setCurrentText(str(datetime.now().year))
            
            # Obnovení záložky nastavení
            self.tabs.setCurrentIndex(0)
            
            self.show_message("Smazáno", f"Všechna data pro rok {year} byla smazána.")
            
            # Aktualizace všech zobrazení
            for exercise in ['kliky', 'dřepy', 'skrčky']:
                self.update_exercise_tab(exercise)
            self.refresh_overview()
    
    def create_settings_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Verze aplikace
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
        
        # Správa roků
        years_group = QGroupBox("📅 Správa roků")
        years_layout = QVBoxLayout()
        
        available_years = self.get_available_years()
        years_text = f"Dostupné roky s daty: {', '.join(map(str, available_years))}"
        
        info_label = QLabel(years_text)
        info_label.setStyleSheet("padding: 10px; color: #14919b;")
        info_label.setWordWrap(True)
        years_layout.addWidget(info_label)
        
        # Seznam roků
        self.years_list = QListWidget()
        self.years_list.setMaximumHeight(150)
        for year in available_years:
            # Počet záznamů pro tento rok
            year_workouts = sum(1 for date_str in self.data['workouts'].keys() 
                              if int(date_str.split('-')[0]) == year)
            
            item = QListWidgetItem(f"📆 Rok {year} ({year_workouts} dnů s cvičením)")
            item.setData(Qt.UserRole, year)
            self.years_list.addItem(item)
        
        years_layout.addWidget(self.years_list)
        
        # Tlačítka pro správu roků
        years_buttons = QHBoxLayout()
        
        add_year_btn = QPushButton("➕ Začít nový rok")
        add_year_btn.clicked.connect(self.add_new_year)
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
        
        # Upozornění
        warning_label = QLabel(
            "⚠️ Poznámka: První týden je proporcionální podle počtu dní.\n"
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
        
        # Skupina: Startovní datum
        date_group = QGroupBox("Startovní datum")
        date_layout = QFormLayout()
        
        self.start_date_edit = QDateEdit()
        start_date = QDate.fromString(self.data['settings']['start_date'], 'yyyy-MM-dd')
        self.start_date_edit.setDate(start_date)
        self.start_date_edit.setCalendarPopup(True)
        date_layout.addRow("Datum zahájení:", self.start_date_edit)
        
        date_group.setLayout(date_layout)
        layout.addWidget(date_group)
        
        # Skupina: Základní cíle
        base_goals_group = QGroupBox("Základní cíle (na startovní datum)")
        base_goals_layout = QFormLayout()
        
        self.base_kliky = QSpinBox()
        self.base_kliky.setRange(0, 1000)
        self.base_kliky.setValue(self.data['settings']['base_goals']['kliky'])
        base_goals_layout.addRow("Kliky:", self.base_kliky)
        
        self.base_drepy = QSpinBox()
        self.base_drepy.setRange(0, 1000)
        self.base_drepy.setValue(self.data['settings']['base_goals']['dřepy'])
        base_goals_layout.addRow("Dřepy:", self.base_drepy)
        
        self.base_skrcky = QSpinBox()
        self.base_skrcky.setRange(0, 1000)
        self.base_skrcky.setValue(self.data['settings']['base_goals']['skrčky'])
        base_goals_layout.addRow("Skrčky:", self.base_skrcky)
        
        base_goals_group.setLayout(base_goals_layout)
        layout.addWidget(base_goals_group)
        
        # Skupina: Týdenní přírůstky
        increment_group = QGroupBox("Týdenní přírůstky (za každý celý týden)")
        increment_layout = QFormLayout()
        
        self.increment_kliky = QSpinBox()
        self.increment_kliky.setRange(0, 100)
        self.increment_kliky.setValue(self.data['settings']['weekly_increment']['kliky'])
        increment_layout.addRow("Kliky (+týdně):", self.increment_kliky)
        
        self.increment_drepy = QSpinBox()
        self.increment_drepy.setRange(0, 100)
        self.increment_drepy.setValue(self.data['settings']['weekly_increment']['dřepy'])
        increment_layout.addRow("Dřepy (+týdně):", self.increment_drepy)
        
        self.increment_skrcky = QSpinBox()
        self.increment_skrcky.setRange(0, 100)
        self.increment_skrcky.setValue(self.data['settings']['weekly_increment']['skrčky'])
        increment_layout.addRow("Skrčky (+týdně):", self.increment_skrcky)
        
        increment_group.setLayout(increment_layout)
        layout.addWidget(increment_group)
        
        # Tlačítka
        save_btn = QPushButton("💾 Uložit nastavení")
        save_btn.clicked.connect(self.save_settings)
        layout.addWidget(save_btn)
        
        diag_btn = QPushButton("🔍 Zobrazit diagnostiku výpočtu cílů")
        diag_btn.clicked.connect(self.show_diagnostics)
        layout.addWidget(diag_btn)
        
        layout.addStretch()
        
        return widget
    
    def delete_year_from_list(self):
        """Smaže vybraný rok ze seznamu"""
        selected_items = self.years_list.selectedItems()
        if not selected_items:
            self.show_message("Chyba", "Vyber rok, který chceš smazat", QMessageBox.Warning)
            return
        
        year = selected_items[0].data(Qt.UserRole)
        self.delete_year_data(year)
        
        # Obnovení seznamu roků
        self.years_list.clear()
        for y in self.get_available_years():
            year_workouts = sum(1 for date_str in self.data['workouts'].keys() 
                              if int(date_str.split('-')[0]) == y)
            item = QListWidgetItem(f"📆 Rok {y} ({year_workouts} dnů s cvičením)")
            item.setData(Qt.UserRole, y)
            self.years_list.addItem(item)
    
    def add_new_year(self):
        """Přidá aktuální rok do sledování"""
        current_year = datetime.now().year
        
        has_current_year = any(
            int(date_str.split('-')[0]) == current_year 
            for date_str in self.data['workouts'].keys()
        )
        
        if has_current_year:
            self.show_message(
                "Informace", 
                f"Rok {current_year} už je v seznamu sledovaných roků!",
                QMessageBox.Information
            )
        else:
            for selector in self.exercise_year_selectors.values():
                if selector.findText(str(current_year)) == -1:
                    selector.insertItem(0, str(current_year))
                    selector.setCurrentText(str(current_year))
            
            if hasattr(self, 'overview_year_selector'):
                if self.overview_year_selector.findText(str(current_year)) == -1:
                    self.overview_year_selector.insertItem(0, str(current_year))
                    self.overview_year_selector.setCurrentText(str(current_year))
            
            # Obnovení seznamu roků
            self.years_list.clear()
            for year in self.get_available_years():
                year_workouts = sum(1 for date_str in self.data['workouts'].keys() 
                                  if int(date_str.split('-')[0]) == year)
                item = QListWidgetItem(f"📆 Rok {year} ({year_workouts} dnů s cvičením)")
                item.setData(Qt.UserRole, year)
                self.years_list.addItem(item)
            
            self.show_message(
                "Úspěch",
                f"Rok {current_year} byl přidán do sledování!\nMůžeš začít zaznamenávat svá cvičení.",
                QMessageBox.Information
            )
    
    def show_diagnostics(self):
        """Zobrazí diagnostické okno s výpočty"""
        diag_window = QWidget()
        diag_window.setWindowTitle("Diagnostika výpočtu cílů")
        diag_window.resize(800, 500)
        
        layout = QVBoxLayout(diag_window)
        
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        
        start_date_str = self.data['settings']['start_date']
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        
        diag_text = f"📊 DIAGNOSTIKA VÝPOČTU CÍLŮ\n{'='*70}\n\n"
        diag_text += f"Verze aplikace: {VERSION}\n"
        diag_text += f"Startovní datum: {start_date_str} ({['Po', 'Út', 'St', 'Čt', 'Pá', 'So', 'Ne'][start_date.weekday()]})\n"
        
        days_to_sunday = 6 - start_date.weekday()
        first_week_end = start_date + timedelta(days=days_to_sunday)
        first_full_week_start = first_week_end + timedelta(days=1)
        
        diag_text += f"Konec prvního (neúplného) týdne: {first_week_end.strftime('%Y-%m-%d')}\n"
        diag_text += f"Začátek prvního celého týdne: {first_full_week_start.strftime('%Y-%m-%d')}\n\n"
        
        for exercise in ['kliky', 'dřepy', 'skrčky']:
            base = self.data['settings']['base_goals'][exercise]
            increment = self.data['settings']['weekly_increment'][exercise]
            
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
                (datetime(2025, 12, 31)).strftime('%Y-%m-%d')
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
    
    def save_settings(self):
        self.data['settings']['start_date'] = self.start_date_edit.date().toString('yyyy-MM-dd')
        self.data['settings']['base_goals']['kliky'] = self.base_kliky.value()
        self.data['settings']['base_goals']['dřepy'] = self.base_drepy.value()
        self.data['settings']['base_goals']['skrčky'] = self.base_skrcky.value()
        self.data['settings']['weekly_increment']['kliky'] = self.increment_kliky.value()
        self.data['settings']['weekly_increment']['dřepy'] = self.increment_drepy.value()
        self.data['settings']['weekly_increment']['skrčky'] = self.increment_skrcky.value()
        
        self.save_data()
        self.show_message("Uloženo", "Nastavení bylo úspěšně uloženo!")
        
        for exercise in ['kliky', 'dřepy', 'skrčky']:
            self.update_exercise_tab(exercise)
        self.refresh_overview()
    
    def create_exercise_tab(self, exercise_type, icon):
        """Vytvoří záložku pro konkrétní cvičení"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Přepínač roku nahoře
        year_selector_layout = QHBoxLayout()
        year_selector_layout.addWidget(QLabel(f"📅 Zobrazit rok:"))
        
        year_selector = QComboBox()
        for year in self.get_available_years():
            year_selector.addItem(str(year))
        year_selector.setCurrentText(str(datetime.now().year))
        year_selector.currentTextChanged.connect(lambda: self.update_exercise_tab(exercise_type))
        
        self.exercise_year_selectors[exercise_type] = year_selector
        
        year_selector_layout.addWidget(year_selector)
        year_selector_layout.addStretch()
        
        layout.addLayout(year_selector_layout)
        
        # Panel s cíli
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
        today_goal_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #14919b; padding: 5px;")
        goals_layout.addWidget(today_goal_label)
        
        calc_label = QLabel()
        calc_label.setObjectName(f"calc_label_{exercise_type}")
        calc_label.setStyleSheet("font-size: 11px; color: #a0a0a0; padding: 2px; font-style: italic;")
        goals_layout.addWidget(calc_label)
        
        performance_label = QLabel()
        performance_label.setObjectName(f"performance_label_{exercise_type}")
        performance_label.setStyleSheet("font-size: 14px; font-weight: bold; padding: 5px;")
        goals_layout.addWidget(performance_label)
        
        year_goal_label = QLabel()
        year_goal_label.setObjectName(f"year_goal_label_{exercise_type}")
        year_goal_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #32c766; padding: 5px;")
        goals_layout.addWidget(year_goal_label)
        
        progress_bar = QProgressBar()
        progress_bar.setObjectName(f"progress_bar_{exercise_type}")
        progress_bar.setTextVisible(True)
        goals_layout.addWidget(progress_bar)
        
        stats_label = QLabel()
        stats_label.setObjectName(f"stats_label_{exercise_type}")
        stats_label.setStyleSheet("font-size: 12px; color: #a0a0a0; padding: 5px;")
        goals_layout.addWidget(stats_label)
        
        layout.addWidget(goals_frame)
        
        # Zadání výkonu
        input_group = QGroupBox("Zadání výkonu")
        input_layout = QHBoxLayout()
        
        date_edit = QDateEdit()
        date_edit.setDate(QDate.currentDate())
        date_edit.setCalendarPopup(True)
        input_layout.addWidget(QLabel("Datum:"))
        input_layout.addWidget(date_edit)
        
        value_spin = QSpinBox()
        value_spin.setRange(0, 1000)
        value_spin.setValue(0)
        input_layout.addWidget(QLabel(f"Počet {exercise_type}:"))
        input_layout.addWidget(value_spin)
        
        add_btn = QPushButton("➕ Přidat výkon")
        add_btn.clicked.connect(
            lambda: self.add_workout(exercise_type, date_edit.date().toString('yyyy-MM-dd'), value_spin.value())
        )
        input_layout.addWidget(add_btn)
        
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)
        
        # Tabulka s historií - PŘIDÁN SLOUPEC ČAS
        table = QTableWidget()
        table.setObjectName(f"table_{exercise_type}")
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels(["Datum", "Čas přidání", "Výkon", "Cíl", "Splněno", "Akce"])
        
        table.verticalHeader().setDefaultSectionSize(35)
        table.verticalHeader().setMinimumSectionSize(35)
        
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        
        layout.addWidget(table)
        
        self.update_exercise_tab(exercise_type)
        
        return widget
    
    def calculate_goal(self, exercise_type, date_str):
        start_date = datetime.strptime(self.data['settings']['start_date'], '%Y-%m-%d')
        target_date = datetime.strptime(date_str, '%Y-%m-%d')
        
        base_goal = self.data['settings']['base_goals'][exercise_type]
        increment = self.data['settings']['weekly_increment'][exercise_type]
        
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
        start_date = datetime.strptime(self.data['settings']['start_date'], '%Y-%m-%d')
        target_date = datetime.strptime(date_str, '%Y-%m-%d')
        
        base = self.data['settings']['base_goals'][exercise_type]
        increment = self.data['settings']['weekly_increment'][exercise_type]
        
        days_to_sunday = 6 - start_date.weekday()
        first_week_end = start_date + timedelta(days=days_to_sunday)
        
        if target_date <= first_week_end:
            return f"První (neúplný) týden: základní cíl = {base}"
        
        first_full_week_start = first_week_end + timedelta(days=1)
        days_since = (target_date - first_full_week_start).days
        full_weeks = (days_since // 7) + 1
        
        return f"Výpočet: {base} + {full_weeks} celých týdnů × {increment} = {base + full_weeks * increment}"
    
    def calculate_yearly_goal(self, exercise_type, year):
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
        total_goal = self.calculate_yearly_goal(exercise_type, year)
        
        total_performed = 0
        for date_str, workouts in self.data['workouts'].items():
            workout_year = int(date_str.split('-')[0])
            if workout_year == year and exercise_type in workouts:
                workout_data = workouts[exercise_type]
                if isinstance(workout_data, dict):
                    total_performed += workout_data['value']
                else:
                    total_performed += workout_data
        
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
    
    def add_workout(self, exercise_type, date_str, value):
        if value == 0:
            self.show_message("Chyba", "Zadej nenulovou hodnotu!", QMessageBox.Warning)
            return
        
        if date_str not in self.data['workouts']:
            self.data['workouts'][date_str] = {}
        
        # Uložení s časovou značkou
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.data['workouts'][date_str][exercise_type] = {
            'value': value,
            'timestamp': timestamp
        }
        
        self.save_data()
        
        self.update_exercise_tab(exercise_type)
        self.refresh_overview()
        
        self.show_message("Přidáno", f"Výkon byl zaznamenán: {value} {exercise_type}\nČas: {timestamp}")
    
    def edit_workout(self, exercise_type, date_str):
        workout_data = self.data['workouts'][date_str][exercise_type]
        
        if isinstance(workout_data, dict):
            current_value = workout_data['value']
            timestamp = workout_data.get('timestamp', 'N/A')
        else:
            current_value = workout_data
            timestamp = None
        
        dialog = EditWorkoutDialog(exercise_type, date_str, current_value, timestamp, self)
        
        if dialog.exec():
            if dialog.delete_requested:
                del self.data['workouts'][date_str][exercise_type]
                
                if not self.data['workouts'][date_str]:
                    del self.data['workouts'][date_str]
                
                self.show_message("Smazáno", "Záznam byl smazán")
            else:
                new_value = dialog.get_value()
                # Zachování původního timestampu, přidání úpravy
                edit_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.data['workouts'][date_str][exercise_type] = {
                    'value': new_value,
                    'timestamp': timestamp if timestamp else edit_timestamp,
                    'edited': edit_timestamp
                }
                self.show_message("Upraveno", f"Záznam byl upraven na: {new_value} {exercise_type}")
            
            self.save_data()
            self.update_exercise_tab(exercise_type)
            self.refresh_overview()
    
    def update_exercise_tab(self, exercise_type):
        """Aktualizuje zobrazení záložky cvičení"""
        selected_year = int(self.exercise_year_selectors[exercise_type].currentText())
        
        today = datetime.now()
        today_str = today.strftime('%Y-%m-%d')
        
        today_goal = self.calculate_goal(exercise_type, today_str)
        today_goal_label = self.findChild(QLabel, f"today_goal_label_{exercise_type}")
        if today_goal_label:
            today_goal_label.setText(f"🎯 Dnešní cíl: {today_goal} {exercise_type}")
        
        calc_label = self.findChild(QLabel, f"calc_label_{exercise_type}")
        if calc_label:
            calc_text = self.get_goal_calculation_text(exercise_type, today_str)
            calc_label.setText(calc_text)
        
        total_performed, total_yearly_goal, goal_to_date = self.calculate_yearly_progress(exercise_type, selected_year)
        difference = total_performed - goal_to_date
        
        performance_label = self.findChild(QLabel, f"performance_label_{exercise_type}")
        if performance_label:
            if difference > 0:
                performance_label.setText(f"📈 Náskok: +{difference:,} {exercise_type} nad plán")
                performance_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #32c766; padding: 5px;")
            elif difference < 0:
                performance_label.setText(f"📉 Skluz: {difference:,} {exercise_type} pod plán")
                performance_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #ff6b6b; padding: 5px;")
            else:
                performance_label.setText(f"✅ Přesně podle plánu")
                performance_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #14919b; padding: 5px;")
        
        year_goal_label = self.findChild(QLabel, f"year_goal_label_{exercise_type}")
        if year_goal_label:
            year_goal_label.setText(
                f"📅 Roční cíl {selected_year}: {total_yearly_goal:,} {exercise_type} celkem"
            )
        
        progress_bar = self.findChild(QProgressBar, f"progress_bar_{exercise_type}")
        if progress_bar and goal_to_date > 0:
            percentage = int((total_performed / goal_to_date) * 100)
            progress_bar.setValue(percentage)
            progress_bar.setFormat(f"{total_performed:,} / {goal_to_date:,} ({percentage}%)")
        elif progress_bar:
            progress_bar.setValue(0)
            progress_bar.setFormat("Žádný cíl pro tento rok")
        
        stats_label = self.findChild(QLabel, f"stats_label_{exercise_type}")
        if stats_label:
            remaining = max(0, goal_to_date - total_performed)
            
            days_trained = sum(1 for date_str, workouts in self.data['workouts'].items() 
                             if int(date_str.split('-')[0]) == selected_year and exercise_type in workouts)
            
            stats_label.setText(
                f"📈 Splněno: {total_performed:,} | "
                f"🎯 Zbývá do dnes: {remaining:,} | "
                f"📊 Dní s tréninkem: {days_trained}"
            )
        
        table = self.findChild(QTableWidget, f"table_{exercise_type}")
        if table:
            table.setRowCount(0)
            
            selected_year_workouts = []
            for date_str in self.data['workouts'].keys():
                workout_year = int(date_str.split('-')[0])
                if workout_year == selected_year and exercise_type in self.data['workouts'][date_str]:
                    selected_year_workouts.append(date_str)
            
            sorted_dates = sorted(selected_year_workouts, reverse=True)
            
            for date_str in sorted_dates:
                workout_data = self.data['workouts'][date_str][exercise_type]
                
                if isinstance(workout_data, dict):
                    value = workout_data['value']
                    timestamp = workout_data.get('timestamp', 'N/A')
                    # Zobrazení pouze času (bez data)
                    time_only = timestamp.split(' ')[1] if ' ' in timestamp else timestamp
                else:
                    value = workout_data
                    time_only = 'N/A'
                
                goal = self.calculate_goal(exercise_type, date_str)
                achieved = value >= goal
                
                row = table.rowCount()
                table.insertRow(row)
                
                table.setItem(row, 0, QTableWidgetItem(date_str))
                table.setItem(row, 1, QTableWidgetItem(time_only))
                table.setItem(row, 2, QTableWidgetItem(str(value)))
                table.setItem(row, 3, QTableWidgetItem(str(goal)))
                
                status_item = QTableWidgetItem("✅ Ano" if achieved else "❌ Ne")
                if achieved:
                    status_item.setBackground(QColor(50, 200, 100))
                else:
                    status_item.setBackground(QColor(200, 50, 50))
                table.setItem(row, 4, status_item)
                
                edit_btn = QPushButton("✏️")
                edit_btn.setMaximumSize(30, 30)
                edit_btn.setToolTip("Upravit záznam")
                edit_btn.clicked.connect(lambda checked, d=date_str, e=exercise_type: self.edit_workout(e, d))
                table.setCellWidget(row, 5, edit_btn)
    
    def create_overview_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        controls_layout = QHBoxLayout()
        
        controls_layout.addWidget(QLabel("📅 Rok:"))
        self.overview_year_selector = QComboBox()
        for year in self.get_available_years():
            self.overview_year_selector.addItem(str(year))
        self.overview_year_selector.setCurrentText(str(datetime.now().year))
        self.overview_year_selector.currentTextChanged.connect(self.refresh_overview)
        controls_layout.addWidget(self.overview_year_selector)
        
        controls_layout.addStretch()
        
        refresh_btn = QPushButton("🔄 Aktualizovat")
        refresh_btn.clicked.connect(self.refresh_overview)
        controls_layout.addWidget(refresh_btn)
        
        layout.addLayout(controls_layout)
        
        legend_frame = QFrame()
        legend_frame.setStyleSheet("background-color: #2d2d2d; border: 1px solid #3d3d3d; padding: 5px;")
        legend_layout = QHBoxLayout(legend_frame)
        
        def create_color_sample(color, text):
            sample_layout = QHBoxLayout()
            color_box = QLabel()
            color_box.setFixedSize(20, 20)
            color_box.setStyleSheet(f"background-color: {color}; border: 1px solid #3d3d3d;")
            sample_layout.addWidget(color_box)
            sample_layout.addWidget(QLabel(text))
            return sample_layout
        
        legend_layout.addLayout(create_color_sample("#000000", "Před začátkem"))
        legend_layout.addLayout(create_color_sample("#90EE90", "Všechna cvičení"))
        legend_layout.addLayout(create_color_sample("#FFD700", "Částečně"))
        legend_layout.addLayout(create_color_sample("#FF6B6B", "Necvičil"))
        legend_layout.addLayout(create_color_sample("#4d4d4d", "Budoucí den"))
        legend_layout.addLayout(create_color_sample("#87CEEB", "Dnešek"))
        legend_layout.addStretch()
        layout.addWidget(legend_frame)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        self.calendar_widget = QWidget()
        self.calendar_layout = QVBoxLayout(self.calendar_widget)
        
        scroll.setWidget(self.calendar_widget)
        layout.addWidget(scroll)
        
        self.stats_label = QLabel()
        self.stats_label.setStyleSheet("font-size: 14px; padding: 10px; background-color: #2d2d2d; color: #e0e0e0; border-radius: 5px;")
        layout.addWidget(self.stats_label)
        
        return widget
    
    def refresh_overview(self):
        while self.calendar_layout.count():
            child = self.calendar_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        selected_year = int(self.overview_year_selector.currentText())
        
        months = ['Leden', 'Únor', 'Březen', 'Duben', 'Květen', 'Červen',
                  'Červenec', 'Srpen', 'Září', 'Říjen', 'Listopad', 'Prosinec']
        
        months_grid = QGridLayout()
        
        for month_num in range(1, 13):
            month_widget = self.create_month_calendar(selected_year, month_num, months[month_num-1])
            row = (month_num - 1) // 3
            col = (month_num - 1) % 3
            months_grid.addWidget(month_widget, row, col)
        
        self.calendar_layout.addLayout(months_grid)
        
        self.update_statistics(selected_year)
    
    def create_month_calendar(self, year, month, month_name):
        group = QGroupBox(f"{month_name} {year}")
        layout = QGridLayout()
        layout.setSpacing(2)
        
        days = ['Po', 'Út', 'St', 'Čt', 'Pá', 'So', 'Ne']
        for col, day in enumerate(days):
            label = QLabel(day)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("font-weight: bold; padding: 5px; color: #e0e0e0;")
            layout.addWidget(label, 0, col)
        
        first_day = datetime(year, month, 1)
        first_weekday = first_day.weekday()
        
        if month == 12:
            last_day = datetime(year + 1, 1, 1) - timedelta(days=1)
        else:
            last_day = datetime(year, month + 1, 1) - timedelta(days=1)
        days_in_month = last_day.day
        
        today = datetime.now().date()
        start_date = datetime.strptime(self.data['settings']['start_date'], '%Y-%m-%d').date()
        
        row = 1
        col = first_weekday
        
        for day in range(1, days_in_month + 1):
            date = datetime(year, month, day)
            date_str = date.strftime('%Y-%m-%d')
            
            day_label = QLabel(str(day))
            day_label.setAlignment(Qt.AlignCenter)
            day_label.setFixedSize(35, 35)
            day_label.setFrameStyle(QFrame.Box)
            
            color = self.get_day_color(date_str, date.date(), today, start_date)
            day_label.setStyleSheet(f"background-color: {color}; font-weight: bold; color: #ffffff; border: 1px solid #3d3d3d;")
            
            layout.addWidget(day_label, row, col)
            
            col += 1
            if col > 6:
                col = 0
                row += 1
        
        group.setLayout(layout)
        return group
    
    def get_day_color(self, date_str, date, today, start_date):
        if date < start_date:
            return '#000000'
        
        if date > today:
            return '#4d4d4d'
        
        if date == today:
            return '#87CEEB'
        
        if date_str in self.data['workouts']:
            workout = self.data['workouts'][date_str]
            exercises = ['kliky', 'dřepy', 'skrčky']
            count = sum(1 for ex in exercises if ex in workout)
            
            if count == 3:
                return '#90EE90'
            elif count > 0:
                return '#FFD700'
        
        return '#FF6B6B'
    
    def update_statistics(self, year):
        year_workouts = {}
        for date_str, data in self.data['workouts'].items():
            workout_year = int(date_str.split('-')[0])
            if workout_year == year:
                year_workouts[date_str] = data
        
        total_days = len(year_workouts)
        
        kliky_days = sum(1 for data in year_workouts.values() if 'kliky' in data)
        drepy_days = sum(1 for data in year_workouts.values() if 'dřepy' in data)
        skrcky_days = sum(1 for data in year_workouts.values() if 'skrčky' in data)
        
        complete_days = sum(1 for data in year_workouts.values() 
                           if all(ex in data for ex in ['kliky', 'dřepy', 'skrčky']))
        
        today = datetime.now()
        if year == today.year:
            days_in_year = (today - datetime(year, 1, 1)).days + 1
        elif year < today.year:
            days_in_year = 365 + (1 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 0)
        else:
            days_in_year = 0
        
        if days_in_year > 0:
            activity_percent = (total_days / days_in_year) * 100
        else:
            activity_percent = 0
        
        self.stats_label.setText(
            f"📊 Statistiky pro rok {year}:\n"
            f"Celkem dnů s cvičením: {total_days} ({activity_percent:.1f}% z uplynulých dní) | "
            f"Kompletní tréninky: {complete_days} | "
            f"Kliky: {kliky_days} dnů | Dřepy: {drepy_days} dnů | Skrčky: {skrcky_days} dnů"
        )


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_THEME)
    window = FitnessTrackerApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
