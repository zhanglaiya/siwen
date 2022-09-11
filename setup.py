import siwen
from setuptools import setup, find_packages


requires = ['flask==0.12.5']

entry_points = {
    'console_scripts': [
        'siwen = siwen.__main__:main',
    ]
}

# description = '\n'.join([README, CHANGELOG])

setup(
    name='siwen',
    version=siwen.version,
    url='https://zhanglaiya.github.io/',
    author='zhanglaiya',
    author_email='315396460@qq.com',
    description="Static site generator supporting Markdown source content.",
    project_urls={
        'Documentation': '',
        'Funding': '',
        'Source': 'https://github.com/zhanglaiya/siwen',
        'Tracker': 'https://github.com/zhanglaiya/siwen/issues',
    },
    keywords='static web site generator Markdown',
    license='Apache',
    # long_description=description,
    # long_description_content_type='text/x-rst',
    packages=find_packages(),
    include_package_data=True,  # includes all in MANIFEST.in if in package
    # NOTE : This will collect any files that happen to be in the themes
    # directory, even though they may not be checked into version control.
    # package_data={  # pelican/themes is not a package, so include manually
    #     'pelican': [relpath(join(root, name), 'pelican')
    #                 for root, _, names in walk(join('pelican', 'themes'))
    #                 for name in names],
    # },
    install_requires=requires,
    entry_points=entry_points,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Framework :: Siwen',
        'License :: Apache :: 2.0',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    test_suite='siwen.tests',
)
