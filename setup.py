"""
Python Package Setup
Todo & Hava Durumu Uygulaması için setup dosyası
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="todo-weather-app",
    version="1.0.0",
    author="Kyetim",
    author_email="kyetim@example.com",
    description="Python Flask Todo & Hava Durumu Uygulaması",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kyetim/todo-weather-app2",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "todo-weather-app=main:main",
        ],
    },
    keywords="python flask todo weather web application",
    project_urls={
        "Bug Reports": "https://github.com/kyetim/todo-weather-app2/issues",
        "Source": "https://github.com/kyetim/todo-weather-app2",
        "Documentation": "https://github.com/kyetim/todo-weather-app2#readme",
    },
)
