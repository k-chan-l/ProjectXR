// Fill out your copyright notice in the Description page of Project Settings.


#include "IndoorNavigationSubsystem.h"

void UIndoorNavigationSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
	Super::Initialize(Collection);
}

void UIndoorNavigationSubsystem::Deinitialize()
{
	Super::Deinitialize();
}

void UIndoorNavigationSubsystem::TestRequest()
{
	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request =
		FHttpModule::Get().CreateRequest();

	Request->SetURL("http://127.0.0.1:8000/");
	Request->SetVerb("GET");

	Request->OnProcessRequestComplete().BindUObject(
		this,
		&UIndoorNavigationSubsystem::OnResponseReceived
	);

	Request->ProcessRequest();
}

void UIndoorNavigationSubsystem::OnResponseReceived(
	FHttpRequestPtr Request,
	FHttpResponsePtr Response,
	bool bWasSuccessful)
{
	if (!bWasSuccessful || !Response.IsValid())
	{
		UE_LOG(LogTemp, Error, TEXT("Request failed"));
		return;
	}

	FString ResponseString = Response->GetContentAsString();

	UE_LOG(LogTemp, Warning, TEXT("Response: %s"), *ResponseString);
}
