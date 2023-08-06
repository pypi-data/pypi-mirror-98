# -*- coding: utf-8 -*-

import codecs

from setuptools import find_packages, setup



setup(
    name="django-allauth-2fa-foxtail",
    version="0.9",
    packages=find_packages('.', include=('allauth_2fa', 'allauth_2fa.*')),
    include_package_data=True,
    install_requires=[
        "django>=1.11",
        "qrcode>=5.3",
        "django-allauth>=0.25",
        "django-otp>=0.3.12",
    ],
    author="Víðir Valberg Guðmundsson",
    author_email="valberg@orn.li",
    description="Adds two factor authentication to django-allauth",
    license="Apache 2.0",
    keywords=['otp', 'auth', 'two factor authentication', 'allauth', 'django', '2fa'],
    url="https://github.com/percipient/django-allauth-2fa",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Environment :: Web Environment',
        'Topic :: Internet',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: Apache Software License',
    ],
    python_requires=">=3.5",
)
