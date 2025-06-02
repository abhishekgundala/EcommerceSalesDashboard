# E-commerce Analytics Dashboard 📊

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31.1-red.svg)
![Plotly](https://img.shields.io/badge/Plotly-5.18.0-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

An interactive, real-time analytics dashboard for e-commerce data visualization and analysis. Built with Streamlit and Plotly, this dashboard provides comprehensive insights into sales patterns, product performance, and customer behavior.

![Dashboard Preview](https://raw.githubusercontent.com/abhishekgundala/EcommerceSalesDashboard/main/preview.png)

## 🚀 Features

### Analytics & Visualization
- **Real-time Metrics Display**
  - Total Products Overview
  - Price Statistics (High/Low/Median)
  - Sales Performance Indicators

- **Interactive Charts**
  - Price Distribution Analysis
  - Top Brands Performance
  - Time Series Event Tracking
  - Category-wise Analysis

### User Experience
- **Dynamic Filtering**
  - Date Range Selection
  - Brand/Category Filters
  - Custom Data Views

- **Responsive Design**
  - Mobile-friendly Interface
  - Adaptive Layouts
  - Smooth Animations

## 🛠️ Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/abhishekgundala/EcommerceSalesDashboard.git
   cd EcommerceSalesDashboard
   ```

2. **Set Up Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Quick Start

1. **Prepare Your Data**
   - Place your CSV file in the project root
   - Ensure it follows the required data structure (see below)

2. **Run the Dashboard**
   ```bash
   streamlit run dashboard.py --server.port 4000
   ```

3. **Access the Dashboard**
   - Local: http://localhost:4000
   - Network: http://[your-ip]:4000

## 📊 Data Structure Requirements

Your CSV file should include these columns:
```
event_time    : Timestamp of the event
event_type    : Type of event (purchase, view, etc.)
product_id    : Unique identifier for products
category_code : Product category name
brand        : Product brand name
price        : Product price
user_id      : User identifier
user_session : Session identifier
```

## 🔧 Configuration

The dashboard is highly configurable through the UI:
- **Date Range**: Select custom date ranges for analysis
- **Visualization Options**: Customize chart types and metrics
- **Data Upload**: Support for new data files
- **Display Settings**: Adjust layout and appearance

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📬 Contact

Abhishek Gundala - [@abhishekgundala](https://github.com/abhishekgundala)

Project Link: [https://github.com/abhishekgundala/EcommerceSalesDashboard](https://github.com/abhishekgundala/EcommerceSalesDashboard) 