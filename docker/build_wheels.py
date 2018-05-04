import os
import subprocess

CYTHON_VERSION = '0.27.3'
CUPY_VERSION = '4.0.0'
PYNVVL_VERSION = '0.0.1'

WHEEL_CONFIGS = {
    '8.0': {
        'lib': 'docker/lib/cuda-8.0',
        'tag': 'mitmul/pynvvl:cuda-8.0-wheels',
        'test': 'mitmul/pynvvl:cuda-8.0-test',
    },
    '9.0': {
        'lib': 'docker/lib/cuda-9.0',
        'tag': 'mitmul/pynvvl:cuda-9.0-wheels',
        'test': 'mitmul/pynvvl:cuda-9.0-test',
    },
    '9.1': {
        'lib': 'docker/lib/cuda-9.1',
        'tag': 'mitmul/pynvvl:cuda-9.1-wheels',
        'test': 'mitmul/pynvvl:cuda-9.1-test',
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


def build_docker_image(cuda_version, tag, test):
    python_versions = ' '.join(PYTHON_VERSIONS.keys())
    cudda_version_no_dot = cuda_version.replace('.', '')
    subprocess.call([
        'docker', 'build',
        '--build-arg', 'cuda_version={}'.format(cuda_version),
        '--build-arg', 'python_versions={}'.format(python_versions),
        '--build-arg', 'cython_version={}'.format(CYTHON_VERSION),
        '--build-arg', 'cupy_version={}'.format(CUPY_VERSION),
        '--build-arg', 'cupy_package_name=cupy-cuda{}'.format(
            cudda_version_no_dot),
        '-t', tag,
        '-f', 'docker/Dockerfile.wheels', 'docker'
    ])
    subprocess.call([
        'docker', 'build',
        '--build-arg', 'cuda_version={}'.format(cuda_version),
        '--build-arg', 'python_versions={}'.format(python_versions),
        '--build-arg', 'cython_version={}'.format(CYTHON_VERSION),
        '--build-arg', 'cupy_version={}'.format(CUPY_VERSION),
        '--build-arg', 'pynvvl_version={}'.format(PYNVVL_VERSION),
        '--build-arg', 'cupy_package_name=cupy-cuda{}'.format(
            cudda_version_no_dot),
        '-t', test,
        '-f', 'docker/Dockerfile.test', 'docker'
    ])


def build_wheels(cuda_version, tag):
    for python_version in PYTHON_VERSIONS.keys():
        print('-' * 10,
              'Building for Python {}'.format(python_version),
              '-' * 10)
        subprocess.call(
            'nvidia-docker run'
            ' --rm'
            ' -v {source_dir}:/pynvvl'
            ' -t {tag}'
            ' bash -c'
            ' " \
            find / -name \"*libnvcuvid.so.1\" | \
            xargs -IXXX ln -s XXX /usr/local/lib/libnvcuvid.so && \
            pyenv global {python_version} && pyenv rehash && \
            cd /pynvvl && python setup.py bdist_wheel \
            -d dist/cuda-{cuda_version} \
            --package-name {package_name} \
            "'.format(
                source_dir=os.getcwd(),
                tag=tag,
                python_version=python_version,
                cuda_version=cuda_version,
                package_name='pynvvl_cuda{}'.format(
                    cuda_version.replace('.', '')),
            ), shell=True)

    subprocess.call(
        'nvidia-docker run'
        ' --rm'
        ' -v {source_dir}:/pynvvl'
        ' -t {tag}'
        ' bash -c'
        ' " \
        for file in \$(ls /pynvvl/dist/cuda-{cuda_version}/*.whl); \
        do \
            echo \$file | \
            sed --expression=\"s/linux/manylinux1/g\" | \
            xargs -IXXX mv \$file XXX; \
        done; \
        "'.format(
            source_dir=os.getcwd(),
            tag=tag,
            cuda_version=cuda_version,
        ), shell=True)

    for python_version in PYTHON_VERSIONS.keys():
        print('-' * 10,
              'Testing wheel for Python {}'.format(python_version),
              '-' * 10)
        if python_version.startswith('2.7'):
            package_python = 'cp27-cp27mu'
        elif python_version.startswith('3.4'):
            package_python = 'cp34-cp34m'
        elif python_version.startswith('3.5'):
            package_python = 'cp35-cp35m'
        elif python_version.startswith('3.6'):
            package_python = 'cp36-cp36m'
        else:
            raise ValueError('unknown python version')

        # Test the wheel
        subprocess.call(
            'nvidia-docker run'
            ' --rm'
            ' -v {source_dir}/examples:/examples'
            ' -v {source_dir}/dist/cuda-{cuda_version}:/wheels'
            ' -t {tag}'
            ' bash -c'
            ' " \
            pyenv global {python_version} && pyenv rehash && \
            pip install /wheels/{package_name}-{pynvvl_version}-{package_python}-manylinux1_x86_64.whl && \
            cd / && python examples/simple_load.py \
            >> /examples/cuda-{cuda_version}_python-{python_version}.out \
            "'.format(
                source_dir=os.getcwd(),
                tag=tag,
                cuda_version=cuda_version,
                pynvvl_version=PYNVVL_VERSION,
                python_version=python_version,
                package_python=package_python,
                package_name='pynvvl_cuda{}'.format(
                    cuda_version.replace('.', '')),
            ), shell=True)

# Build Docker images
for cuda_version, wheel_config in WHEEL_CONFIGS.items():
    build_docker_image(cuda_version, wheel_config['tag'], wheel_config['test'])

# Build wheels
for cuda_version, wheel_config in WHEEL_CONFIGS.items():
    print('-' * 10, 'Building for CUDA {}'.format(cuda_version), '-' * 10)
    build_wheels(cuda_version, wheel_config['tag'])
    print('=' * 30)
