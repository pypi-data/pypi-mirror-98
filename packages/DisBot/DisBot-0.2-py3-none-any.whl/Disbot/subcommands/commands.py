import click
import os
from pathlib import Path


@click.command()
@click.argument('name')
# @click.argument('path')
def createbot(name):

    path='.'

    if os.path.isdir(os.path.join(name,path)):
        click.echo(f"\u001b[31mError\u001b[0m : '{name}' folder already exists in the current directory.")
        return

    """Main folder"""
    os.mkdir(os.path.join(path,name))

    """Cogs folder"""
    os.mkdir(os.path.join(path,name,'Cogs'))

    """Embeds folder"""
    os.mkdir(os.path.join(path,name,'Embeds'))

    base=Path(__file__).parent.parent
    template=os.path.join(base,'template')

    """gitignore file"""
    with open(os.path.join(template,'gitignore.py'),'r') as f_source,open(os.path.join(path,name,'.gitignore'),'w') as f_dest:
        f_dest.write('\n'.join(f_source.read().split('\n')[1:-1]))
    
    """_constants file"""
    with open(os.path.join(template,'_constants.py'),'r') as f_source,open(os.path.join(path,name,'_constants.py'),'w') as f_dest:
        f_dest.write(f_source.read())

    """Main file"""
    with open(os.path.join(template,'Main.py'),'r') as f_source,open(os.path.join(path,name,'Main.py'),'w') as f_dest:
        f_dest.write(f_source.read())

    """secret file"""
    with open(os.path.join(template,'secret.py'),'r') as f_source,open(os.path.join(path,name,'secret.py'),'w') as f_dest:
        f_dest.write(f_source.read())

    """settings file"""
    with open(os.path.join(template,'settings.py'),'r') as f_source,open(os.path.join(path,name,'settings.py'),'w') as f_dest:
        f_dest.write(f_source.read())

    """__init__ file"""
    with open(os.path.join(path,name,'__init__.py'),'w') as f:
        pass
    
    with open(os.path.join(path,name,'Cogs','__init__.py'),'w') as f:
        pass

    with open(os.path.join(path,name,'Embeds','__init__.py'),'w') as f:
        pass

    """Cogs"""
    with open(os.path.join(template,'Cogs','Base.py'),'r') as f_source,open(os.path.join(path,name,'Cogs','Base.py'),'w') as f_dest:
        f_dest.write(f_source.read())

    with open(os.path.join(template,'Cogs','Errors.py'),'r') as f_source,open(os.path.join(path,name,'Cogs','Errors.py'),'w') as f_dest:
        f_dest.write(f_source.read())
    
    with open(os.path.join(template,'Cogs','General.py'),'r') as f_source,open(os.path.join(path,name,'Cogs','General.py'),'w') as f_dest:
        f_dest.write(f_source.read())
    
    """Embeds"""
    with open(os.path.join(template,'Embeds','GeneralEmbed.py'),'r') as f_source,open(os.path.join(path,name,'Embeds','GeneralEmbed.py'),'w') as f_dest:
        f_dest.write(f_source.read())

    """README"""
    with open(os.path.join(template,'README.md'),'r') as f_source,open(os.path.join(path,name,'README.md'),'w') as f_dest:
        f_dest.write(f_source.read())
    
    click.echo(f"\n\u001b[32mSuccessfully created '{name}' in the current directory\u001b[0m\n")