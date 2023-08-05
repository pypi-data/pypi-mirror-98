from distutils.core import setup
setup(
    name = 'beancount_balexpr',
    packages = ['.'],
    version = '0.1.0',
    license = 'MIT',
    description = 'Check balances against simple expressions combining multiple accounts in beancount',
    author = 'Di Weng',
    author_email = 'mystery.wd@gmail.com',
    url = 'https://github.com/w1ndy/beancount_balexpr',
    keywords = [ 'beancount' ],
    install_requires = [
        'beancount',
    ],
)