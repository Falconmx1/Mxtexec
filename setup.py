from setuptools import setup, find_packages

setup(
    name="mxtexec",
    version="0.1",
    author="Falconmx1",
    description="Mxtexec - Herramienta de ejecución en red con caparazón de tortuga",
    packages=find_packages(),
    install_requires=[
        "impacket>=0.11.0",
        "pywinrm>=0.4.3",
        "cryptography>=41.0.0",
        "colorama>=0.4.6"
    ],
    entry_points={
        "console_scripts": [
            "mxc = mxc.__main__:main",
        ]
    },
    python_requires=">=3.8",
)
