import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "color_transfer_py",
    version = "0.0.5",
    author = "Phat Tran",
    author_email = "phatth1203@gmail.com",
    description = "Color transfer between images",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/ptran1203/color_transfer",
    project_urls = {
        "Bug Tracker": "https://github.com/ptran1203/color_transfer/issues",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # package_dir = {"": "."},
    packages=setuptools.find_packages(),
    install_requires=['opencv-python>=4.7.0.72', 'torch>=1.13.0'],
    setup_requires=['pytest-runner==5.3.1'],
    tests_require=['pytest==6.2.5', 'opencv-python>=4.7.0.72'],
)