import shelve
with shelve.open("src/file")  as d:
    d['tScore'] = [5, 4, 3, 2, 1]
    d.close()