from core import account

acc = account.Account()
acc.setup()

fund = acc.HoldFunds[0]

print fund.Name, fund.Code
fund.dailyHistory(10);




