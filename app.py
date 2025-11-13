"""Material Specification Generator - Streamlit Web UI."""

import streamlit as st
import tempfile
from pathlib import Path
from typing import List, Optional
import io

from utils.vision import VisionAnalyzer
from utils.spec_generator import SpecGenerator
from utils.formatter import save_specification

# Page configuration
st.set_page_config(
    page_title="Material Specification Generator",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state
if "analyses" not in st.session_state:
    st.session_state.analyses = {}
if "specifications" not in st.session_state:
    st.session_state.specifications = {}
if "processing_complete" not in st.session_state:
    st.session_state.processing_complete = False


def main():
    """Main Streamlit application."""
    
    # Header
    st.title("🏗️ Material Specification Generator")
    st.markdown(
        "Analyze architectural visualization images and generate professional "
        "material specifications using AI. Upload images and optionally provide "
        "a project brief to get started."
    )
    
    st.divider()
    
    # Sidebar for options
    with st.sidebar:
        st.header("⚙️ Options")
        
        include_sustainability = st.checkbox(
            "Include Sustainability Considerations",
            value=False,
            help="Add sustainability and environmental impact sections to specifications",
        )
        
        include_alternatives = st.checkbox(
            "Include Alternative Materials",
            value=False,
            help="Add alternative material options and comparisons",
        )
        
        st.divider()
        st.markdown("### 📖 About")
        st.markdown(
            "This tool uses Claude AI to analyze architectural visualizations "
            "and generate professional material specifications organized by "
            "CSI MasterFormat divisions."
        )
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📤 Upload Images")
        uploaded_images = st.file_uploader(
            "Select architectural visualization images",
            type=["png", "jpg", "jpeg"],
            accept_multiple_files=True,
            help="Upload one or more images. Supported formats: PNG, JPG, JPEG",
        )
        
        if uploaded_images:
            st.success(f"✅ {len(uploaded_images)} image(s) uploaded")
            
            # Show image previews
            with st.expander("📷 Preview Images", expanded=False):
                for img in uploaded_images:
                    st.image(img, caption=img.name, width=200)
    
    with col2:
        st.header("📝 Project Brief (Optional)")
        
        # Brief input method selector
        brief_method = st.radio(
            "Input method:",
            ["Text Area", "File Upload"],
            horizontal=True,
        )
        
        brief_text = ""
        
        if brief_method == "Text Area":
            brief_text = st.text_area(
                "Enter project brief",
                height=200,
                placeholder="PROJECT: Modern Office Building\nARCHITECT: Design Studio\n\nPROJECT DESCRIPTION:\n...",
                help="Provide context about your project to improve material identification",
            )
        else:
            uploaded_brief = st.file_uploader(
                "Upload brief file",
                type=["txt", "md"],
                help="Upload a text file containing your project brief",
            )
            if uploaded_brief:
                brief_text = uploaded_brief.read().decode("utf-8")
                st.success("✅ Brief file loaded")
    
    st.divider()
    
    # Generate button
    if st.button("🚀 Generate Specifications", type="primary", use_container_width=True):
        if not uploaded_images:
            st.error("❌ Please upload at least one image")
            return
        
        # Process images
        process_images(
            uploaded_images,
            brief_text,
            include_sustainability,
            include_alternatives,
        )
    
    # Display results if processing is complete
    if st.session_state.processing_complete:
        display_results()


def process_images(
    uploaded_images: List,
    brief_text: str,
    include_sustainability: bool,
    include_alternatives: bool,
) -> None:
    """Process uploaded images and generate specifications."""
    
    try:
        # Initialize components
        with st.spinner("Initializing..."):
            vision_analyzer = VisionAnalyzer()
            spec_generator = SpecGenerator()
        
        # Create temporary directory for images
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Save uploaded images to temp directory
            image_paths = []
            for uploaded_file in uploaded_images:
                file_path = temp_path / uploaded_file.name
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                image_paths.append(file_path)
            
            # Prepare brief excerpt
            brief_excerpt = brief_text[:200] + "..." if len(brief_text) > 200 else brief_text
            
            # Analyze images with progress
            st.header("🔍 Analyzing Images")
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            analyses = {}
            for i, image_path in enumerate(image_paths):
                status_text.text(f"Analyzing {image_path.name}... ({i+1}/{len(image_paths)})")
                progress_bar.progress((i) / len(image_paths))
                
                try:
                    analysis = vision_analyzer.analyze_image(image_path, brief_excerpt)
                    analyses[image_path.name] = analysis
                except Exception as e:
                    analyses[image_path.name] = f"ERROR: {str(e)}"
            
            progress_bar.progress(1.0)
            status_text.text("✅ Analysis complete!")
            
            # Store analyses
            st.session_state.analyses = analyses
            
            # Generate specifications
            st.header("📋 Generating Specifications")
            spec_progress = st.progress(0)
            spec_status = st.empty()
            
            valid_analyses = {
                k: v for k, v in analyses.items()
                if not v.startswith("ERROR:")
            }
            
            if not valid_analyses:
                st.error("❌ No images could be analyzed successfully")
                return
            
            image_specs = []
            for i, (image_name, analysis) in enumerate(valid_analyses.items()):
                spec_status.text(f"Generating spec for {image_name}... ({i+1}/{len(valid_analyses)})")
                spec_progress.progress(i / len(valid_analyses))
                
                try:
                    image_spec = spec_generator.generate_specification_for_image(
                        image_name=image_name,
                        brief_text=brief_text or "No project brief provided.",
                        material_analysis=analysis,
                        include_sustainability=include_sustainability,
                        include_alternatives=include_alternatives,
                    )
                    image_specs.append((image_name, image_spec))
                except Exception as e:
                    st.warning(f"⚠️ Could not generate spec for {image_name}: {str(e)}")
                    continue
            
            spec_progress.progress(1.0)
            spec_status.text("✅ Specifications generated!")
            
            # Store specifications
            st.session_state.specifications = dict(image_specs)
            st.session_state.processing_complete = True
            
            st.success("🎉 Processing complete! Scroll down to view results.")
            st.rerun()
    
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.exception(e)


def display_results():
    """Display analysis results and specifications."""
    
    st.divider()
    st.header("📊 Results")
    
    # Material Analysis Summary
    with st.expander("🔍 Material Analysis Summary", expanded=True):
        analyses = st.session_state.analyses
        
        # Create summary table
        import pandas as pd
        
        summary_data = []
        for img_name, analysis in analyses.items():
            status = "✅ Success" if not analysis.startswith("ERROR:") else "❌ Error"
            preview = analysis[:100] + "..." if len(analysis) > 100 else analysis
            summary_data.append({
                "Image": img_name,
                "Status": status,
                "Preview": preview,
            })
        
        df = pd.DataFrame(summary_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Specifications per image
    st.header("📄 Material Specifications")
    
    specifications = st.session_state.specifications
    
    if not specifications:
        st.warning("No specifications were generated")
        return
    
    # Combine all specs for download
    combined_specs = []
    for i, (image_name, spec) in enumerate(specifications.items()):
        if i > 0:
            combined_specs.append("\n\n---\n\n")
        combined_specs.append(spec)
    
    full_specification = "".join(combined_specs)
    
    # Display each image's specification in collapsible sections
    for image_name, specification in specifications.items():
        with st.expander(f"📷 {image_name}", expanded=False):
            st.markdown(specification)
    
    # Download button
    st.divider()
    
    # Generate download file
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
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
    
    full_document = header + full_specification + footer
    
    st.download_button(
        label="📥 Download Specifications (Markdown)",
        data=full_document,
        file_name=f"material_specifications_{timestamp}.md",
        mime="text/markdown",
        use_container_width=True,
    )


if __name__ == "__main__":
    main()

