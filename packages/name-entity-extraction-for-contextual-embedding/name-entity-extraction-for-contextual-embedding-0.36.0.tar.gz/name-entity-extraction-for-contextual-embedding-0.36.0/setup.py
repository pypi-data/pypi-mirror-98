from setuptools import find_packages, setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

print(find_packages())
setup(
    name="name-entity-extraction-for-contextual-embedding",
    packages=find_packages(),
    version="0.36.0",
    description="a machine learning project for mlm task for contextual embedding",
    author="Simon Meoni",
    license="MIT",
    install_requires=requirements,
    entry_points="""
    [console_scripts]
    camembert_ner_ft=contextual_ner.models.camembert_ner_ft:main
    make_dataset=contextual_ner.data.make_dataset:main
    """,
    package_data={
        "contextual_ner": [
            "resources/log_config.ini",
        ]
    },
)
