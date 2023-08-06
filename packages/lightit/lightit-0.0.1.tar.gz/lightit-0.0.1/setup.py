from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fr:
    requirements_list = [line.strip() for line in fr.readlines()]

setup(
    name='lightit',
    version='0.0.1',
    description='lightit',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='kylin',
    author_email='464840061@qq.com',
    url='https://github.com/kylinat2688/fastutil',
    python_requires=">=3.6.0",
    install_requires=requirements_list,
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "taskplan = lightit.tool.task:show"
        ]
    }
)
