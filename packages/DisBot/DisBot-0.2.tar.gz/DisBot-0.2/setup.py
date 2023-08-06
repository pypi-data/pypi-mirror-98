from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README=readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY=history_file.read()

setup_args=dict(
    name='DisBot',
    version='0.2',
    description='Tool to create a quick new discord.py bot',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='Sri Harsha G',
    author_email='sri_3007@hotmail.com',
    keywords=['discord.py', 'discord template', 'discord bot template', 'Disbot'],
    url='https://github.com/GSri30/Disbot',
    download_url='https://pypi.org/project/DisBot',
    include_package_data=True,
    entry_points={
            'console_scripts':[
                'disbot-admin=Disbot.cli:Main'
            ]
        },
)

install_requires=[
    'click',
    'python-dotenv',
    'discord.py',
]

if __name__=="__main__":
    setup(**setup_args,install_requires=install_requires)