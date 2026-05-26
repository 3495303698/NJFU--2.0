from setuptools import setup, find_packages

setup(
    name="stereo_distillation",
    version="0.1.0",
    description="Stereo Matching Distillation Framework",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "torch>=1.12",
        "torchvision",
        "numpy",
        "opencv-python",
        "albumentations",
        "tqdm",
        "tensorboard",
        "omegaconf",
        "kornia",
        "scipy",
        "pyyaml",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "stereo-train=stereo_distillation.cli.train:main",
            "stereo-eval=stereo_distillation.cli.eval:main",
        ],
    },
)