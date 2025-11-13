"""Configuration and prompt templates for material specification generation."""

from pathlib import Path
from typing import Dict

# API Configuration
# Using Claude Haiku 4.5 for cost-effective image analysis
# Haiku is 3x cheaper than Sonnet ($1/$5 vs $3/$15 per million tokens)
CLAUDE_MODEL = "claude-haiku-4-5-20251001"
VISION_MAX_TOKENS = 1024
SPEC_GENERATION_MAX_TOKENS = 4096

# CSI MasterFormat Division Mappings
# These organize materials by standard architectural specification divisions
CSI_DIVISIONS: Dict[str, str] = {
    "03": "Concrete",
    "04": "Masonry",
    "05": "Metals",
    "06": "Wood, Plastics, and Composites",
    "07": "Thermal and Moisture Protection",
    "08": "Openings",
    "09": "Finishes",
    "10": "Specialties",
}

# Material category to CSI division mapping
# Helps organize materials into appropriate specification sections
MATERIAL_TO_DIVISION: Dict[str, str] = {
    "concrete": "03",
    "masonry": "04",
    "brick": "04",
    "stone": "04",
    "metal": "05",
    "aluminum": "05",
    "steel": "05",
    "copper": "05",
    "zinc": "05",
    "wood": "06",
    "timber": "06",
    "composite": "06",
    "glass": "08",
    "curtain wall": "08",
    "storefront": "08",
    "cladding": "07",
    "roofing": "07",
}

# Default output directory
DEFAULT_OUTPUT_DIR = Path("output")


def get_vision_analysis_prompt(brief_excerpt: str) -> str:
    """
    Generate prompt for Claude vision API to analyze architectural images.
    
    Args:
        brief_excerpt: Short excerpt from project brief for context
        
    Returns:
        Formatted prompt string for vision analysis
    """
    return f"""Analyze this architectural visualization and identify the materials used.

Project context: {brief_excerpt}

For each material you identify, provide:
1. Material type (use standard architectural terms: glass, concrete, wood, metal, masonry, etc.)
2. Visual characteristics (color, texture, finish, pattern)
3. Approximate coverage/prominence (high/medium/low)
4. Specific architectural observations (e.g., "curtain wall system", "timber cladding", "exposed concrete structure")

Use professional architectural terminology:
- "Curtain wall" not "glass wall system"
- "Cladding" not "exterior covering"
- "Timber" or "wood cladding" not just "wood"
- "CMU" for concrete masonry units
- "Low-E glass" for energy-efficient glazing

Format as a structured list with clear material categories."""


def get_specification_prompt(
    full_brief: str,
    material_analysis: str,
    include_sustainability: bool = False,
    include_alternatives: bool = False,
) -> str:
    """
    Generate prompt for Claude text API to create material specifications.
    
    Args:
        full_brief: Complete project brief text
        material_analysis: Consolidated material analysis from all images
        include_sustainability: Whether to include sustainability considerations
        include_alternatives: Whether to include alternative material options
        
    Returns:
        Formatted prompt string for specification generation
    """
    prompt = f"""You are an architectural specification writer. Based on the material analysis below, 
create a professional material specification document.

PROJECT BRIEF:
{full_brief}

MATERIAL ANALYSIS FROM VISUALIZATIONS:
{material_analysis}

Generate a specification document with these sections:

1. EXECUTIVE SUMMARY
   - Overview of material palette
   - Design intent and material selection rationale
   - Key material characteristics

2. MATERIAL SPECIFICATIONS (organized by CSI MasterFormat divisions)
   For each material category, provide:
   - Material description (use standard architectural terminology)
   - Performance characteristics
   - Typical applications in this project type
   - Installation considerations
   - Visual/esthetic qualities observed
   
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
Be specific but acknowledge limitations of visual analysis."""

    return prompt

