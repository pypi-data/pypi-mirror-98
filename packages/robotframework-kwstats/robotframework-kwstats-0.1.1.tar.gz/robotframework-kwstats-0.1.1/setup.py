from setuptools import find_packages, setup

setup(
      name='robotframework-kwstats',
      version="0.1.1",
      description='Report for keyword statistics',
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
