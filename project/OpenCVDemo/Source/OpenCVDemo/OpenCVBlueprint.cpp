// Fill out your copyright notice in the Description page of Project Settings.

#include "OpenCVBlueprint.h"
#include <opencv2/core/version.hpp>

FString UOpenCVBlueprint::GetOpenCvVersion() {
	return FString(CV_VERSION);
}
