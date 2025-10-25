#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fitness Tracker - Aplikace pro sledování cvičení s progresivními cíli
Verze s opravenými detaily a náskokem/skluzem
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
    QDialog
)
from PySide6.QtCore import Qt, QDate, QTimer
from PySide6.QtGui import QColor, QPalette


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
    def __init__(self, exercise_type, date_str, current_value, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Upravit záznam - {exercise_type}")
        self.exercise_type = exercise_type
        self.date_str = date_str
        
        layout = QVBoxLayout(self)
        
        # Informace
        info_label = QLabel(f"Upravit záznam pro {exercise_type} dne {date_str}")
        info_label.setStyleSheet("font-weight: bold; padding: 10px; color: #e0e0e0;")
        layout.addWidget(info_label)
        
        # Zadání nové hodnoty
        form_layout = QFormLayout()
        
        self.value_spin = QSpinBox()
        self.value_spin.setRange(0, 1000)
        self.value_spin.setValue(current_value)
        form_layout.addRow(f"Nový počet {exercise_type}:", self.value_spin)
        
        layout.addLayout(form_layout)
        
        # Tlačítka
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
        """Označí, že uživatel chce smazat záznam"""
        reply = QMessageBox.question(
            self,
            "Potvrzení smazání",
            f"Opravdu chceš smazat záznam pro {self.exercise_type} ze dne {self.date_str}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.delete_requested = True
            self.accept()
    
    def get_value(self):
        """Vrátí novou hodnotu"""
        return self.value_spin.value()


class FitnessTrackerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fitness Tracker - Sledování cvičení")
        self.setMinimumSize(1200, 700)
        
        # Cesta k datovému souboru
        self.data_file = Path("fitness_data.json")
        
        # Načtení nebo inicializace dat
        self.load_data()
        
        # Vytvoření GUI
        self.setup_ui()
        
        # Obnovení stavu aplikace
        self.restore_app_state()
        
        # Automatická aktualizace každých 5 sekund
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.auto_refresh)
        self.update_timer.start(5000)
        
    def closeEvent(self, event):
        """Při zavření aplikace uloží stav"""
        self.save_app_state()
        event.accept()
        
    def load_data(self):
        """Načte data ze souboru nebo vytvoří výchozí strukturu"""
        if self.data_file.exists():
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        else:
            current_year = datetime.now().year
            self.data = {
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
                    'selected_year': datetime.now().year
                }
            }
            self.save_data()
    
    def save_data(self):
        """Uloží data do souboru"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def save_app_state(self):
        """Uloží stav aplikace"""
        self.data['app_state']['last_tab'] = self.tabs.currentIndex()
        self.data['app_state']['window_geometry'] = {
            'x': self.x(),
            'y': self.y(),
            'width': self.width(),
            'height': self.height()
        }
        if hasattr(self, 'year_selector'):
            self.data['app_state']['selected_year'] = int(self.year_selector.currentText())
        self.save_data()
    
    def restore_app_state(self):
        """Obnoví stav aplikace"""
        if 'app_state' in self.data:
            if self.data['app_state']['window_geometry']:
                geom = self.data['app_state']['window_geometry']
                self.setGeometry(geom['x'], geom['y'], geom['width'], geom['height'])
            
            if 'last_tab' in self.data['app_state']:
                self.tabs.setCurrentIndex(self.data['app_state']['last_tab'])
            
            if hasattr(self, 'year_selector') and 'selected_year' in self.data['app_state']:
                year = str(self.data['app_state']['selected_year'])
                index = self.year_selector.findText(year)
                if index >= 0:
                    self.year_selector.setCurrentIndex(index)
    
    def setup_ui(self):
        """Vytvoří GUI aplikace"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Vytvoření záložek
        self.tabs = QTabWidget()
        self.tabs.currentChanged.connect(self.on_tab_changed)
        layout.addWidget(self.tabs)
        
        # Záložky
        self.tabs.addTab(self.create_settings_tab(), "⚙️ Nastavení")
        self.tabs.addTab(self.create_exercise_tab('kliky', '💪'), "💪 Kliky")
        self.tabs.addTab(self.create_exercise_tab('dřepy', '🦵'), "🦵 Dřepy")
        self.tabs.addTab(self.create_exercise_tab('skrčky', '🧘'), "🧘 Skrčky")
        self.tabs.addTab(self.create_overview_tab(), "📊 Roční přehled")
        
    def on_tab_changed(self, index):
        """Automaticky aktualizuje zobrazení při přepnutí na záložku"""
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
        """Automatická aktualizace aktivní záložky"""
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
    
    def create_settings_tab(self):
        """Vytvoří záložku pro nastavení"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
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
    
    def show_diagnostics(self):
        """Zobrazí diagnostické okno s výpočty"""
        diag_window = QWidget()
        diag_window.setWindowTitle("Diagnostika výpočtu cílů")
        diag_window.resize(800, 500)
        
        layout = QVBoxLayout(diag_window)
        
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        
        # Vytvoření diagnostického textu
        start_date_str = self.data['settings']['start_date']
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        
        diag_text = f"📊 DIAGNOSTIKA VÝPOČTU CÍLŮ\n{'='*70}\n\n"
        diag_text += f"Startovní datum: {start_date_str} ({['Po', 'Út', 'St', 'Čt', 'Pá', 'So', 'Ne'][start_date.weekday()]})\n"
        
        # Výpočet konce prvního týdne
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
            
            # Příklady
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
                
                # Detailní výpočet
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
        """Uloží nastavení"""
        self.data['settings']['start_date'] = self.start_date_edit.date().toString('yyyy-MM-dd')
        self.data['settings']['base_goals']['kliky'] = self.base_kliky.value()
        self.data['settings']['base_goals']['dřepy'] = self.base_drepy.value()
        self.data['settings']['base_goals']['skrčky'] = self.base_skrcky.value()
        self.data['settings']['weekly_increment']['kliky'] = self.increment_kliky.value()
        self.data['settings']['weekly_increment']['dřepy'] = self.increment_drepy.value()
        self.data['settings']['weekly_increment']['skrčky'] = self.increment_skrcky.value()
        
        self.save_data()
        QMessageBox.information(self, "Uloženo", "Nastavení bylo úspěšně uloženo!")
        
        for exercise in ['kliky', 'dřepy', 'skrčky']:
            self.update_exercise_tab(exercise)
        self.refresh_overview()
    
    def create_exercise_tab(self, exercise_type, icon):
        """Vytvoří záložku pro konkrétní cvičení"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
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
        
        # NOVÉ: Label pro náskok/skluz
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
        
        # Tabulka s historií
        table = QTableWidget()
        table.setObjectName(f"table_{exercise_type}")
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["Datum", "Výkon", "Cíl", "Splněno", "Akce"])
        
        # OPRAVA: Nastavení výšky řádků
        table.verticalHeader().setDefaultSectionSize(35)
        table.verticalHeader().setMinimumSectionSize(35)
        
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        
        layout.addWidget(table)
        
        self.update_exercise_tab(exercise_type)
        
        return widget
    
    def calculate_goal(self, exercise_type, date_str):
        """Vypočítá cíl pro daný den s podporou proporcionálního prvního týdne"""
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
        """Vrátí text s vysvětlením výpočtu"""
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
        """Vypočítá aktuální progress pro roční cíl"""
        total_goal = self.calculate_yearly_goal(exercise_type, year)
        
        total_performed = 0
        for date_str, workouts in self.data['workouts'].items():
            if date_str.startswith(str(year)) and exercise_type in workouts:
                total_performed += workouts[exercise_type]
        
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
        """Přidá výkon do databáze"""
        if value == 0:
            QMessageBox.warning(self, "Chyba", "Zadej nenulovou hodnotu!")
            return
        
        if date_str not in self.data['workouts']:
            self.data['workouts'][date_str] = {}
        
        self.data['workouts'][date_str][exercise_type] = value
        self.save_data()
        
        self.update_exercise_tab(exercise_type)
        self.refresh_overview()
        
        QMessageBox.information(self, "Přidáno", f"Výkon byl zaznamenán: {value} {exercise_type}")
    
    def edit_workout(self, exercise_type, date_str):
        """Otevře dialog pro editaci záznamu"""
        current_value = self.data['workouts'][date_str][exercise_type]
        
        dialog = EditWorkoutDialog(exercise_type, date_str, current_value, self)
        
        if dialog.exec():
            if dialog.delete_requested:
                del self.data['workouts'][date_str][exercise_type]
                
                if not self.data['workouts'][date_str]:
                    del self.data['workouts'][date_str]
                
                QMessageBox.information(self, "Smazáno", f"Záznam byl smazán")
            else:
                new_value = dialog.get_value()
                self.data['workouts'][date_str][exercise_type] = new_value
                QMessageBox.information(self, "Upraveno", f"Záznam byl upraven na: {new_value} {exercise_type}")
            
            self.save_data()
            self.update_exercise_tab(exercise_type)
            self.refresh_overview()
    
    def update_exercise_tab(self, exercise_type):
        """Aktualizuje zobrazení záložky cvičení"""
        today = datetime.now()
        today_str = today.strftime('%Y-%m-%d')
        current_year = today.year
        
        today_goal = self.calculate_goal(exercise_type, today_str)
        today_goal_label = self.findChild(QLabel, f"today_goal_label_{exercise_type}")
        if today_goal_label:
            today_goal_label.setText(f"🎯 Dnešní cíl: {today_goal} {exercise_type}")
        
        calc_label = self.findChild(QLabel, f"calc_label_{exercise_type}")
        if calc_label:
            calc_text = self.get_goal_calculation_text(exercise_type, today_str)
            calc_label.setText(calc_text)
        
        # NOVÉ: Výpočet náskopu/skluzu
        total_performed, total_yearly_goal, goal_to_date = self.calculate_yearly_progress(exercise_type, current_year)
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
                f"📅 Roční cíl {current_year}: {total_yearly_goal:,} {exercise_type} celkem"
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
                             if date_str.startswith(str(current_year)) and exercise_type in workouts)
            
            stats_label.setText(
                f"📈 Splněno: {total_performed:,} | "
                f"🎯 Zbývá do dnes: {remaining:,} | "
                f"📊 Dní s tréninkem: {days_trained}"
            )
        
        table = self.findChild(QTableWidget, f"table_{exercise_type}")
        if table:
            table.setRowCount(0)
            
            sorted_dates = sorted(
                [date for date in self.data['workouts'].keys() 
                 if exercise_type in self.data['workouts'][date]],
                reverse=True
            )
            
            for date_str in sorted_dates:
                value = self.data['workouts'][date_str][exercise_type]
                goal = self.calculate_goal(exercise_type, date_str)
                achieved = value >= goal
                
                row = table.rowCount()
                table.insertRow(row)
                
                table.setItem(row, 0, QTableWidgetItem(date_str))
                table.setItem(row, 1, QTableWidgetItem(str(value)))
                table.setItem(row, 2, QTableWidgetItem(str(goal)))
                
                status_item = QTableWidgetItem("✅ Ano" if achieved else "❌ Ne")
                if achieved:
                    status_item.setBackground(QColor(50, 200, 100))
                else:
                    status_item.setBackground(QColor(200, 50, 50))
                table.setItem(row, 3, status_item)
                
                # OPRAVA: Menší tlačítko
                edit_btn = QPushButton("✏️")
                edit_btn.setMaximumSize(30, 30)
                edit_btn.setToolTip("Upravit záznam")
                edit_btn.clicked.connect(lambda checked, d=date_str, e=exercise_type: self.edit_workout(e, d))
                table.setCellWidget(row, 4, edit_btn)
    
    def create_overview_tab(self):
        """Vytvoří záložku s ročním přehledem"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        controls_layout = QHBoxLayout()
        
        controls_layout.addWidget(QLabel("📅 Rok:"))
        self.year_selector = QComboBox()
        self.populate_year_selector()
        self.year_selector.currentTextChanged.connect(self.refresh_overview)
        controls_layout.addWidget(self.year_selector)
        
        controls_layout.addStretch()
        
        refresh_btn = QPushButton("🔄 Aktualizovat")
        refresh_btn.clicked.connect(self.refresh_overview)
        controls_layout.addWidget(refresh_btn)
        
        layout.addLayout(controls_layout)
        
        # OPRAVA: Aktualizovaná legenda s černou pro dny před začátkem
        legend_frame = QFrame()
        legend_frame.setStyleSheet("background-color: #2d2d2d; border: 1px solid #3d3d3d; padding: 5px;")
        legend_layout = QHBoxLayout(legend_frame)
        
        # Vytvoření vzorků barev
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
    
    def populate_year_selector(self):
        """Naplní selector dostupnými roky"""
        current_year = datetime.now().year
        
        years = set([current_year])
        for date_str in self.data['workouts'].keys():
            year = int(date_str.split('-')[0])
            years.add(year)
        
        start_year = int(self.data['settings']['start_date'].split('-')[0])
        years.add(start_year)
        
        for year in sorted(years, reverse=True):
            self.year_selector.addItem(str(year))
        
        self.year_selector.setCurrentText(str(current_year))
    
    def refresh_overview(self):
        """Vytvoří nebo aktualizuje roční kalendář"""
        while self.calendar_layout.count():
            child = self.calendar_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        selected_year = int(self.year_selector.currentText())
        
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
        """Vytvoří kalendář pro jeden měsíc"""
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
        """Určí barvu pro konkrétní den"""
        # OPRAVA: Dny před začátkem cvičení jsou černé
        if date < start_date:
            return '#000000'
        
        # Budoucí den
        if date > today:
            return '#4d4d4d'
        
        # Dnešek
        if date == today:
            return '#87CEEB'
        
        # Minulý den - kontrola cvičení
        if date_str in self.data['workouts']:
            workout = self.data['workouts'][date_str]
            exercises = ['kliky', 'dřepy', 'skrčky']
            count = sum(1 for ex in exercises if ex in workout)
            
            if count == 3:
                return '#90EE90'
            elif count > 0:
                return '#FFD700'
        
        # Necvičil jsem
        return '#FF6B6B'
    
    def update_statistics(self, year):
        """Aktualizuje statistiky pro vybraný rok"""
        year_workouts = {date: data for date, data in self.data['workouts'].items() 
                        if date.startswith(str(year))}
        
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
    
    # Aplikace dark theme
    app.setStyleSheet(DARK_THEME)
    
    window = FitnessTrackerApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
