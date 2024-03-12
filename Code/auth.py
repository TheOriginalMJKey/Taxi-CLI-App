import os
import click
import getpass
from passlib.hash import sha256_crypt

# Database or file storage for user accounts and trip history
# (replace with actual implementation)
USERS = {}

TRIPS = []

@click.group()
def cli():
    """Taxi ordering CLI application"""

@cli.command()
@click.argument('username')
@click.argument('password')
def register(username, password):
    """Register a new user"""
    if username in USERS:
        raise click.ClickException("User already exists")
    hashed_password = hash_password(password)
    USERS[username] = hashed_password
    click.echo(f"User {username} registered successfully!")
    click.echo(USERS)

@cli.command()
@click.argument('username')
@click.argument('password')
def login(username, password):
    """Log in to the system"""
    if username not in USERS or not check_password(password, USERS[username]):
        raise click.ClickException("Invalid username or password")
    click.echo(f"Welcome, {username}!")

@cli.command()
def orders():
    """Create a new taxi order"""
    click.echo("Creating a new taxi order...")
    # Add your order processing here

@cli.command()
def history():
    """View your trip history"""
    click.echo("Your trip history:")
    for trip in TRIPS:
        click.echo(f"- {trip}")

def hash_password(password):
    return sha256_crypt.hash(password)

def check_password(password, hashed_password):
    return sha256_crypt.verify(password, hashed_password)

if __name__ == "__main__":
    cli()
