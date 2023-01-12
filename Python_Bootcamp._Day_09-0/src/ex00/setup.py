from setuptools import setup, Extension

setup(
    name="calculator",
    version="1.0",
    description="This is a calculator module",
    author="DonOutcast",
    author_email="sham1996@yandex.ru",
    ext_modules=[
        Extension('calculator', sources=["calculator.c"])
    ])
