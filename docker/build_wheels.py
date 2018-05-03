import os
import subprocess

CYTHON_VERSION = '0.27.3'

WHEEL_CONFIGS = {
    '8.0': {
        'name': 'pynvvl-cuda80',
        'image': 'nvidia/cuda:8.0-cudnn7-devel-centos6',
        'lib': 'docker/lib/cuda-8.0',
        'tag': 'mitmul/pynvvl:cuda-8.0-dev',
    },
    '9.0': {
        'name': 'pynvvl-cuda90',
        'image': 'nvidia/cuda:9.0-cudnn7-devel-centos6',
        'lib': 'docker/lib/cuda-9.0',
        'tag': 'mitmul/pynvvl:cuda-9.0-dev',
    },
    '9.1': {
        'name': 'pynvvl-cuda91',
        'image': 'nvidia/cuda:9.1-cudnn7-devel-centos6',
        'lib': 'docker/lib/cuda-9.1',
        'tag': 'mitmul/pynvvl:cuda-9.1-dev',
    },
}

PYTHON_VERSIONS = {
    '2.7.6': {
        'python_tag': 'cp27',
        'linux_abi_tag': 'cp27mu',
    },
    '3.4.7': {
        'python_tag': 'cp34',
        'linux_abi_tag': 'cp34m',
    },
    '3.5.1': {
        'python_tag': 'cp35',
        'linux_abi_tag': 'cp35m',
    },
    '3.6.0': {
        'python_tag': 'cp36',
        'linux_abi_tag': 'cp36m',
    },
}


def build_docker_image(base_image, tag):
    python_versions = ' '.join(PYTHON_VERSIONS.keys())
    subprocess.call([
        'docker', 'build',
        '--build-arg', 'base_image={}'.format(base_image),
        '--build-arg', 'python_versions={}'.format(python_versions),
        '--build-arg', 'cython_version={}'.format(CYTHON_VERSION),
        '-t', tag,
        '-f', 'docker/Dockerfile.wheels', 'docker'
    ])


def build_wheels(lib_dir, tag, python_version):
    for python_version in PYTHON_VERSIONS.keys():

        subprocess.call(
            'nvidia-docker run'
            ' --rm'
            ' -v {lib_dir}:/prebuilt_libs'
            ' -v {source_dir}:/pynvvl'
            ' -t {tag}'
            ' bash -c'
            ' "find / -name \"*libnvcuvid.so.1\" | \
            xargs -IXXX ln -s XXX /usr/local/lib/libnvcuvid.so && \
            pyenv global {python_version} && \
            pyenv rehash && \
            export CPATH=/opt/pyenv/versions/{python_version}/include/python2.7 && \
            cd /pynvvl && \
            python setup.py bdist_wheel && \
            if [ ! -d dist/cuda-{cuda_version} ]; then \
                mkdir -p dist/cuda-{cuda_version}; \
            fi && \
            ls dist/*.whl | \
            xargs -IXXX mv XXX dist/cuda-{cuda_version}/"'.format(
                lib_dir=os.path.join(os.getcwd(), lib_dir),
                source_dir=os.getcwd(),
                tag=tag,
                python_version=python_version,
                cuda_version=os.path.basename(lib_dir)
            ), shell=True)


# Build Docker images
for wheel_config in WHEEL_CONFIGS.values():
    build_docker_image(wheel_config['image'], wheel_config['tag'])

# Build wheels
for wheel_config in WHEEL_CONFIGS.values():
    for python_version in PYTHON_VERSIONS.keys():
        build_wheels(
            wheel_config['lib'], wheel_config['tag'], python_version)
