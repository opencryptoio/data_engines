
import dateparser
from datetime import timedelta
from datetime import datetime

twitterdate = dateparser.parse("12.01.2022").strftime('%d.%m.%Y')
print(twitterdate)

print((datetime.strptime(twitterdate, '%d.%m.%Y') - timedelta(days = 365)).strftime('%d.%m.%Y'))




    
