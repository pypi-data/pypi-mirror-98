from setuptools import setup, find_packages

setup(name="radif_messenger_client",
      version="0.3.3",
      description="radif.ru",
      author="Radif.ru",
      author_email="i@radif.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
