import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
                             QStackedWidget, QGridLayout, QFrame, QSizePolicy, QTextEdit, QRadioButton, QButtonGroup,
                             QFileDialog, QComboBox)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class FunctionWidget(QFrame):
    def __init__(self, title, description, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        
        self.button = QPushButton(title)
        self.button.setStyleSheet("""
            font-size: 18px;
            padding: 10px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
        """)
        
        self.description = QLabel(description)
        self.description.setWordWrap(True)
        self.description.setStyleSheet("font-size: 14px; margin-top: 10px;")
        
        layout.addWidget(self.button)
        layout.addWidget(self.description)
        
        self.setLayout(layout)
        self.setFrameShape(QFrame.Shape.Box)
        self.setStyleSheet("""
            FunctionWidget {
                border: 2px solid #ddd;
                border-radius: 10px;
                background-color: #f9f9f9;
                padding: 15px;
            }
        """)
        
        # 设置大小策略为扩展
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
    def mousePressEvent(self, event):
        self.button.click()
        super().mousePressEvent(event)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("古籍处理工具")
        self.setGeometry(100, 100, 1200, 800)

        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        nav_layout = QHBoxLayout()
        nav_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.home_button = QPushButton("首页")
        self.func1_button = QPushButton("如是OCR")
        self.func2_button = QPushButton("智能标点")
        self.func3_button = QPushButton("标点迁移")
        self.func4_button = QPushButton("多文本比对")

        for button in [self.home_button, self.func1_button, self.func2_button, self.func3_button, self.func4_button]:
            button.setStyleSheet("""
                QPushButton {
                    font-size: 14px;
                    padding: 5px 10px;
                    background-color: #008CBA;
                    color: white;
                    border: none;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #005f7f;
                }
            """)
            nav_layout.addWidget(button)

        self.stacked_widget = QStackedWidget()
        self.home_page = self.create_home_page()
        self.func1_page = self.create_ocr_page()
        self.func2_page = self.create_punctuation_page()
        self.func3_page = self.create_migration_page()
        self.func4_page = self.create_comparison_page()

        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.func1_page)
        self.stacked_widget.addWidget(self.func2_page)
        self.stacked_widget.addWidget(self.func3_page)
        self.stacked_widget.addWidget(self.func4_page)

        main_layout.addLayout(nav_layout)
        main_layout.addWidget(self.stacked_widget)

        self.home_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.home_page))
        self.func1_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.func1_page))
        self.func2_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.func2_page))
        self.func3_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.func3_page))
        self.func4_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.func4_page))

    def create_home_page(self):
        page = QWidget()
        main_layout = QVBoxLayout()

        title = QLabel("欢迎使用古籍处理工具")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("SimHei", 24))
        title.setStyleSheet("margin-bottom: 20px;")
        main_layout.addWidget(title)

        # 创建一个水平布局来包含功能分区和左右空白
        h_layout = QHBoxLayout()
        h_layout.addStretch(1)  # 左侧空白

        functions_layout = QGridLayout()
        functions_layout.setSpacing(50)  # 增加小部件之间的间距
        functions = [
            ("如是OCR", """您可以上传古籍图片到系统，系统将调用人工智能古籍OCR引擎对图片进行文字识别，然后您可以对识别结果进行文字校对。
系统提供"按列校对"和"按页校对"两种校对方式。如果发现有字符检测（漏框、多框或者切错）或者字序的问题，则可以在"切分校对"页面对字框和字序进行修改。
用户上传的所有图片，都可以在"我的图片"中进行管理。"""),
            ("智能标点", """您可以提交古籍文本到系统，系统将调用人工智能自动标点引擎对文本进行标点，然后您可以对标点结果进行修改、保存和复制导出。
系统提供"现代标点"和"句读"两种标点方式。用户保存的所有文本，都可以在"我的标点"中进行管理。"""),
            ("标点迁移", """古籍标点时，常常需要用到或参考他人已有的标点成果。由于他人标点所用的文本跟我们整理的文本之间不尽相同，无法直接使用他人的带标点的文本，
而是需要将标点迁移至我们的文本中，即"标点迁移"。标点迁移指的是针对两份相似文本一份有标点一份没有标点时，将标点符号从一份文本迁移至另一份文本的过程。
用户可以通过本功能自动完成标点迁移，然后将迁移的结果复制导出。"""),
            ("多文本比对", """古籍整理中，常会需要对多份相似文本进行比对，找出其中的差异。比如，多版本校勘时，需要比对多份文本的差异，进而形成校勘记。
再如，同本异译的多份文本之间，也需要比对多份文本差异，以便进一步研究。一般的文本比对技术，仅仅能针对两份文本进行比对，本功能则可以对多份的相似文本进行同时比对。""")
        ]

        for i, (title, description) in enumerate(functions):
            func_widget = FunctionWidget(title, description)
            func_widget.button.clicked.connect(lambda checked, index=i+1: self.stacked_widget.setCurrentIndex(index))
            functions_layout.addWidget(func_widget, i // 2, i % 2)

        # 将功能分区布局添加到水平布局中
        h_layout.addLayout(functions_layout)
        h_layout.addStretch(1)  # 右侧空白

        # 将水平布局添加到主布局
        main_layout.addLayout(h_layout)
        main_layout.addStretch(1)  # 底部空白

        page.setLayout(main_layout)
        return page
    
    def create_ocr_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        title = QLabel("如是OCR")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("SimHei", 20))
        layout.addWidget(title)

        # 添加间距
        layout.addSpacing(20)

        # 上传选项
        upload_options = QHBoxLayout()
        single_upload = QRadioButton("单页上传")
        batch_upload = QRadioButton("批量上传")
        upload_group = QButtonGroup()
        upload_group.addButton(single_upload)
        upload_group.addButton(batch_upload)
        upload_options.addWidget(single_upload)
        upload_options.addWidget(batch_upload)
        layout.addLayout(upload_options)

        # 添加间距
        layout.addSpacing(20)

        # 第一步：文件选择
        step1_label = QLabel("第一步：选择文件")
        step1_label.setFont(QFont("SimHei", 16))
        layout.addWidget(step1_label)

        file_info = QLabel("请选择单页图片，大小不超过2MB，单字像素在45px以上，支持jpg、png、tiff、gif等格式，不支持黑底白字")
        file_info.setWordWrap(True)
        layout.addWidget(file_info)

        select_file_button = QPushButton("选择文件")
        layout.addWidget(select_file_button)

        # 添加间距
        layout.addSpacing(20)

        # 第二步：版面选择
        step2_label = QLabel("第二步：选择版面")
        step2_label.setFont(QFont("SimHei", 16))
        layout.addWidget(step2_label)

        layout_options = QHBoxLayout()
        single_column = QRadioButton("单栏")
        double_column = QRadioButton("上下两栏")
        triple_column = QRadioButton("上下三栏")
        layout_group = QButtonGroup()
        layout_group.addButton(single_column)
        layout_group.addButton(double_column)
        layout_group.addButton(triple_column)
        layout_options.addWidget(single_column)
        layout_options.addWidget(double_column)
        layout_options.addWidget(triple_column)
        layout.addLayout(layout_options)

        # 添加弹性空间
        layout.addStretch(1)

        page.setLayout(layout)
        return page

    def create_punctuation_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        title = QLabel("智能标点")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("SimHei", 20))
        layout.addWidget(title)

        # 添加间距
        layout.addSpacing(20)

        text_edit = QTextEdit()
        text_edit.setMinimumHeight(400)  # 设置最小高度
        layout.addWidget(text_edit)

        # 添加间距
        layout.addSpacing(20)

        punctuate_button = QPushButton("进行标点")
        punctuate_button.setMinimumWidth(200)  # 设置最小宽度
        punctuate_button.setStyleSheet("font-size: 16px; padding: 10px;")  # 设置样式
        layout.addWidget(punctuate_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # 添加弹性空间
        layout.addStretch(1)

        page.setLayout(layout)
        return page

    def create_migration_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        title = QLabel("标点迁移")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("SimHei", 20))
        layout.addWidget(title)

        # Navigation buttons
        nav_buttons = QHBoxLayout()
        nav_buttons.setAlignment(Qt.AlignmentFlag.AlignRight)
        for button_text in ["加载示例", "清除标点", "进行迁移", "复制结果"]:
            button = QPushButton(button_text)
            nav_buttons.addWidget(button)
        layout.addLayout(nav_buttons)

        # Text areas
        text_areas = QHBoxLayout()
        source_text = QTextEdit()
        target_text = QTextEdit()
        source_label = QLabel("来源文本")
        target_label = QLabel("目标文本")
        
        source_layout = QVBoxLayout()
        source_layout.addWidget(source_label)
        source_layout.addWidget(source_text)
        
        target_layout = QVBoxLayout()
        target_layout.addWidget(target_label)
        target_layout.addWidget(target_text)
        
        text_areas.addLayout(source_layout)
        text_areas.addLayout(target_layout)
        layout.addLayout(text_areas)

        page.setLayout(layout)
        return page

    def create_comparison_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        title = QLabel("多文本比对")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("SimHei", 20))
        layout.addWidget(title)

        # Navigation buttons
        nav_buttons = QHBoxLayout()
        nav_buttons.setAlignment(Qt.AlignmentFlag.AlignRight)
        for button_text in ["加载示例", "清除标点", "进行对比", "复制结果"]:
            button = QPushButton(button_text)
            nav_buttons.addWidget(button)
        layout.addLayout(nav_buttons)

        # Text areas
        text_areas = QHBoxLayout()
        
        # Left text area with combo box
        left_layout = QVBoxLayout()
        text_selector = QComboBox()
        text_selector.addItems(["底本"] + [f"文本{i}" for i in range(1, 10)])
        left_layout.addWidget(text_selector)
        left_text = QTextEdit()
        left_layout.addWidget(left_text)
        
        # Right text area
        right_layout = QVBoxLayout()
        right_label = QLabel("目标文本")
        right_layout.addWidget(right_label)
        right_text = QTextEdit()
        right_layout.addWidget(right_text)
        
        text_areas.addLayout(left_layout)
        text_areas.addLayout(right_layout)
        layout.addLayout(text_areas)

        page.setLayout(layout)
        return page

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())