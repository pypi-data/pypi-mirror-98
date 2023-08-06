from setuptools import find_packages, setup

setup(
      name='robotframework-kwstats',
      version="0.1.3",
      description='Report for keyword statistics',
      long_description='Custom report which provides detailed info about keyword in project like: Count, Pass Percentage and Time stats',
      classifiers=[
          'Framework :: Robot Framework',
          'Programming Language :: Python',
          'Topic :: Software Development :: Testing',
      ],
      keywords='robotframework keyword report',
      author='Shiva Prasad Adirala',
      author_email='adiralashiva8@gmail.com',
      url='https://github.com/adiralashiva8/robotframework-kwstats',
      license='MIT',

      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,

      install_requires=[
          'robotframework',
          'beautifulsoup4',
      ],
      entry_points={
          'console_scripts': [
              'robotkwstats=robotframework_kwstats.runner:main',
          ]
      },
)
