import os
import sys
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

try:
    import pybind11
except ImportError:
    print("`pybind11` not found. Install `pybind11[global]>=2.6.0` first.")
    sys.exit(1)


root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
installed_dir = os.path.join(root, "install")
installed_include_dir = os.path.join(installed_dir, "include")
installed_webrtc_dir = os.path.join(installed_include_dir, "webrtc-audio-processing-2")
installed_lib_dir = os.path.join(installed_dir, "lib")

# define the extension modules
ext_modules = [
    Extension(
        name="webrtc_audio_processing",
        sources=["webrtc_audio_processing.cpp"],
        include_dirs=[
            pybind11.get_include(),  # pybind11 includes
            installed_include_dir,  # installed webrtc headers
            installed_webrtc_dir,
        ],
        libraries=["webrtc-audio-processing-2"],  # Link against the installed library
        library_dirs=[
            "/usr/local/lib",  # common installed location
            installed_lib_dir,  # local installed directory from meson build
        ],
        language="c++",
        define_macros=[("VERSION_INFO", '"dev"')],
    ),
]


class BuildExt(build_ext):
    """A custom build extension for adding compiler-specific options."""

    def build_extensions(self):
        # add C++ standard flag
        ct = self.compiler.compiler_type
        opts = []
        link_opts = []
        if ct == "unix":
            opts.append("-std=c++17")
            if sys.platform == "darwin":
                opts.append("-stdlib=libc++")
                link_opts.append("-stdlib=libc++")
        elif ct == "msvc":
            opts.append("/std:c++17")
        for ext in self.extensions:
            ext.extra_compile_args = opts
            ext.extra_link_args = link_opts
        super().build_extensions()


if __name__ == "__main__":
    setup(
        ext_modules=ext_modules,
        cmdclass={"build_ext": BuildExt},
        zip_safe=False,
        python_requires=">=3.8",
    )
