

with open('/Users/oswaldo/desktop/lista.txt') as file:
    for line in file:

        if line.startswith('title="+55'):
            print(line[10:len(line)-2])

