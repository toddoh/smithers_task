from datetime import datetime
from pytz import timezone    

est = timezone('America/New_York')
now_est = datetime.now(est)
print(now_est.strftime('%H-%M-%S'))