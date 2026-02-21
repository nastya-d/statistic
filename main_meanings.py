
def read_data(filepath: str = 'input.txt'):
    with open(filepath, 'r') as f:
        data = f.read()
        return  list(map(float, data.strip().split()))

reliability = 0.92
significance = 0.02
