import json
import sys

from app import CW3TradeSquareBotApp
from configuration import Configuration, UnexpectedConfigurationArgumentsError, RequiredConfigurationArgumentsError, \
    ConfigurationArgumentsTypeError


def main(argv):
    if len(argv) < 2:
        print("Path to configuration file doesn't specified")
        return -1
    if len(argv) > 2:
        print("Too many command line arguments")
        return -1

    config_path = argv[1]
    try:
        with open(config_path) as config_f:
            config = Configuration.from_json(config_f)
    except FileNotFoundError:
        print("Can't find specified configuration file")
        return -1
    except UnexpectedConfigurationArgumentsError as exc:
        print("Unexpected configuration arguments:", *map(repr, exc.args), sep="\n")
        return -2
    except RequiredConfigurationArgumentsError as exc:
        print("Required configuration arguments:", *map(repr, exc.args), sep="\n")
        return -2
    except json.JSONDecodeError as exc:
        print("Error while parsing configuration file:")
        print(exc.msg)
        return -2
    except ConfigurationArgumentsTypeError as exc:
        print(
            f"Wrong type of key {repr(exc.key)}: expected {repr(exc.exp.__name__)}, required {repr(exc.req.__name__)}"
        )
        return -2
    del config_path, config_f

    app = CW3TradeSquareBotApp(config)
    return app.exec()


if __name__ == '__main__':
    exit(main(sys.argv))
