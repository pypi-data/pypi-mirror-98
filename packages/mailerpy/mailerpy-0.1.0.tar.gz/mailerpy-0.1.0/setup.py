import setuptools

with open("mailerpy/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mailerpy", # Replace with your own username
    version="0.1.0",
    author="Rabindra Sapkota",
    author_email="rabindrasapkota2@gmail.com",
    description="A package to send mail",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Rabindra-Sapkota/mailer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    # install_requires=['smtplib', 'email', 're']
)
