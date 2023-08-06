from setuptools import setup, find_packages

classifiers = [
    "Development Status :: 5 - Production/Stable",
    'Intended Audience :: Developers',
    "Programming Language :: Python :: 3",
    "Operating System :: OS Independent",
    ""

]

setup(
    name="JSETracker",
    version='1.0.0',
    description="Real Time JSE stock data for free",
    long_description_content_type="text/markdown",
    long_description=open('README.md').read(),
    url="https://github.com/SNR99/JSETracker",
    author="Ntwanano Rikhotso",
    author_email="sanele.rikhotso.99@gmail.com",
    license="MIT",
    classifiers=classifiers,
    packages=find_packages(),
    keywords=["Python", "JSE", "Stock Price API", "Stock Price", "JSE API ", "Johannesburg Stock Exchange", "API",
              "Johannesburg Stock Exchange API"],
    install_requires=["bs4", "requests"]
)
