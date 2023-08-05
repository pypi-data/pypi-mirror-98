from argparse import ArgumentParser
parser = ArgumentParser(description = 'Choose specific keyboard sound setup')
parser.add_argument('-k', '--keyboard', metavar='', type=str, help='Setup [default: qwertyuioplkjhgfdsazxcvbnm]')
args = parser.parse_args()
keys = list('qwertyuioplkjhgfdsazxcvbnm') if args.keyboard is None else list(args.keyboard)
