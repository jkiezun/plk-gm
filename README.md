# PLK GM

Fantasy league for Polish Basketlball League (PLK).  
UNDER DEVELOPMENT

## Getting Started

Backed uses Python Django framework. Frontend uses pure Javascript. Most of the data is scraped from plk.pl website.

### Requirements

Django
Pandas
requests
BeautifulSoup
(Pandas, requests and BeautifulSoup are used to scrape and prepare the data)

### Running the app

    # Change into project directory
    cd plk_gm

    # Make virtual enviornment
    python3 -m venv plk_gm_env

    # Activate virtual env
    source plk_gm_env/bin/activate

    # Install requirements
    pip install -r requirements.txt

    # Start development server
    python manage.py runserver
