import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-compositepk-model", # Replace with your own username
    version="1.0.2",
    author="Arisophy",
    author_email="arisophy@is-jpn.com",
    description="Extended Django Model class with composite-primary-key support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Arisophy/django-compositepk-model",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
        "Topic :: Database",
    ],
    python_requires='>=3.6',
)