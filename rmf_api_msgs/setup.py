from glob import glob
from setuptools import find_packages, setup

package_name = "rmf_api_msgs"

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/' + package_name, ['package.xml']),
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        (
            'share/' + package_name + '/schemas',
            glob('schemas/*.schema.json')),
    ],
    install_requires=['setuptools'],
    author='Youliang',
    author_email='youliang@openrobotics.org',
    zip_safe=True,
    maintainer='youliang',
    maintainer_email='youliang@openrobotics.org',
    description='A package containing api schemas for rmf',
    license='Apache License Version 2.0',
    # entry_points={
    #     'console_scripts': [
    #     ],
    # },
)
