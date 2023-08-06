import setuptools

setuptools.setup(
    name="txtoflow",
    version="0.3.2",
    author="Krishna",
    author_email="krishna.vijay4444@gmail.com",
    description="Library to generate flowcharts from pseudo code",
    long_description=open('README.rst').read(),
    keywords=['automatic flowchart', 'code2flow', 'text2flow', 'text to flowchart', 'txtoflow'],
    platforms=['any'],
    scripts=['bin/txtoflow'],
    license='MIT License',
    long_description_content_type="text/x-rst",
    url="https://krishkasula.gitlab.io/txtoflow/index.html",
    packages=setuptools.find_packages(),
    install_requires=['sly', 'pygraphviz'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
