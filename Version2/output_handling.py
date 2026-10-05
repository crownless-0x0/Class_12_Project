from tabulate import tabulate

def output(in1, stock):
    last_close = in1[0]
    predictions = in1[1]

    price = sum(predictions) / len(predictions)

    inc_per = ((price - last_close) / last_close) * 100

    up_count = 0
    for i in predictions:
        if i > last_close:
            up_count += 1

    prob_up = (up_count / len(predictions)) * 100
    prob_down = 100 - prob_up

    if 47 <= prob_up <= 53:
        call = 'STAY'
    elif prob_up > 53:
        call = 'BUY'
    else:
        call = 'SELL'

    data = [[stock, last_close, round(price, 2), str(round(inc_per, 2)) + '%', str(round(prob_up, 2)) + '%', str(round(prob_down, 2)) + '%', call]]

    headers = ['Name','Last Close','Predicted Price','Increase %','Probability Up %','Probability Down %','Call']
    print()
    print(tabulate(data, headers=headers, tablefmt='grid'))
    print()

def portflio_out(query_result):
    print('=' * 80)
    print('YOUR PORTFOLIO'.center(70))
    print('=' * 80)
    data = [[query_result[0], query_result[1], query_result[2], query_result[3], query_result[4]]]
    headers = ['UserID', 'Total Amount Spent', 'Stocks Owned', 'Last Trade', 'Profit/Loss']
    print()
    print(tabulate(data, headers=headers, tablefmt='grid'))
    print()
