"""from distutils.core import setup
setup(
  name = 'yamniiMod',         # How you named your package folder (MyLib)
  packages = ['yamniiMod'],   # Chose the same as "name"
  version = '0.5',     # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'just test task',   # Give a short description about your library
  author = 'Arsenii Yamnii',                   # Type in your name
  author_email = 'yamnii@ya.ru',      # Type in your E-Mail
  url = 'https://github.com/arseniiyamnii/history-cllass-TestTask',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/arseniiyamnii/history-cllass-TestTask/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['just', 'test', 'task'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second

      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
"""
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yamniiMod", # Replace with your own username
    version="0.6",
    author="Arsenii Yamnii",
    author_email="yamnii@ya.ru",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    project_urls={
        "Bug Tracker": "https://github.com/arseniiyamnii/history-cllass-TestTask/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "yamniiMod"},
    packages=setuptools.find_packages(where="yamniiMod"),
    python_requires=">=3.6",
)
