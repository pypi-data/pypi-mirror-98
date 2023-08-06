from setuptools import setup
import pathlib

here = pathlib.Path(__file__).parent
readme = (here / "README.rst").read_text(encoding="utf-8")

setup(
    name="saudi-id-validator",
    version="1.0.6",
    description="Validate ID numbers of Saudi Arabian identity cards",
    long_description=readme,
    long_description_content_type="text/x-rst",
    url="https://github.com/dralshehri/saudi-id-validator",
    author="Mohammed Alshehri",
    author_email="",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Utilities",
        "Typing :: Typed"
    ],
    keywords="saudi government validator identity number",
    py_modules=[module.stem for module in here.glob("src/*.py")],
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">=3.5",
)
