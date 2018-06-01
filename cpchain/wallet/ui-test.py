#!/usr/bin/python3
import sys, os
import os.path as osp
import string
import logging


from PyQt5.QtWidgets import (QMainWindow, QApplication, QFrame, QDesktopWidget, QPushButton, QHBoxLayout, QMessageBox, 
                             QVBoxLayout, QGridLayout, QWidget, QScrollArea, QListWidget, QListWidgetItem, QTabWidget, QLabel,
                             QWidget, QLineEdit, QSpacerItem, QSizePolicy, QTableWidget, QFormLayout, QComboBox, QTextEdit,
                             QAbstractItemView, QTableWidgetItem, QMenu, QHeaderView, QAction, QFileDialog, QDialog, QRadioButton, QCheckBox, QProgressBar)
from PyQt5.QtCore import Qt, QSize, QPoint, pyqtSignal
from PyQt5.QtGui import QIcon, QCursor, QPixmap, QStandardItem, QFont, QPainter

from cpchain import config, root_dir
from cpchain.wallet.wallet import Wallet
from cpchain.wallet import fs

from twisted.internet import threads, defer, reactor
from twisted.internet.threads import deferToThread
from twisted.internet.task import LoopingCall

wallet = Wallet(reactor)


# utils
logger = logging.getLogger(__name__)

def get_icon(name):
    path = osp.join(root_dir, "cpchain/assets/wallet/icons", name)
    return QIcon(path)

def get_pixm(name):
    path = osp.join(root_dir, "cpchain/assets/wallet/icons", name)
    return QPixmap(path)

    

def load_stylesheet(wid, name):
    path = osp.join(root_dir, "cpchain/assets/wallet/qss", name)

    subs = dict(asset_dir=osp.join(root_dir, "cpchain/assets/wallet"))

    with open(path) as f:
        s = string.Template(f.read())
        wid.setStyleSheet(s.substitute(subs))

# widgets



#class PersonalHomePageTab(QScrollArea)
class PeferenceTab(QScrollArea):
    def __init__(self, parent=None, item={}):
        super().__init__(parent)
        self.parent = parent
        #for testing this Tab @rayhueng
        #self.setObjectName("cart_tab")
        self.setObjectName("preferencepage")
        self.init_ui()

    def init_ui(self):
        #Labels def
        self.downloadpath_label = downloadpath_label = QLabel("Download Path:")
        downloadpath_label.setObjectName("downloadpath_label")
        self.tips_label = tips_label = QLabel("Send message in these conditions:")
        tips_label.setObjectName("tips_label")
        self.messageset_label = messageset_label = QLabel("Message Setting:")
        messageset_label.setObjectName("messageset_label")
        self.tag_label = tag_label = QLabel("Following Tags:")
        tag_label.setObjectName("tag_label")
        self.seller_label = seller_label = QLabel("Following Sellers:")
        seller_label.setObjectName("seller_label")

        #TextEdit def
        self.downloadpath_edit = downloadpath_edit = QLineEdit()
        downloadpath_edit.setObjectName("downloadpath_edit")

        #Buttons and Tags
        self.tag = ["tag1", "tag2", "tag3", "tag4"]
        self.tag_num = 4
        self.tag_btn_list = []
        for i in range(self.tag_num):
            self.tag_btn_list.append(QPushButton(self.tag[i], self))
            self.tag_btn_list[i].setObjectName("tag_btn_{0}".format(i))
            self.tag_btn_list[i].setProperty("t_value", 1)
            self.tag_btn_list[i].setCursor(QCursor(Qt.PointingHandCursor))

        #openpath button: open the download path in file browser on click
        #handler self.handle_openpath
        self.openpath_btn = openpath_btn = QPushButton(self)
        self.openpath_btn.setObjectName("openpath_btn")
        self.openpath_btn.setText("Open...")
        self.openpath_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.openpath_btn.clicked.connect(self.handle_openpath)

        #addtag button: open the page for adding a customized tag on click 
        #handler self.handle_addtag       
        self.addtag_btn = addtag_btn = QPushButton(self)
        self.addtag_btn.setObjectName("addtag_btn")
        self.addtag_btn.setText("Add...")
        self.addtag_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.addtag_btn.clicked.connect(self.handle_addtag)

        #three checkboxes
        self.messageset_checkbox_1 = messageset_checkbox_1 = QCheckBox(self)
        self.messageset_checkbox_1.setObjectName("messageset_checkbox_1")
        self.messageset_checkbox_1.setText("New Order")

        self.messageset_checkbox_2 = messageset_checkbox_2 = QCheckBox(self)
        self.messageset_checkbox_2.setObjectName("messageset_checkbox_2")
        self.messageset_checkbox_2.setText("Account spending")

        self.messageset_checkbox_3 = messageset_checkbox_3 = QCheckBox(self)
        self.messageset_checkbox_3.setObjectName("messageset_checkbox_3")
        self.messageset_checkbox_3.setText("Download failed")

        #widgets for following sellers
        product_counter = 20
        self.seller_avatar = seller_avatar = QLabel("ICONHERE")
        seller_avatar.setObjectName("seller_avatar")       
        self.seller_id = seller_id = QLabel("Christopher Chak")
        seller_id.setObjectName("seller_avatar")  
        self.seller_pcount = seller_pcount = QLabel("Products {}".format(product_counter))
        seller_pcount.setObjectName("seller_pcount")                
        self.unfollow_btn = unfollow_btn = QPushButton("Unfollow")
        self.unfollow_btn.setObjectName("unfollow_btn")
        self.unfollow_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.unfollow_btn.clicked.connect(self.handle_unfollow)

        def set_layout():
            self.pinfo_preference_layout = pinfo_preference_layout = QGridLayout(self)
            #self.pinfo_top_layout.setSpacing(10)
            self.pinfo_preference_layout.setContentsMargins(40, 40, 150, 100)
            self.pinfo_preference_layout.addWidget(downloadpath_label, 1, 1, 1, 1)
            self.pinfo_preference_layout.addWidget(downloadpath_edit, 1, 3, 1, 20)
            self.pinfo_preference_layout.addWidget(openpath_btn, 2, 3, 1, 2)   
                     
            self.pinfo_preference_layout.addWidget(messageset_label, 3, 1, 1, 1)
            self.pinfo_preference_layout.addWidget(tips_label, 3, 3, 1, 5)
            self.pinfo_preference_layout.addWidget(messageset_checkbox_1, 4, 3, 1, 2)
            self.pinfo_preference_layout.addWidget(messageset_checkbox_2, 5, 3, 1, 2)
            self.pinfo_preference_layout.addWidget(messageset_checkbox_3, 6, 3, 1, 2)

            #embeded layout for tag button
            self.pinfo_preference_layout.addWidget(tag_label, 7, 1, 1, 1)
            self.pinfo_tag_layout = pinfo_tag_layout = QHBoxLayout(self)
            for i in range(self.tag_num): 
                self.pinfo_tag_layout.addWidget(self.tag_btn_list[i])
                self.pinfo_tag_layout.addSpacing(5)

            self.pinfo_tag_layout.addStretch(1)
            self.pinfo_preference_layout.addLayout(pinfo_tag_layout, 7, 3, 1, 10)
            self.pinfo_preference_layout.addWidget(addtag_btn, 8, 3, 1, 2)

            self.pinfo_preference_layout.addWidget(seller_label, 9, 1, 1, 1)
            self.pinfo_preference_layout.addWidget(seller_avatar, 9, 3, 2, 2) 
            self.pinfo_preference_layout.addWidget(seller_id, 9, 6, 1, 1) 
            self.pinfo_preference_layout.addWidget(seller_pcount, 10, 6, 1, 1)
            self.pinfo_preference_layout.addWidget(unfollow_btn, 9, 20, 2, 2)            
                       
            self.setLayout(pinfo_preference_layout)
        set_layout()
        print("Loading stylesheet of cloud tab widget")
        #load_stylesheet(self, "pinfo.qss")

    def handle_openpath(self):
        pass

    def handle_addtag(self):
        pass

    def handle_unfollow(self):
        pass


class PersonalInfoPage(QScrollArea):
    def __init__(self, parent=None, item={}):
        super().__init__(parent)
        self.parent = parent
        #for testing this Tab @rayhueng
        self.setObjectName("PersonalInfoPage")
        #self.setObjectName("cart_tab")
        self.init_ui()

    def init_ui(self):
    #Labels def
        self.avatar_label = avatar_label = QLabel("Avatar")
        avatar_label.setObjectName("avatar_label")
        self.avatar_icon = avatar_icon = QLabel("ICONHERE")
        avatar_icon.setObjectName("avatar_icon")
        self.username_label = username_label = QLabel("Username:")
        username_label.setObjectName("username_label")
        self.email_label = email_label = QLabel("Email:")
        email_label.setObjectName("email_label")
        self.gender_label = gender_label = QLabel("Gender:")
        gender_label.setObjectName("gender_label")
        self.phone_label = phone_label = QLabel("Mobile Phone")
        phone_label.setObjectName("phone_label")

        #TextEdit def
        self.username_edit = username_edit = QLineEdit()
        username_edit.setObjectName("username_edit")
        self.email_edit = email_edit = QLineEdit()
        email_edit.setObjectName("email_edit")
        self.phone_edit = phone_edit = QLineEdit()
        phone_edit.setObjectName("phone_edit")


        #Buttons and Tags
        self.avataripload_btn = avataripload_btn = QPushButton(self)
        self.avataripload_btn.setObjectName("avataripload_btn")
        self.avataripload_btn.setText("Upload/Save")
        self.avataripload_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.avataripload_btn.clicked.connect(self.handle_submit)

        self.gender_btn = gender_btn = QPushButton(self)
        self.gender_btn.setObjectName("gender_btn")
        self.gender_btn.setText("Male/Female")

        self.submit_btn = submit_btn = QPushButton(self)
        self.submit_btn.setObjectName("submit_btn")
        self.submit_btn.setText("Submit")
        self.submit_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.submit_btn.clicked.connect(self.handle_submit)


        def set_layout():
            self.pinfo_top_layout = pinfo_top_layout = QGridLayout(self)
            #self.pinfo_top_layout.setSpacing(10)
            self.pinfo_top_layout.setContentsMargins(40, 40, 300, 100)
            self.pinfo_top_layout.addWidget(avatar_label, 1, 1, 1, 1)
            self.pinfo_top_layout.addWidget(avatar_icon, 1, 3, 3, 3)
            self.pinfo_top_layout.addWidget(avataripload_btn, 4, 3, 1, 1)

            self.pinfo_top_layout.addWidget(username_label, 5, 1, 1, 1)
            self.pinfo_top_layout.addWidget(username_edit, 5, 3, 1, 5)      
            self.pinfo_top_layout.addWidget(email_label, 6, 1, 1, 1)
            self.pinfo_top_layout.addWidget(email_edit, 6, 3, 1, 20)        
            self.pinfo_top_layout.addWidget(gender_label, 7, 1, 1, 1)
            self.pinfo_top_layout.addWidget(gender_btn, 7, 3, 1, 1)       
            self.pinfo_top_layout.addWidget(phone_label, 8, 1, 1, 1)
            self.pinfo_top_layout.addWidget(phone_edit, 8, 3, 1, 20)
            self.pinfo_top_layout.addWidget(submit_btn, 10, 3, 1, 2)

            self.setLayout(pinfo_top_layout)
        set_layout()
        #print("Loading stylesheet of cloud tab widget")
        #load_stylesheet(self, "pinfo.qss")
    def handle_submit(self):
        pass




class CollectedTab(QScrollArea):
    class SearchBar(QLineEdit):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.parent = parent
            self.init_ui()

        def init_ui(self):
            self.setObjectName("search_bar")
            self.setFixedSize(300, 25)
            self.setTextMargins(25, 0, 20, 0)

            self.search_btn = search_btn = QPushButton(self)
            search_btn.setObjectName("search_btn")
            search_btn.setFixedSize(18, 18)
            search_btn.setCursor(QCursor(Qt.PointingHandCursor))

            def bind_slots():
                print("Binding slots of clicked-search-btn......")

            bind_slots()

            def set_layout():
                main_layout = QHBoxLayout()
                main_layout.addWidget(search_btn_cloud)
                main_layout.addStretch()
                main_layout.setContentsMargins(5, 0, 0, 0)
                self.setLayout(main_layout)

            set_layout()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        # self.setObjectName("purchase_tab")
        self.setObjectName("collect_tab")
        self.init_ui()

    def update_table(self):
        # file_list = get_file_list()
        print("Updating file list......")
        file_list = []
        # single element data structure (assumed); to be changed
        dict_exa = {"name": "Avengers: Infinity War - 2018", "size": "7200", "price": "200"}
        for i in range(self.row_number):
            file_list.append(dict_exa)

        for cur_row in range(self.row_number):
            if cur_row == len(file_list):
                break
            checkbox_item = QTableWidgetItem()
            checkbox_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            checkbox_item.setCheckState(Qt.Unchecked)
            self.file_table.setItem(cur_row, 0, checkbox_item)
            self.file_table.setItem(cur_row, 1, QTableWidgetItem(file_list[cur_row]["name"]))
            self.file_table.setItem(cur_row, 2, QTableWidgetItem(file_list[cur_row]["price"]))
            self.file_table.setItem(cur_row, 3, QTableWidgetItem(file_list[cur_row]["size"]))

    def init_ui(self):

        self.check_list = []
        self.purchased_total_orders = 103
        self.num_file = 100
        self.cur_clicked = 0

        self.uncollect_btn = uncollect_btn = QPushButton("Uncollect")
        uncollect_btn.setObjectName("uncollect_btn")

        self.time_rank_label = time_rank_label = QLabel("Time")
        time_rank_label.setObjectName("time_rank_label")

        self.uncollect_btn.clicked.connect(self.handle_uncollect)
        self.search_bar = PurchasedDownloadedTab.SearchBar(self)

        self.row_number = 100

        def create_file_table():
            self.file_table = file_table = TableWidget(self)

            file_table.horizontalHeader().setStretchLastSection(True)
            file_table.verticalHeader().setVisible(False)
            file_table.setShowGrid(False)
            file_table.setAlternatingRowColors(True)
            file_table.resizeColumnsToContents()
            file_table.resizeRowsToContents()
            file_table.setFocusPolicy(Qt.NoFocus)
            # do not highlight (bold-ize) the header
            file_table.horizontalHeader().setHighlightSections(False)
            file_table.setColumnCount(4)
            file_table.setRowCount(self.row_number)
            file_table.setSelectionBehavior(QAbstractItemView.SelectRows)
            # file_table.set_right_menu(right_menu)
            file_table.setHorizontalHeaderLabels(['CheckState', 'Product Name', 'Price', 'Size'])
            file_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            file_table.setSortingEnabled(True)

            # file_list = get_file_list()
            file_list = []
            print("Getting file list.......")
            dict_exa = {"name": "Avengers: Infinity War - 2018", "size": "7200", "ordertime": "2018/2/4 08:30",
                        "price": "36"}
            for i in range(self.row_number):
                file_list.append(dict_exa)

            self.check_record_list = []
            self.checkbox_list = []
            for cur_row in range(self.row_number):
                if cur_row == len(file_list):
                    break
                checkbox_item = QTableWidgetItem()
                checkbox_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                checkbox_item.setCheckState(Qt.Unchecked)
                self.file_table.setItem(cur_row, 0, checkbox_item)
                self.file_table.setItem(cur_row, 1, QTableWidgetItem(file_list[cur_row]["name"]))
                self.file_table.setItem(cur_row, 2, QTableWidgetItem(file_list[cur_row]["price"]))
                self.file_table.setItem(cur_row, 3, QTableWidgetItem(file_list[cur_row]["size"]))
                self.check_record_list.append(False)

        create_file_table()
        self.file_table.sortItems(2)
        self.file_table.horizontalHeader().setStyleSheet("QHeaderView::section{background: #f3f3f3; border: 1px solid #dcdcdc}")

        # record rows that are clicked or checked
        def record_check(item):
            self.cur_clicked = item.row()
            if item.checkState() == Qt.Checked:
                self.check_record_list[item.row()] = True

        self.file_table.itemClicked.connect(record_check)

        def set_layout():
            self.main_layout = main_layout = QVBoxLayout(self)
            main_layout.addSpacing(0)
            self.collection_upper_layout = QHBoxLayout(self)
            self.collection_upper_layout.addSpacing(5)
            self.collection_upper_layout.addWidget(self.search_bar)
            self.collection_upper_layout.addSpacing(5)
            self.collection_upper_layout.addWidget(self.time_rank_label)
            self.collection_upper_layout.addStretch(1)
            self.collection_upper_layout.addWidget(self.uncollect_btn)
            self.collection_upper_layout.addSpacing(10)
            
            self.main_layout.addLayout(self.collection_upper_layout)
            self.main_layout.addSpacing(2)
            self.main_layout.addWidget(self.file_table)
            self.main_layout.addSpacing(2)
            self.setLayout(self.main_layout)

        set_layout()
        # print("Loading stylesheet of cloud tab widget")
        load_stylesheet(self, "collection.qss")

    def handle_uncollect(self):
        for i in range(len(self.check_record_list)):
            if self.check_record_list[i] == True:
                self.file_table.removeRow(i)
                print("handle_uncollect files permanently from the collection...")
                self.update_table()



class PurchasedTab(QScrollArea):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.parent = parent
        self.setObjectName("purchase_tab")
        #self.setObjectName("purchased_downloading_tab")
        self.init_ui()

    def init_ui(self):
        self.purchased_dled_tab_btn = purchased_dled_tab_btn = QPushButton("Downloaded")
        self.purchased_dled_tab_btn.setObjectName("purchased_dled_tab_btn")
        self.purchased_dling_tab_btn = purchased_dling_tab_btn = QPushButton("Downloading")
        self.purchased_dling_tab_btn.setObjectName("purchased_dling_tab_btn")

        self.purchased_main_tab = purchased_main_tab = QTabWidget(self)
        purchased_main_tab.setObjectName("purchased_main_tab")
        purchased_main_tab.tabBar().hide()
        # Temporily modified for easy test by @hyiwr
        purchased_main_tab.addTab(PurchasedDownloadedTab(purchased_main_tab), "")
        purchased_main_tab.addTab(PurchasedDownloadingTab(purchased_main_tab), "")

        def dled_btn_clicked(item):
            self.purchased_main_tab.setCurrentIndex(0)
            self.purchased_dled_tab_btn.setStyleSheet("QPushButton{ padding-left: 14px; padding-right: 14px; border: 1px solid #3173d8; border-top-left-radius: 5px; border-bottom-left-radius: 5px; color: #ffffff; min-height: 30px; max-height: 30px; background: #3173d8; }")
            self.purchased_dling_tab_btn.setStyleSheet("QPushButton{ padding-left: 14px; padding-right: 14px; border: 1px solid #3173d8; border-top-right-radius: 5px; border-bottom-right-radius: 5px; color: #3173d8; min-height: 30px; max-height: 30px; background: #ffffff; }")
                   
        self.purchased_dled_tab_btn.clicked.connect(dled_btn_clicked)

        def dling_btn_clicked(item):
            self.purchased_main_tab.setCurrentIndex(1)
            self.purchased_dling_tab_btn.setStyleSheet("QPushButton{ padding-left: 14px; padding-right: 14px; border: 1px solid #3173d8; border-top-right-radius: 5px; border-bottom-right-radius: 5px; color: #ffffff; min-height: 30px; max-height: 30px; background: #3173d8; }")
            self.purchased_dled_tab_btn.setStyleSheet("QPushButton{ padding-left: 14px; padding-right: 14px; border: 1px solid #3173d8; border-top-left-radius: 5px; border-bottom-left-radius: 5px; color: #3173d8; min-height: 30px; max-height: 30px; background: #ffffff; }")

        self.purchased_dling_tab_btn.clicked.connect(dling_btn_clicked)


        def set_layout():
            self.purchased_main_layout = purchased_main_layout = QVBoxLayout(self)

            #add downloaded/downloading buttons for tab switch
            self.purchased_switch_layout = purchased_switch_layout = QHBoxLayout(self)
            self.purchased_switch_layout.setContentsMargins(0, 0, 0, 0) 
            self.purchased_switch_layout.setSpacing(0)
            self.purchased_switch_layout.addStretch(1)
            self.purchased_switch_layout.addWidget(self.purchased_dled_tab_btn)
            self.purchased_switch_layout.addWidget(self.purchased_dling_tab_btn)
            self.purchased_switch_layout.addStretch(1)

            self.purchased_main_layout.addLayout(self.purchased_switch_layout)
            self.purchased_main_layout.addSpacing(5)
            self.purchased_main_layout.addWidget(self.purchased_main_tab)
            self.setLayout(self.purchased_main_layout)
        set_layout()
        print("Loading stylesheet of cloud tab widget")
        load_stylesheet(self, "purchased.qss")

class PurchasedDownloadedTab(QScrollArea):
    class SearchBar(QLineEdit):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.parent = parent
            self.init_ui()

        def init_ui(self):
            self.setObjectName("search_bar")
            self.setFixedSize(300, 25)
            self.setTextMargins(25, 0, 20, 0)

            self.search_btn_cloud = search_btn_cloud = QPushButton(self)
            search_btn_cloud.setObjectName("search_btn")
            search_btn_cloud.setFixedSize(18, 18)
            search_btn_cloud.setCursor(QCursor(Qt.PointingHandCursor))

            def bind_slots():
                print("Binding slots of clicked-search-btn......")
            bind_slots()

            def set_layout():
                main_layout = QHBoxLayout()
                main_layout.addWidget(search_btn_cloud)
                main_layout.addStretch()
                main_layout.setContentsMargins(5, 0, 0, 0)
                self.setLayout(main_layout)
            set_layout()

    def __init__(self, parent = None):
        super().__init__(parent)
        self.parent = parent
        #self.setObjectName("purchase_tab")
        self.setObjectName("purchased_downloaded_tab")
        self.init_ui()

    def update_table(self):
        #file_list = get_file_list()
        print("Updating file list......")
        file_list = []
        # single element data structure (assumed); to be changed 
        dict_exa = {"name": "Avengers: Infinity War - 2018", "size": "7200", "ordertime": "2018/2/4 08:30", "price": "36"}
        for i in range(self.row_number):
            file_list.append(dict_exa)

        for cur_row in range(self.row_number):
            if cur_row == len(file_list):
                break
            checkbox_item = QTableWidgetItem()
            checkbox_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            checkbox_item.setCheckState(Qt.Unchecked)
            self.file_table.setItem(cur_row, 0, checkbox_item)
            self.file_table.setItem(cur_row, 1, QTableWidgetItem(file_list[cur_row]["name"]))
            self.file_table.setItem(cur_row, 2, QTableWidgetItem(file_list[cur_row]["price"]))
            self.file_table.setItem(cur_row, 3, QTableWidgetItem(file_list[cur_row]["size"]))
            self.file_table.setItem(cur_row, 4, QTableWidgetItem(file_list[cur_row]["price"]))

    # def set_right_menu(self, func):
    #     self.customContextMenuRequested[QPoint].connect(func)

    # def handle_upload(self):
    #         self.local_file = QFileDialog.getOpenFileName()[0]
            #defered = threads.deferToThread(upload_file_ipfs, self.local_file)
            #defered.addCallback(handle_callback_upload)

    def init_ui(self):

        self.check_list = []
        self.purchased_total_orders = 103
        self.num_file = 100
        self.cur_clicked = 0

        self.purchased_dled_delete_btn = purchased_dled_delete_btn = QPushButton("Delete")
        purchased_dled_delete_btn.setObjectName("purchased_dled_delete_btn")

        self.purchased_total_orders_label = purchased_total_orders_label = QLabel("Total Orders: ")
        purchased_total_orders_label.setObjectName("purchased_total_orders_label")
        self.total_orders_value = total_orders_value = QLabel("{}".format(self.purchased_total_orders))
        self.total_orders_value.setObjectName("total_orders_value")
        self.purchased_dled_delete_btn.clicked.connect(self.handle_delete)
        self.search_bar = PurchasedDownloadedTab.SearchBar(self)
        self.time_label = time_label = QLabel("Time")
        time_label.setObjectName("time_label")
        self.open_path = open_path = QLabel("Open file path...")
        open_path.setObjectName("open_path")
    
        self.row_number = 100


        def create_file_table():
            self.file_table = file_table = TableWidget(self) 

            file_table.horizontalHeader().setStretchLastSection(True)
            file_table.verticalHeader().setVisible(False)
            file_table.setShowGrid(False)
            file_table.setAlternatingRowColors(True)
            file_table.resizeColumnsToContents()  
            file_table.resizeRowsToContents()
            file_table.setFocusPolicy(Qt.NoFocus) 
            # do not highlight (bold-ize) the header
            file_table.horizontalHeader().setHighlightSections(False)
            file_table.setColumnCount(5)
            file_table.setRowCount(self.row_number)
            file_table.setSelectionBehavior(QAbstractItemView.SelectRows)
            #file_table.set_right_menu(right_menu)
            file_table.setHorizontalHeaderLabels(['CheckState', 'Product Name', 'Price', 'Size', 'Order Time'])
            file_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            file_table.setSortingEnabled(True)

            #file_list = get_file_list()
            file_list = []
            print("Getting file list.......")
            dict_exa = {"name": "Avengers: Infinity War - 2018", "size": "7200", "ordertime": "2018/2/4 08:30", "price": "36"}
            for i in range(self.row_number):
                file_list.append(dict_exa)

            self.check_record_list = []
            self.checkbox_list = []
            for cur_row in range(self.row_number):
                if cur_row == len(file_list):
                    break
                checkbox_item = QTableWidgetItem()
                checkbox_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                checkbox_item.setCheckState(Qt.Unchecked)
                self.file_table.setItem(cur_row, 0, checkbox_item)
                self.file_table.setItem(cur_row, 1, QTableWidgetItem(file_list[cur_row]["name"]))
                self.file_table.setItem(cur_row, 2, QTableWidgetItem(file_list[cur_row]["price"]))
                self.file_table.setItem(cur_row, 3, QTableWidgetItem(file_list[cur_row]["size"]))
                self.file_table.setItem(cur_row, 4, QTableWidgetItem(file_list[cur_row]["ordertime"]))
                self.check_record_list.append(False)
        create_file_table()    
        self.file_table.sortItems(2)
        self.file_table.horizontalHeader().setStyleSheet("QHeaderView::section{background: #f3f3f3; border: 1px solid #dcdcdc}")
        # record rows that are clicked or checked
        def record_check(item):
            self.cur_clicked = item.row()
            if item.checkState() == Qt.Checked:
                self.check_record_list[item.row()] = True
        self.file_table.itemClicked.connect(record_check)

        def set_layout():
            self.main_layout = main_layout = QVBoxLayout(self)
            main_layout.addSpacing(0)
            self.purchased_dled_upper_layout = QHBoxLayout(self)
            self.purchased_dled_upper_layout.addSpacing(0)
            self.purchased_dled_upper_layout.addWidget(self.purchased_total_orders_label)
            self.purchased_dled_upper_layout.addSpacing(0)
            self.purchased_dled_upper_layout.addWidget(self.total_orders_value)
            self.purchased_dled_upper_layout.addSpacing(10)
            self.purchased_dled_upper_layout.addWidget(self.search_bar)
            self.purchased_dled_upper_layout.addSpacing(10)
            self.purchased_dled_upper_layout.addWidget(self.time_label)
            self.purchased_dled_upper_layout.addSpacing(10)           
            self.purchased_dled_upper_layout.addWidget(self.open_path)
            self.purchased_dled_upper_layout.addStretch(1)
            self.purchased_dled_upper_layout.addWidget(self.purchased_dled_delete_btn)

            self.main_layout.addLayout(self.purchased_dled_upper_layout)
            self.main_layout.addSpacing(2)
            self.main_layout.addWidget(self.file_table)
            self.main_layout.addSpacing(2)
            self.setLayout(self.main_layout)
        set_layout()
        #print("Loading stylesheet of cloud tab widget")
        #load_stylesheet(self, "cloud.qss")

    def handle_delete(self):
        for i in range(len(self.check_record_list)):
            if self.check_record_list[i] == True:
                self.file_table.removeRow(i)
                print("Deleting files permanently from the cloud...")
                self.update_table()




class PurchasedDownloadingTab(QScrollArea):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.parent = parent
        #self.setObjectName("purchase_tab")
        self.setObjectName("purchased_downloading_tab")
        self.init_ui()

    def update_table(self):
        #file_list = get_file_list()
        print("Updating file list......")
        file_list = []
        # single element data structure (assumed); to be changed 
        dict_exa = {"name": "Avengers: Infinity War - 2018", "size": "7200", "ordertime": "2018/2/4 08:30", "price": "36"}
        for i in range(self.row_number):
            file_list.append(dict_exa)

        for cur_row in range(self.row_number):
            if cur_row == len(file_list):
                break
            checkbox_item = QTableWidgetItem()
            checkbox_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            checkbox_item.setCheckState(Qt.Unchecked)
            dling_progressbar = QProgressBar()
            #dling_progressbar.setFixedSize(150,8)
            dling_progressbar.setMaximum(100)
            dling_progressbar.setMinimum(0)
            dling_progressbar.setValue(49)
            self.file_table.setItem(cur_row, 0, checkbox_item)
            self.file_table.setItem(cur_row, 1, QTableWidgetItem(file_list[cur_row]["name"]))
            self.file_table.setCellWidget(cur_row, 2, dling_progressbar)
            self.file_table.setItem(cur_row, 3, QTableWidgetItem(file_list[cur_row]["ordertime"]))

    def set_right_menu(self, func):
        self.customContextMenuRequested[QPoint].connect(func)

    def handle_upload(self):
            self.local_file = QFileDialog.getOpenFileName()[0]

    def init_ui(self):
        self.check_list = []
        self.purchased_total_orders = 103
        self.num_file = 100
        self.cur_clicked = 0

        self.purchased_total_orders_label = purchased_total_orders_label = QLabel("Total Orders: ")
        purchased_total_orders_label.setObjectName("purchased_total_orders_label")
        self.total_orders_value = total_orders_value = QLabel("{}".format(self.purchased_total_orders))
        self.total_orders_value.setObjectName("total_orders_value")
        self.purchased_dling_delete_btn = purchased_dling_delete_btn = QPushButton("Delete")
        purchased_dling_delete_btn.setObjectName("purchased_dling_delete_btn")
        self.purchased_dling_start_btn = purchased_dling_start_btn = QPushButton("Start")
        purchased_dling_start_btn.setObjectName("purchased_dling_start_btn")
        self.purchased_dling_pause_btn = purchased_dling_pause_btn = QPushButton("Pause")
        purchased_dling_pause_btn.setObjectName("purchased_dling_pause_btn")

        self.purchased_dling_delete_btn.clicked.connect(self.handle_purchased_delete)
        self.open_path = open_path = QLabel("Open file path...")
        open_path.setObjectName("open_path")
    
        self.row_number = 100


        def create_file_table():
            self.file_table = file_table = TableWidget(self) 
            def right_menu():
                self.purchased_right_menu = QMenu(file_table)
                self.purchased_delete_act = QAction('Delete', self)
                self.purchased_publish_act = QAction('Publish', self)

                self.purchased_delete_act.triggered.connect(self.handle_delete_act)
                self.purchased_publish_act.triggered.connect(self.handle_publish_act)

                self.purchased_right_menu.addAction(self.purchased_delete_act)
                self.purchased_right_menu.addAction(self.purchased_publish_act)

                self.purchased_right_menu.exec_(QCursor.pos())

            file_table.horizontalHeader().setStretchLastSection(True)
            file_table.verticalHeader().setVisible(False)
            file_table.setShowGrid(False)
            file_table.setAlternatingRowColors(True)
            file_table.resizeColumnsToContents()  
            file_table.resizeRowsToContents()
            file_table.setFocusPolicy(Qt.NoFocus) 
            # do not highlight (bold-ize) the header
            file_table.horizontalHeader().setHighlightSections(False)
            file_table.setColumnCount(4)
            file_table.setRowCount(self.row_number)
            file_table.setSelectionBehavior(QAbstractItemView.SelectRows)
            file_table.set_right_menu(right_menu)
            file_table.setHorizontalHeaderLabels(['CheckState', 'Product Name', 'Progress', 'Order Time'])
            file_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            file_table.setSortingEnabled(True)

            #file_list = get_file_list()
            file_list = []
            print("Getting file list.......")
            dict_exa = {"name": "Avengers: Infinity War - 2018", "size": "7200", "ordertime": "2018/2/4 08:30", "price": "36", "progress": "50%"}
            for i in range(self.row_number):
                file_list.append(dict_exa)

            self.check_record_list = []
            self.checkbox_list = []
            for cur_row in range(self.row_number):
                if cur_row == len(file_list):
                    break
                checkbox_item = QTableWidgetItem()
                checkbox_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                checkbox_item.setCheckState(Qt.Unchecked)
                dling_progressbar = QProgressBar()
                dling_progressbar.setMaximum(100)
                dling_progressbar.setMinimum(0)
                dling_progressbar.setValue(49)
                self.file_table.setItem(cur_row, 0, checkbox_item)
                self.file_table.setItem(cur_row, 1, QTableWidgetItem(file_list[cur_row]["name"]))
                self.file_table.setCellWidget(cur_row, 2, dling_progressbar)
                #self.file_table.setItem(cur_row, 2, QTableWidgetItem(file_list[cur_row]["progress"]))
                self.file_table.setItem(cur_row, 3, QTableWidgetItem(file_list[cur_row]["ordertime"]))
                self.check_record_list.append(False)
        create_file_table()    

        self.file_table.sortItems(2)
        self.file_table.horizontalHeader().setStyleSheet("QHeaderView::section{background: #f3f3f3; border: 1px solid #dcdcdc}")
        # record rows that are clicked or checked
        def record_check(item):
            self.cur_clicked = item.row()
            if item.checkState() == Qt.Checked:
                self.check_record_list[item.row()] = True
        self.file_table.itemClicked.connect(record_check)

        def set_layout():
            self.main_layout = main_layout = QVBoxLayout(self)
            main_layout.addSpacing(0)
            self.purchased_upper_layout = QHBoxLayout(self)
            self.purchased_upper_layout.addSpacing(0)
            self.purchased_upper_layout.addWidget(self.purchased_total_orders_label)
            self.purchased_upper_layout.addSpacing(0)
            self.purchased_upper_layout.addWidget(self.total_orders_value)
            self.purchased_upper_layout.addSpacing(10)         
            self.purchased_upper_layout.addWidget(self.open_path)
            self.purchased_upper_layout.addStretch(1)
            self.purchased_upper_layout.addWidget(self.purchased_dling_start_btn)
            self.purchased_upper_layout.addSpacing(10)
            self.purchased_upper_layout.addWidget(self.purchased_dling_pause_btn)
            self.purchased_upper_layout.addSpacing(10)            
            self.purchased_upper_layout.addWidget(self.purchased_dling_delete_btn)
            self.purchased_upper_layout.addSpacing(5)

            self.main_layout.addLayout(self.purchased_upper_layout)
            self.main_layout.addSpacing(2)
            self.main_layout.addWidget(self.file_table)
            self.main_layout.addSpacing(2)
            self.setLayout(self.main_layout)
        set_layout()

    def handle_purchased_delete(self):
        # TODO: delete event
        for i in range(len(self.check_record_list)):
            if self.check_record_list[i] == True:
                self.file_table.removeRow(i)
                #self.update_table()
        logger.debug("Delete the corresponding row (i.e. self.cur_clicked) in TableWidget as before")
        logger.debug("Cancel uploading from backend")
        logger.debug("Uploading the table")


class PublishDialog(QDialog):
    def __init__(self, parent=None, item={}):
        super().__init__(parent)
        self.parent = parent
        #for testing this Tab @rayhueng
        self.setObjectName("cart_tab")
        #self.setObjectName("product_info_tab")
        self.init_ui()

    def init_ui(self):

        #Labels def
        self.pinfo_title_label = pinfo_title_label = QLabel("Title:")
        pinfo_title_label.setObjectName("pinfo_title_label")
        self.pinfo_descrip_label = pinfo_descrip_label = QLabel("Description:")
        pinfo_descrip_label.setObjectName("pinfo_descrip_label")
        self.pinfo_tag_label = pinfo_tag_label = QLabel("Tag:")
        pinfo_tag_label.setObjectName("pinfo_tag_label")
        self.pinfo_price_label = pinfo_price_label = QLabel("Price:")
        pinfo_price_label.setObjectName("pinfo_price_label")
        self.pinfo_cpc_label = pinfo_cpc_label = QLabel("CPC")
        pinfo_cpc_label.setObjectName("pinfo_cpc_label")

        #TextEdit def
        self.pinfo_title_edit = pinfo_title_edit = QLineEdit()
        pinfo_title_edit.setObjectName("pinfo_title_edit")
        self.pinfo_descrip_edit = pinfo_descrip_edit = QTextEdit()
        pinfo_descrip_edit.setObjectName("pinfo_descrip_edit")
        self.pinfo_tag_edit = pinfo_tag_edit = QLineEdit()
        pinfo_tag_edit.setObjectName("pinfo_tag_edit")
        self.pinfo_price_edit = pinfo_price_edit = QLineEdit()
        pinfo_price_edit.setObjectName("pinfo_price_edit")

        #Buttons and Tags
        self.tag = ["tag1", "tag2", "tag3", "tag4"]
        self.tag_num = 4
        self.tag_btn_list = []
        for i in range(self.tag_num):
            self.tag_btn_list.append(QPushButton(self.tag[i], self))
            self.tag_btn_list[i].setObjectName("tag_btn_{0}".format(i))
            #ser property t_value = 1 for the convience of specifying QSS
            self.tag_btn_list[i].setProperty("t_value", 1)
            self.tag_btn_list[i].setCursor(QCursor(Qt.PointingHandCursor))

        self.pinfo_cancel_btn = pinfo_cancel_btn = QPushButton(self)
        self.pinfo_cancel_btn.setObjectName("pinfo_cancel_btn")
        self.pinfo_cancel_btn.setText("Cancel")
        self.pinfo_cancel_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.pinfo_cancel_btn.clicked.connect(self.handle_cancel)

        self.pinfo_publish_btn = pinfo_publish_btn = QPushButton(self)
        self.pinfo_publish_btn.setObjectName("pinfo_publish_btn")
        self.pinfo_publish_btn.setText("Publish")
        self.pinfo_publish_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.pinfo_publish_btn.clicked.connect(self.handle_publish)

        self.pinfo_checkbox = pinfo_checkbox = QCheckBox(self)
        self.pinfo_checkbox.setObjectName("pinfo_checkbox")
        self.pinfo_checkbox.setText("I agree with the CPC Agreement")


        def set_layout():
            self.pinfo_top_layout = pinfo_top_layout = QGridLayout(self)
            #self.pinfo_top_layout.setSpacing(10)
            self.pinfo_top_layout.setContentsMargins(40, 40, 150, 100)
            self.pinfo_top_layout.addWidget(pinfo_title_label, 1, 1, 1, 1)
            self.pinfo_top_layout.addWidget(pinfo_title_edit, 1, 3, 1, 20)
            self.pinfo_top_layout.addWidget(pinfo_descrip_label, 2, 1, 1, 1)
            self.pinfo_top_layout.addWidget(pinfo_descrip_edit, 2, 3, 3, 20)
            self.pinfo_top_layout.addWidget(pinfo_tag_label, 8, 1, 1, 1)

            #embeded layout for tag button
            self.pinfo_tag_layout = pinfo_tag_layout = QHBoxLayout(self)
            for i in range(self.tag_num): 
                self.pinfo_tag_layout.addWidget(self.tag_btn_list[i])
                self.pinfo_tag_layout.addSpacing(5)

            self.pinfo_tag_layout.addStretch(1)
            self.pinfo_top_layout.addLayout(pinfo_tag_layout, 8, 3, 1, 10)
            self.pinfo_top_layout.addWidget(pinfo_tag_edit, 9, 3, 1, 3)

            #embeded layout for price input
            self.pinfo_price_layout = pinfo_price_layout = QHBoxLayout(self)
            self.pinfo_price_layout.addWidget(pinfo_price_edit)
            self.pinfo_price_layout.addSpacing(5)
            self.pinfo_price_layout.addWidget(pinfo_cpc_label)
            self.pinfo_price_layout.addStretch(1)
            #add the layout of price input to upper layer layout
            self.pinfo_top_layout.addLayout(pinfo_price_layout, 10, 3, 1, 10) 
            self.pinfo_top_layout.addWidget(pinfo_price_label, 10, 1, 1, 1)   
            self.pinfo_top_layout.addWidget(pinfo_checkbox, 12, 3, 1, 2)

            #embeded layout for two buttons
            self.pinfo_btn_layout = pinfo_btn_layout = QHBoxLayout(self)
            self.pinfo_btn_layout.addWidget(pinfo_cancel_btn)
            self.pinfo_btn_layout.addSpacing(80)
            self.pinfo_btn_layout.addWidget(pinfo_publish_btn)
            self.pinfo_btn_layout.addStretch(1)
            #add the layout of price input to upper layer layout
            self.pinfo_top_layout.addLayout(pinfo_btn_layout, 13, 3, 1, 15)    

            self.setLayout(pinfo_top_layout)
        set_layout()
        print("Loading stylesheet of cloud tab widget")
        load_stylesheet(self, "pinfo.qss")

        self.show()

    def handle_publish(self):
        self.pinfo_title = self.pinfo_title_edit.text()
        self.pinfo_descrip = self.pinfo_descrip_edit.toPlainText()
        self.pinfo_tag = self.pinfo_tag_edit.text()
        self.pinfo_price = self.pinfo_price_edit.text()
        self.pinfo_checkbox_state = self.pinfo_checkbox.isChecked()
        if self.pinfo_title and self.pinfo_descrip and self.pinfo_tag and self.pinfo_price and self.pinfo_checkbox_state:
            print("Updating item info in wallet database and other relevant databases")
            print("Updating self.parent tab info: selling tab or cloud tab")
            QMessageBox.information(self, "Tips", "Successful !")
            self.close()
        else:
            QMessageBox.warning(self, "Warning", "Please fill out the necessary selling information first!")

    def handle_cancel(self):
        print("exiting the current dialog")
        self.close()
        # will be changed next according to calling tab (cloud tab or selling tab)




class SellTab(QScrollArea):
    class SearchBar(QLineEdit):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.parent = parent
            self.init_ui()

        def init_ui(self):
            self.setObjectName("search_bar")
            self.setFixedSize(300, 25)
            self.setTextMargins(25, 0, 20, 0)

            self.search_btn_cloud = search_btn_cloud = QPushButton(self)
            search_btn_cloud.setObjectName("search_btn_sell")
            search_btn_cloud.setFixedSize(18, 18)
            search_btn_cloud.setCursor(QCursor(Qt.PointingHandCursor))

            def bind_slots():
                print("Binding slots of clicked-search-btn......")
            bind_slots()

            def set_layout():
                main_layout = QHBoxLayout()
                main_layout.addWidget(search_btn_cloud)
                main_layout.addStretch()
                main_layout.setContentsMargins(5, 0, 0, 0)
                self.setLayout(main_layout)
            set_layout()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setObjectName("selling_tab")

        self.init_ui()

    def update_table(self):
        #file_list = get_file_list()
        print("Updating file list......")
        file_list = []
        # single element data structure (assumed); to be changed 
        dict_exa = {"type": "mkv", "name": "Infinity War", "size": "1.2 GB", "remote_type": "ipfs", "is_published": "published"}
        for i in range(self.row_number):
            file_list.append(dict_exa)

        for cur_row in range(self.row_number):
            if cur_row == len(file_list):
                break
            checkbox_item = QTableWidgetItem()
            checkbox_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            checkbox_item.setCheckState(Qt.Unchecked)
            self.file_table.setItem(cur_row, 0, checkbox_item)
            self.file_table.setItem(cur_row, 1, QTableWidgetItem(file_list[cur_row]["type"]))
            self.file_table.setItem(cur_row, 2, QTableWidgetItem(file_list[cur_row]["name"]))
            self.file_table.setItem(cur_row, 3, QTableWidgetItem(file_list[cur_row]["size"]))
            self.file_table.setItem(cur_row, 4, QTableWidgetItem(file_list[cur_row]["remote_type"]))
            self.file_table.setItem(cur_row, 5, QTableWidgetItem(file_list[cur_row]["is_published"]))

    def set_right_menu(self, func):
        self.customContextMenuRequested[QPoint].connect(func)

    def handle_upload(self):
            self.local_file = QFileDialog.getOpenFileName()[0]
            #defered = threads.deferToThread(upload_file_ipfs, self.local_file)
            #defered.addCallback(handle_callback_upload)

    def init_ui(self):
        self.frame = QFrame()
        self.frame.setObjectName("sell_frame")
        self.setWidget(self.frame)
        self.setWidgetResizable(True)
        self.frame.setMinimumWidth(500)
        #self.frame.setMaximumHeight(800)

        self.check_list = []
        self.sell_product = 100
        self.total_orders = 103
        self.total_sales = 1234
        self.cur_clicked = 0

        self.sell_product_label = sell_product_label = QLabel("Products:")
        sell_product_label.setObjectName("sell_product_label")
        self.product_value = product_value = QLabel("{}".format(self.sell_product))
        product_value.setObjectName("product_value")  

        self.sell_orders_label = sell_orders_label = QLabel("Total Orders:")
        sell_orders_label.setObjectName("sell_orders_label")
        self.order_value = order_value = QLabel("{}".format(self.total_orders))
        order_value.setObjectName("order_value") 

        self.total_sales_label = total_sales_label = QLabel("Total Sales($):")
        total_sales_label.setObjectName("total_sales_label")
        self.sales_value = sales_value = QLabel("{}".format(self.total_sales))
        sales_value.setObjectName("sales_value") 

        self.time_rank_label = time_rank_label = QLabel("Time")
        time_rank_label.setObjectName("time_rank_label")

        self.tag_rank_label = tag_rank_label = QLabel("Tag")
        tag_rank_label.setObjectName("tag_rank_label")        

        self.sell_delete_btn = sell_delete_btn = QPushButton("Delete")
        sell_delete_btn.setObjectName("sell_delete_btn")
        self.sell_delete_btn.clicked.connect(self.handle_delete)

        self.sell_publish_btn = sell_publish_btn = QPushButton("Publish")
        sell_publish_btn.setObjectName("sell_publish_btn")
        #please define the handler of publish event
        #self.sell_publish_btn.clicked.connect(self.handle_publish)


        self.search_bar_sell = SellTab.SearchBar(self)
        self.time_label = time_label = QLabel("Time")
    
        self.row_number = 100


        def create_file_table():
            self.file_table = file_table = TableWidget(self)

            file_table.horizontalHeader().setStretchLastSection(True)
            file_table.verticalHeader().setVisible(False)
            file_table.setShowGrid(False)
            file_table.setAlternatingRowColors(True)
            file_table.resizeColumnsToContents()  
            file_table.resizeRowsToContents()
            file_table.setFocusPolicy(Qt.NoFocus) 
            # do not highlight (bold-ize) the header
            file_table.horizontalHeader().setHighlightSections(False)
            file_table.setColumnCount(7)
            file_table.setRowCount(self.row_number)
            file_table.setSelectionBehavior(QAbstractItemView.SelectRows)

            file_table.setHorizontalHeaderLabels(['CheckState', 'Product Name', 'Price ($)', 'Order', 'Sales', 'Rating', 'Update Time'])
            file_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            file_table.setSortingEnabled(True)

            #file_list = get_file_list()
            file_list = []
            print("Getting file list.......")
            dict_exa = {"type": "mkv", "name": "Infinity War", "price": "200", "order": "36", "sales": "7200", "rating": "4.5", "updatetime": "2018/5/14 08:30"}
            for i in range(self.row_number):
                file_list.append(dict_exa)

            self.check_record_list = []
            self.checkbox_list = []
            for cur_row in range(self.row_number):
                if cur_row == len(file_list):
                    break
                checkbox_item = QTableWidgetItem()
                checkbox_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                checkbox_item.setCheckState(Qt.Unchecked)
                self.file_table.setItem(cur_row, 0, checkbox_item)
                self.file_table.setItem(cur_row, 1, QTableWidgetItem(file_list[cur_row]["name"]))
                self.file_table.setItem(cur_row, 2, QTableWidgetItem(file_list[cur_row]["price"]))
                self.file_table.setItem(cur_row, 3, QTableWidgetItem(file_list[cur_row]["order"]))
                self.file_table.setItem(cur_row, 4, QTableWidgetItem(file_list[cur_row]["sales"]))
                self.file_table.setItem(cur_row, 5, QTableWidgetItem(file_list[cur_row]["rating"]))
                self.file_table.setItem(cur_row, 6, QTableWidgetItem(file_list[cur_row]["updatetime"]))
                self.check_record_list.append(False)
        create_file_table()    
        self.file_table.sortItems(2)
        self.file_table.horizontalHeader().setStyleSheet("QHeaderView::section{background: #f3f3f3; border: 1px solid #dcdcdc}")
        # record rows that are clicked or checked
        def record_check(item):
            self.cur_clicked = item.row()
            if item.checkState() == Qt.Checked:
                self.check_record_list[item.row()] = True
        self.file_table.itemClicked.connect(record_check)

        def set_layout():
            self.main_layout = main_layout = QVBoxLayout(self)
            main_layout.addSpacing(0)
            self.layout1 = QHBoxLayout(self)
            self.layout1.addSpacing(0)
            self.layout1.addWidget(self.sell_product_label)
            self.layout1.addWidget(self.product_value)
            self.layout1.addSpacing(5)
            self.layout1.addWidget(self.sell_orders_label)
            self.layout1.addWidget(self.order_value)
            self.layout1.addSpacing(5)
            self.layout1.addWidget(self.total_sales_label)
            self.layout1.addWidget(self.sales_value)
            self.layout1.addStretch(1)
            self.main_layout.addLayout(self.layout1)
            
            self.layout2 = QHBoxLayout(self)
            self.layout2.addWidget(self.search_bar_sell)
            self.layout2.addSpacing(10)
            self.layout2.addWidget(self.time_rank_label)
            self.layout2.addSpacing(10)
            self.layout2.addWidget(self.tag_rank_label)
            self.layout2.addStretch(1)
            self.layout2.addWidget(self.sell_delete_btn)
            self.layout2.addSpacing(5)
            self.layout2.addWidget(self.sell_publish_btn)
            self.layout2.addSpacing(5)
            self.main_layout.addLayout(self.layout2)
            
            self.main_layout.addSpacing(2)
            self.main_layout.addWidget(self.file_table)
            self.main_layout.addSpacing(2)
            self.setLayout(self.main_layout)
        set_layout()
        print("Loading stylesheet of cloud tab widget")
        load_stylesheet(self, "sell.qss")

    def handle_delete(self):
        for i in range(len(self.check_record_list)):
            if self.check_record_list[i] == True:
                self.file_table.removeRow(i)
                print("Deleting files permanently from the cloud...")
                self.update_table()

    class UploadDialog(QDialog):
        def __init__(self, parent=None):
            super().__init__()
            self.parent = parent
            self.setWindowTitle("Publish your products")
            self.cloud_choice = {"ipfs": False, "s3": False}
            self.file_choice = ""

            self.init_ui()

        def init_ui(self):

            def create_btns():
                self.ipfs_btn = ipfs_btn = QRadioButton(self)
                ipfs_btn.setText("IPFS")
                ipfs_btn.setObjectName("ipfs_btn")
                ipfs_btn.setChecked(True)
                self.s3_btn = s3_btn = QRadioButton(self)
                s3_btn.setText("Amazon S3")
                s3_btn.setObjectName("s3_btn")
                self.file_choose_btn = file_choose_btn = QPushButton("Open File")
                file_choose_btn.setObjectName("file_choose_btn")

                self.cancel_btn = cancel_btn = QPushButton("Cancel")
                cancel_btn.setObjectName("cancel_btn")
                self.ok_btn = ok_btn = QPushButton("OK")
                ok_btn.setObjectName("ok_btn")
            create_btns()

            def create_labels():
                self.choice_label = choice_label = QLabel("Please select where you want to upload your data from one of the below two services: ")
                choice_label.setObjectName("choice_label")
            create_labels()

            def bind_slots():
                self.file_choose_btn.clicked.connect(self.choose_file)
                self.cancel_btn.clicked.connect(self.handle_cancel)
                self.ok_btn.clicked.connect(self.handle_ok)
            bind_slots()

            def set_layout():
                self.main_layout = main_layout = QVBoxLayout()
                main_layout.addSpacing(0)
                main_layout.addWidget(self.choice_label)
                main_layout.addSpacing(2)
                main_layout.addWidget(self.file_choose_btn)
                main_layout.addSpacing(1)
                main_layout.addWidget(self.ipfs_btn)
                main_layout.addSpacing(1)
                main_layout.addWidget(self.s3_btn)
                self.confirm_layout = confirm_layout = QHBoxLayout()
                confirm_layout.addSpacing(0)
                confirm_layout.addWidget(self.ok_btn)
                confirm_layout.addSpacing(2)
                confirm_layout.addWidget(self.cancel_btn)

                main_layout.addLayout(self.confirm_layout)
                self.setLayout(self.main_layout)
            set_layout()

            self.show()

            print("Loading stylesheet of publish dialog....")

        def choose_file(self):
            self.file_choice = QFileDialog.getOpenFileName()[0]

        def handle_cancel(self):
            self.file_choice = ""
            self.ipfs_btn.setChecked(True)
            self.s3_btn.setChecked(False)

            self.close()

        def handle_ok(self):
            if self.file_choice == "":
                QMessageBox.warning(self, "Warning", "Please select your files to upload first !")
                return
            print("Uploading files to....")
            QMessageBox.information(self, "Tips", "Log in successfully !")

    def handle_upload(self):
        print("Uploading local files....")
        self.upload_dialog = CloudTab.UploadDialog(self)


    def handle_delete_act(self):
        self.file_table.removeRow(self.cur_clicked)
        print("row {} has been removed...".format(self.cur_clicked))

    def handle_publish_act(self):
        print("handle publish act....")
        

class FollowingTagTab(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setObjectName("follow_tab_tag")
        self.init_ui()

    def init_ui(self):  
        self.frame = QFrame()
        self.frame.setObjectName("follow_tag_frame")
        self.setWidget(self.frame)
        self.setWidgetResizable(True)
        self.frame.setMinimumWidth(500)
        #self.frame.setMaximumHeight(800) 

        self.follow_item_num = 5
        self.follow_promo_num = 2

        self.item_lists = []

        def get_items(products):
            print("Getting items from backend......")
            for i in range(self.follow_item_num):
                self.item_lists.append(Product(self, item=products[i]))
            set_layout()

        d_products = wallet.market_client.query_recommend_product()
        d_products.addCallback(get_items)

        self.promo_label = QLabel(self)

        def get_promotion(promotion):
            print("Getting promotion images from backend.....")
            self.promo_label.setObjectName("promo_label")
            path = osp.join(root_dir, promotion[0]['image'])
            pixmap = QPixmap(path)
            pixmap = pixmap.scaled(250, 123)
            self.promo_label.setPixmap(pixmap)

        d_promotion = wallet.market_client.query_promotion()
        d_promotion.addCallback(get_promotion)

        def set_layout():
            self.follow_main_layout = QHBoxLayout(self)

            self.follow_tag_product_layout=QVBoxLayout(self)
            self.follow_tag_product_layout.addSpacing(0)

            self.follow_tag_promotion_layout=QVBoxLayout(self)
            self.follow_tag_promotion_layout.addSpacing(0)

            for i in range(self.follow_item_num):
                self.follow_tag_product_layout.addWidget(self.item_lists[i])
                self.follow_tag_product_layout.addSpacing(0)

            self.follow_tag_promotion_layout.addWidget(self.promo_label)
            self.follow_tag_promotion_layout.addStretch(5)
                    
            self.follow_main_layout.addLayout(self.follow_tag_product_layout)
            self.follow_main_layout.addSpacing(1)
            #self.bottom_layout.setStretchFactor(recom_layout,4)
            self.follow_main_layout.addLayout(self.follow_tag_promotion_layout)

            self.setLayout(self.follow_main_layout)


class FollowingSellTab(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setObjectName("follow_sell_tag")
        self.init_ui()

    def init_ui(self):
        self.frame = QFrame()
        self.frame.setObjectName("follow_sell_frame")
        self.setWidget(self.frame)
        self.setWidgetResizable(True)
        self.frame.setMinimumWidth(500)
        # self.frame.setMaximumHeight(800)

        self.follow_item_num = 5

        self.item_lists = []

        # def create_btns():
        #     self.follow_rank_btn = QPushButton("Rank", self)
        #     self.follow_time_btn = QPushButton("Time", self)
        #     self.follow_price_btn = QPushButton("Price", self)
        #     self.follow_sales_btn = QPushButton("Sales", self)
        #     self.follow_filter_btn = QPushButton("Filter", self)

        #     self.follow_rank_btn.setObjectName("follow_rank_btn")
        #     self.follow_time_btn.setObjectName("follow_time_btn")
        #     self.follow_price_btn.setObjectName("follow_price_btn")
        #     self.follow_sales_btn.setObjectName("follow_sales_btn")
        #     self.follow_filter_btn.setObjectName("follow_filter_btn")
        # create_btns()

        self.header_horline = HorizontalLine(self, 2)
        self.header_horline.setObjectName("header_horline")

        def get_items(products):
            print("Getting items from backend......")
            for i in range(self.follow_item_num):
                self.item_lists.append(Product(self, item=products[i]))
            set_layout()

        d_products = wallet.market_client.query_recommend_product()
        d_products.addCallback(get_items)

        self.promo_label = QLabel(self)

        def get_promotion(promotion):
            print("Getting promotion images from backend.....")
            self.promo_label.setObjectName("promo_label")
            path = osp.join(root_dir, promotion[0]['image'])
            pixmap = QPixmap(path)
            pixmap = pixmap.scaled(250, 123)
            self.promo_label.setPixmap(pixmap)

        d_promotion = wallet.market_client.query_promotion()
        d_promotion.addCallback(get_promotion)

        def set_layout():

            self.follow_main_layout = QHBoxLayout(self)

            self.follow_tag_product_layout = QVBoxLayout(self)
            self.follow_tag_product_layout.addSpacing(0)

            self.follow_tag_promotion_layout = QVBoxLayout(self)
            self.follow_tag_promotion_layout.addSpacing(0)

            for i in range(self.follow_item_num):
                self.follow_tag_product_layout.addWidget(self.item_lists[i])
                self.follow_tag_product_layout.addSpacing(1)

            self.follow_tag_promotion_layout.addWidget(self.promo_label)
            self.follow_tag_promotion_layout.addStretch(5)

            self.follow_main_layout.addLayout(self.follow_tag_product_layout)
            self.follow_main_layout.addSpacing(1)
            self.follow_main_layout.addLayout(self.follow_tag_promotion_layout)

            # self.follow_all_layout.addLayout(self.follow_rank_layout)
            # self.follow_all_layout.addWidget(self.header_horline)
            # self.follow_all_layout.addLayout(self.follow_main_layout)

            self.setLayout(self.follow_main_layout)

class FollowingTab(QScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setObjectName("follow_tab")
        self.init_ui()   

    def init_ui(self):

        #self.follow_tag_btn = follow_tag_btn = QPushButton(self)
        #self.follow_tag_btn.setObjectName("follow_tag_btn")

        def add_content_tabs():
            self.follow_tabs = follow_tabs = QTabWidget(self)
            follow_tabs.setObjectName("follow_tabs")
            #follow_tabs.tabBar().hide()
            follow_tabs.addTab(FollowingTagTab(follow_tabs), "Tag")
            follow_tabs.addTab(FollowingSellTab(follow_tabs), "Sell")
        add_content_tabs()

        def set_layout():
            self.follow_main_layout = follow_main_layout = QHBoxLayout()
            #self.follow_main_layout.setSpacing(0)
            #self.follow_main_layout.setContentsMargins(0, 0, 0, 0) 
            #self.follow_main_layout.addSpacing(0)
            #follow_main_layout.addWidget(self.follow_tag_btn)
            follow_main_layout.addWidget(self.follow_tabs)
            self.setLayout(self.follow_main_layout)
            #self.main_layout.addLayout(self.content_layout)

            #wid = QWidget(self)
            #wid.setLayout(self.main_layout)
            #self.setCentralWidget(wid)
        set_layout()
        load_stylesheet(self, "follow.qss")
        print("Loading stylesheet of following tab widget")

# widgets
class TableWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        # size
        self.setMinimumWidth(self.parent.width())
        # context menu
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.horizontalHeader().setStretchLastSection(True)
        self.verticalHeader().setVisible(False)
        self.setShowGrid(False)
        self.setAlternatingRowColors(True)
        # do not highlight (bold-ize) the header
        self.horizontalHeader().setHighlightSections(False)


    def set_right_menu(self, func):
        self.customContextMenuRequested[QPoint].connect(func)



class HorizontalLine(QFrame):
    def __init__(self, parent=None, wid=2):
        super().__init__(parent)
        self.parent = parent
        self.wid = wid
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Plain)
        self.setLineWidth(self.wid)



class Product(QScrollArea):
    def __init__(self, parent=None, item={}):
        super().__init__(parent)
        self.parent = parent
        self.item = item
        self.init_ui()

    def init_ui(self):
        #self.frame.setMinimumWidth(500)
        self.setMinimumHeight(200)
        self.setMaximumHeight(500)
        self.title_btn = QPushButton(self.item['title'])
        self.setMinimumHeight(120)
        self.setMaximumHeight(120)
        self.title_btn = QPushButton("Medicine big data from Mayo Clinic")
        self.title_btn.setObjectName("title_btn")

        self.seller_btn = QPushButton("Barack Obama")
        self.seller_btn.setObjectName("seller_btn")
        self.seller_btn.setCursor(QCursor(Qt.PointingHandCursor))

        self.time_label = QLabel("May 4, 2018")
        self.time_label.setObjectName("time_label")
        self.total_sale_label = QLabel("128 sales")
        self.total_sale_label.setObjectName("total_sale_label")
        self.price_label = QLabel("$18")
        self.price_label.setObjectName("price_label")
        self.price_label.setFont(QFont("Arial", 15, QFont.Bold))

        self.gap_line = HorizontalLine(self, 2)
        self.gap_line.setObjectName("gap_line")

        self.tag = ["tag1", "tag2", "tag3", "tag4"]
        self.tag_num = 4
        self.tag_btn_list = []

        for i in range(self.tag_num):
            self.tag_btn_list.append(QPushButton(self.tag[i], self))
            self.tag_btn_list[i].setObjectName("tag_btn_{0}".format(i))
            self.tag_btn_list[i].setProperty("t_value", 1)
            self.tag_btn_list[i].setCursor(QCursor(Qt.PointingHandCursor))

        def bind_slots():
            print("Binding slots of buttons......")
        bind_slots()

        def setlayout():
            self.main_layout = main_layout = QVBoxLayout(self)
            main_layout.addSpacing(0)
            main_layout.addWidget(self.title_btn)
            main_layout.addSpacing(5)

            self.sales_layout = QHBoxLayout(self)
            self.sales_layout.addWidget(self.total_sale_label)
            self.sales_layout.addStretch(1)
            self.sales_layout.addWidget(self.seller_btn)
            self.sales_layout.addSpacing(5)
            self.sales_layout.addWidget(self.time_label)
            self.sales_layout.addStretch(2)
            

            self.main_layout.addLayout(self.sales_layout)
            main_layout.addSpacing(10)
            self.main_layout.addWidget(self.price_label)

            self.tag_layout = QHBoxLayout(self)
            self.tag_layout.addSpacing(1)
            for i in range(self.tag_num):
                self.tag_layout.addWidget(self.tag_btn_list[i])
                self.tag_layout.addSpacing(5)

            self.tag_layout.addStretch(1)
            self.main_layout.addLayout(self.tag_layout)
            self.main_layout.addSpacing(5)
            self.main_layout.addWidget(self.gap_line)
            #self.main_layout.addStretch(1)
            self.setLayout(self.main_layout)
        setlayout()
        print("Loading stylesheet of item")


class PopularTab(QScrollArea):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.parent = parent
        self.setObjectName("popular_tab")

        self.init_ui()

    def init_ui(self):
        # self.frame = QFrame()
        # self.frame.setObjectName("popular_frame")
        # self.setWidget(self.frame)
        # self.setWidgetResizable(True)
        # self.frame.setMinimumWidth(500)
        #self.frame.setMaximumHeight(800)

        self.item_num_max = 2
        self.promo_num_max = 1

        self.horline1 = HorizontalLine(self, 2)
        self.horline1.setObjectName("horline1")
        self.horline2 = HorizontalLine(self, 2)
        self.horline2.setObjectName("horline2")

        self.banner_label = QLabel(self)
        def create_banner(carousel):
            print(carousel)
            print("Getting banner images......")
            path = osp.join(root_dir, carousel[0]['image'])
            print(path)
            pixmap = QPixmap(path)  # get_pixm('cpc-logo-single.png')
            pixmap = pixmap.scaled(740, 195)
            self.banner_label.setPixmap(pixmap)

        d_banner = wallet.market_client.query_carousel()
        d_banner.addCallback(create_banner)

        self.hot_label = QLabel("Hot Industry")
        self.hot_label.setObjectName("hot_label")
        self.hot_label.setFont(QFont("Arial", 13))
        self.hot_label.setMinimumHeight(2)
        self.hot_label.setMaximumHeight(25)

        self.more_btn_1 = more_btn_1 = QPushButton("More>", self)
        more_btn_1.setObjectName("more_btn_1")
        self.more_btn_1.setCursor(QCursor(Qt.PointingHandCursor))
        #more_btn.setFixedSize(30, 18)
        self.more_btn_2 = more_btn_2 = QPushButton("More>", self)
        more_btn_2.setObjectName("more_btn_2")
        self.more_btn_2.setCursor(QCursor(Qt.PointingHandCursor))

        def create_hot_industry():
            self.hot_industry_label = []
            for i in range(config.wallet.hot_industry_num):
                hot_industry = QLabel(self)
                hot_industry.setObjectName('hot_industry_' + str(i))
                self.hot_industry_label.append(hot_industry)
                print('create label' + str(i))
        create_hot_industry()

        def set_hot_industry(hot_industry):
            for i in range(config.wallet.hot_industry_num):
                self.hot_industry_label[i].setText(hot_industry[i]['tag'])
                self.hot_industry_label[i].setFont(QFont("Arial", 13, QFont.Light))
                self.hot_industry_label[i].setAlignment(Qt.AlignCenter)
                path = osp.join(root_dir, hot_industry[i]['image'])
                print(path)
                self.hot_industry_label[i].setStyleSheet("border-image: url({0}); color: #fefefe".format(path))
                # pixmap = QPixmap(path)
                # pixmap = pixmap.scaled(230, 136)
                # self.hot_industry_label[i].setPixmap(pixmap)
        d_hot_industry = wallet.market_client.query_hot_tag()
        d_hot_industry.addCallback(set_hot_industry)

        self.recom_label = QLabel("Recommended")
        self.recom_label.setObjectName("recom_label")
        self.recom_label.setFont(QFont("Arial", 13, QFont.Light))
        self.recom_label.setMaximumHeight(25)

        self.promo_label = QLabel(self)

        def get_promotion(promotion):
            print("Getting promotion images from backend.....")
            self.promo_label.setObjectName("promo_label")
            path = osp.join(root_dir, promotion[0]['image'])
            pixmap = QPixmap(path)
            pixmap = pixmap.scaled(250, 123)
            self.promo_label.setPixmap(pixmap)

        d_promotion = wallet.market_client.query_promotion()
        d_promotion.addCallback(get_promotion)

        self.item_lists = []

        def get_items(products):
            print("Getting items from backend......")
            for i in range(self.item_num_max):
                self.item_lists.append(Product(self, item=products[i]))
            set_layout()

        d_products = wallet.market_client.query_recommend_product()
        d_products.addCallback(get_items)

        def set_layout():
            self.main_layout = QVBoxLayout(self)

            self.banner_layout = QHBoxLayout(self)
            self.banner_layout.addWidget(self.banner_label)
            self.main_layout.addLayout(self.banner_layout)
            self.main_layout.addSpacing(35)
            self.main_layout.addWidget(self.hot_label)

            self.hot_layout = QHBoxLayout(self)
            self.hot_layout.addSpacing(0)
            self.hot_layout.addWidget(self.hot_label)
            self.hot_layout.addSpacing(50)
            self.hot_layout.addWidget(more_btn_1)
            self.main_layout.addLayout(self.hot_layout)
            self.main_layout.addSpacing(1)
            self.main_layout.addWidget(self.horline1)

            self.hot_img_layout = QHBoxLayout(self)
            for i in range(config.wallet.hot_industry_num):
                self.hot_img_layout.addSpacing(25)
                self.hot_img_layout.addWidget(self.hot_industry_label[i])
            self.main_layout.addLayout(self.hot_img_layout)
            self.main_layout.addSpacing(1)
            
            self.recom_layout = QHBoxLayout(self)
            self.recom_layout.addSpacing(0)
            self.recom_layout.addWidget(self.recom_label)
            self.recom_layout.addSpacing(50)
            self.recom_layout.addWidget(more_btn_2)
            self.main_layout.addLayout(self.recom_layout)
            self.main_layout.addSpacing(1)
            self.main_layout.addWidget(self.horline2)
            self.main_layout.addSpacing(1)
            
            self.bottom_layout = QHBoxLayout(self)

            self.product_layout = QVBoxLayout(self)
            for i in range(self.item_num_max):
                self.product_layout.addWidget(self.item_lists[i])
                self.product_layout.addSpacing(1)

            self.promo_layout = QVBoxLayout(self)
            self.promo_layout.addWidget(self.promo_label)
            self.promo_layout.addSpacing(1)

            self.bottom_layout.addLayout(self.product_layout)
            #self.bottom_layout.setStretchFactor(recom_layout,4)
            self.bottom_layout.addLayout(self.promo_layout)
            #self.bottom_layout.setStretch(promo_layout,1)

            self.main_layout.addLayout(self.bottom_layout)
        load_stylesheet(self, "popular.qss")
        print("Loading stylesheet of cloud tab widget")


class CloudTab(QScrollArea):
    class SearchBar(QLineEdit):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.parent = parent
            self.init_ui()

        def init_ui(self):
            self.setObjectName("search_bar")
            #self.setFixedSize(300, 25)
            self.setTextMargins(25, 0, 20, 0)

            self.search_btn_cloud = search_btn_cloud = QPushButton(self)
            search_btn_cloud.setObjectName("search_btn_cloud")
            search_btn_cloud.setFixedSize(18, 18)
            search_btn_cloud.setCursor(QCursor(Qt.PointingHandCursor))

            def bind_slots():
                print("Binding slots of clicked-search-btn......")
            bind_slots()

            def set_layout():
                main_layout = QHBoxLayout()
                main_layout.addWidget(search_btn_cloud)
                main_layout.addStretch()
                main_layout.setContentsMargins(5, 0, 0, 0)
                self.setLayout(main_layout)
            set_layout()

    def __init__(self, parent = None):
        super().__init__(parent)
        self.parent = parent
        self.setObjectName("cloud_tab")

        self.init_ui()

    def update_table(self):
        #file_list = get_file_list()
        print("Updating file list......")
        self.file_list = fs.get_file_list()
        print(len(self.file_list))
        self.row_number = len(self.file_list)
        for cur_row in range(self.row_number):
            # if cur_row == len(file_list):
            #     break
            print(str(cur_row) + " row")
            checkbox_item = QTableWidgetItem()
            checkbox_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            checkbox_item.setCheckState(Qt.Unchecked)
            self.file_table.setItem(cur_row, 0, checkbox_item)
            self.file_table.setItem(cur_row, 1, QTableWidgetItem(self.file_list[cur_row].name))
            self.file_table.setItem(cur_row, 2, QTableWidgetItem(str(self.file_list[cur_row].size)))
            self.file_table.setItem(cur_row, 3, QTableWidgetItem(self.file_list[cur_row].remote_type))
            self.file_table.setItem(cur_row, 4, QTableWidgetItem(str(self.file_list[cur_row].is_published)))

    def set_right_menu(self, func):
        self.customContextMenuRequested[QPoint].connect(func)


    def init_ui(self):

        self.check_list = []
        self.num_file = 100
        self.cur_clicked = 0
        self.total_label = total_label = QLabel("{} Files".format(self.num_file))
        total_label.setObjectName("total_label")

        self.delete_btn = delete_btn = QPushButton("Delete")
        delete_btn.setObjectName("delete_btn")
        self.delete_btn.clicked.connect(self.handle_delete)
        self.upload_btn = upload_btn = QPushButton("Upload")
        upload_btn.setObjectName("upload_btn")

        #upload_btn.clicked.connect(handle_upload)
        self.upload_btn.clicked.connect(self.handle_upload)

        self.search_bar = CloudTab.SearchBar(self)

        self.time_rank_label = time_rank_label = QLabel("Time")
        time_rank_label.setObjectName("time_rank_label")

        self.tag_rank_label = tag_rank_label = QLabel("Tag")
        tag_rank_label.setObjectName("tag_rank_label")  
    
        self.row_number = 6


        def create_file_table():
            self.file_table = file_table = TableWidget(self) 
            def right_menu():
                self.cloud_right_menu = QMenu(file_table)
                self.cloud_delete_act = QAction('Delete', self)
                self.cloud_publish_act = QAction('Publish', self)

                self.cloud_delete_act.triggered.connect(self.handle_delete_act)
                self.cloud_publish_act.triggered.connect(self.handle_publish_act)

                self.cloud_right_menu.addAction(self.cloud_delete_act)
                self.cloud_right_menu.addAction(self.cloud_publish_act)

                self.cloud_right_menu.exec_(QCursor.pos())

            file_table.horizontalHeader().setStretchLastSection(True)
            file_table.verticalHeader().setVisible(False)
            file_table.setShowGrid(False)
            file_table.setAlternatingRowColors(True)
            file_table.resizeColumnsToContents()  
            file_table.resizeRowsToContents()
            file_table.setFocusPolicy(Qt.NoFocus) 
            # do not highlight (bold-ize) the header
            file_table.horizontalHeader().setHighlightSections(False)
            file_table.setColumnCount(5)
            file_table.setRowCount(self.row_number)
            file_table.setSelectionBehavior(QAbstractItemView.SelectRows)
            file_table.set_right_menu(right_menu)
            file_table.setHorizontalHeaderLabels(['CheckState', 'Product Name', 'Size', 'Remote Type', 'Published'])
            file_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            file_table.setSortingEnabled(True)

            self.file_list = fs.get_file_list()

            self.check_record_list = []
            self.checkbox_list = []
            self.row_number = len(self.file_list)
            print("init cloud table, row num: ")
            print(self.row_number)

            for cur_row in range(self.row_number):
                # if cur_row == len(file_list):export PYTHONPATH=/home/cpchainpublic1/Documents/cpchain/
                #     break
                checkbox_item = QTableWidgetItem()
                checkbox_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                checkbox_item.setCheckState(Qt.Unchecked)
                self.file_table.setItem(cur_row, 0, checkbox_item)
                self.file_table.setItem(cur_row, 1, QTableWidgetItem(self.file_list[cur_row].name))
                self.file_table.setItem(cur_row, 2, QTableWidgetItem(str(self.file_list[cur_row].size)))
                #size
                self.file_table.setItem(cur_row, 3, QTableWidgetItem(self.file_list[cur_row].name))
                #remote_type
                self.file_table.setItem(cur_row, 4, QTableWidgetItem(str(self.file_list[cur_row].is_published)))
                self.check_record_list.append(False)
        create_file_table()    
        self.file_table.sortItems(2)
        self.file_table.horizontalHeader().setStyleSheet("QHeaderView::section{background: #f3f3f3; border: 1px solid #dcdcdc}")
        # record rows that are clicked or checked
        def record_check(item):
            self.cur_clicked = item.row()
            if item.checkState() == Qt.Checked:
                self.check_record_list[item.row()] = True
        self.file_table.itemClicked.connect(record_check)

        def set_layout():
            self.main_layout = main_layout = QVBoxLayout(self)
            main_layout.addSpacing(0)
            self.layout1 = QHBoxLayout(self)
            self.layout1.addWidget(self.search_bar)
            self.layout1.addSpacing(10)
            self.layout1.addWidget(self.time_rank_label)
            self.layout1.addSpacing(10)
            self.layout1.addWidget(self.tag_rank_label)
            self.layout1.addStretch(1)
            self.layout1.addWidget(self.delete_btn)
            self.layout1.addSpacing(5)
            self.layout1.addWidget(self.upload_btn)
            self.layout1.addSpacing(5)

            self.main_layout.addLayout(self.layout1)
            self.main_layout.addSpacing(2)
            self.main_layout.addWidget(self.file_table)
            self.setLayout(self.main_layout)
        set_layout()
        print("Loading stylesheet of cloud tab widget")
        load_stylesheet(self, "cloud.qss")

    def handle_delete(self):
        for i in range(len(self.check_record_list)):
            if self.check_record_list[i] == True:
                self.file_table.removeRow(i)
                print("Deleting files permanently from the cloud...")
                self.update_table()

    class UploadDialog(QDialog):
        def __init__(self, parent=None):
            super().__init__()
            self.parent = parent
            self.setWindowTitle("Publish your products")
            self.cloud_choice = {"ipfs": False, "s3": False}
            self.file_choice = ""

            self.init_ui()

        def init_ui(self):

            def create_btns():
                self.ipfs_btn = ipfs_btn = QRadioButton(self)
                ipfs_btn.setText("IPFS")
                ipfs_btn.setObjectName("ipfs_btn")
                ipfs_btn.setChecked(True)
                self.s3_btn = s3_btn = QRadioButton(self)
                s3_btn.setText("Amazon S3")
                s3_btn.setObjectName("s3_btn")
                self.file_choose_btn = file_choose_btn = QPushButton("Open File")
                file_choose_btn.setObjectName("file_choose_btn")

                self.cancel_btn = cancel_btn = QPushButton("Cancel")
                cancel_btn.setObjectName("cancel_btn")
                self.ok_btn = ok_btn = QPushButton("OK")
                ok_btn.setObjectName("ok_btn")
            create_btns()

            def create_labels():
                self.choice_label = choice_label = QLabel("Please select where you want to upload your data from one of the below two services: ")
                choice_label.setObjectName("choice_label")
            create_labels()

            def bind_slots():
                self.file_choose_btn.clicked.connect(self.choose_file)
                self.cancel_btn.clicked.connect(self.handle_cancel)
                self.ok_btn.clicked.connect(self.handle_ok)
            bind_slots()

            def set_layout():
                self.main_layout = main_layout = QVBoxLayout()
                main_layout.addSpacing(0)
                main_layout.addWidget(self.choice_label)
                main_layout.addSpacing(2)
                main_layout.addWidget(self.file_choose_btn)
                main_layout.addSpacing(1)
                main_layout.addWidget(self.ipfs_btn)
                main_layout.addSpacing(1)
                main_layout.addWidget(self.s3_btn)
                self.confirm_layout = confirm_layout = QHBoxLayout()
                confirm_layout.addSpacing(0)
                confirm_layout.addWidget(self.ok_btn)
                confirm_layout.addSpacing(2)
                confirm_layout.addWidget(self.cancel_btn)

                main_layout.addLayout(self.confirm_layout)
                self.setLayout(self.main_layout)
            set_layout()

            self.show()

            print("Loading stylesheet of publish dialog....")

        def choose_file(self):
            self.file_choice = QFileDialog.getOpenFileName()[0]

        def handle_cancel(self):
            self.file_choice = ""
            self.ipfs_btn.setChecked(True)
            self.s3_btn.setChecked(False)

            self.close()

        def handle_ok(self):
            if self.file_choice == "":
                QMessageBox.warning(self, "Warning", "Please select your files to upload first !")
                return
            else:
                if self.ipfs_btn.isChecked():
                    print("start uploading")
                    d_upload = deferToThread(fs.upload_file_ipfs, self.file_choice)
                    d_upload.addCallback(self.handle_ok_callback)
                if self.s3_btn.isChecked():
                    print("upload to s3")
                    # encrypt and uoload self.file_choice

            print("Uploading files to....")
            self.close()

        def handle_ok_callback(self, file_hash):
            print("upload succeed: " + file_hash)
            self.parent.update_table()

    def handle_upload(self):
        # Maybe useful for buyer.
        # row_selected = self.file_table.selectionModel().selectedRows()[0].row()
        # selected_fpath = self.file_table.item(row_selected, 2).text()
        print("Uploading local files....")
        self.upload_dialog = CloudTab.UploadDialog(self)

    #def handle_upload(self):
        # Maybe useful for buyer.
        # row_selected = self.file_table.selectionModel().selectedRows()[0].row()
        # selected_fpath = self.file_table.item(row_selected, 2).text()
        #self.local_file = QFileDialog.getOpenFileName()[0]
        #print("Uploading local files....")
        # defered = threads.deferToThread(upload_file_ipfs, self.local_file)
        # def handle_callback_upload(x):
        #     print("in handle_callback_upload" + x)
        #     self.update_table()
        # defered.addCallback(handle_callback_upload)

    def handle_delete_act(self):
        self.file_table.removeRow(self.cur_clicked)
        print("row {} has been removed...".format(self.cur_clicked))

    def handle_publish_act(self):
        item = {"name": "Avengers: Infinity War - 2018", "size": "1.2 GB", "remote_type": "ipfs", "is_published": "Published"}
        self.publish_dialog = PublishDialog(self, item)
        # self.file_list[self.cur_clicked]
        print("handle publish act....")



class SideBar(QScrollArea):
    def __init__(self, parent):
        super().__init__(parent)
        # needed
        self.parent = parent
        self.content_tabs = parent.content_tabs

        self.init_ui()


    def init_ui(self):
        self.setObjectName("sidebar")
        self.setMaximumWidth(180)

        self.frame = QFrame()
        self.setWidget(self.frame)
        self.setWidgetResizable(True)
        self.frame.setMinimumWidth(150)

        def add_labels():
            self.trend_label = QLabel("Trending")
            self.trend_label.setObjectName("trend_label")
            self.trend_label.setMaximumHeight(25)

            self.mine_label = QLabel("Mine")
            self.mine_label.setObjectName("mine_label")
            self.trend_label.setMaximumHeight(25)

            self.treasure_label = QLabel("Treasure")
            self.treasure_label.setObjectName("treasure_label")
            self.treasure_label.setMaximumHeight(25)
        add_labels()

        def add_lists():
            self.trending_list = QListWidget()
            #self.trending_list.setMinimumHeight(100)
            self.trending_list.setMaximumHeight(100)
            self.trending_list.addItem(QListWidgetItem(get_icon("pop.png"), "Popular"))
            self.trending_list.addItem(QListWidgetItem(get_icon("following.png"), "Following"))

            self.mine_list = QListWidget()
            self.mine_list.setMaximumHeight(100)
            self.mine_list.addItem(QListWidgetItem(get_icon("cloud.png"), "Cloud"))
            self.mine_list.addItem(QListWidgetItem(get_icon("store.png"), "Selling"))

            self.treasure_list = QListWidget()
            self.treasure_list.setMaximumHeight(100)
            self.treasure_list.addItem(QListWidgetItem(get_icon("purchased.png"), "Purchased"))
            self.treasure_list.addItem(QListWidgetItem(get_icon("collection.png"), "Collection"))
            self.treasure_list.addItem(QListWidgetItem(get_icon("collection.png"), "Shopping Cart"))

            self.trending_list.setCurrentRow(0)
        add_lists()

        def bind_slots():
            def trending_list_clicked(item):
                item_to_tab_name = {
                    "Popular": "popular_tab",
                    "Following": "follow_tab",
                }
                wid = self.content_tabs.findChild(QWidget, item_to_tab_name[item.text()])
                self.content_tabs.setCurrentWidget(wid)
            self.trending_list.itemPressed.connect(trending_list_clicked)

            def mine_list_clicked(item):
                item_to_tab_name = {
                    "Cloud": "cloud_tab",
                    "Selling": "selling_tab",
                }
                wid = self.content_tabs.findChild(QWidget, item_to_tab_name[item.text()])
                self.content_tabs.setCurrentWidget(wid)
            self.mine_list.itemPressed.connect(mine_list_clicked)

            def treasure_list_clicked(item):
                item_to_tab_name = {
                    "Purchased": "purchase_tab",
                    "Collection": "collect_tab",
                    "Shopping Cart": "cart_tab",
                }
                wid = self.content_tabs.findChild(QWidget, item_to_tab_name[item.text()])
                self.content_tabs.setCurrentWidget(wid)
            self.treasure_list.itemPressed.connect(treasure_list_clicked)

        bind_slots()

        def set_layout():
            self.main_layout = main_layout = QVBoxLayout(self.frame)
            main_layout.addSpacing(10)
            main_layout.addWidget(self.trend_label)
            main_layout.addSpacing(3)
            main_layout.addWidget(self.trending_list)
            main_layout.addSpacing(1)
            main_layout.addWidget(self.mine_label)
            main_layout.addSpacing(3)
            main_layout.addWidget(self.mine_list)
            main_layout.addSpacing(1)
            main_layout.addWidget(self.treasure_label)
            main_layout.addSpacing(3)
            main_layout.addWidget(self.treasure_list)
            main_layout.setContentsMargins(0, 0, 0, 0)
            main_layout.addStretch(1)
            self.setLayout(self.main_layout)
        set_layout()
        load_stylesheet(self, "sidebar.qss")
        print("Loading stylesheet of Sidebar")


class Header(QFrame):
    class SearchBar(QLineEdit):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.parent = parent
            self.init_ui()

        def init_ui(self):
            self.setObjectName("search_bar")
            self.setFixedSize(300, 25)
            self.setTextMargins(25, 0, 20, 0)

            self.search_btn_cloud = search_btn_cloud = QPushButton(self)
            search_btn_cloud.setObjectName("search_btn")
            search_btn_cloud.setFixedSize(18, 18)
            search_btn_cloud.setCursor(QCursor(Qt.PointingHandCursor))

            def bind_slots():
                print("Binding slots of clicked-search-btn......")
            bind_slots()

            def set_layout():
                main_layout = QHBoxLayout()
                main_layout.addWidget(search_btn_cloud)
                main_layout.addStretch()
                main_layout.setContentsMargins(5, 0, 0, 0)
                self.setLayout(main_layout)
            set_layout()

    class LoginDialog(QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.parent = parent
            self.setWindowTitle("Log In")

            self.init_ui()

        def init_ui(self):

            def create_btns():
                self.account1_btn = account1_btn = QRadioButton(self)
                account1_btn.setText("Account 1")
                account1_btn.setObjectName("account1_btn")
                account1_btn.setChecked(True)
                self.account2_btn = account2_btn = QRadioButton(self)
                account2_btn.setText("Account 2")
                account2_btn.setObjectName("account2_btn")

                self.cancel_btn = cancel_btn = QPushButton("Cancel")
                cancel_btn.setObjectName("cancel_btn")
                self.login_btn = login_btn = QPushButton("Log in")
                login_btn.setObjectName("login_btn")
            create_btns()

            def create_labels():
                self.choice_label = choice_label = QLabel("Please select which account you would like to log in: ")
                choice_label.setObjectName("choice_label")
            create_labels()

            def bind_slots():
                self.cancel_btn.clicked.connect(self.handle_cancel)
                self.login_btn.clicked.connect(self.handle_login)
            bind_slots()

            def set_layout():
                self.main_layout = main_layout = QVBoxLayout()
                main_layout.addSpacing(0)
                main_layout.addWidget(self.choice_label)
                main_layout.addSpacing(2)
                main_layout.addWidget(self.account1_btn)
                main_layout.addSpacing(1)
                main_layout.addWidget(self.account2_btn)
                self.confirm_layout = confirm_layout = QHBoxLayout()
                confirm_layout.addSpacing(0)
                confirm_layout.addWidget(self.cancel_btn)
                confirm_layout.addSpacing(2)
                confirm_layout.addWidget(self.login_btn)

                main_layout.addLayout(self.confirm_layout)
                self.setLayout(self.main_layout)
            set_layout()

            self.show()

            print("Loading stylesheet of publish dialog....")

        def handle_cancel(self):
            self.account1_btn.setChecked(True)
            self.account2_btn.setChecked(False)

            self.close()

        def handle_login(self):
            print("check access......")
            d_login = wallet.market_client.login()

            def login_result(status):
                if status == 1:
                    QMessageBox.information(self, "Tips", "Successful !")
                elif status == 2:
                    QMessageBox.information(self, "Tips", "Failed !")
                else:
                    QMessageBox.information(self, "Tips", "New Users !")
                    # TODO: jump to userfile
            d_login.addCallback(login_result)
            self.close()



    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()


    def init_ui(self):
        def create_logos():
            self.logo_label = logo_label = QLabel(self)
            pixmap = get_pixm('cpc-logo-single.png')
            pixmap = pixmap.scaled(45, 45)
            logo_label.setPixmap(pixmap)
            self.word_label = word_label = QLabel(self)
            self.word_label.setText("<b>CPChain</b>")
            self.word_label.setFont(QFont("Roman times", 25, QFont.Bold));
            
            print("Pic label has not been set !")
        create_logos()

        def create_search_bar():
            self.search_bar = search_bar = Header.SearchBar(self)
            search_bar.setPlaceholderText("Search")
        create_search_bar()

        def create_btns():
            self.prev_btn = QPushButton("", self)
            self.prev_btn.setObjectName("prev_btn")

            self.nex_btn = QPushButton("", self)
            self.nex_btn.setObjectName("nex_btn")

            self.download_btn = QPushButton("", self)
            self.download_btn.setObjectName("download_btn")

            self.upload_btn = QPushButton("", self)
            self.upload_btn.setObjectName("upload_btn")
            self.upload_btn.setCursor(QCursor(Qt.PointingHandCursor))

            self.message_btn = QPushButton("", self)
            self.message_btn.setObjectName("message_btn")
            self.message_btn.setCursor(QCursor(Qt.PointingHandCursor))

            self.profile_page_btn = QPushButton("", self)
            self.profile_page_btn.setObjectName("profile_page_btn")
            self.profile_page_btn.setCursor(QCursor(Qt.PointingHandCursor))
            self.profile_page_btn.clicked.connect(self.login)

            self.profile_btn = QPushButton("", self)
            self.profile_btn.setObjectName("profile_btn")

            self.minimize_btn = QPushButton("_", self)
            self.minimize_btn.setObjectName("minimize_btn")
            self.minimize_btn.setFixedSize(10, 10)
            self.minimize_btn.clicked.connect(self.parent.showMinimized)


            self.maximize_btn = QPushButton("□", self)
            self.maximize_btn.setObjectName("maxmize_btn")
            self.maximize_btn.setFixedSize(10, 10)
            def toggle_maximization():
                state = Qt.WindowFullScreen | Qt.WindowMaximized
                if state & self.parent.windowState():
                    self.parent.showNormal()
                else:
                    self.parent.showMaximized()
            self.maximize_btn.clicked.connect(toggle_maximization)

            self.close_btn = QPushButton("x", self)
            self.close_btn.setObjectName("close_btn")
            self.close_btn.setFixedSize(10, 10)
            self.close_btn.clicked.connect(self.parent.close)

            def create_popmenu():
                self.profile_menu = profile_menu = QMenu('Profile', self)
                profile_view_act = QAction('Profile', self)
                pro_setting_act = QAction('Profile Settins', self)
                acc_setting_act = QAction('Account Settings', self)
                bill_man_act = QAction('Bill Management', self)
                help_act = QAction('Help', self)

                profile_menu.addAction(profile_view_act)
                profile_menu.addAction(pro_setting_act)
                profile_menu.addAction(acc_setting_act)
                profile_menu.addAction(bill_man_act)
                profile_menu.addAction(help_act)
            create_popmenu()
            self.profile_btn.setMenu(self.profile_menu)

        create_btns()


        def bind_slots():
            # TODO
            print("Binding slots of clicked-search-btn......")
            print("Binding slots of pre-btn......")
            print("Binding slots of nex-btn......")
        bind_slots()

        def set_layout():
            self.all_layout = all_layout = QVBoxLayout(self)
            all_layout.addSpacing(0)

            self.extra_layout = extra_layout = QHBoxLayout(self)
            extra_layout.addStretch(1)
            extra_layout.addWidget(self.minimize_btn)
            extra_layout.addSpacing(2)
            extra_layout.addWidget(self.maximize_btn)
            extra_layout.addSpacing(2)
            extra_layout.addWidget(self.close_btn)
            extra_layout.addSpacing(2)

            self.main_layout = main_layout = QHBoxLayout(self)
            main_layout.setSpacing(0)
            main_layout.setContentsMargins(0, 0, 0, 0)
            main_layout.addWidget(self.logo_label)
            main_layout.addSpacing(5)
            main_layout.addWidget(self.word_label)
            main_layout.addSpacing(30)
            main_layout.addWidget(self.prev_btn)
            main_layout.addSpacing(0)
            main_layout.addWidget(self.nex_btn)
            main_layout.addSpacing(28)
            main_layout.addWidget(self.search_bar)
            main_layout.addStretch(20)
            main_layout.addWidget(self.upload_btn)
            main_layout.addSpacing(18)
            main_layout.addWidget(self.message_btn)
            main_layout.addSpacing(18)
            main_layout.addWidget(self.download_btn)
            main_layout.addSpacing(20)
            main_layout.addWidget(self.profile_page_btn)
            main_layout.addSpacing(8)
            main_layout.addWidget(self.profile_btn)

            all_layout.addLayout(self.extra_layout)
            all_layout.addLayout(self.main_layout)

            self.setLayout(self.all_layout)

        set_layout()

        load_stylesheet(self, "headertest.qss")

    def login(self):
        self.login_dialog = Header.LoginDialog(self)
        print("")

    # drag support
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.parent.m_DragPosition = event.globalPos() - self.parent.pos()
            self.parent.m_drag = True
            event.accept()


    def mouseMoveEvent(self, event):
        try:
            if Qt.LeftButton and event.buttons():
                self.parent.move(event.globalPos()-self.parent.m_DragPosition)
                event.accept()

        except AttributeError:
            pass


    def mouseReleaseEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.m_drag = False


class MainWindow(QMainWindow):
    def __init__(self, reactor):
        super().__init__()
        self.reactor = reactor
        self.init_ui()


    def init_ui(self):
        # overall window settings
        self.setWindowTitle('CPChain Wallet')
        self.setObjectName("main_window")
        # no borders.  we make our own header panel.
        #self.setWindowFlags(Qt.FramelessWindowHint)

        def set_geometry():
            self.resize(1002, 710)  # resize before centering.
            self.setMinimumSize(800, 500)
            center_pt = QDesktopWidget().availableGeometry().center()
            qrect = self.frameGeometry()
            qrect.moveCenter(center_pt)
            self.move(qrect.topLeft())
        set_geometry()

        def add_content_tabs():
            self.content_tabs = content_tabs = QTabWidget(self)
            content_tabs.setObjectName("content_tabs")
            content_tabs.tabBar().hide()
            # Temporily modified for easy test by @hyiwr
            content_tabs.addTab(PopularTab(content_tabs), "")
            content_tabs.addTab(CloudTab(content_tabs), "")
            content_tabs.addTab(FollowingTab(content_tabs), "")
            content_tabs.addTab(SellTab(content_tabs), "")
            # content_tabs.addTab(ProductInfoEdit(content_tabs), "")
            #content_tabs.addTab(PurchasedDownloadedTab(content_tabs), "") 
            #content_tabs.addTab(PurchasedDownloadingTab(content_tabs), "") 
            content_tabs.addTab(PeferenceTab(content_tabs), "")
            content_tabs.addTab(PersonalInfoPage(content_tabs), "") 
            content_tabs.addTab(PurchasedTab(content_tabs), "")
            content_tabs.addTab(CollectedTab(content_tabs), "")
            print("Adding tabs(shopping cart tab, etc.) to content_tabs")
            print("Loading stylesheet to content_tabs")
        add_content_tabs()

        # add panes
        self.header = Header(self)
        self.sidebar = SideBar(self)


        # set layout
        def set_layout():
            self.main_layout = main_layout = QVBoxLayout()
            self.main_layout.setSpacing(0)
            self.main_layout.setContentsMargins(0, 0, 0, 0) 
            main_layout.addSpacing(0)
            main_layout.addWidget(self.header)

            self.content_layout = content_layout = QHBoxLayout()
            self.content_layout.setSpacing(0)
            self.content_layout.setContentsMargins(0, 0, 0, 0) 
            content_layout.addSpacing(0)
            content_layout.addWidget(self.sidebar)
            content_layout.addSpacing(0)
            content_layout.addWidget(self.content_tabs)

            self.main_layout.addLayout(self.content_layout)

            wid = QWidget(self)
            wid.setLayout(self.main_layout)
            self.setCentralWidget(wid)
        set_layout()
        load_stylesheet(self, "main_window.qss") 
        print("Seting stylesheet of MainWindow......")
          
        self.show()


    def closeEvent(self, event):
        self.reactor.stop()



def _handle_keyboard_interrupt():
    def sigint_handler(*args):
        QApplication.quit()

    import signal
    signal.signal(signal.SIGINT, sigint_handler)

    # cf. https://stackoverflow.com/a/4939113/855160
    from PyQt5.QtCore import QTimer

    # make it global, o.w. the timer will soon vanish.
    _handle_keyboard_interrupt.timer = QTimer()
    timer = _handle_keyboard_interrupt.timer
    timer.start(300) # run each 300ms
    timer.timeout.connect(lambda: None)


    
def initialize_system():
    def initialize_net():
        # Temporily modified for easy test by @hyiwr
        print("Initializing network......")
    initialize_net()
    
    def monitor_chain_event():
        # Temporily modified for easy test by @hyiwr
        print("Monitoring chain event......")
    monitor_chain_event()


def main():
    global main_wnd
    from twisted.internet import reactor
    main_wnd = MainWindow(reactor)
    _handle_keyboard_interrupt()

    initialize_system()
    
    sys.exit(reactor.run())


if __name__ == '__main__':
    main()