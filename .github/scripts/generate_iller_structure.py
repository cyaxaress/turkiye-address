#!/usr/bin/env python3
"""
Script to generate folder structure for iller from ptt_il_ilce_mahalle.json

This script reads the main JSON file and creates:
- PTT/iller/{il_adi}/ilceler.json - contains list of ilceler for each il
- PTT/iller/{il_adi}/{ilce_adi}/mahalleler.json - contains list of mahalleler for each il/ilce
"""

import json
from pathlib import Path


def sanitize_filename(name):
    """Sanitize filename to remove invalid characters"""
    # Replace invalid characters with underscore
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, '_')
    return name.strip()


def generate_iller_structure():
    """Generate folder structure from ptt_il_ilce_mahalle.json"""
    
    # Paths
    base_dir = Path(__file__).parent.parent.parent
    input_file = base_dir / "PTT" / "ptt_il_ilce_mahalle.json"
    iller_dir = base_dir / "PTT" / "iller"
    
    # Read the main JSON file
    print(f"Reading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Create iller directory if it doesn't exist
    iller_dir.mkdir(parents=True, exist_ok=True)
    
    # Process each il
    for il in data:
        il_adi = il['il_adi']
        ilceler = il['ilceler']
        
        # Sanitize il name for folder
        il_folder_name = sanitize_filename(il_adi)
        il_dir = iller_dir / il_folder_name
        
        # Create il directory
        il_dir.mkdir(parents=True, exist_ok=True)
        print(f"Processing {il_adi}...")
        
        # Create ilceler.json
        ilceler_data = []
        for ilce in ilceler:
            ilceler_data.append({
                "ilce_id": ilce['ilce_id'],
                "ilce_adi": ilce['ilce_adi']
            })
        
        ilceler_file = il_dir / "ilceler.json"
        with open(ilceler_file, 'w', encoding='utf-8') as f:
            json.dump(ilceler_data, f, ensure_ascii=False, indent=4)
        
        # Process each ilce
        for ilce in ilceler:
            ilce_adi = ilce['ilce_adi']
            mahalleler = ilce.get('mahalleler', [])
            
            # Sanitize ilce name for folder
            ilce_folder_name = sanitize_filename(ilce_adi)
            ilce_dir = il_dir / ilce_folder_name
            
            # Create ilce directory
            ilce_dir.mkdir(parents=True, exist_ok=True)
            
            # Create mahalleler.json
            mahalleler_file = ilce_dir / "mahalleler.json"
            with open(mahalleler_file, 'w', encoding='utf-8') as f:
                json.dump(mahalleler, f, ensure_ascii=False, indent=4)
        
        print(f"  Created {len(ilceler_data)} ilceler and their mahalleler")
    
    print(f"\nSuccessfully generated folder structure in {iller_dir}")


if __name__ == "__main__":
    generate_iller_structure()

