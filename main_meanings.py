import os
from dotenv import load_dotenv

load_dotenv()

reliability = os.getenv('RELIABILITY')
significance = os.getenv('SIGNIFICANCE')


def read_data(filepath: str = 'input.txt'):
    with open(filepath, 'r') as f:
        data = f.read()
        return  list(map(float, data.strip().split()))

