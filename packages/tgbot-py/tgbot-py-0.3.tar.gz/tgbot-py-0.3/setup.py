import pathlib
import setuptools

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()


setuptools.setup(
     name='tgbot-py',
     version='0.3',
     author='Alexander Teplov',
     author_email='teplov_aa@rtsoft.ru',
     description='Python SDK for telegram bot microservice',
     long_description=README,
     long_description_content_type='text/markdown',
     url='https://github.com/rtsoftSG/tgbot-py',
     packages=setuptools.find_packages(),
     license='MIT',
     include_package_data=True,
     install_requires=['opentracing', 'opentracing-instrumentation', 'jaeger-client', "requests"],
     classifiers=[
         'License :: OSI Approved :: MIT License',
         'Programming Language :: Python :: 3',
         'Programming Language :: Python :: 3.7',
     ],
)
