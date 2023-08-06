from setuptools import setup, find_packages

setup(
    name='pointercratepy',
    version='1.0.1',
    packages=find_packages(),
    url='https://github.com/bretheskevin/pointercrate.py',
    license='MIT License',
    author='Hikudo',
    author_email='bretheskevin@gmail.com',
    description='A pointercrate API wrapper for Python',
    long_description=open("README.md").read() + '\n\n' + open("CHANGELOG.txt").read(),
    long_description_content_type = "text/markdown",
    keywords='pointercratepy',
    install_requires=['requests~=2.25.1']
)
