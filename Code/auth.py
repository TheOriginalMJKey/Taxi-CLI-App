import os
import click
import getpass
from passlib.hash import sha256_crypt
import csv

USERS = 'users.csv'

TRIPS = []

@click.group()
def cli():
    """Taxi ordering CLI application"""

@cli.command()
@click.argument('username')
@click.argument('password')

def register(username, password):
    """Register a new user"""
    if os.path.exists('users.csv'):
        with open('users.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == username:
                    raise click.ClickException("User already exists")
    else:
        with open(USERS_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["username", "password"]) 

    hashed_password = hash_password(password)
    with open('users.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([username, hashed_password])
    click.echo(f"User {username} registered successfully!")
    click.echo(f"Users: {get_users()}")

def get_users():
    """Get a list of all registered users"""
    users = []
    if os.path.exists('users.csv'):
        with open('users.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)  
            for row in reader:
                users.append(row[0])
    return users

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
