hshsjsisisshshsaaa  a# AI Expense Tracker 💰asssssssssss
aaaaaaaa wowwo cool

A professional desktop application for tracking income and expshsbsbshshshsheshshshhshshshsshushssjjshsenses with AI-powered spending hsshhshseadwaadhshshhshshsanalysis, beautiful UI, and comprehensive reporting features.aaaaaaaa
  aa
## Features ✨    aa  aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
     aaahshsjshshsjsewqeqeq
- **User Authentication**: Secure login system with password hashingaaaa
- **AI-Powered Analysis**: Google Generative AI integration for spending insights 
- **Beautiful UI**: Modern CustomTkinter interface with dark mode supportaadad
- **Charts & Reports**: Visual representations of spending patterns
- **Export Options**: PDF and Excel export functionality     
- **Budget Management**: Set and track budget limits adada
- **Notifications**: Real-time alerts for budget thresholdsaaa
- **Database**: SQLite with SQLAlchemy ORMqadda
- **Backup & Recovery**: Automatic backup and recovery featuresadadada
- **Search & Filter**: Advanced filtering and sorting capabilitiesaaaaaaaaaaaaaa
- **Responsive Design**: Professional layout with animationsaadadaddada
 
## System Requirements

- **Python**: 3.12 or higher
- **OS**: Windows, macOS, or Linux
- **RAM**: Minimum 2GB
- **Disk Space**: Minimum 500MB

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/arpan085/ai-expense-tracker.git
cd ai-expense-tracker
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create Environment File
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```
GOOGLE_API_KEY=your_google_generative_ai_key
DATABASE_PATH=data/expenses.db
LOG_LEVEL=INFO
```

### 5. Initialize Database
```bash
python app/database.py
```

### 6. Run the Application
```bash
python main.py
```

## Project Structure

```
ai-expense-tracker/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── auth.py
│   ├── logger.py
│   ├── exceptions.py
│   ├── security.py
│   ├── validators.py
│   ├── services/
│   ├── ui/
│   └── utils/
├── tests/
├── data/
├── logs/
├── backup/
├── docs/
├── main.py
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```
aaaa
## Usage

### Starting the Application
```bash
python main.py
```

### First Time Setup
1. Click "Register" to create a new account
2. Enter username and password
3. Click "Sign Up"
4. Login with your credentials
5. Start tracking expenses!

## Configuration

Edit `.env` file to customize settings like database path, API keys, and UI preferences.

## Testing

```bash
pytest
```
dadaaaaaaaaaaaaaaaaaaaaaa
## License

MIT License - See [LICENSE](LICENSE) file for details.

## Author

**Arpan** - Senior Python Software Engineer

---

**Happy Tracking! 💼📊**
