# This script automatically removes table from a CT volume
import slicer

# Generate input data
################################################

import SampleData

# Get input image (in this example, download a sample data set)
sampleDataLogic = SampleData.SampleDataLogic()
masterVolumeNode = sampleDataLogic.downloadCTACardio()
threshold = -44

# Process
################################################

# Create segmentation
segmentationNode = slicer.vtkMRMLSegmentationNode()
slicer.mrmlScene.AddNode(segmentationNode)
segmentationNode.CreateDefaultDisplayNodes() # only needed for display
segmentationNode.SetReferenceImageGeometryParameterFromVolumeNode(masterVolumeNode)

# Create segment editor to get access to effects
slicer.app.processEvents()
segmentEditorWidget = slicer.qMRMLSegmentEditorWidget()
# To show segment editor widget (useful for debugging): segmentEditorWidget.show()
segmentEditorWidget.setMRMLScene(slicer.mrmlScene)
segmentEditorNode = slicer.vtkMRMLSegmentEditorNode()
slicer.mrmlScene.AddNode(segmentEditorNode)
segmentEditorWidget.setMRMLSegmentEditorNode(segmentEditorNode)
segmentEditorWidget.setSegmentationNode(segmentationNode)
segmentEditorWidget.setMasterVolumeNode(masterVolumeNode)

# Check that required extensions are installed

if not segmentEditorWidget.effectByName("Wrap Solidify"):
    slicer.util.errorDisplay("Please install 'SurfaceWrapSolidify' extension using Extension Manager.")

if not segmentEditorWidget.effectByName("Mask volume"):
    slicer.util.errorDisplay("Please install 'SegmentEditorExtraEffects' extension using Extension Manager.")

# Create object of interest segment by thresholding
slicer.app.processEvents()
volumeScalarRange = masterVolumeNode.GetImageData().GetScalarRange()
objectSegmentID = segmentationNode.GetSegmentation().AddEmptySegment()
segmentEditorNode.SetSelectedSegmentID(objectSegmentID)
segmentEditorWidget.setActiveEffectByName("Threshold")
effect = segmentEditorWidget.activeEffect()
effect.setParameter("MinimumThreshold",str(threshold))
effect.setParameter("MaximumThreshold",str(volumeScalarRange[1]))
effect.self().onApply()

# Find largest object, remove all other regions from the segment
slicer.app.processEvents()
segmentEditorWidget.setActiveEffectByName("Islands")
effect = segmentEditorWidget.activeEffect()
effect.setParameterDefault("Operation", "KEEP_LARGEST_ISLAND")
effect.self().onApply()

# Fill holes in the segment to create a solid region of interest
slicer.app.processEvents()
segmentEditorWidget.setActiveEffectByName("Wrap Solidify")
effect = segmentEditorWidget.activeEffect()
effect.setParameter("region", "outerSurface")
effect.setParameter("outputType", "segment")
effect.setParameter("remeshOversampling", 0.3)  # speed up solidification by lowering resolution
effect.self().onApply()

# Blank out the volume outside the object segment
slicer.app.processEvents()
segmentEditorWidget.setActiveEffectByName('Mask volume')
effect = segmentEditorWidget.activeEffect()
effect.setParameter('FillValue', -1000)
effect.setParameter('Operation', 'FILL_OUTSIDE')
effect.self().onApply()

# Remove temporary nodes and widget
segmentEditorWidget = None
slicer.mrmlScene.RemoveNode(segmentEditorNode)
slicer.mrmlScene.RemoveNode(segmentationNode)

# Show masked volume
maskedVolume = slicer.mrmlScene.GetFirstNodeByName(masterVolumeNode.GetName()+" masked")
slicer.util.setSliceViewerLayers(background=maskedVolume)
