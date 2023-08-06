import argparse

def main():
    parser = argparse.ArgumentParser(prog='gfg', description='GfG Article')
    parser.add_argument('name', type=str, action='store')

    args = parser.parse_args()

    print(args)