import typer

app = typer.Typer()

@app.command()
def main():
    typer.echo("Hello from get-papers-list!")

if __name__ == "__main__":
    app()
