# pubmed_fetcher/main.py
import typer
from pubmed_fetcher.fetcher import fetch_papers
from pubmed_fetcher.utils import save_to_csv

app = typer.Typer()

@app.command()
def main(
    query: str = typer.Argument(..., help="PubMed search query"),
    file: str = typer.Option(None, "-f", "--file", help="Output CSV filename"),
    debug: bool = typer.Option(False, "-d", "--debug", help="Enable debug mode")
):
    """Fetch PubMed papers with non-academic authors in pharma/biotech"""
    if debug:
        typer.echo(f"Running in debug mode...\nQuery: {query}")
    
    results = fetch_papers(query, debug=debug)
    
    if file:
        save_to_csv(results, file)
        typer.echo(f"Results saved to {file}")
    else:
        for row in results:
            typer.echo(row)

if __name__ == "__main__":
    app()
