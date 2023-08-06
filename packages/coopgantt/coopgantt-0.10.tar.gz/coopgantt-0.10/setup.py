import setuptools

with open('README.md') as f:
    README = f.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(name='coopgantt',
      version='0.10',
      description='Used for scheduling tasks based on various input configuration criteria',
      url='https://github.com/tylertjburns/coopgantt',
      author='tburns',
      author_email='tyler.tj.burns@gmail.com',
      license='MIT',
      packages=setuptools.find_packages(),
      python_requires=">3.5",
      install_requires=requirements,
      long_description_content_type="text/markdown",
      long_description=README,
      zip_safe=False,
      include_package_data=True,
      package_data={
        "coopgantt": ['rendering/assets/styles.css', 'rendering/assets/myScripts.js'],
      },
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',

      ])

if __name__ == "__main__":
    print(setuptools.find_packages())