"""Material Specification Generator - CLI entry point."""

import sys
from pathlib import Path
from typing import Optional

import click

from utils.vision import VisionAnalyzer
from utils.spec_generator import SpecGenerator
from utils.formatter import (
    display_header,
    display_progress,
    display_material_analysis_table,
    display_success,
    display_error,
    display_warning,
    display_info,
    save_specification,
    display_file_saved,
    console,
)


@click.command()
@click.option(
    "--images",
    required=True,
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    help="Directory containing architectural visualization images",
)
@click.option(
    "--brief",
    required=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=Path),
    help="Path to project brief text file",
)
@click.option(
    "--output",
    type=click.Path(file_okay=False, dir_okay=True, path_type=Path),
    default=None,
    help="Output directory for specification files (default: ./output)",
)
@click.option(
    "--sustainability",
    is_flag=True,
    default=False,
    help="Include sustainability considerations in specifications",
)
@click.option(
    "--alternatives",
    is_flag=True,
    default=False,
    help="Include alternative material options in specifications",
)
def main(
    images: Path,
    brief: Path,
    output: Optional[Path],
    sustainability: bool,
    alternatives: bool,
) -> None:
    """
    Generate material specifications from architectural visualization images.
    
    This tool analyzes images using Claude's vision API and generates
    professional material specifications organized by CSI MasterFormat divisions.
    """
    try:
        # Display header
        display_header()
        
        # Initialize components
        try:
            vision_analyzer = VisionAnalyzer()
            spec_generator = SpecGenerator()
        except ValueError as e:
            display_error(str(e))
            sys.exit(1)
        
        # Read brief
        display_info("Reading project brief...")
        try:
            brief_text = spec_generator.read_brief(brief)
            # Use first 200 characters as excerpt for vision analysis context
            brief_excerpt = brief_text[:200] + "..." if len(brief_text) > 200 else brief_text
            display_success("Brief loaded")
        except ValueError as e:
            display_error(str(e))
            sys.exit(1)
        
        # Analyze images
        display_info("Analyzing images...")
        try:
            with display_progress("Processing images with Claude vision API..."):
                analyses = vision_analyzer.analyze_images(images, brief_excerpt)
        except ValueError as e:
            display_error(str(e))
            sys.exit(1)
        except RuntimeError as e:
            display_error(str(e))
            sys.exit(1)
        
        # Check if we got any valid analyses
        valid_analyses = {
            k: v for k, v in analyses.items()
            if not v.startswith("ERROR:")
        }
        
        # Show any errors that occurred
        error_analyses = {
            k: v for k, v in analyses.items()
            if v.startswith("ERROR:")
        }
        
        if error_analyses:
            # Check if all errors are the same (common case like API credits)
            error_messages = [v.replace("ERROR: ", "") for v in error_analyses.values()]
            unique_errors = set(error_messages)
            
            if len(unique_errors) == 1:
                # All errors are the same - show summary
                error_msg = list(unique_errors)[0]
                display_warning(f"Failed to analyze {len(error_analyses)} image(s)")
                console.print(f"  [red]{error_msg}[/red]\n")
            else:
                # Different errors - show details
                display_warning(f"Failed to analyze {len(error_analyses)} image(s):")
                for img_name, error_msg in list(error_analyses.items())[:5]:  # Show first 5
                    clean_error = error_msg.replace("ERROR: ", "")
                    console.print(f"  • {img_name}: [red]{clean_error}[/red]")
                if len(error_analyses) > 5:
                    console.print(f"  ... and {len(error_analyses) - 5} more")
                console.print()  # Empty line
        
        if not valid_analyses:
            display_error(
                "No images could be analyzed successfully. "
                "Please check your images and API key, then try again."
            )
            sys.exit(1)
        
        display_success(f"Analyzed {len(valid_analyses)} image(s)")
        
        # Display analysis results
        display_material_analysis_table(analyses)
        
        # Generate specifications for each image
        display_info("Generating specifications...")
        try:
            image_specs = []
            with display_progress("Creating specification documents..."):
                for image_name, analysis in valid_analyses.items():
                    try:
                        # Generate spec for this specific image
                        image_spec = spec_generator.generate_specification_for_image(
                            image_name=image_name,
                            brief_text=brief_text,
                            material_analysis=analysis,
                            include_sustainability=sustainability,
                            include_alternatives=alternatives,
                        )
                        image_specs.append((image_name, image_spec))
                    except RuntimeError as e:
                        display_warning(f"Could not generate spec for {image_name}: {str(e)}")
                        continue
            
            if not image_specs:
                display_error("No specifications could be generated")
                sys.exit(1)
            
            # Combine all image specs with clear separators
            specification_parts = []
            for i, (image_name, spec) in enumerate(image_specs):
                if i > 0:
                    # Add separator between image specs
                    specification_parts.append("\n\n---\n\n")
                specification_parts.append(spec)
            
            specification = "".join(specification_parts)
            
        except RuntimeError as e:
            display_error(str(e))
            sys.exit(1)
        
        display_success(f"Generated {len(image_specs)} specification(s)")
        
        # Save specification
        try:
            file_path = save_specification(specification, output)
            display_file_saved(file_path)
        except IOError as e:
            display_error(str(e))
            sys.exit(1)
        
        # Success message
        display_success("Complete!")
        
    except KeyboardInterrupt:
        display_error("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        display_error(f"Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

