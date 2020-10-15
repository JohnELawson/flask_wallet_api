from setuptools import find_packages, setup

setup(
    name="wallet",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "flask==1.1.2",
        "Flask-HTTPAuth==4.1.0",
        "Werkzeug==1.0.1",
        "pytest==6.1.1",
        "pytest-cov==2.10.1",
    ],
)

