
with open('NYSE-Value.csv', 'r') as nyse:
    with open('NYSE-Value-Clean.csv', 'w+') as clean:
        lines = nyse.readlines()
        for line in lines[1:4]:
            linelist = line.split(',')
            sample = linelist[2].strip(',')
            try:
                sample = float(sample)
            except ValueError:
                linelist.pop(2)
            result = ','.join(linelist)
            clean.write(result)
