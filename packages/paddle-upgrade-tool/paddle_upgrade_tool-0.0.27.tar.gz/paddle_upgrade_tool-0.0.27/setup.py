import paddle_upgrade_tool
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    REQUIREMENTS = f.read().splitlines()

with open("README.md", "r")as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='paddle_upgrade_tool',
    version=paddle_upgrade_tool.__version__,
    install_requires=REQUIREMENTS,
    author='T8T9, PaddlePaddle',
    author_email='taoshibo@baidu.com',
    keywords=('paddle_upgrade_tool', 'paddle', 'paddlepaddle'),
    url='https://github.com/PaddlePaddle/paddle_upgrade_tool',
    packages = find_packages(),
    package_data={'fissix': ['*.txt']},
    test_suite="paddle_upgrade_tool.tests",
    description='Upgrade python project from paddle-1.x to paddle-2.0',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license="Apache License 2.0",
    python_requires=">=3.5.4",
    setup_requires=['wheel'],
    scripts=[],
    entry_points={
        'console_scripts': [
            'paddle_upgrade_tool=paddle_upgrade_tool.main:main',
            'find_pattern=tools.find_pattern:main',
            'find_match_node=tools.find_match_node:main',
        ],
    },
    build_dir="build",
    zip_safe=False,
    classifiers=(
        "License :: OSI Approved",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ),
)
