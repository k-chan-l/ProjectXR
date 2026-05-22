// Copyright Epic Games, Inc. All Rights Reserved.

using UnrealBuildTool;

public class XRBuilding : ModuleRules
{
	public XRBuilding(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

		PublicDependencyModuleNames.AddRange(new string[] {
			"Core",
			"CoreUObject",
			"Engine",
			"InputCore",
			"EnhancedInput",
			"AIModule",
			"StateTreeModule",
			"GameplayStateTreeModule",
			"UMG",
			"Slate",
			"HTTP",
			"Json",
			"JsonUtilities",
			"RenderCore"
		});

		PrivateDependencyModuleNames.AddRange(new string[] { });

		PublicIncludePaths.AddRange(new string[] {
			"XRBuilding",
			"XRBuilding/Variant_Horror",
			"XRBuilding/Variant_Horror/UI",
			"XRBuilding/Variant_Shooter",
			"XRBuilding/Variant_Shooter/AI",
			"XRBuilding/Variant_Shooter/UI",
			"XRBuilding/Variant_Shooter/Weapons"
		});

		// Uncomment if you are using Slate UI
		// PrivateDependencyModuleNames.AddRange(new string[] { "Slate", "SlateCore" });

		// Uncomment if you are using online features
		// PrivateDependencyModuleNames.Add("OnlineSubsystem");

		// To include OnlineSubsystemSteam, add it to the plugins section in your uproject file with the Enabled attribute set to true
	}
}
