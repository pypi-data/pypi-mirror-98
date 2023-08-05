from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='numerical_derivative_checker',
    version='0.8',
    packages=find_packages(),
    license='MIT',
    description='Simple numerical derivative checker with randomized input sampling.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['numpy'],
    url='https://github.com/etpr/numerical_derivative_checker',
    author='etpr',
    author_email='englertpr@gmail.com',
    include_package_data=True,
    python_requires='>=3.7'
)