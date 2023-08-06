from distutils.core import setup

setup(
    name="zowie-utils",
    packages=["zowie"],
    package_data={"zowie": ["py.typed"]},
    version="0.8",
    license="MIT",
    description="Zowie python commons",
    author="zowie-dev",
    author_email="lukasz.kazmierczak@zowie.ai",
    url="https://github.com/chatbotizeteam/python-commons",
    keywords=[],
    install_requires=[
        "regex",
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.6",
)
