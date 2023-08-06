import setuptools

with open("Readme.md", "r",encoding='UTF-8') as fh:
    long_description = fh.read()


setuptools.setup(
    name="My_face_recognize_ID", # Replace with your own username
    version="0.1.0",
    author="Sakura",
    author_email="author@example.com",
    description="A small example package 20200712",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="none",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2',
    py_modules=['last_project']
)
