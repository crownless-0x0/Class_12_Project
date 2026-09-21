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

    data = [[stock,last_close,price,str(inc_per) + '%',str(prob_up) + '%',str(prob_down) + '%',call]]

    headers = ['Name','Last Close','Predicted Price','Increase %','Probability Up %','Probability Down %','Call']
    print()
    print(tabulate(data, headers=headers, tablefmt='grid'))
    print()

def portflio_out(query_result):
    
