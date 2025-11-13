"""Output formatting and display utilities."""

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich import box

from config import DEFAULT_OUTPUT_DIR

console = Console()


def display_header() -> None:
    """Display tool header."""
    console.print("\n[bold blue]Material Specification Generator[/bold blue]")
    console.print("=" * 50 + "\n")


def display_progress(message: str) -> Progress:
    """
    Create and return a progress indicator.
    
    Args:
        message: Progress message to display
        
    Returns:
        Progress context manager
    """
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    )


def display_material_analysis_table(analyses: Dict[str, str]) -> None:
    """
    Display material analysis results in a formatted table.
    
    Args:
        analyses: Dictionary mapping image filenames to analysis results
    """
    table = Table(
        title="[cyan]Material Analysis Results[/cyan]",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan",
    )
    
    table.add_column("Image", style="blue", no_wrap=True)
    table.add_column("Materials Identified", style="green")
    
    for image_name, analysis in analyses.items():
        if analysis.startswith("ERROR:"):
            # Display error in red
            table.add_row(
                image_name,
                f"[red]{analysis}[/red]",
            )
        else:
            # Extract first few materials for display (simplified)
            # In a real implementation, you might parse the analysis more carefully
            lines = analysis.split("\n")[:5]  # First 5 lines
            preview = "\n".join(lines)
            if len(analysis) > len(preview):
                preview += "\n..."
            
            table.add_row(image_name, preview)
    
    console.print("\n")
    console.print(table)
    console.print("\n")


def display_success(message: str) -> None:
    """
    Display success message.
    
    Args:
        message: Success message text
    """
    console.print(f"[green][OK][/green] {message}")


def display_error(message: str) -> None:
    """
    Display error message.
    
    Args:
        message: Error message text
    """
    console.print(f"[red][ERROR][/red] {message}")


def display_warning(message: str) -> None:
    """
    Display warning message.
    
    Args:
        message: Warning message text
    """
    console.print(f"[yellow][WARNING][/yellow] {message}")


def display_info(message: str) -> None:
    """
    Display informational message.
    
    Args:
        message: Info message text
    """
    console.print(f"[cyan][INFO][/cyan] {message}")


def save_specification(
    specification: str,
    output_dir: Optional[Path] = None,
) -> Path:
    """
    Save specification to markdown file.
    
    Args:
        specification: Specification markdown content
        output_dir: Directory to save file (defaults to config default)
        
    Returns:
        Path to saved file
    """
    if output_dir is None:
        output_dir = DEFAULT_OUTPUT_DIR
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"material_specifications_{timestamp}.md"
    file_path = output_dir / filename
    
    # Add header to specification
    header = f"""# Material Specifications
*Generated from design visualizations - {datetime.now().strftime("%B %d, %Y at %I:%M %p")}*

*This document contains material specifications for each analyzed image. Each section begins with the image filename as a prominent header.*

---
"""
    
    footer = """

---
*Note: These specifications are preliminary and based on design intent visualizations. 
Verify all material selections with manufacturers and project requirements.*
"""
    
    full_content = header + specification + footer
    
    # Write file
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(full_content)
        return file_path
    except Exception as e:
        raise IOError(f"Could not save specification file: {str(e)}") from e


def display_file_saved(file_path: Path) -> None:
    """
    Display message showing where file was saved.
    
    Args:
        file_path: Path to saved file
    """
    absolute_path = file_path.resolve()
    console.print(
        f"\n[green]Specification saved to:[/green] {absolute_path}\n"
    )

