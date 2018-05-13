# OpenCV Integration Demo for UE4 with conan-ue4cli

This repository contains demo code for using the Conan packages from the [conan-ue4cli](https://github.com/adamrehn/conan-ue4cli) repository to build a custom OpenCV package that links against the UE4-bundled versions of zlib and libpng, and then consume the custom-built OpenCV package in a simple UE4 project.

**You can find the full details of the conan-ue4cli workflow in this article: <http://adamrehn.com/articles/cross-platform-library-integration-in-unreal-engine-4/>.**

Note that Unreal Engine **4.19.0 or newer** is required.


## Contents

- [Building the demo](#building-the-demo)
    - [Step 1: Installing the conan-ue4cli wrapper packages](#step-1-installing-the-conan-ue4cli-wrapper-packages)
    - [Step 2: Compiling our custom OpenCV build](#step-2-compiling-our-custom-opencv-build)
    - [Step 3: Building and running the UE4 test project](#step-3-building-and-running-the-ue4-test-project)
- [Performing automated builds with Jenkins](#performing-automated-builds-with-jenkins)


## Building the demo

### Step 1: Installing the conan-ue4cli wrapper packages

Follow the instructions from the README of the [conan-ue4cli](https://github.com/adamrehn/conan-ue4cli) repository to generate and install the wrapper packages for the UE4-bundled libraries.

### Step 2: Compiling our custom OpenCV build

The [packages](./packages/) directory contains a Conan recipe for our custom build of OpenCV that uses the UE4-bundled versions of zlib and libpng.

To build the OpenCV package, run `python3 ./build.py` from the `packages/opencv-ue4` subdirectory.

### Step 3: Building and running the UE4 test project

The [project](./project/) directory contains a simple UE4 test project that consumes the Conan package we created in Step 2. Open the file `project/OpenCVDemo/OpenCVDemo.uproject` in the Unreal Editor and allow it to compile the modules for the project.

The build rules for the project are in [project/OpenCVDemo/Source/OpenCVDemo/OpenCVDemo.Build.cs](./project/OpenCVDemo/Source/OpenCVDemo/OpenCVDemo.Build.cs). The code in this file invokes `conan install` as a child process in the root directory of the project and then parses the JSON output to retrieve the build flags from Conan and pass them to UnrealBuildTool. Under Windows, you will see a command window flash briefly during the build process - this is the Conan command being run by UnrealBuildTool.

Once the project has built, select the map **"default.umap"** and hit the Play button. The text "3.3.0" should appear in the top-left of the game preview. If you open the level blueprint for the map, you can see that this is the OpenCV version string that is being retrieved and printed.

The source code for the "Get OpenCV Version" blueprint function is in [project/OpenCVDemo/Source/OpenCVDemo/OpenCVBlueprint.cpp](./project/OpenCVDemo/Source/OpenCVDemo/OpenCVBlueprint.cpp). It simply includes the OpenCV `<opencv2/core/version.hpp>` header and casts the `CV_VERSION` macro to an `FString` instance.


## Performing automated builds with Jenkins

Example Jenkinsfiles are provided that use the Windows and Linux Docker images from [docker-ue4](https://github.com/adamrehn/ue4-docker) to build both the custom OpenCV Conan package and the UE4 project that consumes it. Performing an automated build requires a bit of up-front configuration to get working but is extremely straightforward once the required infrastructure is in place.

To get everything up and running:

1. Follow the instructions in the [docker-ue4](https://github.com/adamrehn/ue4-docker) repository README to create the Docker images for Unreal Engine 4 that will be used for performing builds. **The example Jenkinsfile requires Unreal Engine 4.19.1.** Create a Windows Docker image on a Windows host and a Linux Docker image on either a Linux or macOS host (Linux is recommended since a macOS host will require additional configuration to set the appropriate memory and disk limits.) Note that the example code does not currently support Linux containers running under a Windows host.

2. Next, spin up two Docker containers for the required servers:
    - Start an instance of [JFrog Artifactory Community Edition for C/C++](https://jfrog.com/blog/announcing-jfrog-artifactory-community-edition-c-c/) using the `docker.bintray.io/jfrog/artifactory-cpp-ce` Docker image.
    - Start an instance of [Jenkins](https://jenkins.io/) using the `jenkins/jenkins` Docker image. The `latest` tag is recommended since a recent version of Jenkins with the latest version of the [Pipeline Plugin](https://wiki.jenkins.io/display/JENKINS/Pipeline+Plugin) is required.

3. Run through the setup wizard to configure the Artifactory CE instance. At the end of the wizard, opt to create a Conan repository. This will create a repository called `conan-local` that will be used to store the packages produced by the automated build process.

4. Run through the setup wizard to configure the Jenkins instance. Be sure to install the following plugins:
    - [Git Plugin](https://wiki.jenkins.io/display/JENKINS/Git+Plugin)
    - [Pipeline Plugin](https://wiki.jenkins.io/display/JENKINS/Pipeline+Plugin)
    - [Windows Slaves Plugin](https://wiki.jenkins.io/display/JENKINS/Windows+Slaves+Plugin)

5. Configure the Jenkins build agents:
    - Add the Windows host (the one with the UE4 Windows Docker image) as a permanent build agent with the label `windows-containers`.
    - Add the Linux/macOS host (the one with the UE4 Linux Docker image) as a permanent build agent with the label `linux-containers`.

6. Configure the Jenkins credentials related to the Conan repository:
    - Add a Secret Text with ID `jenkins-conan-server` containing the Conan repository URL (you can find this by selecting `conan-local` from the "Set Me Up" section of the web interface of the Artifactory instance.)
    - Add a Secret Text with ID `jenkins-conan-username` containing the administrator username for the Artifactory instance.
    - Add a Secret Text with ID `jenkins-conan-password` containing the administrator password for the Artifactory instance.

To build the custom OpenCV Conan package:

- Create a new Pipeline job with whatever name you like.
- Under the "Pipeline" section of the job configuration, set the Definition to *Pipeline script from SCM*.
- Set the SCM to *Git* and the Repository URL to `https://github.com/adamrehn/ue4-opencv-demo.git`. No credentials are required.
- Set the Script Path to `packages/opencv-ue4/Jenkinsfile`.
- Click "Save" and you will be taken to the job page for the newly-created job.
- To perform a build, simply click the "Build Now" button from the Jenkins job page.

To build the UE4 project:

- Create a new Pipeline job with whatever name you like.
- Under the "Pipeline" section of the job configuration, set the Definition to *Pipeline script from SCM*.
- Set the SCM to *Git* and the Repository URL to `https://github.com/adamrehn/ue4-opencv-demo.git`. No credentials are required.
- Set the Script Path to `project/OpenCVDemo/Jenkinsfile`.
- Click "Save" and you will be taken to the job page for the newly-created job.
- To perform a build, simply click the "Build Now" button from the Jenkins job page.
- Note that builds may take quite some time, particularly during the content cooking stage when shader compilation occurs.
