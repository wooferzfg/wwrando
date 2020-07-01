# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'randomizer_window.ui'
##
## Created by: Qt User Interface Compiler version 5.15.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(943, 671)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scroll_for_main = QScrollArea(self.centralwidget)
        self.scroll_for_main.setObjectName(u"scroll_for_main")
        self.scroll_for_main.setFrameShape(QFrame.NoFrame)
        self.scroll_for_main.setWidgetResizable(True)
        self.content_for_main_scroll = QWidget()
        self.content_for_main_scroll.setObjectName(u"content_for_main_scroll")
        self.content_for_main_scroll.setGeometry(QRect(0, 0, 978, 614))
        self.verticalLayout_4 = QVBoxLayout(self.content_for_main_scroll)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.tab_for_main = QTabWidget(self.content_for_main_scroll)
        self.tab_for_main.setObjectName(u"tab_for_main")
        self.tab_for_main.setEnabled(True)
        self.tab_for_settings = QWidget()
        self.tab_for_settings.setObjectName(u"tab_for_settings")
        self.verticalLayout_2 = QVBoxLayout(self.tab_for_settings)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.grid_for_paths = QGridLayout()
        self.grid_for_paths.setObjectName(u"grid_for_paths")
        self.seed = QLineEdit(self.tab_for_settings)
        self.seed.setObjectName(u"seed")

        self.grid_for_paths.addWidget(self.seed, 2, 1, 1, 1)

        self.label_for_clean = QLabel(self.tab_for_settings)
        self.label_for_clean.setObjectName(u"label_for_clean")

        self.grid_for_paths.addWidget(self.label_for_clean, 0, 0, 1, 1)

        self.clean_iso_path = QLineEdit(self.tab_for_settings)
        self.clean_iso_path.setObjectName(u"clean_iso_path")

        self.grid_for_paths.addWidget(self.clean_iso_path, 0, 1, 1, 1)

        self.label_for_output = QLabel(self.tab_for_settings)
        self.label_for_output.setObjectName(u"label_for_output")

        self.grid_for_paths.addWidget(self.label_for_output, 1, 0, 1, 1)

        self.output_folder = QLineEdit(self.tab_for_settings)
        self.output_folder.setObjectName(u"output_folder")

        self.grid_for_paths.addWidget(self.output_folder, 1, 1, 1, 1)

        self.output_folder_browse_button = QPushButton(self.tab_for_settings)
        self.output_folder_browse_button.setObjectName(u"output_folder_browse_button")

        self.grid_for_paths.addWidget(self.output_folder_browse_button, 1, 2, 1, 1)

        self.label_for_seed = QLabel(self.tab_for_settings)
        self.label_for_seed.setObjectName(u"label_for_seed")

        self.grid_for_paths.addWidget(self.label_for_seed, 2, 0, 1, 1)

        self.generate_seed_button = QPushButton(self.tab_for_settings)
        self.generate_seed_button.setObjectName(u"generate_seed_button")

        self.grid_for_paths.addWidget(self.generate_seed_button, 2, 2, 1, 1)

        self.clean_iso_path_browse_button = QPushButton(self.tab_for_settings)
        self.clean_iso_path_browse_button.setObjectName(u"clean_iso_path_browse_button")

        self.grid_for_paths.addWidget(self.clean_iso_path_browse_button, 0, 2, 1, 1)


        self.verticalLayout_2.addLayout(self.grid_for_paths)

        self.group_for_locations = QGroupBox(self.tab_for_settings)
        self.group_for_locations.setObjectName(u"group_for_locations")
        self.gridLayout_2 = QGridLayout(self.group_for_locations)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.progression_platforms_rafts = QCheckBox(self.group_for_locations)
        self.progression_platforms_rafts.setObjectName(u"progression_platforms_rafts")

        self.gridLayout_2.addWidget(self.progression_platforms_rafts, 7, 0, 1, 1)

        self.progression_long_sidequests = QCheckBox(self.group_for_locations)
        self.progression_long_sidequests.setObjectName(u"progression_long_sidequests")

        self.gridLayout_2.addWidget(self.progression_long_sidequests, 4, 1, 1, 1)

        self.progression_dungeons = QCheckBox(self.group_for_locations)
        self.progression_dungeons.setObjectName(u"progression_dungeons")
        self.progression_dungeons.setChecked(True)

        self.gridLayout_2.addWidget(self.progression_dungeons, 0, 0, 1, 1)

        self.progression_short_sidequests = QCheckBox(self.group_for_locations)
        self.progression_short_sidequests.setObjectName(u"progression_short_sidequests")

        self.gridLayout_2.addWidget(self.progression_short_sidequests, 4, 0, 1, 1)

        self.progression_treasure_charts = QCheckBox(self.group_for_locations)
        self.progression_treasure_charts.setObjectName(u"progression_treasure_charts")

        self.gridLayout_2.addWidget(self.progression_treasure_charts, 9, 1, 1, 1)

        self.progression_submarines = QCheckBox(self.group_for_locations)
        self.progression_submarines.setObjectName(u"progression_submarines")
        self.progression_submarines.setChecked(False)

        self.gridLayout_2.addWidget(self.progression_submarines, 7, 1, 1, 1)

        self.progression_triforce_charts = QCheckBox(self.group_for_locations)
        self.progression_triforce_charts.setObjectName(u"progression_triforce_charts")

        self.gridLayout_2.addWidget(self.progression_triforce_charts, 9, 0, 1, 1)

        self.progression_spoils_trading = QCheckBox(self.group_for_locations)
        self.progression_spoils_trading.setObjectName(u"progression_spoils_trading")

        self.gridLayout_2.addWidget(self.progression_spoils_trading, 4, 2, 1, 1)

        self.progression_minigames = QCheckBox(self.group_for_locations)
        self.progression_minigames.setObjectName(u"progression_minigames")

        self.gridLayout_2.addWidget(self.progression_minigames, 6, 0, 1, 1)

        self.progression_battlesquid = QCheckBox(self.group_for_locations)
        self.progression_battlesquid.setObjectName(u"progression_battlesquid")

        self.gridLayout_2.addWidget(self.progression_battlesquid, 6, 1, 1, 1)

        self.progression_big_octos_gunboats = QCheckBox(self.group_for_locations)
        self.progression_big_octos_gunboats.setObjectName(u"progression_big_octos_gunboats")

        self.gridLayout_2.addWidget(self.progression_big_octos_gunboats, 7, 2, 1, 1)

        self.progression_expensive_purchases = QCheckBox(self.group_for_locations)
        self.progression_expensive_purchases.setObjectName(u"progression_expensive_purchases")
        self.progression_expensive_purchases.setChecked(True)

        self.gridLayout_2.addWidget(self.progression_expensive_purchases, 6, 2, 1, 1)

        self.progression_great_fairies = QCheckBox(self.group_for_locations)
        self.progression_great_fairies.setObjectName(u"progression_great_fairies")
        self.progression_great_fairies.setChecked(True)

        self.gridLayout_2.addWidget(self.progression_great_fairies, 1, 0, 1, 1)

        self.progression_combat_secret_caves = QCheckBox(self.group_for_locations)
        self.progression_combat_secret_caves.setObjectName(u"progression_combat_secret_caves")

        self.gridLayout_2.addWidget(self.progression_combat_secret_caves, 0, 2, 1, 1)

        self.progression_free_gifts = QCheckBox(self.group_for_locations)
        self.progression_free_gifts.setObjectName(u"progression_free_gifts")
        self.progression_free_gifts.setChecked(True)

        self.gridLayout_2.addWidget(self.progression_free_gifts, 1, 1, 1, 1)

        self.progression_savage_labyrinth = QCheckBox(self.group_for_locations)
        self.progression_savage_labyrinth.setObjectName(u"progression_savage_labyrinth")

        self.gridLayout_2.addWidget(self.progression_savage_labyrinth, 0, 3, 1, 1)

        self.progression_puzzle_secret_caves = QCheckBox(self.group_for_locations)
        self.progression_puzzle_secret_caves.setObjectName(u"progression_puzzle_secret_caves")
        self.progression_puzzle_secret_caves.setChecked(True)

        self.gridLayout_2.addWidget(self.progression_puzzle_secret_caves, 0, 1, 1, 1)

        self.progression_misc = QCheckBox(self.group_for_locations)
        self.progression_misc.setObjectName(u"progression_misc")
        self.progression_misc.setChecked(True)

        self.gridLayout_2.addWidget(self.progression_misc, 1, 2, 1, 1)

        self.progression_eye_reef_chests = QCheckBox(self.group_for_locations)
        self.progression_eye_reef_chests.setObjectName(u"progression_eye_reef_chests")

        self.gridLayout_2.addWidget(self.progression_eye_reef_chests, 7, 3, 1, 1)

        self.progression_mail = QCheckBox(self.group_for_locations)
        self.progression_mail.setObjectName(u"progression_mail")

        self.gridLayout_2.addWidget(self.progression_mail, 4, 3, 1, 1)

        self.progression_tingle_chests = QCheckBox(self.group_for_locations)
        self.progression_tingle_chests.setObjectName(u"progression_tingle_chests")

        self.gridLayout_2.addWidget(self.progression_tingle_chests, 1, 3, 1, 1)

        self.progression_island_puzzles = QCheckBox(self.group_for_locations)
        self.progression_island_puzzles.setObjectName(u"progression_island_puzzles")

        self.gridLayout_2.addWidget(self.progression_island_puzzles, 6, 3, 1, 1)


        self.verticalLayout_2.addWidget(self.group_for_locations)

        self.group_for_settings_secondary = QGroupBox(self.tab_for_settings)
        self.group_for_settings_secondary.setObjectName(u"group_for_settings_secondary")
        self.gridLayout_3 = QGridLayout(self.group_for_settings_secondary)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.layout_for_sword = QHBoxLayout()
        self.layout_for_sword.setObjectName(u"layout_for_sword")
        self.label_for_sword_mode = QLabel(self.group_for_settings_secondary)
        self.label_for_sword_mode.setObjectName(u"label_for_sword_mode")

        self.layout_for_sword.addWidget(self.label_for_sword_mode)

        self.sword_mode = QComboBox(self.group_for_settings_secondary)
        self.sword_mode.addItem("")
        self.sword_mode.addItem("")
        self.sword_mode.addItem("")
        self.sword_mode.setObjectName(u"sword_mode")

        self.layout_for_sword.addWidget(self.sword_mode)


        self.gridLayout_3.addLayout(self.layout_for_sword, 0, 0, 1, 1)

        self.randomize_charts = QCheckBox(self.group_for_settings_secondary)
        self.randomize_charts.setObjectName(u"randomize_charts")

        self.gridLayout_3.addWidget(self.randomize_charts, 2, 0, 1, 1)

        self.randomize_starting_island = QCheckBox(self.group_for_settings_secondary)
        self.randomize_starting_island.setObjectName(u"randomize_starting_island")

        self.gridLayout_3.addWidget(self.randomize_starting_island, 2, 1, 1, 1)

        self.keylunacy = QCheckBox(self.group_for_settings_secondary)
        self.keylunacy.setObjectName(u"keylunacy")

        self.gridLayout_3.addWidget(self.keylunacy, 1, 0, 1, 1)

        self.layout_for_starting_triforce_shards = QHBoxLayout()
        self.layout_for_starting_triforce_shards.setObjectName(u"layout_for_starting_triforce_shards")
        self.label_for_num_starting_triforce_shards = QLabel(self.group_for_settings_secondary)
        self.label_for_num_starting_triforce_shards.setObjectName(u"label_for_num_starting_triforce_shards")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_for_num_starting_triforce_shards.sizePolicy().hasHeightForWidth())
        self.label_for_num_starting_triforce_shards.setSizePolicy(sizePolicy)

        self.layout_for_starting_triforce_shards.addWidget(self.label_for_num_starting_triforce_shards)

        self.num_starting_triforce_shards = QComboBox(self.group_for_settings_secondary)
        self.num_starting_triforce_shards.addItem("")
        self.num_starting_triforce_shards.addItem("")
        self.num_starting_triforce_shards.addItem("")
        self.num_starting_triforce_shards.addItem("")
        self.num_starting_triforce_shards.addItem("")
        self.num_starting_triforce_shards.addItem("")
        self.num_starting_triforce_shards.addItem("")
        self.num_starting_triforce_shards.addItem("")
        self.num_starting_triforce_shards.addItem("")
        self.num_starting_triforce_shards.setObjectName(u"num_starting_triforce_shards")
        self.num_starting_triforce_shards.setMaximumSize(QSize(40, 16777215))

        self.layout_for_starting_triforce_shards.addWidget(self.num_starting_triforce_shards)

        self.widget = QWidget(self.group_for_settings_secondary)
        self.widget.setObjectName(u"widget")

        self.layout_for_starting_triforce_shards.addWidget(self.widget)


        self.gridLayout_3.addLayout(self.layout_for_starting_triforce_shards, 1, 2, 1, 1)

        self.race_mode = QCheckBox(self.group_for_settings_secondary)
        self.race_mode.setObjectName(u"race_mode")

        self.gridLayout_3.addWidget(self.race_mode, 1, 1, 1, 1)

        self.layout_for_randomize_entrances = QHBoxLayout()
        self.layout_for_randomize_entrances.setObjectName(u"layout_for_randomize_entrances")
        self.label_for_randomize_entrances = QLabel(self.group_for_settings_secondary)
        self.label_for_randomize_entrances.setObjectName(u"label_for_randomize_entrances")

        self.layout_for_randomize_entrances.addWidget(self.label_for_randomize_entrances)

        self.randomize_entrances = QComboBox(self.group_for_settings_secondary)
        self.randomize_entrances.addItem("")
        self.randomize_entrances.addItem("")
        self.randomize_entrances.addItem("")
        self.randomize_entrances.addItem("")
        self.randomize_entrances.addItem("")
        self.randomize_entrances.setObjectName(u"randomize_entrances")

        self.layout_for_randomize_entrances.addWidget(self.randomize_entrances)

        self.widget_2 = QWidget(self.group_for_settings_secondary)
        self.widget_2.setObjectName(u"widget_2")

        self.layout_for_randomize_entrances.addWidget(self.widget_2)


        self.gridLayout_3.addLayout(self.layout_for_randomize_entrances, 0, 1, 1, 2)

        self.randomize_music = QCheckBox(self.group_for_settings_secondary)
        self.randomize_music.setObjectName(u"randomize_music")
        self.randomize_music.setEnabled(False)

        self.gridLayout_3.addWidget(self.randomize_music, 2, 3, 1, 1)

        self.randomize_enemy_palettes = QCheckBox(self.group_for_settings_secondary)
        self.randomize_enemy_palettes.setObjectName(u"randomize_enemy_palettes")
        self.randomize_enemy_palettes.setEnabled(True)

        self.gridLayout_3.addWidget(self.randomize_enemy_palettes, 2, 2, 1, 1)

        self.randomize_enemies = QCheckBox(self.group_for_settings_secondary)
        self.randomize_enemies.setObjectName(u"randomize_enemies")
        self.randomize_enemies.setEnabled(False)

        self.gridLayout_3.addWidget(self.randomize_enemies, 0, 3, 1, 1)

        self.layout_for_num_dungeon_race_mode = QHBoxLayout()
        self.layout_for_num_dungeon_race_mode.setObjectName(u"layout_for_num_dungeon_race_mode")
        self.label_for_num_dungeon_race_mode = QLabel(self.group_for_settings_secondary)
        self.label_for_num_dungeon_race_mode.setObjectName(u"label_for_num_dungeon_race_mode")
        sizePolicy.setHeightForWidth(self.label_for_num_dungeon_race_mode.sizePolicy().hasHeightForWidth())
        self.label_for_num_dungeon_race_mode.setSizePolicy(sizePolicy)

        self.layout_for_num_dungeon_race_mode.addWidget(self.label_for_num_dungeon_race_mode)

        self.num_dungeon_race_mode = QComboBox(self.group_for_settings_secondary)
        self.num_dungeon_race_mode.addItem("")
        self.num_dungeon_race_mode.addItem("")
        self.num_dungeon_race_mode.addItem("")
        self.num_dungeon_race_mode.addItem("")
        self.num_dungeon_race_mode.addItem("")
        self.num_dungeon_race_mode.addItem("")
        self.num_dungeon_race_mode.addItem("")
        self.num_dungeon_race_mode.setObjectName(u"num_dungeon_race_mode")
        self.num_dungeon_race_mode.setMaximumSize(QSize(40, 16777215))

        self.layout_for_num_dungeon_race_mode.addWidget(self.num_dungeon_race_mode)

        self.widget_9 = QWidget(self.group_for_settings_secondary)
        self.widget_9.setObjectName(u"widget_9")

        self.layout_for_num_dungeon_race_mode.addWidget(self.widget_9)


        self.gridLayout_3.addLayout(self.layout_for_num_dungeon_race_mode, 1, 3, 1, 1)


        self.verticalLayout_2.addWidget(self.group_for_settings_secondary)

        self.group_for_convenience = QGroupBox(self.tab_for_settings)
        self.group_for_convenience.setObjectName(u"group_for_convenience")
        self.gridLayout_4 = QGridLayout(self.group_for_convenience)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.instant_text_boxes = QCheckBox(self.group_for_convenience)
        self.instant_text_boxes.setObjectName(u"instant_text_boxes")
        self.instant_text_boxes.setChecked(True)

        self.gridLayout_4.addWidget(self.instant_text_boxes, 0, 1, 1, 1)

        self.skip_rematch_bosses = QCheckBox(self.group_for_convenience)
        self.skip_rematch_bosses.setObjectName(u"skip_rematch_bosses")
        self.skip_rematch_bosses.setChecked(True)

        self.gridLayout_4.addWidget(self.skip_rematch_bosses, 1, 0, 1, 1)

        self.reveal_full_sea_chart = QCheckBox(self.group_for_convenience)
        self.reveal_full_sea_chart.setObjectName(u"reveal_full_sea_chart")
        self.reveal_full_sea_chart.setChecked(True)

        self.gridLayout_4.addWidget(self.reveal_full_sea_chart, 0, 2, 1, 1)

        self.add_shortcut_warps_between_dungeons = QCheckBox(self.group_for_convenience)
        self.add_shortcut_warps_between_dungeons.setObjectName(u"add_shortcut_warps_between_dungeons")

        self.gridLayout_4.addWidget(self.add_shortcut_warps_between_dungeons, 1, 1, 1, 1)

        self.swift_sail = QCheckBox(self.group_for_convenience)
        self.swift_sail.setObjectName(u"swift_sail")
        self.swift_sail.setChecked(True)

        self.gridLayout_4.addWidget(self.swift_sail, 0, 0, 1, 1)

        self.remove_title_and_ending_videos = QCheckBox(self.group_for_convenience)
        self.remove_title_and_ending_videos.setObjectName(u"remove_title_and_ending_videos")
        self.remove_title_and_ending_videos.setChecked(True)

        self.gridLayout_4.addWidget(self.remove_title_and_ending_videos, 1, 2, 1, 1)

        self.remove_music = QCheckBox(self.group_for_convenience)
        self.remove_music.setObjectName(u"remove_music")

        self.gridLayout_4.addWidget(self.remove_music, 1, 3, 1, 1)

        self.invert_camera_x_axis = QCheckBox(self.group_for_convenience)
        self.invert_camera_x_axis.setObjectName(u"invert_camera_x_axis")

        self.gridLayout_4.addWidget(self.invert_camera_x_axis, 0, 3, 1, 1)


        self.verticalLayout_2.addWidget(self.group_for_convenience)

        self.group_for_advanced = QGroupBox(self.tab_for_settings)
        self.group_for_advanced.setObjectName(u"group_for_advanced")
        self.gridLayout_6 = QGridLayout(self.group_for_advanced)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.disable_tingle_chests_with_tingle_bombs = QCheckBox(self.group_for_advanced)
        self.disable_tingle_chests_with_tingle_bombs.setObjectName(u"disable_tingle_chests_with_tingle_bombs")

        self.gridLayout_6.addWidget(self.disable_tingle_chests_with_tingle_bombs, 0, 1, 1, 1)

        self.do_not_generate_spoiler_log = QCheckBox(self.group_for_advanced)
        self.do_not_generate_spoiler_log.setObjectName(u"do_not_generate_spoiler_log")
        self.do_not_generate_spoiler_log.setChecked(True)

        self.gridLayout_6.addWidget(self.do_not_generate_spoiler_log, 0, 0, 1, 1)

        self.widget_3 = QWidget(self.group_for_advanced)
        self.widget_3.setObjectName(u"widget_3")

        self.gridLayout_6.addWidget(self.widget_3, 0, 2, 1, 1)

        self.widget_4 = QWidget(self.group_for_advanced)
        self.widget_4.setObjectName(u"widget_4")

        self.gridLayout_6.addWidget(self.widget_4, 0, 3, 1, 1)


        self.verticalLayout_2.addWidget(self.group_for_advanced)

        self.tab_for_main.addTab(self.tab_for_settings, "")
        self.tab_for_starting_items = QWidget()
        self.tab_for_starting_items.setObjectName(u"tab_for_starting_items")
        self.tab_for_starting_items.setEnabled(True)
        self.verticalLayout_10 = QVBoxLayout(self.tab_for_starting_items)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.layout_for_starting_items = QHBoxLayout()
        self.layout_for_starting_items.setObjectName(u"layout_for_starting_items")
        self.layout_for_randomized_gear = QVBoxLayout()
        self.layout_for_randomized_gear.setObjectName(u"layout_for_randomized_gear")
        self.label_for_randomized_gear = QLabel(self.tab_for_starting_items)
        self.label_for_randomized_gear.setObjectName(u"label_for_randomized_gear")

        self.layout_for_randomized_gear.addWidget(self.label_for_randomized_gear)

        self.randomized_gear = QListView(self.tab_for_starting_items)
        self.randomized_gear.setObjectName(u"randomized_gear")
        self.randomized_gear.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.randomized_gear.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.layout_for_randomized_gear.addWidget(self.randomized_gear)


        self.layout_for_starting_items.addLayout(self.layout_for_randomized_gear)

        self.layout_for_gear_options = QVBoxLayout()
        self.layout_for_gear_options.setObjectName(u"layout_for_gear_options")
        self.spacer_for_options_gear_top = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.layout_for_gear_options.addItem(self.spacer_for_options_gear_top)

        self.remove_gear = QPushButton(self.tab_for_starting_items)
        self.remove_gear.setObjectName(u"remove_gear")
        self.remove_gear.setMinimumSize(QSize(0, 80))

        self.layout_for_gear_options.addWidget(self.remove_gear)

        self.add_gear = QPushButton(self.tab_for_starting_items)
        self.add_gear.setObjectName(u"add_gear")
        self.add_gear.setMinimumSize(QSize(0, 80))

        self.layout_for_gear_options.addWidget(self.add_gear)

        self.spacer_for_options_gear_bottom = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.layout_for_gear_options.addItem(self.spacer_for_options_gear_bottom)


        self.layout_for_starting_items.addLayout(self.layout_for_gear_options)

        self.layout_for_starting_gear = QVBoxLayout()
        self.layout_for_starting_gear.setObjectName(u"layout_for_starting_gear")
        self.label_for_starting_gear = QLabel(self.tab_for_starting_items)
        self.label_for_starting_gear.setObjectName(u"label_for_starting_gear")

        self.layout_for_starting_gear.addWidget(self.label_for_starting_gear)

        self.starting_gear = QListView(self.tab_for_starting_items)
        self.starting_gear.setObjectName(u"starting_gear")
        self.starting_gear.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.starting_gear.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.layout_for_starting_gear.addWidget(self.starting_gear)


        self.layout_for_starting_items.addLayout(self.layout_for_starting_gear)


        self.verticalLayout_10.addLayout(self.layout_for_starting_items)

        self.layout_for_starting_health = QHBoxLayout()
        self.layout_for_starting_health.setObjectName(u"layout_for_starting_health")
        self.label_for_heart_container = QLabel(self.tab_for_starting_items)
        self.label_for_heart_container.setObjectName(u"label_for_heart_container")

        self.layout_for_starting_health.addWidget(self.label_for_heart_container)

        self.starting_hcs = QSpinBox(self.tab_for_starting_items)
        self.starting_hcs.setObjectName(u"starting_hcs")
        self.starting_hcs.setLayoutDirection(Qt.LeftToRight)
        self.starting_hcs.setMaximum(6)
        self.starting_hcs.setValue(0)
        self.starting_hcs.setDisplayIntegerBase(10)

        self.layout_for_starting_health.addWidget(self.starting_hcs)

        self.label_for_heart_piece = QLabel(self.tab_for_starting_items)
        self.label_for_heart_piece.setObjectName(u"label_for_heart_piece")

        self.layout_for_starting_health.addWidget(self.label_for_heart_piece)

        self.starting_pohs = QSpinBox(self.tab_for_starting_items)
        self.starting_pohs.setObjectName(u"starting_pohs")
        self.starting_pohs.setMaximum(44)
        self.starting_pohs.setValue(0)
        self.starting_pohs.setDisplayIntegerBase(10)

        self.layout_for_starting_health.addWidget(self.starting_pohs)

        self.current_health = QLabel(self.tab_for_starting_items)
        self.current_health.setObjectName(u"current_health")

        self.layout_for_starting_health.addWidget(self.current_health)

        self.spacer_for_health_end = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.layout_for_starting_health.addItem(self.spacer_for_health_end)


        self.verticalLayout_10.addLayout(self.layout_for_starting_health)

        self.tab_for_main.addTab(self.tab_for_starting_items, "")
        self.tab_for_model_customization = QWidget()
        self.tab_for_model_customization.setObjectName(u"tab_for_model_customization")
        self.verticalLayout_3 = QVBoxLayout(self.tab_for_model_customization)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.grid_for_model_general_options = QGridLayout()
        self.grid_for_model_general_options.setObjectName(u"grid_for_model_general_options")
        self.layout_for_custom_player_model = QHBoxLayout()
        self.layout_for_custom_player_model.setObjectName(u"layout_for_custom_player_model")
        self.label_for_custom_player_model = QLabel(self.tab_for_model_customization)
        self.label_for_custom_player_model.setObjectName(u"label_for_custom_player_model")

        self.layout_for_custom_player_model.addWidget(self.label_for_custom_player_model)

        self.custom_player_model = QComboBox(self.tab_for_model_customization)
        self.custom_player_model.setObjectName(u"custom_player_model")

        self.layout_for_custom_player_model.addWidget(self.custom_player_model)


        self.grid_for_model_general_options.addLayout(self.layout_for_custom_player_model, 0, 0, 1, 1)

        self.layout_for_custom_preset = QHBoxLayout()
        self.layout_for_custom_preset.setObjectName(u"layout_for_custom_preset")
        self.label_for_custom_color_preset = QLabel(self.tab_for_model_customization)
        self.label_for_custom_color_preset.setObjectName(u"label_for_custom_color_preset")

        self.layout_for_custom_preset.addWidget(self.label_for_custom_color_preset)

        self.custom_color_preset = QComboBox(self.tab_for_model_customization)
        self.custom_color_preset.setObjectName(u"custom_color_preset")

        self.layout_for_custom_preset.addWidget(self.custom_color_preset)


        self.grid_for_model_general_options.addLayout(self.layout_for_custom_preset, 1, 0, 1, 1)

        self.layout_for_randomize_color_options = QHBoxLayout()
        self.layout_for_randomize_color_options.setObjectName(u"layout_for_randomize_color_options")
        self.randomize_all_custom_colors_together = QPushButton(self.tab_for_model_customization)
        self.randomize_all_custom_colors_together.setObjectName(u"randomize_all_custom_colors_together")

        self.layout_for_randomize_color_options.addWidget(self.randomize_all_custom_colors_together)

        self.randomize_all_custom_colors_separately = QPushButton(self.tab_for_model_customization)
        self.randomize_all_custom_colors_separately.setObjectName(u"randomize_all_custom_colors_separately")

        self.layout_for_randomize_color_options.addWidget(self.randomize_all_custom_colors_separately)


        self.grid_for_model_general_options.addLayout(self.layout_for_randomize_color_options, 1, 1, 1, 1)

        self.layout_for_misc_options = QHBoxLayout()
        self.layout_for_misc_options.setObjectName(u"layout_for_misc_options")
        self.player_in_casual_clothes = QCheckBox(self.tab_for_model_customization)
        self.player_in_casual_clothes.setObjectName(u"player_in_casual_clothes")

        self.layout_for_misc_options.addWidget(self.player_in_casual_clothes)

        self.disable_custom_player_voice = QCheckBox(self.tab_for_model_customization)
        self.disable_custom_player_voice.setObjectName(u"disable_custom_player_voice")

        self.layout_for_misc_options.addWidget(self.disable_custom_player_voice)

        self.disable_custom_player_items = QCheckBox(self.tab_for_model_customization)
        self.disable_custom_player_items.setObjectName(u"disable_custom_player_items")

        self.layout_for_misc_options.addWidget(self.disable_custom_player_items)


        self.grid_for_model_general_options.addLayout(self.layout_for_misc_options, 0, 1, 1, 1)


        self.verticalLayout_3.addLayout(self.grid_for_model_general_options)

        self.custom_model_comment = QLabel(self.tab_for_model_customization)
        self.custom_model_comment.setObjectName(u"custom_model_comment")
        self.custom_model_comment.setMaximumSize(QSize(810, 16777215))
        self.custom_model_comment.setWordWrap(True)

        self.verticalLayout_3.addWidget(self.custom_model_comment)

        self.layout_for_color_visualizer = QHBoxLayout()
        self.layout_for_color_visualizer.setObjectName(u"layout_for_color_visualizer")
        self.layout_for_color_layout = QVBoxLayout()
        self.layout_for_color_layout.setObjectName(u"layout_for_color_layout")
        self.custom_colors_layout = QVBoxLayout()
        self.custom_colors_layout.setObjectName(u"custom_colors_layout")

        self.layout_for_color_layout.addLayout(self.custom_colors_layout)

        self.spacer_for_colors_layout = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.layout_for_color_layout.addItem(self.spacer_for_colors_layout)


        self.layout_for_color_visualizer.addLayout(self.layout_for_color_layout)

        self.layout_for_model_preview = QVBoxLayout()
        self.layout_for_model_preview.setObjectName(u"layout_for_model_preview")
        self.custom_model_preview_label = QLabel(self.tab_for_model_customization)
        self.custom_model_preview_label.setObjectName(u"custom_model_preview_label")

        self.layout_for_model_preview.addWidget(self.custom_model_preview_label)

        self.spacer_for_model_preview = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.layout_for_model_preview.addItem(self.spacer_for_model_preview)


        self.layout_for_color_visualizer.addLayout(self.layout_for_model_preview)


        self.verticalLayout_3.addLayout(self.layout_for_color_visualizer)

        self.tab_for_main.addTab(self.tab_for_model_customization, "")

        self.verticalLayout_4.addWidget(self.tab_for_main)

        self.scroll_for_main.setWidget(self.content_for_main_scroll)

        self.verticalLayout.addWidget(self.scroll_for_main)

        self.option_description = QLabel(self.centralwidget)
        self.option_description.setObjectName(u"option_description")
        self.option_description.setMinimumSize(QSize(0, 32))
        self.option_description.setWordWrap(True)

        self.verticalLayout.addWidget(self.option_description)

        self.layout_for_permalink = QHBoxLayout()
        self.layout_for_permalink.setObjectName(u"layout_for_permalink")
        self.label_for_permalink = QLabel(self.centralwidget)
        self.label_for_permalink.setObjectName(u"label_for_permalink")

        self.layout_for_permalink.addWidget(self.label_for_permalink)

        self.permalink = QLineEdit(self.centralwidget)
        self.permalink.setObjectName(u"permalink")

        self.layout_for_permalink.addWidget(self.permalink)


        self.verticalLayout.addLayout(self.layout_for_permalink)

        self.update_checker_label = QLabel(self.centralwidget)
        self.update_checker_label.setObjectName(u"update_checker_label")
        self.update_checker_label.setOpenExternalLinks(True)

        self.verticalLayout.addWidget(self.update_checker_label)

        self.layout_for_finalize = QHBoxLayout()
        self.layout_for_finalize.setObjectName(u"layout_for_finalize")
        self.about_button = QPushButton(self.centralwidget)
        self.about_button.setObjectName(u"about_button")

        self.layout_for_finalize.addWidget(self.about_button)

        self.horizontal_brake_for_about = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.layout_for_finalize.addItem(self.horizontal_brake_for_about)

        self.reset_settings_to_default = QPushButton(self.centralwidget)
        self.reset_settings_to_default.setObjectName(u"reset_settings_to_default")
        self.reset_settings_to_default.setMinimumSize(QSize(180, 0))

        self.layout_for_finalize.addWidget(self.reset_settings_to_default)

        self.horizontal_brake_for_reset = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.layout_for_finalize.addItem(self.horizontal_brake_for_reset)

        self.randomize_button = QPushButton(self.centralwidget)
        self.randomize_button.setObjectName(u"randomize_button")

        self.layout_for_finalize.addWidget(self.randomize_button)


        self.verticalLayout.addLayout(self.layout_for_finalize)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tab_for_main.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Wind Waker Randomizer", None))
        self.label_for_clean.setText(QCoreApplication.translate("MainWindow", u"Clean WW ISO", None))
        self.label_for_output.setText(QCoreApplication.translate("MainWindow", u"Output Folder", None))
        self.output_folder_browse_button.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.label_for_seed.setText(QCoreApplication.translate("MainWindow", u"Seed (optional)", None))
        self.generate_seed_button.setText(QCoreApplication.translate("MainWindow", u"New seed", None))
        self.clean_iso_path_browse_button.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.group_for_locations.setTitle(QCoreApplication.translate("MainWindow", u"Where Should Progress Items Appear?", None))
        self.progression_platforms_rafts.setText(QCoreApplication.translate("MainWindow", u"Lookout Platforms and Rafts", None))
        self.progression_long_sidequests.setText(QCoreApplication.translate("MainWindow", u"Long Sidequests", None))
        self.progression_dungeons.setText(QCoreApplication.translate("MainWindow", u"Dungeons", None))
        self.progression_short_sidequests.setText(QCoreApplication.translate("MainWindow", u"Short Sidequests", None))
        self.progression_treasure_charts.setText(QCoreApplication.translate("MainWindow", u"Sunken Treasure (From Treasure Charts)", None))
        self.progression_submarines.setText(QCoreApplication.translate("MainWindow", u"Submarines", None))
        self.progression_triforce_charts.setText(QCoreApplication.translate("MainWindow", u"Sunken Treasure (From Triforce Charts)", None))
        self.progression_spoils_trading.setText(QCoreApplication.translate("MainWindow", u"Spoils Trading", None))
        self.progression_minigames.setText(QCoreApplication.translate("MainWindow", u"Minigames", None))
        self.progression_battlesquid.setText(QCoreApplication.translate("MainWindow", u"Battlesquid Minigame", None))
        self.progression_big_octos_gunboats.setText(QCoreApplication.translate("MainWindow", u"Big Octos and Gunboats", None))
        self.progression_expensive_purchases.setText(QCoreApplication.translate("MainWindow", u"Expensive Purchases", None))
        self.progression_great_fairies.setText(QCoreApplication.translate("MainWindow", u"Great Fairies", None))
        self.progression_combat_secret_caves.setText(QCoreApplication.translate("MainWindow", u"Combat Secret Caves", None))
        self.progression_free_gifts.setText(QCoreApplication.translate("MainWindow", u"Free Gifts", None))
        self.progression_savage_labyrinth.setText(QCoreApplication.translate("MainWindow", u"Savage Labyrinth", None))
        self.progression_puzzle_secret_caves.setText(QCoreApplication.translate("MainWindow", u"Puzzle Secret Caves", None))
        self.progression_misc.setText(QCoreApplication.translate("MainWindow", u"Miscellaneous", None))
        self.progression_eye_reef_chests.setText(QCoreApplication.translate("MainWindow", u"Eye Reef Chests", None))
        self.progression_mail.setText(QCoreApplication.translate("MainWindow", u"Mail", None))
        self.progression_tingle_chests.setText(QCoreApplication.translate("MainWindow", u"Tingle Chests", None))
        self.progression_island_puzzles.setText(QCoreApplication.translate("MainWindow", u"Island Puzzles", None))
        self.group_for_settings_secondary.setTitle(QCoreApplication.translate("MainWindow", u"Additional Randomization Options", None))
        self.label_for_sword_mode.setText(QCoreApplication.translate("MainWindow", u"Sword Mode", None))
        self.sword_mode.setItemText(0, QCoreApplication.translate("MainWindow", u"Start with Sword", None))
        self.sword_mode.setItemText(1, QCoreApplication.translate("MainWindow", u"Randomized Sword", None))
        self.sword_mode.setItemText(2, QCoreApplication.translate("MainWindow", u"Swordless", None))

        self.randomize_charts.setText(QCoreApplication.translate("MainWindow", u"Randomize Charts", None))
        self.randomize_starting_island.setText(QCoreApplication.translate("MainWindow", u"Randomize Starting Island", None))
        self.keylunacy.setText(QCoreApplication.translate("MainWindow", u"Key-Lunacy", None))
        self.label_for_num_starting_triforce_shards.setText(QCoreApplication.translate("MainWindow", u"Starting Triforce Shards", None))
        self.num_starting_triforce_shards.setItemText(0, QCoreApplication.translate("MainWindow", u"0", None))
        self.num_starting_triforce_shards.setItemText(1, QCoreApplication.translate("MainWindow", u"1", None))
        self.num_starting_triforce_shards.setItemText(2, QCoreApplication.translate("MainWindow", u"2", None))
        self.num_starting_triforce_shards.setItemText(3, QCoreApplication.translate("MainWindow", u"3", None))
        self.num_starting_triforce_shards.setItemText(4, QCoreApplication.translate("MainWindow", u"4", None))
        self.num_starting_triforce_shards.setItemText(5, QCoreApplication.translate("MainWindow", u"5", None))
        self.num_starting_triforce_shards.setItemText(6, QCoreApplication.translate("MainWindow", u"6", None))
        self.num_starting_triforce_shards.setItemText(7, QCoreApplication.translate("MainWindow", u"7", None))
        self.num_starting_triforce_shards.setItemText(8, QCoreApplication.translate("MainWindow", u"8", None))

        self.race_mode.setText(QCoreApplication.translate("MainWindow", u"Race Mode", None))
        self.label_for_randomize_entrances.setText(QCoreApplication.translate("MainWindow", u"Randomize Entrances", None))
        self.randomize_entrances.setItemText(0, QCoreApplication.translate("MainWindow", u"Disabled", None))
        self.randomize_entrances.setItemText(1, QCoreApplication.translate("MainWindow", u"Dungeons", None))
        self.randomize_entrances.setItemText(2, QCoreApplication.translate("MainWindow", u"Secret Caves", None))
        self.randomize_entrances.setItemText(3, QCoreApplication.translate("MainWindow", u"Dungeons & Secret Caves (Separately)", None))
        self.randomize_entrances.setItemText(4, QCoreApplication.translate("MainWindow", u"Dungeons & Secret Caves (Together)", None))

        self.randomize_music.setText(QCoreApplication.translate("MainWindow", u"Randomize Music", None))
        self.randomize_enemy_palettes.setText(QCoreApplication.translate("MainWindow", u"Randomize Enemy Palettes", None))
        self.randomize_enemies.setText(QCoreApplication.translate("MainWindow", u"Randomize Enemy Locations", None))
        self.label_for_num_dungeon_race_mode.setText(QCoreApplication.translate("MainWindow", u"Dungeon Number", None))
        self.num_dungeon_race_mode.setItemText(0, QCoreApplication.translate("MainWindow", u"1", None))
        self.num_dungeon_race_mode.setItemText(1, QCoreApplication.translate("MainWindow", u"2", None))
        self.num_dungeon_race_mode.setItemText(2, QCoreApplication.translate("MainWindow", u"3", None))
        self.num_dungeon_race_mode.setItemText(3, QCoreApplication.translate("MainWindow", u"4", None))
        self.num_dungeon_race_mode.setItemText(4, QCoreApplication.translate("MainWindow", u"5", None))
        self.num_dungeon_race_mode.setItemText(5, QCoreApplication.translate("MainWindow", u"6", None))
        self.num_dungeon_race_mode.setItemText(6, QCoreApplication.translate("MainWindow", u"Random", None))

        self.num_dungeon_race_mode.setCurrentText(QCoreApplication.translate("MainWindow", u"4", None))
        self.group_for_convenience.setTitle(QCoreApplication.translate("MainWindow", u"Convenience Tweaks", None))
        self.instant_text_boxes.setText(QCoreApplication.translate("MainWindow", u"Instant Text Boxes", None))
        self.skip_rematch_bosses.setText(QCoreApplication.translate("MainWindow", u"Skip Boss Rematches", None))
        self.reveal_full_sea_chart.setText(QCoreApplication.translate("MainWindow", u"Reveal Full Sea Chart", None))
        self.add_shortcut_warps_between_dungeons.setText(QCoreApplication.translate("MainWindow", u"Add Shortcut Warps Between Dungeons", None))
        self.swift_sail.setText(QCoreApplication.translate("MainWindow", u"Swift Sail", None))
        self.remove_title_and_ending_videos.setText(QCoreApplication.translate("MainWindow", u"Remove Title and Ending Videos", None))
        self.remove_music.setText(QCoreApplication.translate("MainWindow", u"Remove Music", None))
        self.invert_camera_x_axis.setText(QCoreApplication.translate("MainWindow", u"Invert Camera X-Axis", None))
        self.group_for_advanced.setTitle(QCoreApplication.translate("MainWindow", u"Advanced Options", None))
        self.disable_tingle_chests_with_tingle_bombs.setText(QCoreApplication.translate("MainWindow", u"Tingle Bombs Don't Open Tingle Chests", None))
        self.do_not_generate_spoiler_log.setText(QCoreApplication.translate("MainWindow", u"Do Not Generate Spoiler Log", None))
        self.tab_for_main.setTabText(self.tab_for_main.indexOf(self.tab_for_settings), QCoreApplication.translate("MainWindow", u"Randomizer Settings", None))
        self.label_for_randomized_gear.setText(QCoreApplication.translate("MainWindow", u"Randomized Gear", None))
        self.remove_gear.setText(QCoreApplication.translate("MainWindow", u"<-", None))
        self.add_gear.setText(QCoreApplication.translate("MainWindow", u"->", None))
        self.label_for_starting_gear.setText(QCoreApplication.translate("MainWindow", u"Starting Gear", None))
        self.label_for_heart_container.setText(QCoreApplication.translate("MainWindow", u"Heart Containers", None))
        self.label_for_heart_piece.setText(QCoreApplication.translate("MainWindow", u"Heart Pieces", None))
        self.current_health.setText(QCoreApplication.translate("MainWindow", u"Current Starting Health: 3 hearts", None))
        self.tab_for_main.setTabText(self.tab_for_main.indexOf(self.tab_for_starting_items), QCoreApplication.translate("MainWindow", u"Starting Items", None))
        self.label_for_custom_player_model.setText(QCoreApplication.translate("MainWindow", u"Player Model", None))
        self.label_for_custom_color_preset.setText(QCoreApplication.translate("MainWindow", u"Color Preset", None))
        self.randomize_all_custom_colors_together.setText(QCoreApplication.translate("MainWindow", u"Randomize Colors Orderly", None))
        self.randomize_all_custom_colors_separately.setText(QCoreApplication.translate("MainWindow", u"Randomize Colors Chaotically", None))
        self.player_in_casual_clothes.setText(QCoreApplication.translate("MainWindow", u"Casual Clothes", None))
        self.disable_custom_player_voice.setText(QCoreApplication.translate("MainWindow", u"Disable Custom Voice", None))
        self.disable_custom_player_items.setText(QCoreApplication.translate("MainWindow", u"Disable Custom Items", None))
        self.custom_model_comment.setText("")
        self.custom_model_preview_label.setText("")
        self.tab_for_main.setTabText(self.tab_for_main.indexOf(self.tab_for_model_customization), QCoreApplication.translate("MainWindow", u"Player Customization", None))
        self.option_description.setText("")
        self.label_for_permalink.setText(QCoreApplication.translate("MainWindow", u"Permalink (copy paste to share your settings):", None))
        self.update_checker_label.setText(QCoreApplication.translate("MainWindow", u"Checking for updates to the randomizer...", None))
        self.about_button.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.reset_settings_to_default.setText(QCoreApplication.translate("MainWindow", u"Reset All Settings to Default", None))
        self.randomize_button.setText(QCoreApplication.translate("MainWindow", u"Randomize", None))
    # retranslateUi

