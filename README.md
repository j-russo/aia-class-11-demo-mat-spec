# Material Specification Generator

An AI-powered tool for architects that analyzes architectural visualization images and generates professional material specifications using Claude's vision API. Available as both a CLI tool and web application.

**Built for:** "AI for Architects" Class 12 (Custom Tool Development)

## Features

- 🔍 **Vision Analysis** - Automatically identifies materials in architectural renderings using Claude Haiku
- 📋 **Professional Specs** - Generates specifications organized by CSI MasterFormat divisions
- 🖼️ **Per-Image Specifications** - Each image gets its own specification section with prominent headers
- 🌐 **Web UI** - Beautiful Streamlit interface for easy sharing and collaboration
- 💻 **CLI Tool** - Command-line interface for batch processing and automation
- 🌱 **Sustainability** - Optional sustainability considerations and alternative materials
- 🎨 **Rich Terminal UI** - Beautiful progress indicators and formatted output
- ⚡ **Fast Processing** - Analyzes 3-4 images in under 60 seconds
- 💰 **Cost-Effective** - Uses Claude Haiku for 3x lower API costs

## Installation

### Prerequisites

- Python 3.10 or higher
- Anthropic API key ([Get one here](https://console.anthropic.com/))

### Setup

1. **Clone or download this repository**

2. **Create a virtual environment** (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set up API key**:
   - Create a `.env` file in the project root
   - Add your API key:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```

## Usage

### Web UI (Recommended for Most Users)

1. **Activate virtual environment:**
```bash
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Mac/Linux
source venv/bin/activate
```

2. **Run Streamlit app:**
```bash
streamlit run app.py
```

3. **Use in browser:**
   - Upload images (multiple files supported)
   - Enter project brief (optional - text area or file upload)
   - Select options (sustainability, alternatives)
   - Click "Generate Specifications"
   - View results and download markdown file

See [WEB_UI_README.md](WEB_UI_README.md) for detailed web UI instructions.

### CLI Usage

#### Basic Usage

```bash
python material_spec.py \
  --images ./example/renders/ \
  --brief ./example/brief.txt
```

#### With All Options

```bash
python material_spec.py \
  --images ./renders/ \
  --brief ./brief.txt \
  --output ./project_specs/ \
  --sustainability \
  --alternatives
```

#### Command-Line Options

- `--images` (required) - Directory containing architectural visualization images
- `--brief` (required) - Path to project brief text file
- `--output` (optional) - Output directory for specification files (default: `./output`)
- `--sustainability` (flag) - Include sustainability considerations
- `--alternatives` (flag) - Include alternative material options

## Example Output

The tool generates a markdown file with specifications for each analyzed image. Each image section includes:

- **Image Header** - Prominent header showing the source image filename
- **Executive Summary** - Overview of materials visible in that specific image
- **Material Specifications** - Organized by CSI MasterFormat divisions:
  - Division 03: Concrete
  - Division 04: Masonry
  - Division 05: Metals
  - Division 06: Wood, Plastics, and Composites
  - Division 07: Thermal and Moisture Protection
  - Division 08: Openings (glazing systems)
  - Division 09: Finishes
- **Sustainability Considerations** (if enabled)
- **Alternative Materials** (if enabled)

Multiple images are combined into a single document with clear separators, making it easy to see which materials came from which visualization.

## Project Structure

```
material_spec_tool/
├── app.py                    # Streamlit web UI
├── material_spec.py          # CLI entry point
├── config.py                 # Prompts and configuration
├── requirements.txt          # Python dependencies
├── utils/
│   ├── vision.py             # Claude vision integration
│   ├── spec_generator.py     # Specification generation
│   └── formatter.py          # Output formatting
├── example/
│   ├── renders/              # Sample visualization images
│   ├── brief.txt             # Sample project brief
│   └── output/               # Generated specifications
└── venv/                     # Virtual environment (created during setup)
```

## How It Works

1. **Image Analysis** - Uses Claude Haiku vision API to identify materials in each image
2. **Per-Image Processing** - Generates a separate specification for each image
3. **Specification Generation** - Creates professional specification documents with image attribution
4. **Output** - Combines all specifications into a single markdown file with clear image headers

## Supported Image Formats

- PNG
- JPG/JPEG

## Troubleshooting

### "ANTHROPIC_API_KEY not found"
- Make sure you've created a `.env` file with your API key
- Check that the `.env` file is in the project root directory
- Verify the virtual environment is activated when running

### "Could not load image"
- Verify image format is PNG, JPG, or JPEG
- Check that images are in the specified directory
- Ensure image files are not corrupted

### "API request failed" or "Credit balance too low"
- Check your internet connection
- Verify your API key is valid and has credits
- Check [Anthropic API status](https://status.anthropic.com/)
- The tool uses Claude Haiku for cost-effectiveness - ensure you have API credits

### "No valid images found"
- Ensure images are in the specified directory
- Check that image files have valid extensions (.png, .jpg, .jpeg)

### "streamlit: command not found"
- Make sure the virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`
- Verify Streamlit is installed: `pip list | grep streamlit`

### Web UI not opening
- Check the terminal for the URL (usually `http://localhost:8501`)
- Try a different port: `streamlit run app.py --server.port 8502`
- Ensure no firewall is blocking the connection

## Educational Use

This tool is designed for educational purposes in the "AI for Architects" course. Students can:

- **Tier 1: Tool User** - Use the tool with their own visualization images
- **Tier 2: Tool Customizer** - Modify prompts in `config.py`, add CLI options
- **Tier 3: Tool Builder** - Build entirely different integration tools

## Limitations

- Specifications are preliminary and based on visual analysis
- Material identification depends on image quality and clarity
- Always verify material selections with manufacturers and project requirements
- Tool is designed for educational/demonstration purposes

## Technical Details

- **AI Model:** Claude Haiku 4.5 (`claude-haiku-4-5-20251001`)
- **API Costs:** ~$1/$5 per million tokens (input/output) - 3x cheaper than Sonnet
- **Processing:** Each image analyzed individually, then specifications generated per image
- **Output Format:** Markdown with clear image attribution headers

## Resources

- [Anthropic Claude API Docs](https://docs.anthropic.com/claude/reference/getting-started-with-the-api)
- [Claude API Pricing](https://www.claude.com/pricing#api)
- [CSI MasterFormat](https://www.csiresources.org/standards/masterformat)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Click Documentation](https://click.palletsprojects.com/)
- [Rich Documentation](https://rich.readthedocs.io/)

## Contributing

This is an educational project. Feel free to:
- Fork and modify for your own projects
- Submit issues or improvements
- Share with other architecture students

## License

MIT License - See [LICENSE](LICENSE) file for details.

---

**Instructor:** Jacob Russo  
**Course:** AI for Architects - Class 12  
**Built:** 2025

