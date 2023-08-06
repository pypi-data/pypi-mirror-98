from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
      long_description = fh.read()

setup(name='enrichwrap',
      version='0.0.11',
      description="A small package testing calling out to third party enrichment", # Optional
      long_description=long_description,  # Optional
      long_description_content_type='text/markdown',  # Optional (see note above)
      classifiers=[
            'Development Status :: 3 - Alpha',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2.7',
            'Topic :: Text Processing :: Linguistic',
      ],
      keywords='enrichment',
      url='http://github.com/suhens/enrichwrap',
      author='Sue Hannum',
      author_email='Sue.Hannum@sas.com',
      license='MIT',
      packages=['enrichwrap'],
      install_requires=[
            'markdown',
      ],
      include_package_data=True,
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'],
      scripts=['bin/enrichwrap'],
      entry_points={
            'console_scripts': ['enrichmain=enrichwrap.command_line:main'],
      }
      )

