#!/usr/bin/env python3
import os
import shutil

ART_DIR = "/Users/nathan/.gemini/antigravity/brain/affe4f09-1adf-4c4a-8e08-54786009d8b9"
TARGET_DIR = "/Users/nathan/Daily Drip/public/assets/editorial"

mapping = {
    "binary_genesis": {
        "structure_back": "binary_structure_back_1779508186016.png",
        "fabric_truss": "binary_fabric_truss_1779508199543.png",
        "silhouette": "binary_silhouette_1779508215016.png",
        "the_life": "binary_the_life_1779508227527.png"
    },
    "neural_echoes": {
        "structure_back": "neural_structure_back_1779508257281.png",
        "fabric_truss": "neural_fabric_truss_1779508274761.png",
        "silhouette": "neural_silhouette_1779508285473.png",
        "the_life": "neural_the_life_1779508300821.png"
    },
    "outperformed_by_robot": {
        "structure_back": "robot_structure_back_1779508314531.png",
        "fabric_truss": "robot_fabric_truss_1779508326549.png",
        "silhouette": "robot_silhouette_1779508338810.png",
        "the_life": "robot_the_life_1779508351840.png"
    },
    "peace_sign": {
        "structure_back": "peace_structure_back_1779508381484.png",
        "fabric_truss": "peace_fabric_truss_1779508394125.png",
        "silhouette": "peace_silhouette_1779508405458.png",
        "the_life": "peace_the_life_1779508418291.png"
    },
    "pixelated_soul": {
        "structure_back": "pixel_structure_back_1779508432012.png",
        "fabric_truss": "pixel_fabric_truss_1779508443670.png",
        "silhouette": "pixel_silhouette_1779508455560.png",
        "the_life": "pixel_the_life_1779508468680.png"
    },
    "sage_archives": {
        "structure_back": "sage_structure_back_1779508501694.png",
        "fabric_truss": "sage_fabric_truss_1779508514361.png",
        "silhouette": "sage_silhouette_1779508527778.png",
        "the_life": "sage_the_life_1779508540397.png"
    },
    "vaporwave_paradox": {
        "structure_back": "vapor_structure_back_1779508555757.png",
        "fabric_truss": "vapor_fabric_truss_1779508568435.png",
        "silhouette": "vapor_silhouette_1779508581210.png",
        "the_life": "vapor_the_life_1779508594177.png"
    }
}

for slug, images in mapping.items():
    slug_dir = os.path.join(TARGET_DIR, slug)
    os.makedirs(slug_dir, exist_ok=True)
    for name, src_file in images.items():
        src_path = os.path.join(ART_DIR, src_file)
        dest_path = os.path.join(slug_dir, f"{name}.png")
        if os.path.exists(src_path):
            shutil.copy2(src_path, dest_path)
            print(f"Copied {src_file} -> {dest_path}")
        else:
            print(f"Error: {src_path} does not exist!")
