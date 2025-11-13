"""Specification generation module for creating material specifications."""

from pathlib import Path
from typing import Dict, Optional

from anthropic import Anthropic
from anthropic.types import Message
from dotenv import load_dotenv
import os

from config import (
    CLAUDE_MODEL,
    SPEC_GENERATION_MAX_TOKENS,
    get_specification_prompt,
)

# Load environment variables
load_dotenv()


class SpecGenerator:
    """Generates material specifications from consolidated analysis."""
    
    def __init__(self) -> None:
        """Initialize the specification generator with API client."""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY not found in environment variables. "
                "Please create a .env file with your API key."
            )
        self.client = Anthropic(api_key=api_key)
    
    def read_brief(self, brief_path: Path) -> str:
        """
        Read project brief from file.
        
        Args:
            brief_path: Path to brief text file
            
        Returns:
            Brief text content
            
        Raises:
            ValueError: If file cannot be read
        """
        if not brief_path.exists():
            raise ValueError(
                f"Brief file not found: {brief_path}. Please check the file path."
            )
        
        try:
            with open(brief_path, "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception as e:
            raise ValueError(
                f"Could not read brief file {brief_path}: {str(e)}"
            ) from e
    
    def consolidate_analysis(self, analyses: Dict[str, str]) -> str:
        """
        Consolidate material analyses from multiple images.
        
        Args:
            analyses: Dictionary mapping image filenames to analysis results
            
        Returns:
            Consolidated analysis text
        """
        consolidated = []
        
        for image_name, analysis in analyses.items():
            # Skip error entries
            if analysis.startswith("ERROR:"):
                continue
            
            consolidated.append(f"## Analysis from {image_name}\n{analysis}\n")
        
        if not consolidated:
            return "No valid material analyses available."
        
        return "\n".join(consolidated)
    
    def generate_specification_for_image(
        self,
        image_name: str,
        brief_text: str,
        material_analysis: str,
        include_sustainability: bool = False,
        include_alternatives: bool = False,
    ) -> str:
        """
        Generate material specification document for a single image.
        
        Args:
            image_name: Name of the image file
            brief_text: Full project brief text
            material_analysis: Material analysis for this specific image
            include_sustainability: Whether to include sustainability section
            include_alternatives: Whether to include alternatives section
            
        Returns:
            Generated specification document (markdown format) with image name header
            
        Raises:
            RuntimeError: If API call fails
        """
        try:
            # Generate prompt with emphasis on image name
            prompt = f"""You are an architectural specification writer. Based on the material analysis below, 
create a professional material specification document for this specific visualization.

PROJECT BRIEF:
{brief_text}

MATERIAL ANALYSIS FROM IMAGE: {image_name}
{material_analysis}

IMPORTANT: Start the specification with a prominent header showing the image name:
# Material Specifications - {image_name}

Then generate a specification document with these sections:

1. EXECUTIVE SUMMARY
   - Overview of materials visible in this specific image
   - Design intent and material selection rationale
   - Key material characteristics observed

2. MATERIAL SPECIFICATIONS (organized by CSI MasterFormat divisions)
   For each material category visible in this image, provide:
   - Material description (use standard architectural terminology)
   - Performance characteristics
   - Typical applications in this project type
   - Installation considerations
   - Visual/esthetic qualities observed in this image
   
   Organize materials by CSI divisions:
   - Division 03: Concrete
   - Division 04: Masonry
   - Division 05: Metals
   - Division 06: Wood, Plastics, and Composites
   - Division 07: Thermal and Moisture Protection
   - Division 08: Openings (glazing systems)
   - Division 09: Finishes
"""

            if include_sustainability:
                prompt += """
3. SUSTAINABILITY CONSIDERATIONS
   - Embodied carbon considerations
   - Recyclability and lifecycle impacts
   - Energy performance implications
   - Sustainable sourcing options
"""

            if include_alternatives:
                prompt += """
4. ALTERNATIVE MATERIALS
   - Comparable material options
   - Cost considerations
   - Performance trade-offs
   - Aesthetic alternatives
"""

            prompt += """
Use professional specification language appropriate for architectural documentation.
Acknowledge that these are preliminary specifications based on design intent visualizations.
Include appropriate disclaimers about verifying material selections with manufacturers.

Format in markdown with clear headers, sections, and bullet points.
Be specific but acknowledge limitations of visual analysis.
Focus on materials clearly visible in this specific image."""

            # Call Claude text API
            response: Message = self.client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=SPEC_GENERATION_MAX_TOKENS,
                messages=[{
                    "role": "user",
                    "content": prompt,
                }],
            )
            
            # Extract text from response
            if response.content and len(response.content) > 0:
                return response.content[0].text
            else:
                raise RuntimeError("Empty response from API")
                
        except Exception as e:
            if "rate_limit" in str(e).lower() or "429" in str(e):
                raise RuntimeError(
                    "API rate limit reached - please wait a moment and try again"
                ) from e
            elif "authentication" in str(e).lower() or "401" in str(e):
                raise RuntimeError(
                    "API authentication failed - please check your API key"
                ) from e
            else:
                raise RuntimeError(
                    f"Specification generation failed for {image_name}: {str(e)}"
                ) from e
    
    def generate_specification(
        self,
        brief_text: str,
        material_analysis: str,
        include_sustainability: bool = False,
        include_alternatives: bool = False,
    ) -> str:
        """
        Generate material specification document using Claude API.
        
        Args:
            brief_text: Full project brief text
            material_analysis: Consolidated material analysis from all images
            include_sustainability: Whether to include sustainability section
            include_alternatives: Whether to include alternatives section
            
        Returns:
            Generated specification document (markdown format)
            
        Raises:
            RuntimeError: If API call fails
        """
        try:
            # Generate prompt
            prompt = get_specification_prompt(
                full_brief=brief_text,
                material_analysis=material_analysis,
                include_sustainability=include_sustainability,
                include_alternatives=include_alternatives,
            )
            
            # Call Claude text API
            response: Message = self.client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=SPEC_GENERATION_MAX_TOKENS,
                messages=[{
                    "role": "user",
                    "content": prompt,
                }],
            )
            
            # Extract text from response
            if response.content and len(response.content) > 0:
                return response.content[0].text
            else:
                raise RuntimeError("Empty response from API")
                
        except Exception as e:
            if "rate_limit" in str(e).lower() or "429" in str(e):
                raise RuntimeError(
                    "API rate limit reached - please wait a moment and try again"
                ) from e
            elif "authentication" in str(e).lower() or "401" in str(e):
                raise RuntimeError(
                    "API authentication failed - please check your API key"
                ) from e
            else:
                raise RuntimeError(
                    f"Specification generation failed: {str(e)}"
                ) from e

