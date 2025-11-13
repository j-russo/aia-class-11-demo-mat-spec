# Material Specification Tool - Project Instructions

## Project Overview

**Purpose:** Educational demonstration tool for "AI for Architects" Class 12 (Custom AI Tool Development)

**What it does:** Analyzes architectural visualization images using Claude's vision API and generates professional material specifications with sustainability considerations.

**Target audience:** Architecture students and professionals learning to build custom AI-powered tools

**Build timeline:** 1 day (with demo on following day)

---

## Project Goals

### Primary Objectives
1. **Demonstrate AI integration** - Show how to connect vision AI with text generation for architectural workflows
2. **Teach practical tool building** - Create something students can actually use and extend
3. **Be demo-proof** - Minimal failure points, reliable execution during live class
4. **Educational value** - Code should be readable and well-documented for learning

### Success Criteria
- ✅ Processes 3-4 images in under 60 seconds
- ✅ Generates professional-quality specifications
- ✅ Handles common errors gracefully
- ✅ Students can understand the code structure
- ✅ Tool is actually useful for architecture projects

---

## Technical Architecture

### High-Level Flow
```
Input Images + Design Brief
    ↓
Vision Analysis (Claude API)
    ↓
Material Identification & Consolidation
    ↓
Specification Generation (Claude API)
    ↓
Formatted Output (Markdown/PDF)
```

### Component Breakdown

**1. CLI Entry Point** (`material_spec.py`)
- Parse command-line arguments
- Orchestrate the workflow
- Display progress and results
- Handle top-level errors

**2. Vision Analysis** (`utils/vision.py`)
- Load images from folder
- Encode as base64
- Call Claude vision API
- Parse material identification responses
- Return structured material data

**3. Specification Generator** (`utils/spec_generator.py`)
- Consolidate materials across images
- Add project context from brief
- Generate specification sections
- Format with CSI divisions
- Include sustainability notes if requested

**4. Output Formatter** (`utils/formatter.py`)
- Display terminal tables (material analysis)
- Format progress indicators
- Save markdown files
- (Optional) Convert to PDF

**5. Configuration** (`config.py`)
- Prompt templates
- CSI division mappings
- Default settings
- API configuration

---

## API Integration Details

### Claude Vision API

**Model:** `claude-sonnet-4-20250514`  
**Max tokens:** 1024 (for analysis)  
**Image format:** base64-encoded PNG/JPG

**Request structure:**
```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/png",
                    "data": image_data,
                },
            },
            {
                "type": "text",
                "text": "Analyze this architectural visualization..."
            }
        ],
    }]
)
```

**What to ask for:**
- Material type (glass, concrete, wood, metal, etc.)
- Visual characteristics (color, texture, finish)
- Coverage/prominence (high/medium/low)
- Specific architectural observations

### Claude Text API

**Model:** `claude-sonnet-4-20250514`  
**Max tokens:** 4096 (for specification generation)

**Prompt structure:**
- Project brief context
- Consolidated material analysis
- Requested output format (CSI divisions)
- Optional sections (sustainability, alternatives)

---

## File Structure

```
material_spec_tool/
├── material_spec.py          # Main CLI script
├── requirements.txt          # Python dependencies
├── .env.example              # Template for API keys
├── .cursorrules              # Cursor AI configuration
├── README.md                 # User documentation
├── PROJECT_INSTRUCTIONS.md   # This file
├── config.py                 # Prompts and configuration
├── utils/
│   ├── __init__.py
│   ├── vision.py             # Claude vision integration
│   ├── spec_generator.py     # Specification generation
│   ├── formatter.py          # Output formatting
│   └── file_handler.py       # (Optional) File operations
└── example/
    ├── renders/              # Sample visualization images
    │   ├── render_01.png
    │   ├── render_02.png
    │   └── render_03.png
    ├── brief.txt             # Sample project brief
    └── output/               # Generated specifications
        └── specifications.md
```

---

## Build Phases

### Phase 1: Core Functionality (2 hours)

**Step 1: Project setup (15 min)**
- Create directory structure
- Set up virtual environment
- Install dependencies
- Create `.env` with API key

**Step 2: Vision analysis (45 min)**
- Implement `utils/vision.py`
- Image loading and encoding
- Claude vision API calls
- Response parsing

**Step 3: Specification generation (45 min)**
- Implement `utils/spec_generator.py`
- Material consolidation logic
- Specification prompt engineering
- CSI division formatting

**Step 4: Output formatting (15 min)**
- Implement `utils/formatter.py`
- Markdown generation
- File saving

### Phase 2: CLI & Polish (1 hour)

**Step 5: CLI interface (30 min)**
- Implement `material_spec.py`
- Argument parsing with Click
- Workflow orchestration
- Error handling

**Step 6: Terminal UI (30 min)**
- Progress indicators (rich Progress)
- Material analysis table (rich Table)
- Status messages
- File path display

### Phase 3: Testing & Demo Prep (1 hour)

**Step 7: Example dataset (20 min)**
- Collect 3-4 sample images
- Write sample brief
- Test complete workflow

**Step 8: Documentation (20 min)**
- README with usage examples
- Code comments
- Example output

**Step 9: Demo practice (20 min)**
- Full run-through
- Prepare backup screenshots
- Test on clean environment

---

## Usage Examples

### Basic Usage
```bash
python material_spec.py \
  --images ./example/renders/ \
  --brief ./example/brief.txt
```

### With All Options
```bash
python material_spec.py \
  --images ./renders/ \
  --brief ./brief.txt \
  --output ./project_specs/ \
  --sustainability \
  --alternatives
```

### Expected Output
```
Material Specification Generator
==================================================

Analyzing images...
✓ render_01.png - Materials identified
✓ render_02.png - Materials identified  
✓ render_03.png - Materials identified

┌────────────────┬─────────────────────────────┐
│ Image          │ Materials Identified        │
├────────────────┼─────────────────────────────┤
│ render_01.png  │ Glass curtain wall          │
│                │ Concrete structure          │
│                │ Wood cladding               │
└────────────────┴─────────────────────────────┘

Generating specifications...
✓ Complete!

Specification saved to: ./output/material_specifications_20250112_143022.md
```

---

## Prompt Templates

### Vision Analysis Prompt
```
Analyze this architectural visualization and identify the materials used.

Project context: [brief excerpt]

For each material you identify, provide:
1. Material type (e.g., glass, concrete, wood, metal)
2. Visual characteristics (color, texture, finish)
3. Approximate coverage/prominence (high/medium/low)
4. Specific observations (e.g., "curtain wall system", "timber cladding")

Format as a structured list.
```

### Specification Generation Prompt
```
You are an architectural specification writer. Based on the material analysis below, 
create a professional material specification document.

PROJECT BRIEF:
[full brief text]

MATERIAL ANALYSIS FROM VISUALIZATIONS:
[consolidated analysis from all images]

Generate a specification document with these sections:

1. EXECUTIVE SUMMARY
   - Overview of material palette
   - Design intent

2. MATERIAL SPECIFICATIONS (organized by CSI division)
   For each material category:
   - Material description
   - Performance characteristics
   - Typical applications
   - Installation considerations

[Optional: sustainability notes]
[Optional: alternative materials]

Use professional specification language. Acknowledge these are preliminary 
specifications based on design intent images.

Format in markdown with clear headers.
```

---

## Output Format

### Markdown Structure
```markdown
# Material Specifications
*Generated from design visualizations - [date]*

## Executive Summary
[Overview of material palette and design intent]

## Material Specifications

### Division 04: Masonry
**Concrete Structure**
- Description: [details]
- Performance: [characteristics]
- Application: [typical uses]

### Division 06: Wood, Plastics, and Composites
**Timber Cladding**
- Description: [details]
- Performance: [characteristics]
- Application: [typical uses]

[Continue for all materials...]

## Sustainability Considerations
[If --sustainability flag used]

## Alternative Materials
[If --alternatives flag used]

---
*Note: These specifications are preliminary and based on design intent visualizations. 
Verify all material selections with manufacturers and project requirements.*
```

---

## Error Handling Strategy

### Common Error Scenarios

**1. Missing/invalid images**
```python
# Check: File exists and is valid image format
# Error message: "Could not load render_01.png - file may be missing or corrupted"
# Action: Skip the image, continue with others
```

**2. API failures**
```python
# Check: API response status
# Error message: "API request failed - please check your connection and API key"
# Action: Retry once, then fail gracefully with helpful message
```

**3. Rate limiting**
```python
# Check: Rate limit headers in response
# Error message: "API rate limit reached - waiting 60 seconds..."
# Action: Exponential backoff, retry after delay
```

**4. Invalid brief file**
```python
# Check: File exists and is readable
# Error message: "Could not read brief.txt - please check the file path"
# Action: Exit with error code
```

### Error Message Principles
- Use plain language (avoid technical jargon)
- Explain what went wrong
- Suggest what to do next
- Don't crash without explanation

---

## Testing Checklist

### Before Demo
- [ ] Test with 3-4 architectural images
- [ ] Test with realistic design brief
- [ ] Verify API key is configured
- [ ] Test on clean Python environment
- [ ] Run with all CLI options
- [ ] Check output formatting
- [ ] Verify file paths are correct
- [ ] Test error handling (bad image, no API key)
- [ ] Practice demo run-through
- [ ] Prepare backup screenshots

### Edge Cases to Test
- [ ] Empty image folder
- [ ] Single image
- [ ] Very large images (>5MB)
- [ ] Images with no clear materials
- [ ] Very short brief
- [ ] Very long brief
- [ ] Network interruption
- [ ] Invalid API key

---

## Demo Script

### Setup (Before Class)
1. Open terminal in project directory
2. Activate virtual environment
3. Verify API key is set
4. Have example folder ready
5. Clear previous outputs

### Demo Flow (6 minutes)

**Part 1: Show the problem (1 min)**
```bash
# Show input files
ls example/renders/
cat example/brief.txt
```

**Part 2: Run the tool (1 min)**
```bash
python material_spec.py \
  --images ./example/renders/ \
  --brief ./example/brief.txt \
  --sustainability
```

**Part 3: Watch the output (2 min)**
- Terminal progress indicators
- Material analysis table
- Completion message

**Part 4: Show the result (2 min)**
```bash
# Open generated file
cat output/material_specifications_*.md
# or use markdown previewer
```

### Backup Plan
If live demo fails:
1. Have pre-generated output ready to show
2. Explain what should have happened
3. Show the code structure instead
4. Offer to debug in office hours

---

## Student Assignment Integration

### Tier 1: Tool User
Students will:
- Install the tool
- Run with their Class 11 visualization images
- Evaluate output quality
- Write reflection on usefulness

**Grading focus:** Understanding of tool capabilities and limitations

### Tier 2: Tool Customizer
Students will:
- Modify prompt templates in `config.py`
- Add new CLI option (e.g., `--format csi` vs `--format simple`)
- Extend output formatting
- Test modifications

**Grading focus:** Code modification and experimentation

### Tier 3: Tool Builder
Students will:
- Build entirely different integration tool
- Must include: vision/data analysis + AI + structured output
- Document design decisions
- Create user guide

**Grading focus:** Independent application of concepts

---

## Future Enhancement Ideas

*Not for initial build, but mention in class as possibilities:*

- [ ] Web UI version (Streamlit)
- [ ] Integration with 2050 Materials API for real product data
- [ ] PDF export with styling
- [ ] Batch processing multiple projects
- [ ] Material cost estimation
- [ ] Integration with Grasshopper/Revit
- [ ] Custom prompt templates per project type
- [ ] Image annotation (highlight materials in images)
- [ ] Comparison mode (multiple design options)

---

## Troubleshooting Guide

### "ModuleNotFoundError"
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### "API key not found"
**Solution:** Create `.env` file
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### "Could not load image"
**Solution:** Check image format and path
- Supported: PNG, JPG, JPEG
- Must be in specified folder
- Check file permissions

### "API request failed"
**Solution:** Check network and API key
- Verify internet connection
- Check API key is valid
- Check Anthropic API status

### "No materials identified"
**Solution:** Check image quality
- Images should clearly show materials
- Avoid overly abstract renderings
- Ensure sufficient resolution

---

## Resources

### Documentation
- [Anthropic Claude API Docs](https://docs.anthropic.com/claude/reference/getting-started-with-the-api)
- [Click Documentation](https://click.palletsprojects.com/)
- [Rich Documentation](https://rich.readthedocs.io/)
- [CSI MasterFormat](https://www.csiresources.org/standards/masterformat)

### Example Prompts
- See `config.py` for full prompt templates
- Test prompts in Claude.ai before implementing

### Support
- Office hours: [schedule TBD]
- Course Discord: [link TBD]
- GitHub issues: [if open-sourced]

---

## Success Metrics

### For the Demo
- ✅ Completes without errors
- ✅ Students can follow the logic
- ✅ Output looks professional
- ✅ Takes <2 minutes to run

### For Student Learning
- ✅ Students understand when to build custom tools
- ✅ Students can read and modify the code
- ✅ Students grasp API integration concepts
- ✅ Students see practical value

### For Practical Use
- ✅ Tool actually works on real projects
- ✅ Output is usable in practice
- ✅ Saves time vs manual specification
- ✅ Extendable for different workflows

---

## Notes for Instructor

### Key Teaching Points
1. **Why custom tools?** - Can't do batch image analysis in Claude.ai
2. **API integration** - Show how to read docs and make calls
3. **Prompt engineering** - Demonstrate iterative refinement
4. **Error handling** - Emphasize production-ready code
5. **Simplicity wins** - CLI beats web UI for speed and reliability

### Common Student Questions
- "Why not just use ChatGPT?" → Can't batch process, no file output
- "Why Python?" → Most accessible for architects, great libraries
- "Why CLI not web app?" → Faster to build, easier to debug, more flexible
- "Is this production-ready?" → Yes, with minor additions (auth, validation)

### Time Management
- Don't get stuck debugging live
- Have backup slides ready
- Skip minor bugs, focus on concepts
- Save complex questions for office hours

---

## License & Attribution

**For educational use in "AI for Architects" course.**

Students may use and modify for personal projects. If sharing publicly, credit the course.

---

*Last updated: [Date]*  
*Version: 1.0*  
*Instructor: Jacob Russo*
