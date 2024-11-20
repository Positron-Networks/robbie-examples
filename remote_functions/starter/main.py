from robbie import remote


@remote(tail=True)
def main():
    print('should work without requirement.txt')

main()