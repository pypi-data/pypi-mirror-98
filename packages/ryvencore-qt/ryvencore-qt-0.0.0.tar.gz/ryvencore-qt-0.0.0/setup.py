from setuptools import setup


setup(
    name='ryvencore-qt',
    version='0.0.0',
    license='MIT',
    description='Framework for building flow-based visual scripting editors in Python',
    author='Leon Thomm',
    author_email='l.thomm@mailbox.org',
    packages=[

    ],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    python_requires='>=3.8',
    install_requires=['PySide2'],
)
