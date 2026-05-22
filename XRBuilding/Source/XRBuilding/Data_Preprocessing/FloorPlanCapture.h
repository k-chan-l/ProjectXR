#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "RenderCommandFence.h"
#include "FloorPlanCapture.generated.h"

class USceneComponent;
class USceneCaptureComponent2D;
class AActor;

UCLASS()
class XRBUILDING_API AFloorPlanCapture : public AActor
{
	GENERATED_BODY()
	
public:
	AFloorPlanCapture();

protected:
	virtual void BeginPlay() override;

public:
	// 루트
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="Capture")
	USceneComponent* Root;

	// BP에서 추가한 SceneCaptureComponent2D를 찾아 연결해서 쓸 예정
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="Capture")
	USceneCaptureComponent2D* SceneCapture;

	// 기준 바닥 Plane
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Capture")
	AActor* FloorPlaneActor;

	// 도면 촬영 위치 자동 정렬
	UFUNCTION(BlueprintCallable, Category="Capture")
	void AlignToPlaneForMapCapture();

	// 기존 이름 유지
	UFUNCTION(BlueprintCallable, Category="Capture")
	void CaptureToFile(const FString& FileName);

};