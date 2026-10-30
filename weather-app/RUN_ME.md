# How to run (Windows)

1. Install Python 3.10+ from python.org (tick "Add Python to PATH").
2. Open Command Prompt INSIDE this folder (address bar -> type `cmd` -> Enter).
3. Run:

       python -m pip install --upgrade -r requirements.txt
       python -m streamlit run dashboard.py

4. Browser opens http://localhost:8501  ->  login: admin / weather@123

Common errors
- 'streamlit' is not recognized  -> use `python -m streamlit run dashboard.py`
- FileNotFoundError data/weather.csv -> you are not inside the weather-app folder
- TypeError ... width= / not a valid config option -> old Streamlit: run `python -m pip install --upgrade streamlit`

main.py (analysis script)
- Run:  python main.py   (from inside the weather-app folder)
- Charts open in windows AND are saved as PNG files in the `charts` folder.
