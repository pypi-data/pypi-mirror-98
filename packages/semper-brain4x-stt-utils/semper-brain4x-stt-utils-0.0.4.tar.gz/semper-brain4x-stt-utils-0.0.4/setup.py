import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="semper-brain4x-stt-utils", # Replace with your own username
    version="0.0.4",
    author="Mehmet Uluc Sahin",
    author_email="ulucsahin@gmail.com",
    description="Package for continuously listening to raw audio.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://git.semper-tech.com/arcelik/semper-brain4x-stt-utils/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={'semper_brain4x_stt_utils': 'semper_brain4x_stt_utils'},
    packages=['semper_brain4x_stt_utils'],
    python_requires=">=3.6",
)