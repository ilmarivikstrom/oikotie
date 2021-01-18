'''
Shared utility functions.
'''

from argparse import ArgumentParser


def get_arguments(args, arg_defs):
    '''
    Read and parse program arguments.
    '''

    parser = ArgumentParser()

    for arg_name in arg_defs.keys():
        params= dict()

        has_type = (
            ('type' in arg_defs[arg_name].keys())
            and (arg_defs[arg_name]['type'] is not None)
        )
        if has_type:
            arg_type = arg_defs[arg_name]['type']
            if arg_type in (bool, 'bool'):
                params['action'] = 'store_true'
            elif arg_type in (str, 'str'):
                params['type'] = str
            elif arg_type in (int, 'int'):
                params['type'] = int
            elif arg_type in (float, 'float'):
                params['type'] = float
            else:
                raise ValueError('Argument type \'{}\' is not recognized'.format(arg_type))

        has_default = (
            ('default_value' in arg_defs[arg_name].keys())
            and (arg_defs[arg_name]['default_value'] is not None)
        )
        if has_default:
            params['default'] = arg_defs[arg_name]['default_value']
        has_description = (
            ('description' in arg_defs[arg_name].keys())
            and (arg_defs[arg_name]['description'] is not None)
        )
        if has_description:
            params['help'] = arg_defs[arg_name]['description']
        long_flag = '--' + arg_name
        has_short = (
            ('short_flag' in arg_defs[arg_name].keys())
            and (arg_defs[arg_name]['short_flag'] is not None)
        )
        if has_short:
            short_flag = '-' + arg_defs[arg_name]['short_flag']
            parser.add_argument(short_flag, long_flag, **params)
        else:
            parser.add_argument(long_flag, **params)

    args = parser.parse_args(args[1:])
    return args, parser