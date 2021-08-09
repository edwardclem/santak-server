from setuptools import setup

setup(
    name='santak',
    packages=['santak'],
    include_package_data=True,
    install_requires=[
        "flask", "numpy", "scikit-learn", "matplotlib", "pillow", "ray"
    ],
)