# from setuptools import setup


# with open('README.md') as rf:
#     readme = rf.read()

# setup(
#   name = 'network_serializer',
#   packages = ['network_serializer'],
#   version = '0.8.7',
#   license='MIT',
#   description = 'A Python module to help encode and decode network packets.',
#   long_description=readme,
#   long_description_content_type='text/markdown',
#   author = 'Alvin Lin',
#   author_email = 'hungyeh.alvin.lin@gmail.com',
#   url = 'https://github.com/bubblemans/network-serializer',
#   download_url = 'https://github.com/bubblemans/network-serializer/archive/v0.8.tar.gz',
#   keywords = ['network', 'serilize', 'serializer', 'encode', 'decode', 'packet'],
#   install_requires=[],
#   classifiers=[
#     'Development Status :: 3 - Alpha',
#     'Intended Audience :: Developers',
#     'Topic :: Software Development :: Build Tools',
#     'License :: OSI Approved :: MIT License',
#     'Programming Language :: Python :: 3',
#     'Programming Language :: Python :: 3.4',
#     'Programming Language :: Python :: 3.5',
#     'Programming Language :: Python :: 3.6',
#     'Programming Language :: Python :: 3.7',
#   ],
# )

from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    author='Alvin Lin',
    author_email='hungyeh.alvin.lin@gmail.com',
    description='A Python module to help encode and decode network packets.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    name='network_serializer',
    url='https://github.com/bubblemans/network-serializer',
    version='0.8.8',
)