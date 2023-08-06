from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='besuto',
    version='0.0.3',
    description='library that made for besuto and made by besuto',
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    packages=find_packages(),
    author='Rapepong Pitijaroonpong',
    author_email='bestkpn8965@gmail.com',
    keywords=['image'],
    include_package_data=True,
    url='https://github.com/Besutodesuka/besuto',
    python_requires='>=3.7'
)

installrequires = [
'pandas',
'pillow',
'tensorflow',
'matplotlib',
'seaborn',
'scikit-learn',
'keras_vggface',
'mtcnn',
'scikit-image',
'tqdm'
]


if __name__ == '__main__':
    setup(**setup_args, install_requires=installrequires)