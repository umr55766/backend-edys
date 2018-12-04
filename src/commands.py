import click
from flask.cli import with_appcontext

try:
    from .models import db, PageWordCount
except ImportError:
    from models import db, PageWordCount


@click.command('initdb')
@with_appcontext
def initdb_command():
    """Initializes the database"""
    db.create_all()
    print('\u2714 \u2714 Initialized the database successfully \u2714 \u2714')


CLI_COMMANDS = {
    "initdb": initdb_command,
}
