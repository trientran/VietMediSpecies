import subprocess

# List of PlantCLEF tar.gz URLs
urls = [
    "https://lab.plantnet.org/LifeCLEF/PlantCLEF2022/train/trusted/PlantCLEF2022_trusted_training_images_1.tar.gz",
    "https://lab.plantnet.org/LifeCLEF/PlantCLEF2022/train/trusted/PlantCLEF2022_trusted_training_images_2.tar.gz",
    "https://lab.plantnet.org/LifeCLEF/PlantCLEF2022/train/trusted/PlantCLEF2022_trusted_training_images_3.tar.gz",
    "https://lab.plantnet.org/LifeCLEF/PlantCLEF2022/train/trusted/PlantCLEF2022_trusted_training_images_4.tar.gz",
    "https://lab.plantnet.org/LifeCLEF/PlantCLEF2022/train/trusted/PlantCLEF2022_trusted_training_images_5.tar.gz",
    "https://lab.plantnet.org/LifeCLEF/PlantCLEF2022/train/trusted/PlantCLEF2022_trusted_training_images_6.tar.gz",
    "https://lab.plantnet.org/LifeCLEF/PlantCLEF2022/train/trusted/PlantCLEF2022_trusted_training_images_7.tar.gz",
    "https://lab.plantnet.org/LifeCLEF/PlantCLEF2022/train/trusted/PlantCLEF2022_trusted_training_images_8.tar.gz",
]

# Save to file for aria2 batch
with open("plantclef_urls.txt", "w") as f:
    for url in urls:
        f.write(url + "\n")

# Download using aria2c with 16 parallel connections per file
cmd = ["aria2c", "-x", "16", "-s", "16", "-i", "plantclef_urls.txt"]
subprocess.run(cmd)
