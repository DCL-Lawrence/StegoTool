from setuptools import setup, find_packages

require = ["opencv-python", "scapy"]

setup(
        name="StegoTool",
        version="0.0.4",
        author="Da-Chih Lin",
        author_email="s.au.rn.b@gmail.com",
        description="A steganography tool",
        packages=find_packages(),
        install_requires=require,
        classifiers=[
                "Programming Language :: Python :: 3",
                "License :: OSI Approved :: GNU General Public License v3 or later (LGPLv3+)",
                "Operating System :: OS Independent",
            ],
        )
