# Project Structure
```ImageAlchemy/
├── config/                    # Configuration files
│   └── default_config.json    # Main configuration
├── docs/                      # Documentation
├── images/                    # Reference images directory
├── models/                    # AI model files
├── prompts/                   # Modular prompt components
│   ├── character_styles.json  # Character characteristic prompts
│   ├── negative_prompts.json  # Negative prompt components
│   └── outfit_styles.json     # Outfit style variations
├── scripts/                   # Organized scripts
│   ├── setup/                 # Installation scripts
│   │   ├── 01_setup_mac.sh    # macOS environment setup
│   │   ├── 02_setup_sdxl.sh   # SDXL model setup
│   │   └── 03_setup_custom_sdxl.sh  # Custom model setup
│   ├── run/                   # Execution scripts
│   │   └── 01_run_mac.sh      # macOS launcher
│   └── utils/                 # Utility scripts
│       ├── cleanup.sh         # Cleanup utilities
│       └── prompt_builder.py  # Prompt building utility
├── main.py                    # FastAPI server and image generation core
├── generator.py               # Batch generation script
├── requirements.txt           # Python dependencies
├── INSTALLATION.md            # Step-by-step installation guide
└── README.md                  # Project documentation
```
