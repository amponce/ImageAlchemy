import json
import os

class PromptBuilder:
    """
    A utility class to build prompts from various components stored in JSON files.
    Allows for modular prompt composition.
    """
    
    def __init__(self, config_path="config/default_config.json"):
        """
        Initialize the PromptBuilder with paths to prompt component files.
        
        Args:
            config_path (str): Path to the configuration file
        """
        self.script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.config_path = os.path.join(self.script_dir, config_path)
        
        # Load configuration
        with open(self.config_path, 'r') as f:
            self.config = json.load(f)
        
        # Load prompt components
        self.face_styles = self._load_json(self.config["prompt_files"]["face_styles"])
        self.negative_prompts = self._load_json(self.config["prompt_files"]["negative_prompts"])
        self.outfit_styles = self._load_json(self.config["prompt_files"]["outfit_styles"])
    
    def _load_json(self, relative_path):
        """Load a JSON file from a path relative to the script directory."""
        full_path = os.path.join(self.script_dir, relative_path)
        with open(full_path, 'r') as f:
            return json.load(f)
    
    def get_face_style(self, style_name=None):
        """
        Get face style components.
        
        Args:
            style_name (str, optional): Name of the specific face style. If None, returns default.
            
        Returns:
            dict: Face style components
        """
        # For now we only have one face style, but this allows for future expansion
        return self.face_styles["face_settings"]
    
    def get_outfit_style(self, style_name):
        """
        Get a specific outfit style by name.
        
        Args:
            style_name (str): Name of the outfit style (e.g., "red_dress")
            
        Returns:
            dict: Outfit style with prompt and negative_prompt
        """
        for style in self.outfit_styles["outfit_styles"]:
            if style["name"] == style_name:
                return style
        
        raise ValueError(f"Outfit style '{style_name}' not found")
    
    def get_all_outfit_styles(self):
        """
        Get all available outfit styles.
        
        Returns:
            list: List of all outfit styles
        """
        return self.outfit_styles["outfit_styles"]
    
    def get_negative_prompts(self):
        """
        Get all negative prompt components.
        
        Returns:
            dict: Negative prompt components
        """
        return self.negative_prompts["negative_prompts"]
    
    def build_combined_negative_prompt(self):
        """
        Build a comprehensive negative prompt from all components.
        
        Returns:
            str: Combined negative prompt
        """
        neg_prompts = self.get_negative_prompts()
        return ", ".join([
            neg_prompts["face_negative"],
            neg_prompts["hair_negative"],
            neg_prompts["body_negative"],
            neg_prompts["base_negative"]
        ])
    
    def build_outfit_prompt(self, outfit_name, include_face_details=True):
        """
        Build a complete prompt for a specific outfit, optionally including face details.
        
        Args:
            outfit_name (str): Name of the outfit style
            include_face_details (bool): Whether to include face style details
            
        Returns:
            dict: Complete prompt with positive and negative components
        """
        outfit = self.get_outfit_style(outfit_name)
        
        # Start with the outfit prompt
        prompt = outfit["prompt"]
        
        # Add face details if requested
        if include_face_details:
            face = self.get_face_style()
            face_details = ", ".join([
                face["face_preservation"],
                face["expression_modifier"],
                face["body_preservation"],
                face["base_quality"]
            ])
            # Append to the prompt (careful not to duplicate elements)
            prompt = f"{prompt}, {face_details}"
        
        return {
            "prompt": prompt,
            "negative_prompt": outfit["negative_prompt"]
        }

if __name__ == "__main__":
    # Example usage
    builder = PromptBuilder()
    
    # Print available outfit styles
    print("Available outfit styles:")
    for style in builder.get_all_outfit_styles():
        print(f"- {style['name']}")
    
    # Build a complete prompt for a specific outfit
    outfit_name = "red_dress"
    prompt_data = builder.build_outfit_prompt(outfit_name)
    
    print(f"\nGenerated prompt for {outfit_name}:")
    print(f"Positive prompt: {prompt_data['prompt']}")
    print(f"Negative prompt: {prompt_data['negative_prompt']}")