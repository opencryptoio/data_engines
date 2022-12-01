

counter = 0

with open('articles2.txt', 'w') as f2:
 
    with open('articles.txt', 'r') as f:

        lines = str(f.readlines())

        f2.write(lines.strip())


    


f2.close()
f.close()