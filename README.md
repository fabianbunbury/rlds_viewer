# Visualize RLDS Datasets

# RLDS Viewer

An application designed to easily and quickly visualize RLDS datasets, making the growing database of open-source robotics data searchable and manageable.


## Features

- **User-Friendly Interface:** Built with Dash for a seamless user experience.

- **Python 3.6 or higher:** Ensure you have Python installed. You can download it from [python.org](https://www.python.org/downloads/).

### Setup

1. **Clone the Repository**
     ```bash
     git clone git@github.com:fabianbunbury/rlds_viewer.git
     ```
2. **Create Virtual Environment with Python 3.10 (Optional)**
     I'm sorry that you have to use 3.10.
     ```bash
     cd rlds_viewer
     python3.10 -m venv myvenv
     source myvenv/bin/activate 
     ```
3. **Install Requirements**
     ```bash
     pip install -r requirements.txt
     python app.py
     ```
4. **Use The GUI**
     Go to http://127.0.0.1:8050/. You can select various datasets and episodes. The data is downloaded from Google, so it can take some time to swap between datasets. You can use the mouse to drag left and right to see later states.

