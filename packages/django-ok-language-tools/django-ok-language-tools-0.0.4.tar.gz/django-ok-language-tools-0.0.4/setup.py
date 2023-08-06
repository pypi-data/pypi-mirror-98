from setuptools import setup, find_packages

pkj_name = 'ok_language_tools'

setup(
    name='django-ok-language-tools',
    version='0.0.4',
    long_description_content_type='text/x-rst',
    packages=[pkj_name] + [pkj_name + '.' + x for x in find_packages(pkj_name)],
    include_package_data=True,
)
