from conans import ConanFile, CMake, tools

class OpenCVUE4Conan(ConanFile):
    name = "opencv-ue4"
    version = "3.3.0"
    url = "https://github.com/adamrehn/ue4-opencv-demo"
    description = "OpenCV custom build for UE4"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    requires = (
        "libcxx/ue4@adamrehn/profile",
        "ue4util/ue4@adamrehn/profile"
    )
    
    def requirements(self):
        self.requires("zlib/ue4@adamrehn/{}".format(self.channel))
        self.requires("UElibPNG/ue4@adamrehn/{}".format(self.channel))
    
    def cmake_flags(self):
        flags = [
            
            # Disable a whole bunch of external dependencies
            "-DENABLE_IMPL_COLLECTION=OFF", "-DENABLE_INSTRUMENTATION=OFF", "-DENABLE_NOISY_WARNINGS=OFF",
            "-DENABLE_POPCNT=OFF", "-DENABLE_SOLUTION_FOLDERS=ON", "-DINSTALL_CREATE_DISTRIB=OFF",
            "-DINSTALL_C_EXAMPLES=OFF", "-DINSTALL_PYTHON_EXAMPLES=OFF", "-DINSTALL_TESTS=OFF",
            "-DBUILD_SHARED_LIBS=OFF", "-DBUILD_TESTS=OFF","-DBUILD_PERF_TESTS=OFF", 
            "-DBUILD_opencv_python2=OFF", "-DBUILD_opencv_python3=OFF", "-DBUILD_CUDA_STUBS=OFF",
            "-DWITH_CLP=OFF", "-DWITH_CSTRIPES=OFF", "-DWITH_CUBLAS=OFF", "-DWITH_CUDA=OFF",
            "-DWITH_CUFFT=OFF", "-DWITH_DIRECTX=OFF", "-DWITH_DSHOW=OFF", "-DWITH_EIGEN=OFF",
            "-DWITH_FFMPEG=OFF", "-DWITH_GDAL=OFF", "-DWITH_GDCM=OFF", "-DWITH_GIGEAPI=OFF",
            "-DWITH_GSTREAMER=OFF", "-DWITH_GSTREAMER_0_10=OFF", "-DWITH_INTELPERC=OFF",
            "-DWITH_IPP=OFF", "-DWITH_IPP_A=OFF", "-DWITH_JASPER=OFF", "-DWITH_JPEG=OFF",
            "-DWITH_LAPACK=OFF", "-DWITH_MATLAB=OFF", "-DWITH_MSMF=OFF", "-DWITH_OPENCL=OFF",
            "-DWITH_OPENCLAMDBLAS=OFF", "-DWITH_OPENCLAMDFFT=OFF", "-DWITH_OPENCL_SVM=OFF",
            "-DWITH_OPENEXR=OFF", "-DWITH_OPENGL=OFF", "-DWITH_OPENMP=OFF", "-DWITH_OPENNI=OFF",
            "-DWITH_OPENNI2=OFF", "-DWITH_OPENVX=OFF", "-DWITH_PVAPI=OFF", "-DWITH_QT=OFF",
            "-DWITH_TBB=OFF", "-DWITH_TIFF=OFF", "-DWITH_VFW=OFF", "-DWITH_VTK=OFF",
            "-DWITH_WEBP=OFF", "-DWITH_WIN32UI=OFF", "-DWITH_XIMEA=OFF", "-DWITH_ITT=OFF",
            "-DBUILD_WITH_STATIC_CRT=OFF",
            
            # Just build a few core modules
            "-DBUILD_opencv_apps=OFF", "-DBUILD_opencv_calib3d=OFF", "-DBUILD_opencv_core=ON",
            "-DBUILD_opencv_cudaarithm=OFF", "-DBUILD_opencv_cudabgsegm=OFF", "-DBUILD_opencv_cudacodec=OFF",
            "-DBUILD_opencv_cudafeatures2d=OFF", "-DBUILD_opencv_cudafilters=OFF", "-DBUILD_opencv_cudaimgproc=OFF",
            "-DBUILD_opencv_cudalegacy=OFF", "-DBUILD_opencv_cudaobjdetect=OFF", "-DBUILD_opencv_cudaoptflow=OFF",
            "-DBUILD_opencv_cudastereo=OFF", "-DBUILD_opencv_cudawarping=OFF", "-DBUILD_opencv_cudev=OFF",
            "-DBUILD_opencv_dnn=OFF", "-DBUILD_opencv_features2d=ON", "-DBUILD_opencv_flann=ON",
            "-DBUILD_opencv_highgui=OFF", "-DBUILD_opencv_imgcodecs=ON", "-DBUILD_opencv_imgproc=ON",
            "-DBUILD_opencv_ml=OFF", "-DBUILD_opencv_objdetect=OFF", "-DBUILD_opencv_photo=OFF",
            "-DBUILD_opencv_shape=OFF", "-DBUILD_opencv_stitching=OFF", "-DBUILD_opencv_superres=OFF",
            "-DBUILD_opencv_ts=OFF", "-DBUILD_opencv_video=OFF", "-DBUILD_opencv_videoio=OFF",
            "-DBUILD_opencv_videostab=OFF", "-DBUILD_opencv_world=OFF",
            
            "-DWITH_PNG=ON",
            "-DBUILD_ZLIB=OFF", # Don't use bundled zlib, since we use the version from UE4
            "-DBUILD_PNG=OFF"   # Don't use bundled libpng, since we use the version from UE4
        ]
        
        # Append the flags to ensure OpenCV's FindXXX modules use our UE4-specific dependencies
        from ue4util import Utility
        zlib = self.deps_cpp_info["zlib"]
        libpng = self.deps_cpp_info["UElibPNG"]
        flags.extend([
            "-DPNG_PNG_INCLUDE_DIR=" + libpng.include_paths[0],
            "-DPNG_LIBRARY=" + Utility.resolve_file(libpng.lib_paths[0], libpng.libs[0]),
            "-DZLIB_INCLUDE_DIR=" + zlib.include_paths[0],
            "-DZLIB_LIBRARY=" + Utility.resolve_file(zlib.lib_paths[0], zlib.libs[0])
        ])
        return flags
    
    def source(self):
        self.run("git clone --depth=1 https://github.com/opencv/opencv.git -b {}".format(self.version))
        
        # Disable binary prefixing for installed libs under Windows
        tools.replace_in_file(
            "opencv/CMakeLists.txt",
            '''ocv_update(OPENCV_LIB_INSTALL_PATH   "${OpenCV_INSTALL_BINARIES_PREFIX}staticlib${LIB_SUFFIX}")''',
            '''ocv_update(OPENCV_LIB_INSTALL_PATH   "lib")'''
        )
        
    def build(self):
        
        # Under Linux, restore CC and CXX if the current Conan profile has overridden them
        from libcxx import LibCxx
        LibCxx.set_vars(self)
        
        # Build OpenCV
        cmake = CMake(self)
        cmake.configure(source_folder="opencv", args=self.cmake_flags())
        cmake.build()
        cmake.install()
    
    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
