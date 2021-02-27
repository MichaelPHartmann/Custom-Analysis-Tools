with open('test_csv.csv', 'r+') as f:
    lin = ['Bad','Dog','Good','Cat']
    for i in lin:
        f.writelines(i)
