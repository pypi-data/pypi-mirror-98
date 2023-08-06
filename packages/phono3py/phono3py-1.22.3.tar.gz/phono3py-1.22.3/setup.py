import os
import sys
import numpy
import platform
import sysconfig

try:
    from setuptools import setup, Extension
    use_setuptools = True
    print("setuptools is used.")
except ImportError:
    from distutils.core import setup, Extension
    use_setuptools = False
    print("distutils is used.")

try:
    from setuptools_scm import get_version
except ImportError:
    git_num = None

if 'setuptools_scm' in sys.modules.keys():
    try:
        git_ver = get_version()
        git_num = int(git_ver.split('.')[3].split('+')[0].replace("dev", ""))
    except:
        git_num = None

include_dirs_numpy = [numpy.get_include()]
extra_link_args = []
# Workaround Python issue 21121
config_var = sysconfig.get_config_var("CFLAGS")
if (config_var is not None and
    "-Werror=declaration-after-statement" in config_var):
    os.environ['CFLAGS'] = config_var.replace(
        "-Werror=declaration-after-statement", "")

extra_compile_args = ['-fopenmp', ]
include_dirs = ['c', ] + include_dirs_numpy
define_macros = []

extra_link_args_lapacke = []
include_dirs_lapacke = []


use_mkl = False
# C macro definitions:
# - MULTITHREADED_BLAS
#   This deactivates OpenMP multithread harmonic phonon calculation,
#   since inside each phonon calculation, zheev is called.
#   When using multithread BLAS, this macro has to be set and
#   by this all phonons on q-points should be calculated in series.
# - MKL_LAPACKE:
#   This sets definitions and functions needed when using MKL lapacke.
#   Phono3py complex values are handled based on those provided by Netlib
#   lapacke. However MKL lapacke doesn't provide some macros and functions
#   that provided Netlib. This macro defines those used in phono3py among them.
if os.path.isfile("setup_mkl.py"):
    # This supposes that MKL multithread BLAS is used.
    # This is invoked when setup_mkl.py exists on the current directory.

    print("MKL LAPACKE is to be used.")
    print("Use of icc is assumed (CC='icc').")

    from setup_mkl import mkl_extra_link_args_lapacke, mkl_include_dirs_lapacke

    #### Examples of setup_mkl.py ####
    # For 2015
    # intel_root = "/opt/intel/composer_xe_2015.7.235"
    # mkl_root = "%s/mkl" % intel_root
    # compiler_root = "%s/compiler" % intel_root
    #
    # For 2016
    # intel_root = "/opt/intel/parallel_studio_xe_2016"
    # mkl_root = "%s/mkl" % intel_root
    # compiler_root = "%s" % intel_root
    #
    # For both
    # mkl_extra_link_args_lapacke = ['-L%s/lib/intel64' % mkl_root,
    #                                '-lmkl_rt']
    # mkl_extra_link_args_lapacke += ['-L%s/lib/intel64' % compiler_root,
    #                                 '-lsvml',
    #                                 '-liomp5',
    #                                 '-limf',
    #                                 '-lpthread']
    # mkl_include_dirs_lapacke = ["%s/include" % mkl_root]

    use_mkl = True
    extra_link_args_lapacke += mkl_extra_link_args_lapacke
    include_dirs_lapacke += mkl_include_dirs_lapacke

    if use_setuptools:
        extra_compile_args += ['-DMKL_LAPACKE',
                               '-DMULTITHREADED_BLAS']
    else:
        define_macros += [('MKL_LAPACKE', None),
                          ('MULTITHREADED_BLAS', None)]
elif os.path.isfile("libopenblas.py"):
    # This supposes that multithread openBLAS is used.
    # This is invoked when libopenblas.py exists on the current directory.

    #### Example of libopenblas.py ####
    # extra_link_args_lapacke += ['-lopenblas']

    from libopenblas import extra_link_args_lapacke, include_dirs_lapacke
    include_dirs_lapacke += []
    if use_setuptools:
        extra_compile_args += ['-DMULTITHREADED_BLAS']
    else:
        define_macros += [('MULTITHREADED_BLAS', None)]
elif (platform.system() == 'Darwin' and
      os.path.isfile('/opt/local/lib/libopenblas.a')):
    # This supposes lapacke with single-thread openBLAS provided by MacPort is
    # used.
    # % sudo port install gcc6
    # % sudo port select --set gcc mp-gcc
    # % sudo port install OpenBLAS +gcc6
    extra_link_args_lapacke += ['/opt/local/lib/libopenblas.a']
    include_dirs_lapacke += ['/opt/local/include']
elif ('CONDA_PREFIX' in os.environ and
      (os.path.isfile(os.path.join(os.environ['CONDA_PREFIX'],
                                   'lib', 'liblapacke.dylib')) or
       os.path.isfile(os.path.join(os.environ['CONDA_PREFIX'],
                                   'lib', 'liblapacke.so')))):
    # This is for the system prepared with conda openblas.
    extra_link_args_lapacke += ['-llapacke']
    include_dirs_lapacke += [
        os.path.join(os.environ['CONDA_PREFIX'], 'include'), ]
    if os.path.isfile(os.path.join(os.environ['CONDA_PREFIX'],
                                   'include', 'mkl.h')):
        use_mkl = True
        if use_setuptools:
            extra_compile_args += ['-DMKL_LAPACKE',
                                   '-DMULTITHREADED_BLAS']
        else:
            define_macros += [('MKL_LAPACKE', None),
                              ('MULTITHREADED_BLAS', None)]
    else:
        if use_setuptools:
            extra_compile_args += ['-DMULTITHREADED_BLAS']
        else:
            define_macros += [('MULTITHREADED_BLAS', None)]
elif os.path.isfile('/usr/lib/liblapacke.so'):
    # This supposes that lapacke with single-thread BLAS is installed on
    # system.
    extra_link_args_lapacke += ['-llapacke', '-llapack', '-lblas']
    include_dirs_lapacke += []
else:
    # Here is the default lapacke linkage setting.
    # Please modify according to your system environment.
    # Without using multithreaded BLAS, DMULTITHREADED_BLAS is better to be
    # removed to activate OpenMP multithreading harmonic phonon calculation,
    # but this is not mandatory.
    #
    # The below supposes that lapacke with multithread openblas is used.
    # Even if using single-thread BLAS and deactivating OpenMP
    # multithreading for harmonic phonon calculation, the total performance
    # decrease is considered marginal.
    #
    # For conda: Try installing with dynamic link library of openblas by
    # % conda install numpy scipy h5py pyyaml matplotlib openblas libgfortran
    extra_link_args_lapacke += ['-lopenblas', '-lgfortran']
    if 'CONDA_PREFIX' in os.environ:
        include_dirs_lapacke += [
            os.path.join(os.environ['CONDA_PREFIX'], 'include'), ]
    if use_setuptools:
        extra_compile_args += ['-DMULTITHREADED_BLAS']
    else:
        define_macros += [('MULTITHREADED_BLAS', None)]

cc = None
lib_omp = None
if 'CC' in os.environ:
    if 'clang' in os.environ['CC']:
        cc = 'clang'
        if not use_mkl:
            lib_omp = '-lomp'
        # lib_omp = '-liomp5'
    if 'gcc' in os.environ['CC'] or 'gnu-cc' in os.environ['CC']:
        cc = 'gcc'
if cc == 'gcc' or cc is None:
    lib_omp = '-lgomp'

    if 'CC' in os.environ and 'gcc-' in os.environ['CC']:
        # For macOS & homebrew gcc:
        # Using conda's gcc is more recommended though. Suppose using
        # homebrew gcc whereas conda is used as general environment.
        # This is to avoid linking conda libgomp that is incompatible
        # with homebrew gcc.
        try:
            v = int(os.environ['CC'].split('-')[1])
        except ValueError:
            pass
        else:
            ary = [os.sep, "usr", "local", "opt", "gcc@%d" % v, "lib", "gcc",
                   "%d" % v, "libgomp.a"]
            libgomp_a = os.path.join(*ary)
            if os.path.isfile(libgomp_a):
                lib_omp = libgomp_a

if lib_omp:
    extra_link_args.append(lib_omp)

## Uncomment below to measure reciprocal_to_normal_squared_openmp performance
# define_macros += [('MEASURE_R2N', None)]

extra_link_args += extra_link_args_lapacke
include_dirs += include_dirs_lapacke

print("extra_link_args", extra_link_args)
sources_phono3py = ['c/_phono3py.c',
                    'c/collision_matrix.c',
                    'c/fc3.c',
                    'c/imag_self_energy_with_g.c',
                    'c/interaction.c',
                    'c/isotope.c',
                    'c/kgrid.c',
                    'c/kpoint.c',
                    'c/lapack_wrapper.c',
                    'c/mathfunc.c',
                    'c/phono3py.c',
                    'c/phonoc_utils.c',
                    'c/pp_collision.c',
                    'c/real_self_energy.c',
                    'c/real_to_reciprocal.c',
                    'c/reciprocal_to_normal.c',
                    'c/tetrahedron_method.c',
                    'c/triplet.c',
                    'c/triplet_iw.c',
                    'c/triplet_kpoint.c']
extension_phono3py = Extension(
    'phono3py._phono3py',
    include_dirs=include_dirs,
    extra_compile_args=extra_compile_args,
    extra_link_args=extra_link_args,
    define_macros=define_macros,
    sources=sources_phono3py)

sources_phononmod = ['c/_phononmod.c',
                     'c/dynmat.c',
                     'c/lapack_wrapper.c',
                     'c/phonon.c',
                     'c/phononmod.c']
extension_phononmod = Extension(
    'phono3py._phononmod',
    include_dirs=include_dirs,
    extra_compile_args=extra_compile_args,
    extra_link_args=extra_link_args,
    sources=sources_phononmod)

sources_lapackepy = ['c/_lapackepy.c',
                     'c/lapack_wrapper.c']
extension_lapackepy = Extension(
    'phono3py._lapackepy',
    extra_compile_args=extra_compile_args,
    extra_link_args=extra_link_args,
    include_dirs=include_dirs,
    sources=sources_lapackepy)

packages_phono3py = ['phono3py',
                     'phono3py.cui',
                     'phono3py.interface',
                     'phono3py.other',
                     'phono3py.phonon',
                     'phono3py.phonon3',
                     'phono3py.sscha']
scripts_phono3py = ['scripts/phono3py',
                    'scripts/phono3py-load',
                    'scripts/phono3py-kaccum',
                    'scripts/phono3py-kdeplot',
                    'scripts/phono3py-coleigplot']

########################
# _lapackepy extension #
########################

if __name__ == '__main__':
    version_nums = [None, None, None]
    with open("phono3py/version.py") as w:
        for line in w:
            if "__version__" in line:
                for i, num in enumerate(
                        line.split()[2].strip('\"').split('.')):
                    version_nums[i] = num
                break

    # To deploy to pypi by travis-CI
    if os.path.isfile("__nanoversion__.txt"):
        nanoversion = 0
        with open('__nanoversion__.txt') as nv:
            try:
                for line in nv:
                    nanoversion = int(line.strip())
                    break
            except ValueError:
                nanoversion = 0
        if nanoversion != 0:
            version_nums.append(nanoversion)
    elif git_num:
        version_nums.append(git_num)

    if None in version_nums:
        print("Failed to get version number in setup.py.")
        raise

    version = ".".join(["%s" % n for n in version_nums[:3]])
    if len(version_nums) > 3:
        version += "-%d" % version_nums[3]

    if use_setuptools:
        setup(name='phono3py',
              version=version,
              description='This is the phono3py module.',
              author='Atsushi Togo',
              author_email='atz.togo@gmail.com',
              url='http://phonopy.github.io/phono3py/',
              packages=packages_phono3py,
              install_requires=['numpy', 'scipy', 'PyYAML', 'matplotlib',
                                'h5py', 'spglib', 'phonopy>=2.9.3,<2.10'],
              provides=['phono3py'],
              scripts=scripts_phono3py,
              ext_modules=[extension_phono3py,
                           extension_lapackepy,
                           extension_phononmod])
    else:
        setup(name='phono3py',
              version=version,
              description='This is the phono3py module.',
              author='Atsushi Togo',
              author_email='atz.togo@gmail.com',
              url='http://phonopy.github.io/phono3py/',
              packages=packages_phono3py,
              requires=['numpy', 'scipy', 'PyYAML', 'matplotlib', 'h5py',
                        'phonopy', 'spglib'],
              provides=['phono3py'],
              scripts=scripts_phono3py,
              ext_modules=[extension_phono3py,
                           extension_lapackepy,
                           extension_phononmod])
