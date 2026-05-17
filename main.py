# Nama  : Juan Jordan Anugrah
# NIM   : F1D02310061
# Kelas : D

import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QLabel, QPushButton, QTableWidget, 
                               QTableWidgetItem, QHeaderView, QComboBox, QFrame,
                               QMessageBox, QFileDialog)
from PySide6.QtCore import Qt

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig.patch.set_facecolor('#f5f6fa')
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)

class DashboardApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Supermarket Sales Dashboard - Data Visualization")
        self.resize(1100, 700)
        self.setStyleSheet("""
            QMainWindow, QDialog, QMessageBox {
                background-color: #f5f6fa;
            }
            QWidget {
                color: #2f3542; 
            }
            QTableWidget {
                background-color: white;
                color: black;
                gridline-color: #ced6e0;
            }
            QHeaderView::section {
                background-color: #dfe4ea;
                color: black;
                font-weight: bold;
                border: 1px solid #ced6e0;
                padding: 4px;
            }
            QComboBox {
                background-color: white;
                color: black;
                border: 1px solid #ced6e0;
                border-radius: 4px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: black;
                selection-background-color: #3498db;
                selection-color: white;
            }
        """)

        self.file_path = 'supermarket_sales.csv'
        self.ensure_dataset_exists()
        
        self.load_data()
        self.setup_ui()
        self.update_dashboard()

    def ensure_dataset_exists(self):
        if not os.path.exists(self.file_path):
            dummy_data = """Invoice ID,Branch,City,Customer type,Gender,Product line,Unit price,Quantity,Tax 5%,Total,Date,Time,Payment,cogs,gross margin percentage,gross income,Rating
101,A,Yangon,Member,Female,Health and beauty,74.69,7,26.14,548.97,1/5/2019,13:08,Ewallet,522.83,4.76,26.14,9.1
102,C,Naypyitaw,Normal,Female,Electronic accessories,15.28,5,3.82,80.22,3/8/2019,10:29,Cash,76.4,4.76,3.82,9.6
103,A,Yangon,Normal,Male,Home and lifestyle,46.33,7,16.21,340.52,3/3/2019,13:23,Credit card,324.31,4.76,16.21,7.4
104,A,Yangon,Member,Male,Health and beauty,58.22,8,23.28,489.04,1/27/2019,20:33,Ewallet,465.76,4.76,23.28,8.4
105,A,Yangon,Normal,Male,Sports and travel,86.31,7,30.20,634.43,2/8/2019,10:46,Ewallet,604.17,4.76,30.20,5.3
106,C,Naypyitaw,Normal,Female,Electronic accessories,73.56,3,11.03,231.71,2/25/2019,13:19,Ewallet,220.68,4.76,11.03,4.1
107,B,Mandalay,Member,Female,Fashion accessories,54.84,3,8.22,172.74,2/24/2019,16:05,Ewallet,164.52,4.76,8.22,5.8
108,B,Mandalay,Normal,Female,Health and beauty,73.11,5,18.27,383.82,2/26/2019,9:12,Cash,365.55,4.76,18.27,5.2
109,A,Yangon,Member,Female,Electronic accessories,86.04,5,21.51,451.71,3/2/2019,14:05,Credit card,430.2,4.76,21.51,6.8
110,C,Naypyitaw,Normal,Male,Health and beauty,54.40,6,16.32,342.72,2/20/2019,14:21,Cash,326.4,4.76,16.32,9.6
111,B,Mandalay,Member,Male,Sports and travel,52.59,8,21.03,441.75,2/20/2019,11:12,Ewallet,420.72,4.76,21.03,5.9
112,A,Yangon,Normal,Female,Food and beverages,22.86,6,6.85,144.01,2/26/2019,12:21,Credit card,137.16,4.76,6.85,7.4
113,C,Naypyitaw,Normal,Female,Fashion accessories,61.42,7,21.49,451.48,1/3/2019,10:29,Ewallet,429.94,4.76,21.49,9.4
114,A,Yangon,Normal,Male,Home and lifestyle,22.35,5,5.58,117.33,1/31/2019,13:19,Cash,111.75,4.76,5.58,4.3
115,A,Yangon,Normal,Female,Sports and travel,71.38,6,21.41,449.69,3/27/2019,10:46,Cash,428.28,4.76,21.41,9.0
116,B,Mandalay,Member,Female,Health and beauty,43.19,5,10.79,226.74,1/16/2019,14:05,Ewallet,215.95,4.76,10.79,8.4
117,C,Naypyitaw,Normal,Male,Home and lifestyle,93.72,7,32.80,688.84,1/15/2019,16:05,Credit card,656.04,4.76,32.80,6.1
118,B,Mandalay,Member,Male,Electronic accessories,46.12,4,9.22,193.70,3/22/2019,20:33,Ewallet,184.48,4.76,9.22,4.8
119,A,Yangon,Normal,Female,Fashion accessories,83.91,5,20.97,440.52,2/15/2019,11:12,Cash,419.55,4.76,20.97,7.2
120,A,Yangon,Member,Male,Food and beverages,29.33,7,10.26,215.57,3/12/2019,13:08,Credit card,205.31,4.76,10.26,8.1
121,C,Naypyitaw,Normal,Female,Health and beauty,75.12,3,11.26,236.62,1/21/2019,10:29,Ewallet,225.36,4.76,11.26,9.0
122,B,Mandalay,Member,Male,Sports and travel,50.21,6,15.06,316.32,2/14/2019,13:19,Cash,301.26,4.76,15.06,7.5
123,B,Mandalay,Normal,Female,Fashion accessories,95.66,4,19.13,401.77,3/5/2019,10:46,Ewallet,382.64,4.76,19.13,8.2
124,A,Yangon,Normal,Male,Electronic accessories,30.55,8,12.22,256.62,2/10/2019,16:05,Cash,244.4,4.76,12.22,6.3
125,C,Naypyitaw,Member,Female,Food and beverages,81.23,5,20.30,426.45,1/11/2019,14:05,Credit card,406.15,4.76,20.30,5.4
126,A,Yangon,Member,Male,Home and lifestyle,45.67,6,13.70,287.72,3/20/2019,11:12,Ewallet,274.02,4.76,13.70,9.1
127,C,Naypyitaw,Normal,Male,Sports and travel,60.88,7,21.30,447.46,2/28/2019,20:33,Cash,426.16,4.76,21.30,4.9
128,B,Mandalay,Normal,Female,Health and beauty,33.45,4,6.69,140.49,1/25/2019,13:08,Credit card,133.8,4.76,6.69,8.5
129,A,Yangon,Member,Female,Electronic accessories,88.99,3,13.34,280.31,2/18/2019,13:19,Ewallet,266.97,4.76,13.34,7.8
130,B,Mandalay,Normal,Male,Fashion accessories,76.54,5,19.13,401.83,3/10/2019,10:46,Cash,382.7,4.76,19.13,6.2
131,A,Yangon,Normal,Female,Food and beverages,40.12,6,12.03,252.75,1/8/2019,14:05,Credit card,240.72,4.76,12.03,9.5
132,C,Naypyitaw,Member,Male,Home and lifestyle,92.34,4,18.46,387.82,2/5/2019,16:05,Ewallet,369.36,4.76,18.46,5.1
133,B,Mandalay,Member,Female,Sports and travel,55.67,7,19.48,409.16,3/18/2019,11:12,Cash,389.69,4.76,19.48,8.8
134,A,Yangon,Normal,Male,Health and beauty,67.89,5,16.97,356.42,1/12/2019,20:33,Ewallet,339.45,4.76,16.97,4.2
135,C,Naypyitaw,Member,Female,Electronic accessories,49.50,8,19.80,415.80,2/22/2019,13:08,Credit card,396.0,4.76,19.80,7.3
136,A,Yangon,Normal,Female,Fashion accessories,84.56,3,12.68,266.36,3/25/2019,13:19,Cash,253.68,4.76,12.68,9.2
137,B,Mandalay,Normal,Male,Food and beverages,38.76,6,11.62,244.18,1/30/2019,10:46,Ewallet,232.56,4.76,11.62,5.6
138,C,Naypyitaw,Member,Male,Home and lifestyle,79.12,5,19.78,415.38,2/12/2019,14:05,Cash,395.6,4.76,19.78,8.9
139,A,Yangon,Member,Female,Sports and travel,62.45,4,12.49,262.29,3/8/2019,16:05,Credit card,249.8,4.76,12.49,4.5
140,B,Mandalay,Normal,Male,Health and beauty,51.23,7,17.93,376.54,1/18/2019,11:12,Ewallet,358.61,4.76,17.93,7.9
141,A,Yangon,Normal,Female,Electronic accessories,90.45,3,13.56,284.91,2/2/2019,20:33,Cash,271.35,4.76,13.56,9.8
142,C,Naypyitaw,Member,Male,Fashion accessories,44.67,6,13.40,281.42,3/15/2019,13:08,Ewallet,268.02,4.76,13.40,5.2
143,B,Mandalay,Normal,Female,Food and beverages,88.12,4,17.62,370.10,1/22/2019,13:19,Credit card,352.48,4.76,17.62,8.4
144,A,Yangon,Member,Male,Home and lifestyle,35.89,8,14.35,301.47,2/20/2019,10:46,Cash,287.12,4.76,14.35,4.7
145,C,Naypyitaw,Member,Female,Sports and travel,73.56,5,18.39,386.19,3/28/2019,14:05,Ewallet,367.8,4.76,18.39,9.3
146,B,Mandalay,Normal,Male,Health and beauty,59.34,6,17.80,373.84,1/5/2019,16:05,Cash,356.04,4.76,17.80,6.5
147,A,Yangon,Normal,Female,Electronic accessories,82.45,4,16.49,346.29,2/14/2019,11:12,Credit card,329.8,4.76,16.49,8.1
148,C,Naypyitaw,Member,Male,Fashion accessories,47.89,7,16.76,351.99,3/10/2019,20:33,Ewallet,335.23,4.76,16.76,5.8
149,B,Mandalay,Member,Female,Food and beverages,96.23,3,14.43,303.12,1/15/2019,13:08,Cash,288.69,4.76,14.43,9.7
150,A,Yangon,Normal,Male,Home and lifestyle,31.45,5,7.86,165.11,2/25/2019,13:19,Ewallet,157.25,4.76,7.86,4.1
"""
            with open(self.file_path, 'w') as f:
                f.write(dummy_data.strip())

    def load_data(self):
        try:
            self.df_full = pd.read_csv(self.file_path)
            self.df_filtered = self.df_full.copy()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal memuat dataset: {str(e)}")
            self.df_full = pd.DataFrame()
            self.df_filtered = pd.DataFrame()

    def setup_ui(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        header_layout = QHBoxLayout()
        title_label = QLabel("📊 Supermarket Sales Dashboard")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2f3542;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        self.cb_branch = QComboBox()
        self.cb_branch.addItem("All Branches")
        if not self.df_full.empty:
            self.cb_branch.addItems(sorted(self.df_full['Branch'].unique()))
        self.cb_branch.currentTextChanged.connect(self.apply_filter)
        self.cb_branch.setStyleSheet("padding: 5px; font-size: 14px;")

        self.cb_product = QComboBox()
        self.cb_product.addItem("All Products")
        if not self.df_full.empty:
            self.cb_product.addItems(sorted(self.df_full['Product line'].unique()))
        self.cb_product.currentTextChanged.connect(self.apply_filter)
        self.cb_product.setStyleSheet("padding: 5px; font-size: 14px;")

        btn_refresh = QPushButton("🔄 Refresh Data")
        btn_refresh.clicked.connect(self.refresh_data)
        btn_refresh.setStyleSheet("padding: 5px 15px; font-size: 14px; background-color: #3498db; color: white; border-radius: 4px;")

        btn_export = QPushButton("💾 Export Charts")
        btn_export.clicked.connect(self.export_charts)
        btn_export.setStyleSheet("padding: 5px 15px; font-size: 14px; background-color: #2ecc71; color: white; border-radius: 4px;")

        header_layout.addWidget(QLabel("Filter Branch:"))
        header_layout.addWidget(self.cb_branch)
        header_layout.addWidget(QLabel(" Filter Product:"))
        header_layout.addWidget(self.cb_product)
        header_layout.addWidget(btn_refresh)
        header_layout.addWidget(btn_export)
        main_layout.addLayout(header_layout)

        summary_layout = QHBoxLayout()
        
        card_sales, self.lbl_total_sales = self.create_summary_card("Total Penjualan", "$0.00", "#ff4757")
        card_trx, self.lbl_total_trx = self.create_summary_card("Total Transaksi", "0", "#ffa502")
        card_rating, self.lbl_avg_rating = self.create_summary_card("Rata-rata Rating", "0.0", "#2ed573")
        
        summary_layout.addWidget(card_sales)
        summary_layout.addWidget(card_trx)
        summary_layout.addWidget(card_rating)
        main_layout.addLayout(summary_layout)

        chart_layout = QHBoxLayout()
        self.canvas_bar = MplCanvas(self, width=5, height=4, dpi=100)
        self.canvas_pie = MplCanvas(self, width=5, height=4, dpi=100)
        chart_layout.addWidget(self.canvas_bar)
        chart_layout.addWidget(self.canvas_pie)
        main_layout.addLayout(chart_layout, stretch=2)

        self.table = QTableWidget()
        self.table.setStyleSheet("background-color: white; border: 1px solid #ced6e0; border-radius: 5px;")
        main_layout.addWidget(self.table, stretch=1)

        self.setCentralWidget(main_widget)

    def create_summary_card(self, title, value, color):
        card = QFrame()
        card.setStyleSheet(f"background-color: white; border-top: 4px solid {color}; border-radius: 5px; padding: 10px;")
        layout = QVBoxLayout(card)
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("color: #747d8c; font-size: 14px; font-weight: bold;")
        lbl_val = QLabel(value)
        lbl_val.setStyleSheet("color: #2f3542; font-size: 22px; font-weight: bold;")
        layout.addWidget(lbl_title)
        layout.addWidget(lbl_val)
        
        return card, lbl_val

    def apply_filter(self):
        branch = self.cb_branch.currentText()
        product = self.cb_product.currentText()
        
        self.df_filtered = self.df_full.copy()
        
        if branch != "All Branches":
            self.df_filtered = self.df_filtered[self.df_filtered['Branch'] == branch]
        if product != "All Products":
            self.df_filtered = self.df_filtered[self.df_filtered['Product line'] == product]
            
        self.update_dashboard()

    def refresh_data(self):
        self.load_data()
        self.cb_branch.setCurrentIndex(0)
        self.cb_product.setCurrentIndex(0)
        self.update_dashboard()

    def update_dashboard(self):
        if self.df_filtered.empty:
            return

        total_sales = self.df_filtered['Total'].sum()
        total_trx = len(self.df_filtered)
        avg_rating = self.df_filtered['Rating'].mean()

        self.lbl_total_sales.setText(f"${total_sales:,.2f}")
        self.lbl_total_trx.setText(f"{total_trx}")
        self.lbl_avg_rating.setText(f"{avg_rating:.1f} / 10")

        self.canvas_bar.axes.cla()
        sales_by_product = self.df_filtered.groupby('Product line')['Total'].sum().sort_values()
        bars = self.canvas_bar.axes.barh(sales_by_product.index, sales_by_product.values, color='#3742fa')
        self.canvas_bar.axes.set_title('Total Penjualan per Kategori Produk', fontsize=12, fontweight='bold')
        self.canvas_bar.axes.set_xlabel('Total Penjualan ($)')
        self.canvas_bar.fig.tight_layout()
        self.canvas_bar.draw()

        self.canvas_pie.axes.cla()
        customer_dist = self.df_filtered['Customer type'].value_counts()
        self.canvas_pie.axes.pie(customer_dist.values, labels=customer_dist.index, autopct='%1.1f%%', 
                                 startangle=90, colors=['#ffa502', '#2ed573'])
        self.canvas_pie.axes.set_title('Distribusi Tipe Pelanggan', fontsize=12, fontweight='bold')
        self.canvas_pie.fig.tight_layout()
        self.canvas_pie.draw()

        self.table.clear()
        cols = ['Invoice ID', 'Branch', 'Product line', 'Unit price', 'Quantity', 'Total', 'Payment', 'Rating']
        df_table = self.df_filtered[cols]
        
        self.table.setColumnCount(len(cols))
        self.table.setRowCount(len(df_table))
        self.table.setHorizontalHeaderLabels(cols)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for row_idx, row_data in enumerate(df_table.values):
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_idx, col_idx, item)

    def export_charts(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Simpan Bar Chart", "bar_chart.png", "PNG Files (*.png)")
        if file_name:
            self.canvas_bar.fig.savefig(file_name)
            
            pie_file_name = file_name.replace(".png", "_pie.png")
            self.canvas_pie.fig.savefig(pie_file_name)
            QMessageBox.information(self, "Sukses", f"Chart berhasil diexport ke:\n{file_name}\ndan\n{pie_file_name}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DashboardApp()
    window.show()
    sys.exit(app.exec())