import click, os, platform, shutil
from sys import exit

@click.command()
@click.option('--project','-p', prompt='Project Name', help='Name of your project')
def create(project):
    os.environ['PROJECT_NAME'] = project

    click.echo(f'--- {platform.system()} System Detected ---')
    try:
        os.mkdir(project)
    except FileExistsError:
        click.echo("Folder already exist. Try Again")
        exit(1)

    base_dir = os.path.dirname(__file__)
    copytree(os.path.join(base_dir, 'boilerplate'),os.path.join(os.getcwd(), project))
    replaceVariables(os.path.join(os.getcwd(), project))

    click.secho('Project Ready To Use !', fg='green')
    click.secho(f'Start your project using cd {project} && flask run')


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)

        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

def replaceVariables(src):
    for root, dirs, files in os.walk(src, topdown=False):

        if os.path.basename(os.path.normpath(root)) == '__pycache__':
            shutil.rmtree(root)
            continue

        for name in files:

            with open(os.path.join(root, name), encoding="latin-1") as f:
                s = f.read()
                if "$PROJECT_NAME" not in s:
                    continue

            with open(os.path.join(root, name), 'w', encoding="latin-1") as f:
                s = s.replace("$PROJECT_NAME", os.environ['PROJECT_NAME'])
                f.write(s)
