# go to python REPL
python manage.py shell

# import associated Models
from funds.models import Fund

# hold on fund, latest net price
[fnd.latest_fund_data() for fnd in Fund.objects.all()]

# refresh all Funds price
Fund.refresh_holdon_fund()


