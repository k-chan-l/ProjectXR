// Fill out your copyright notice in the Description page of Project Settings.


#include "Data_Preprocessing/FloorPlanCapture.h"
#include "Components/SceneComponent.h"
#include "Components/SceneCaptureComponent2D.h"
#include "Kismet/KismetRenderingLibrary.h"
#include "RenderingThread.h"

// Sets default values
AFloorPlanCapture::AFloorPlanCapture()
{
 	// Set this actor to call Tick() every frame.  You can turn this off to improve performance if you don't need it.
	PrimaryActorTick.bCanEverTick = false;
	
	// root 생성 및 지정
	Root = CreateDefaultSubobject<USceneComponent>(TEXT("Root"));
	RootComponent = Root;
	
	// scene Capture 컴포넌트 생성 및 지정
	SceneCapture = CreateDefaultSubobject<USceneCaptureComponent2D>(TEXT("SceneCapture"));
	SceneCapture->SetupAttachment(RootComponent);
	// 도면용 기본 세팅
	SceneCapture->bCaptureEveryFrame = false;
	SceneCapture->bCaptureOnMovement = false;
	SceneCapture->ProjectionType = ECameraProjectionMode::Orthographic;
	// SceneCapture->OrthoWidth = 5000.0f; // 건물 크기에 맞게 조정
	SceneCapture->SetRelativeRotation(FRotator(-90.f, 0.f, 0.f));
	SceneCapture->CaptureSource = ESceneCaptureSource::SCS_FinalColorLDR;
	
	SceneCapture->ShowFlags.SetLighting(false);
	SceneCapture->ShowFlags.SetDynamicShadows(false);
	SceneCapture->ShowFlags.SetPostProcessing(false);
	SceneCapture->ShowFlags.SetAmbientOcclusion(false);
	SceneCapture->ShowFlags.SetFog(false);
}

// Called when the game starts or when spawned
void AFloorPlanCapture::BeginPlay()
{
	Super::BeginPlay();
	AlignToPlaneForMapCapture();
}

void AFloorPlanCapture::CaptureToFile(const FString& FileName)
{
	if (!SceneCapture || !SceneCapture->TextureTarget)
	{
		UE_LOG(LogTemp, Error, TEXT("TextureTarget is null"));
		return;
	}
	SceneCapture->CaptureScene();
	
	FlushRenderingCommands();

	FString FileDir = FPaths::ProjectDir() + TEXT("../Backend/Data/FloorPlan/");
	IFileManager::Get().MakeDirectory(*FileDir, true);

	UKismetRenderingLibrary::ExportRenderTarget(
		this,
		SceneCapture->TextureTarget,
		FileDir,
		FileName
	);

	UE_LOG(LogTemp, Warning, TEXT("Saved floor plan: %s%s"), *FileDir, *FileName);
}

void AFloorPlanCapture::AlignToPlaneForMapCapture()
{
	if (!FloorPlaneActor || !SceneCapture)
	{
		UE_LOG(LogTemp, Error, TEXT("FloorPlaneActor or SceneCapture is null"));
		return;
	}

	FVector PlaneOrigin;
	FVector PlaneExtent;
	FloorPlaneActor->GetActorBounds(true, PlaneOrigin, PlaneExtent);

	const float PlaneWidth  = PlaneExtent.X * 2.f;
	const float PlaneHeight = PlaneExtent.Y * 2.f;

	// 중심 위로만 이동
	const FVector CaptureLocation = PlaneOrigin + FVector(0.f, 0.f, 5000.f);
	SetActorLocation(CaptureLocation);

	// 회전은 건드리지 않음 (이미 수동으로 -90 맞췄다고 가정)
	SceneCapture->ProjectionType = ECameraProjectionMode::Orthographic;
	SceneCapture->OrthoWidth = FMath::Max(PlaneWidth, PlaneHeight) * 1.05f;
}