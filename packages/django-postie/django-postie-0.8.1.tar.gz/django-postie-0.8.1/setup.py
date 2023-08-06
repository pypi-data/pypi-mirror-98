from setuptools import find_packages, setup

pkj_name = 'postie'


with open('README.rst') as f:
    readme = f.read()

setup(
    name='django-postie',
    version='0.8.1',
    install_requires=[
        'django>=2',
        'django-ckeditor',
        'django-codemirror2',
        'django-model-utils',
        'django-parler',
        'django-solo',
        'tilda-wrapper-api'
    ],
    packages=find_packages(exclude=['tests']),
    url='https://gitlab.com/cyberbudy/django-postie',
    license='MIT',
    author='cyberbudy',
    author_email='cyberbudy@gmail.com',
    description='Django mailing through admin',
    long_description=readme,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3'
    ],
    include_package_data=True,
    python_requires='>3.7.0'
)
