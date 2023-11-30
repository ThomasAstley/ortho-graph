
def debug_to_file(file, text):
    f = open(file, "a")
    f.write(text + '\n')
    f.close()


def debug(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def generate_json(graphs, file='stdout'):
    if file == 'stdout':
        print(json.dumps(graphs))
    else:
        f = open(file, "w")
        f.write(json.dumps(graphs))
        f.close()

