# E-commerce Analytics Dashboard

An interactive dashboard for visualizing e-commerce data, built with Streamlit and Plotly.

## Features

- Interactive date range selection
- Key metrics display (Total Products, Price Statistics)
- Price distribution visualization
- Top brands analysis
- Event type trends over time
- Category-wise price analysis
- Data summary and raw data viewer
- Support for uploading new monthly data

## Installation

1. Install the required packages:
```bash
pip install -r requirements.txt
```

2. Run the dashboard:
```bash
streamlit run dashboard.py
```

## Usage

1. The dashboard will automatically load the default dataset (2019-Oct.csv) if present
2. To analyze different months:
   - Use the file upload feature in the dashboard
   - Upload any CSV file with the same structure as the original dataset
3. Use the date range selector in the sidebar to filter data
4. Interact with the visualizations:
   - Hover over charts for detailed information
   - Click and drag to zoom
   - Double-click to reset the view

## Data Format Requirements

The CSV file should contain the following columns:
- event_time
- event_type
- product_id
- category_id
- category_code
- brand
- price
- user_id
- user_session

## Contributing

Feel free to submit issues and enhancement requests! 