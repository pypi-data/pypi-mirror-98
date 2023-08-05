from setuptools import setup, find_packages

with open("README.md", "r", encoding="UTF-8") as fh:
    long_description = fh.read()

setup(
    name='Python123',
    version='0.0.7',
    keywords='Python123',
    description='Python123',
    license='MIT License',
    url='https://python123.io/',
    author='学航',
    author_email='30290382@qq.com',
    packages=find_packages(),
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",

)
