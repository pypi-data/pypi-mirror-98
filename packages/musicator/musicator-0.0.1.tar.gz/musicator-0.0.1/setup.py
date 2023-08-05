import setuptools

long_description = '''
Generate Music. Usage:
```
>>> import musicator
>>> composer = musicator.Composer()
>>> composer.tone(hz=400, duration=1)
>>> composer.tone(hz=500, duration=1)
>>> composer.save('output.wav', rate=44100)
```
'''

setuptools.setup(
    name="musicator",
    version="0.0.1",
    author='Vadim Simakin',
    author_email="sima.vad@yandex.com",
    description="Music generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['musicator'],
    install_requires=['numpy', 'scipy'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7'
)
