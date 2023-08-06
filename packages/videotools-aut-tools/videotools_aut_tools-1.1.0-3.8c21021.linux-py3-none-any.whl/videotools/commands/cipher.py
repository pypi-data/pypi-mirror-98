"""
Module with logic to perform encryption and decryption of text values in other modules
"""
import logging
import os

from cryptography.fernet import Fernet

from videotools import APP_KEY_FILE, DEFAULT_ENCODING, COMMANDS

logger = logging.getLogger('cipher')

# -- cypher
_FERNET = None


class NotCipherKeyFoundException(Exception):
    """
    Exception launched when no key can be found in configuration directory
    """


def get_cypher_key(keyfile=APP_KEY_FILE):
    """
    Reads the content of the keyfile and returns it's content. An exception is thrown if the file does not exists
    :param keyfile: The file that contains the cypher key used to encrypt values, and now will be used to decrypt
    :return: The content of the key file as a string
    """
    if not os.path.exists(keyfile):
        raise NotCipherKeyFoundException()

    with open(keyfile, 'r') as _file:
        key = _file.read()
        if not key.endswith('\n'):
            key += f'{key}\n'
    return key.encode(DEFAULT_ENCODING)


def get_cypher(keyfile=APP_KEY_FILE):
    """
    Provides an instance of teh cypher used to encrypt sensitive data, so it can be decrypted and used on demand
    :pass keyfile: File with key to be used in cipher
    :return: An instance of the cipher
    """
    global _FERNET

    # load vault key
    if not _FERNET:
        _FERNET = Fernet(get_cypher_key(keyfile))
    return _FERNET


def encrypt(**kwargs):
    """
    Loads the key from .key file, if needed, and encrypts supplied text
    :param kwargs: optional arguments
            text_to_encrypt: The text to  be encrypted, there can be multiple strings
                    keyfile: The file that contains the key to encode the text. Used to initialize the cypher
    :return: A list with supplied strings encrypted
    """
    logger.info('encrypting supplied text...')

    keyfile = kwargs.get('keyfile', APP_KEY_FILE)
    txt_list = kwargs.get('text_to_encrypt')
    assert txt_list, 'Text is required to perform an encrypt action'

    if not isinstance(txt_list, list):
        txt_list = [txt_list]

    _cipher = get_cypher(keyfile)

    result = []
    for _text in [t.encode(DEFAULT_ENCODING) for t in txt_list]:
        result.append(_cipher.encrypt(_text))
    if len(result) == 1:
        result = result[0]
    return result


def decrypt(**kwargs):
    """
    Loads the key from .key file, if needed, and decrypts supplied text
    :param kwargs: optional arguments
            text_to_decrypt: The text to  be decrypted, there can be multiple strings
                    keyfile: The file that contains the key to encode the text. Used to initialize the cypher
    :return: A list with supplied strings decrypted, or a single one if only one string was supplied
    """
    logger.info('decrypting supplied text...')

    keyfile = kwargs.get('keyfile', APP_KEY_FILE)
    txt_list = kwargs.get('text_to_decrypt')
    assert txt_list, 'Text is required to perform a decrypt action'

    if not isinstance(txt_list, list):
        txt_list = [txt_list]

    _cipher = get_cypher(keyfile)

    result = []
    for _text in txt_list:
        result.append(_cipher.decrypt(_text.encode(DEFAULT_ENCODING)).decode(DEFAULT_ENCODING))
    if len(result) == 1:
        result = result[0]
    return result


def generate_key_file(**kwargs):
    """
    Creates a new key file to use with cipher
    :param kwargs: optional arguments
                   output: File to save new key into
    """
    logger.info('generating new key for cipher...')
    key = Fernet.generate_key().decode(DEFAULT_ENCODING)

    output = kwargs.get('output')
    logger.debug('\t saving key into __%s__...', output)
    with open(output, 'w') as _file:
        _file.write(key)
        _file.flush()
    return ''


def init_parser(parent_parser):
    cipher_parser = parent_parser.add_parser(COMMANDS.CIPHER, help='Used to encrypt, decrypt or generate a key file')
    cipher_subparser = cipher_parser.add_subparsers()
    cipher_subparser.required = True

    # -- new key
    cmd_newkey = cipher_subparser.add_parser('newkey', help='Generate a new key file to use with cipher to '
                                                            'encrypt or decrypt')
    cmd_newkey.set_defaults(func=generate_key_file)
    cmd_newkey.add_argument('--output', '-O', dest='output', default='key.new', required=False)

    # # -- encrypt
    cmd_encrypt = cipher_subparser.add_parser('encrypt', help='Encrypts supplied text using a known cipher key')
    cmd_encrypt.set_defaults(func=encrypt)
    cmd_encrypt.add_argument('text_to_encrypt', nargs='+', type=str, help='Text to be encrypted')

    #
    # -- decrypt
    cmd_decrypt = cipher_subparser.add_parser('decrypt', help='Decrypts supplied text using a known cipher key')
    cmd_decrypt.set_defaults(func=decrypt)
    cmd_decrypt.add_argument('text_to_decrypt', nargs='+', type=str, help='Text to be decrypted')
    return cipher_parser


def command(args):
    """
    Process the call in a script with supplied args
    """
    # copy of arguments for function
    cmd_args = vars(args).copy()

    # remove function from copied args
    del cmd_args['func']

    # execute func and print output
    print(args.func(**cmd_args))
