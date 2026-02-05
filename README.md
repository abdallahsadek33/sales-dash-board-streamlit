# 📊 Sales Performance Dashboard - Tailspin Toys

An interactive sales analytics dashboard built with **Streamlit** and **Plotly** to analyze sales performance, revenue trends, and key business metrics for Tailspin Toys (2013-2016).

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0%2B-red)
![Plotly](https://img.shields.io/badge/Plotly-5.0%2B-brightgreen)

---

## 🎯 Project Overview

This dashboard provides comprehensive insights into sales data, enabling stakeholders to:
- Track revenue and profit trends over time
- Analyze performance by products, customers, territories, and salespeople
- Monitor key performance indicators (KPIs) in real-time
- Make data-driven business decisions

---

## ✨ Key Features

### 📈 **KPI Metrics**
- **Total Revenue**: Overall sales including tax
- **Total Profit**: Net profit from sales
- **Profit Margin**: Percentage margin calculation
- **Order Count**: Total number of orders
- **Average Order Value**: Mean transaction value

### 📊 **Interactive Visualizations**
- **Revenue & Profit Trends**: Monthly time-series analysis with dual-axis charts
- **Top 10 Products**: Best-selling items by revenue
- **Sales by Territory**: Geographic distribution of sales
- **Top 10 Customers**: Highest-value customer analysis
- **Top 10 Salespeople**: Performance tracking for sales team
- **Sales by State**: Top 15 states ranked by revenue with profit margin indicators

### 🔍 **Dynamic Filters**
- Filter by **Year** (2013-2016)
- Filter by **Quarter** (Q1, Q2, Q3, Q4)
- Filter by **Sales Territory**

### 📋 **Data Exploration**
- View detailed transaction data in expandable tables
- Export and analyze up to 100 recent transactions

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| **Python** | Core programming language |
| **Streamlit** | Web app framework for data dashboards |
| **Pandas** | Data manipulation and analysis |
| **Plotly** | Interactive visualizations and charts |
| **Plotly Express** | High-level plotting interface |

---

## 📁 Data Sources

The dashboard integrates multiple data sources:

| File | Description |
|------|-------------|
| `FactSale.csv` | Sales transactions (invoices, quantities, prices, profits) |
| `DimCustomer.csv` | Customer dimension table |
| `DimCity.csv` | City and territory information |
| `DimStockItem.csv` | Product/stock item details |
| `DimEmployee.xlsx` | Employee and salesperson data |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/abdallahsadek33/sales-dash-board-streamlit.git
cd sales-dash-board-streamlit
```

2. **Install required packages**
```bash
pip install streamlit pandas plotly openpyxl
```

3. **Run the dashboard**
```bash
streamlit run dashboard_FIXED_FINAL.py
```

4. **Open in browser**
The dashboard will automatically open at `http://localhost:8501`

---

## 📊 Dashboard Preview

### Main Features:
- **5 Key Metrics** displayed at the top
- **8 Interactive Charts** organized in rows
- **Responsive Layout** with wide-screen optimization
- **Professional Styling** with custom CSS theme

---

## 💡 Usage Tips

1. **Use the sidebar filters** to narrow down data by year, quarter, or territory
2. **Hover over charts** to see detailed tooltips
3. **Click on the "View Transactions" expander** to explore raw data
4. **Select multiple filters** to perform comparative analysis

---

## 🎨 Color Scheme

The dashboard uses a professional blue-and-green color palette:
- Primary: `#004B87` (Dark Blue)
- Accent: `#00A3E0` (Bright Blue)
- Success: `#28A745` (Green)
- Warning: `#FFA500` (Orange)

---

## 📈 Key Insights

This dashboard helps answer critical business questions:
- Which products generate the most revenue?
- What are the monthly revenue and profit trends?
- Which territories and states perform best?
- Who are the top-performing salespeople?
- Which customers contribute the most to revenue?

---

## 🔧 Customization

To adapt this dashboard for your own data:
1. Replace the CSV/Excel files with your datasets
2. Update column names in the code to match your schema
3. Modify the KPI calculations based on your business metrics
4. Adjust filters and visualizations as needed

---

## 📝 License

This project is open-source and available for educational and commercial use.

---

## 👤 Author

**Abdallah Sadek**

- GitHub: [@abdallahsadek33](https://github.com/abdallahsadek33)

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/abdallahsadek33/sales-dash-board-streamlit/issues).

---

## ⭐ Show Your Support

If you found this project helpful, please give it a **⭐ star** on GitHub!

---

**Built with ❤️ using Streamlit and Plotly**
