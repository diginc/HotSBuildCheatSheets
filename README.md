# Data

check the stats

# Running your self

You do not really need to run my script your self unless you're adding functionality (to pull request back hopefully) because the stats I commit into the repo should be up to date.

Also, many people running this script will cause unneeded strain on HotsLogs server, please do not run it without asking for permission to scrape the website your self first.

If you want a copy of the sqlite database where I store history of daily scraped data for tracking feel free to email adam@diginc.us

```
source venv/bin/activate ; pip install -r requirements.txt
python hotslogslogs.py
git diff wiki/
```
