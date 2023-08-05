from distutils.core import setup

setup(
    name='the_generator',  # How you named your package folder (MyLib)
    packages=['the_generator'],  # Chose the same as "name"
    version='0.3',  # Start with a small number and increase it with every change you make
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='Django CRUD Generator',  # Give a short description about your library
    author='Muhammad Fahmi Hidayah',  # Type in your name
    author_email='m.fahmi.hidayah@gmail.com',  # Type in your E-Mail
    url='https://github.com/fahmihidayah/the_generators',  # Provide either the link to your github or to your website
    download_url='https://github.com/fahmihidayah/the_generators',  # I explain this later on
    keywords=['Django', 'CRUD', 'Generator'],  # Keywords that define your package best
    # install_requires=[  # I get to this in a second
    #     'validators',
    #     'beautifulsoup4',
    # ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3',  # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
# setup (
#     name='the_generators',
#     version='0.1',
#     license='MIT',
#     author='Muhammad Fahmi Hidayah',
#     author_email='m.fahmi.hidayah@gmail.com',
#     description='CRUD generator library for django',
#     long_description=long_description,
#     keywords = ['django', 'CRUD', 'Generator'],
#     url='https://github.com/fahmihidayah/the_generators',
#     packages=['the_generators'],
#     package_dir={""},
#     classifiers=[
#         'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
#         'Intended Audience :: Developers',      # Define that your audience are developers
#         'Topic :: Software Development :: Build Tools',
#         'License :: OSI Approved :: MIT License',   # Again, pick a license
#         'Programming Language :: Python :: 3.6'
#       ],
# )
