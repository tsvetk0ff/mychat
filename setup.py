from setuptools import setup

setup(
    name="mychat",
    version='0.2.6',
    description='Simple messenger.',
    long_description='Mychat is a simple GUI & console messenger for Windows.',
    license='MIT',
    packages=[
        'mychat_client',
        'mychat_jim',
        'mychat_log',
        'mychat_repo',
        'mychat_server',
    ],
    package_data={
        '': ['sv_main.ui'],
    },
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'mychat_server = mychat_server.server:main',
            'mychat_client = mychat_client.client_gui:main',
        ]
    },
    install_requires=[
        "PyQt5>=5.9",
        "SQLAlchemy>=1.1.15",
    ],
)
