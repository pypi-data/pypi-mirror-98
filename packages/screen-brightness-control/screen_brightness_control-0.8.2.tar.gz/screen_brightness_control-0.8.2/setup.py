from setuptools import setup

setup(
    name='screen_brightness_control',
    version='0.8.2',
    url='https://github.com/Crozzers/screen_brightness_control',
    project_urls={
        'Documentation': 'https://crozzers.github.io/screen_brightness_control',
        'Issue Tracker': 'https://github.com/Crozzers/screen_brightness_control/issues'
    },
    license='MIT',
    author='Crozzers',
    author_email='captaincrozzers@gmail.com',
    packages=['screen_brightness_control'],
    install_requires=['wmi ; platform_system=="Windows"'],
    description='A Python tool to control monitor brightness on Windows and Linux',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3 :: Only'
    ],
    python_requires='>=3.6'
)
