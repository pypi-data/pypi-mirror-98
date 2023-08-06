from optparse import OptionParser

from .deploy import deploy_layer
from .helpers import get_service_name, get_runtime
from .init import init_layer

usage_str = '''
Usage:  awslayer [OPTION] COMMAND

A simple AWS Lambda Layer manager.

Options:
  -h, --help    Print usage string.

Commands:
  init          Initialize AWS Lambda Layer.
  deploy        Deploy layer to AWS Lambda.
  update        Update layer requirements.

\033[1mTo get more help with this package, contact the repo owner.\033[0m'''


def main():
    parser = OptionParser(description='A simple AWS Lambda Layer manager.', prog='awslayer',
                          epilog='\033[1mTo get more help with this package, contact the repo owner.\033[0m')

    parser.add_option('-e', '--env', dest='env', default='dev', choices=['dev', 'prod'],
                      help="Specify environment, 'dev' by default", metavar='ENV')

    (options, args) = parser.parse_args()

    service = get_service_name()
    runtime = get_runtime()

    init_layer(service, runtime, options.env)
    deploy_layer(runtime, options.env)


if __name__ == '__main__':
    main()
