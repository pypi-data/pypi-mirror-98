from setuptools import setup, find_packages

setup(name="radif_messenger_client",
      version="0.0.3",
      description="radif_messenger_client",
      author="Radif.ru",
      author_email="i@radif.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
