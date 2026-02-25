import typer
from rich import print as rprint
from rich.console import Console
from rich.table import Table
from src.services.ingestion import IngestionService
from src.services.qa import QAService

app = typer.Typer(
    help="CLI for LangChain Document Retrieval.",
    add_completion=False
)
console = Console()

@app.command("ingest")
def ingest(
    path: str = typer.Option(
        "./data/documents", 
        "--path", "-p", 
        help="Path to directory containing documents to ingest."
    )
):
    """Process and index documents into the vector store."""
    console.print(f"[{'cyan'}]Starting ingestion from [bold]{path}[/bold]...[/{'cyan'}]")
    try:
        service = IngestionService()
        result = service.ingest_directory(path)
        
        if result["status"] == "success":
            console.print(f"[green]✓ Success: {result['message']}[/green]")
        else:
            console.print(f"[red]✗ Error: {result['message']}[/red]")
            
    except Exception as e:
        console.print(f"[red]✗ Fatal Error during ingestion: {str(e)}[/red]")

@app.command("query")
def query(
    question: str = typer.Option(
        ..., 
        "--question", "-q", 
        help="Question to ask the AI based on the documents."
    )
):
    """Ask a question and generate an answer using the RAG pipeline."""
    console.print(f"[magenta]Thinking about:[/magenta] [bold]{question}[/bold]")
    try:
        service = QAService()
        result = service.ask_question(question)
        
        console.print("\n[bold green]Answer:[/bold green]")
        console.print(result["answer"])
        
        if result["sources"]:
            table = Table(title="Sources Used", show_header=True, header_style="bold blue")
            table.add_column("File", style="dim")
            table.add_column("Page", justify="right")
            table.add_column("Snippet", style="italic")
            
            for source in result["sources"]:
                table.add_row(
                    source["source"], 
                    str(source["page"]), 
                    source["snippet"].replace("\n", " ")  # Flatten snippet lines
                )
            
            console.print("\n")
            console.print(table)
        else:
            console.print("[yellow]No sources were cited for this answer.[/yellow]")
            
    except Exception as e:
        console.print(f"[red]✗ Error querying RAG chain: {str(e)}[/red]")

if __name__ == "__main__":
    app()
