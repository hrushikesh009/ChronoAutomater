# AutoTimeSheetFiller

Automate the tedious task of filling out your time sheet effortlessly with this Python project. Using Selenium, the script interacts with the time sheet web interface, simplifying the entire process.

## Setup

1. **Clone the repository:**
   ```bash
   https://github.com/hrushikesh009/ChronoAutomater.git
   cd AutoTimeSheetFiller
   ```

2. **Installation:**
```bash 
pip install -r requirements.txt
```

3. **Configure your login credentials:**

* Create a file named login-credentials.ini with the following content:

```bash 
[Credentials]
#Your time sheet web page
LANDING_PAGE=https://google.com/

#Your email address used for login
USERNAME=abc.cbd@gmail.com

# Your one-time password for login
OTP=12345

# The specific workplace you need to log hours for (not case-sensitive, keep it as close as possible)
# quotes are not required
WORKPLACE=Client Name

# Your task list, separated by commas
TASKLIST=Refactoring LE CYC w.r.t to new Table Structure, 
```

4. **Download ChromeDriver**:

* Download ChromeDriver from https://chromedriver.chromium.org/downloads
* Check your Chrome browser version using chrome://version.
* Download the corresponding ChromeDriver version.
* Place the downloaded driver in a secure location.
* Set the path to ChromeDriver in constants.py:


```bash
# Add this in constants.py
CHROME_DRIVER_PATH = '/path/to/chromedriver'
```

5. **Run the script**

```bash
python main.py
```

# Features
* Automatic login to your time sheet.
* Seamless switching between different workspaces or projects.
* Effortless submission of time blocks.
* Feel free to customize and extend the script according to your specific time sheet requirements.

Enjoy the automation journey!