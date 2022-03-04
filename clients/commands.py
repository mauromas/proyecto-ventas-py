from dataclasses import field
from pydoc import cli
import click

from clients.services import ClientService
from clients.models import Client

from tabulate import tabulate

@click.group()
def clients():
    """ Manages the clients lifecycle """
    pass

@clients.command()
@click.option('-n', '--name',
                type=str,
                prompt=True,
                help='The client name')
@click.option('-c', '--company',
                type=str,
                prompt=True,
                help='The company name')
@click.option('-e', '--email',
                type=str,
                prompt=True,
                help='The client email')
@click.option('-p', '--position',
                type=str,
                prompt=True,
                help='The client position')
@click.pass_context
def create(ctx, name, company, email, position):
    """ Create a new client """
    client = Client(name, company, email, position)
    client_service = ClientService(ctx.obj['clients_table'])

    client_service.create_client(client)

@clients.command()
@click.pass_context
def list(ctx):
    """ List all clients """
    client_service = ClientService(ctx.obj['clients_table'])

    client_list = client_service.list_client()

    headers = [field.capitalize() for field in Client.schema()]

    table = []

    
    for client in client_list:
        table.append([client['uid'],
                    client['name'],
                    client['company'],
                    client['email'],
                    client['position']])

    click.echo(tabulate(table, headers))
        

@clients.command()
@click.argument('client_uid', type=str)
@click.pass_context
def update(ctx, client_uid):
    """ Updates a client """
    client_services = ClientService(ctx.obj['clients_table'])

    client_list = client_services.list_client()

    client = [client for client in client_list if client['uid'] == client_uid]

    if client:
        client = _update_client_flow(Client(**client[0]))

        client_services.update_client(client)

        click.echo("Client updated")

    else:
        click.echo("Not found the client.")


def _update_client_flow(client):
    click.echo("Leave empty if you dont want to modify the value ")

    client.name = click.prompt('New Name ', type=str, default=client.name)
    client.company = click.prompt('New company ', type=str, default=client.company)
    client.email = click.prompt('New email ', type=str, default=client.email)
    client.position = click.prompt('New position ', type=str, default=client.position)

    return client

@clients.command()
@click.argument('client_uid', type=str)
@click.pass_context
def delete(ctx, client_uid):
    """ Delete a client """
    client_services = ClientService(ctx.obj['clients_table'])

    client_list = client_services.list_client()

    client = [client for client in client_list if client['uid'] == client_uid]

    if client:
        client_services.delete_client(client)

        click.echo("The client deleted sucessfully")
    else:
        click.echo("Client not found. ")

all = clients