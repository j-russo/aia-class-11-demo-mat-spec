"""Vision analysis module for identifying materials in architectural images."""

import base64
from pathlib import Path
from typing import List, Dict, Optional
from io import BytesIO

from anthropic import Anthropic
from anthropic.types import Message
from PIL import Image
from dotenv import load_dotenv
import os

from config import CLAUDE_MODEL, VISION_MAX_TOKENS, get_vision_analysis_prompt

# Load environment variables
load_dotenv()


class VisionAnalyzer:
    """Handles image analysis using Claude's vision API."""
    
    def __init__(self) -> None:
        """Initialize the vision analyzer with API client."""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY not found in environment variables. "
                "Please create a .env file with your API key."
            )
        self.client = Anthropic(api_key=api_key)
    
    def load_images(self, image_dir: Path) -> List[Path]:
        """
        Load all valid image files from a directory.
        
        Args:
            image_dir: Path to directory containing images
            
        Returns:
            List of image file paths
            
        Raises:
            ValueError: If directory doesn't exist or contains no valid images
        """
        if not image_dir.exists():
            raise ValueError(f"Image directory not found: {image_dir}")
        
        if not image_dir.is_dir():
            raise ValueError(f"Path is not a directory: {image_dir}")
        
        # Supported image formats
        valid_extensions = {".png", ".jpg", ".jpeg", ".PNG", ".JPG", ".JPEG"}
        image_files = [
            f for f in image_dir.iterdir()
            if f.is_file() and f.suffix in valid_extensions
        ]
        
        if not image_files:
            raise ValueError(
                f"No valid images found in {image_dir}. "
                "Supported formats: PNG, JPG, JPEG"
            )
        
        return sorted(image_files)
    
    def encode_image(self, image_path: Path) -> tuple[str, str]:
        """
        Encode image file to base64 for API transmission.
        
        Args:
            image_path: Path to image file
            
        Returns:
            Tuple of (base64_encoded_data, media_type)
            
        Raises:
            ValueError: If image cannot be loaded or is invalid
        """
        try:
            # Open and validate image
            with Image.open(image_path) as img:
                # Convert to RGB if necessary (handles RGBA, P, etc.)
                if img.mode != "RGB":
                    img = img.convert("RGB")
                
                # Save to bytes buffer as JPEG (universal format)
                # This ensures compatibility regardless of original format
                buffer = BytesIO()
                img.save(buffer, format="JPEG", quality=95)
                buffer.seek(0)
                
                # Encode to base64
                image_data = base64.b64encode(buffer.read()).decode("utf-8")
                
                # Always use JPEG media type since we convert everything to JPEG
                media_type = "image/jpeg"
                
                return image_data, media_type
                
        except Exception as e:
            raise ValueError(
                f"Could not load {image_path.name} - file may be corrupted or invalid format"
            ) from e
    
    def analyze_image(
        self,
        image_path: Path,
        brief_excerpt: str = "",
    ) -> str:
        """
        Analyze a single image using Claude vision API.
        
        Args:
            image_path: Path to image file
            brief_excerpt: Short excerpt from project brief for context
            
        Returns:
            Material analysis text from Claude
            
        Raises:
            ValueError: If image cannot be processed
            RuntimeError: If API call fails
        """
        try:
            # Encode image
            image_data, media_type = self.encode_image(image_path)
            
            # Generate prompt
            prompt = get_vision_analysis_prompt(brief_excerpt)
            
            # Call Claude vision API
            response: Message = self.client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=VISION_MAX_TOKENS,
                messages=[{
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": image_data,
                            },
                        },
                        {
                            "type": "text",
                            "text": prompt,
                        },
                    ],
                }],
            )
            
            # Extract text from response
            if response.content and len(response.content) > 0:
                return response.content[0].text
            else:
                raise RuntimeError("Empty response from API")
                
        except Exception as e:
            error_str = str(e).lower()
            
            # Check for specific error types
            if "rate_limit" in error_str or "429" in error_str:
                raise RuntimeError(
                    "API rate limit reached - please wait a moment and try again"
                ) from e
            elif "authentication" in error_str or "401" in error_str:
                raise RuntimeError(
                    "API authentication failed - please check your API key"
                ) from e
            elif "credit balance" in error_str or "too low" in error_str:
                raise RuntimeError(
                    "API credit balance too low - please add credits to your Anthropic account"
                ) from e
            elif isinstance(e, (ValueError, RuntimeError)):
                raise
            else:
                # Try to extract a cleaner error message
                error_msg = str(e)
                if "message" in error_msg and "'message':" in error_msg:
                    # Try to extract the message from the error dict
                    try:
                        import json
                        # Find the message in the error string
                        if "'message':" in error_msg:
                            start = error_msg.find("'message':") + len("'message':")
                            # Extract the message value
                            msg_start = error_msg.find("'", start) + 1
                            msg_end = error_msg.find("'", msg_start)
                            if msg_end > msg_start:
                                error_msg = error_msg[msg_start:msg_end]
                    except:
                        pass
                
                raise RuntimeError(
                    f"API request failed for {image_path.name}: {error_msg}"
                ) from e
    
    def analyze_images(
        self,
        image_dir: Path,
        brief_excerpt: str = "",
    ) -> Dict[str, str]:
        """
        Analyze all images in a directory.
        
        Args:
            image_dir: Path to directory containing images
            brief_excerpt: Short excerpt from project brief for context
            
        Returns:
            Dictionary mapping image filenames to analysis results
            
        Raises:
            ValueError: If directory is invalid or contains no images
        """
        image_files = self.load_images(image_dir)
        results: Dict[str, str] = {}
        
        for image_path in image_files:
            try:
                analysis = self.analyze_image(image_path, brief_excerpt)
                results[image_path.name] = analysis
            except Exception as e:
                # Log error but continue with other images
                error_msg = f"Could not analyze {image_path.name}: {str(e)}"
                results[image_path.name] = f"ERROR: {error_msg}"
        
        return results

