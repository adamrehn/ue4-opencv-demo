OpenCV Integration Demo for UE4 with conan-ue4cli
=================================================

This repository contains demo code for using the Conan packages from the [conan-ue4cli](https://github.com/adamrehn/conan-ue4cli) repository to build a custom OpenCV package that links against the UE4-bundled versions of zlib and libpng, and then consume the custom-built OpenCV package in a simple UE4 project.

**You can find the full details of the conan-ue4cli workflow in this article: <http://adamrehn.com/articles/cross-platform-library-integration-in-unreal-engine-4/>.**

Note that Unreal Engine **4.19.0 or newer** is required.


Step 1: Installing the conan-ue4cli wrapper packages
----------------------------------------------------

Follow the instructions from the README of the [conan-ue4cli](https://github.com/adamrehn/conan-ue4cli) repository to generate and install the wrapper packages for the UE4-bundled libraries.


Step 2: Compiling our custom OpenCV build
-----------------------------------------

The [packages](./packages/) directory contains a Conan recipe for our custom build of OpenCV that uses the UE4-bundled versions of zlib and libpng.

To build the OpenCV package, run `python3 ./build.py` from the `packages/opencv-ue4` subdirectory.


Step 3: Building and running the UE4 test project
-------------------------------------------------

The [project](./project/) directory contains a simple UE4 test project that consumes the Conan package we created in Step 2. Open the file `project/OpenCVDemo/OpenCVDemo.uproject` in the Unreal Editor and allow it to compile the modules for the project.

The build rules for the project are in [project/OpenCVDemo/Source/OpenCVDemo/OpenCVDemo.Build.cs](./project/OpenCVDemo/Source/OpenCVDemo/OpenCVDemo.Build.cs). The code in this file invokes `conan install` as a child process in the root directory of the project and then parses the JSON output to retrieve the build flags from Conan and pass them to UnrealBuildTool. Under Windows, you will see a command window flash briefly during the build process - this is the Conan command being run by UnrealBuildTool.

Once the project has built, select the map **"default.umap"** and hit the Play button. The text "3.3.0" should appear in the top-left of the game preview. If you open the level blueprint for the map, you can see that this is the OpenCV version string that is being retrieved and printed.

The source code for the "Get OpenCV Version" blueprint function is in [project/OpenCVDemo/Source/OpenCVDemo/OpenCVBlueprint.cpp](./project/OpenCVDemo/Source/OpenCVDemo/OpenCVBlueprint.cpp). It simply includes the OpenCV `<opencv2/core/version.hpp>` header and casts the `CV_VERSION` macro to an `FString` instance.
