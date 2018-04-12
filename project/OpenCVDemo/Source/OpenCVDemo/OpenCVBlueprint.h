// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "OpenCVBlueprint.generated.h"

/**
 * 
 */
UCLASS()
class OPENCVDEMO_API UOpenCVBlueprint : public UBlueprintFunctionLibrary
{
	GENERATED_BODY()
	
	UFUNCTION(BlueprintCallable, Category = "OpenCV")
	static FString GetOpenCvVersion();
	
};
