How to Install/Run

1. Have Python 3 installed
    - For Linux, sudo apt-get install python3 python3-dev python3-venv
    - For Windows, download and install from Python's website
2. Create a virtual environment
    - python3 -m venv venv
3. Activate the venv
    - Linux - source venv/bin/activate
    - Windows - venv/Scripts/Activate
4. Download dependencies
    - Linux - pip install -r requirements-linux.txt
    - Windows - pip install -r requirements-windows.txt
    - If you can't install via requirements, there are only a couple dependencies
       -  pip install colorama
       -  (FOR LINUX ONLY) pip install getch
5. Run scoundrel.py
    - python3 scoundrel.py
