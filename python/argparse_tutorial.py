# from argparse import ArgumentParser, Namespace
# parser = ArgumentParser()
# parser.add_argument('number', help = 'squares the number and prints it on the terminal', type = int, default=0, nargs ='?')
# parser.add_argument('-v', '--verbose', help='provides a description. -vv for extra verbose',  action = "count")

# args : Namespace = parser.parse_args()
# result :int = (args.number)**2
# print(type((args)))

# if args.verbose == 1:
#     print(f"the square of {args.number} is {result}")
# if args.verbose == 2:
#     print(f"{args.number}^2 = {result}")
# else :
#     print((args.number)**2)


from argparse import ArgumentParser, Namespace
parser = ArgumentParser()

parser.add_argument("")