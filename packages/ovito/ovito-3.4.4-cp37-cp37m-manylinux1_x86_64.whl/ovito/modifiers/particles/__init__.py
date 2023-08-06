# Load dependencies
import ovito.modifiers
import ovito.modifiers.stdmod
import ovito.modifiers.stdobj
import ovito.modifiers.mesh
import ovito.modifiers.grid

# Load the native code modules.
from ovito.plugins.ParticlesPython import (
        AmbientOcclusionModifier, WrapPeriodicImagesModifier, ExpandSelectionModifier,
        CommonNeighborAnalysisModifier, AcklandJonesModifier, CreateBondsModifier, CentroSymmetryModifier, ClusterAnalysisModifier,
        CoordinationAnalysisModifier, CalculateDisplacementsModifier, AtomicStrainModifier, WignerSeitzAnalysisModifier,
        VoronoiAnalysisModifier, IdentifyDiamondModifier, LoadTrajectoryModifier, PolyhedralTemplateMatchingModifier,
        CoordinationPolyhedraModifier, SmoothTrajectoryModifier, GenerateTrajectoryLinesModifier, UnwrapTrajectoriesModifier,
        ChillPlusModifier, ConstructSurfaceModifier)

# Load submodules.
from .compute_property_modifier import ComputePropertyModifier
from .structure_identification_modifier import StructureIdentificationModifier

# Inject classes into parent module.
ovito.modifiers.AmbientOcclusionModifier = AmbientOcclusionModifier
ovito.modifiers.WrapPeriodicImagesModifier = WrapPeriodicImagesModifier
ovito.modifiers.ExpandSelectionModifier = ExpandSelectionModifier
ovito.modifiers.StructureIdentificationModifier = StructureIdentificationModifier
ovito.modifiers.CommonNeighborAnalysisModifier = CommonNeighborAnalysisModifier
ovito.modifiers.AcklandJonesModifier = AcklandJonesModifier
ovito.modifiers.CreateBondsModifier = CreateBondsModifier
ovito.modifiers.CentroSymmetryModifier = CentroSymmetryModifier
ovito.modifiers.ClusterAnalysisModifier = ClusterAnalysisModifier
ovito.modifiers.CoordinationAnalysisModifier = CoordinationAnalysisModifier
ovito.modifiers.CalculateDisplacementsModifier = CalculateDisplacementsModifier
ovito.modifiers.AtomicStrainModifier = AtomicStrainModifier
ovito.modifiers.WignerSeitzAnalysisModifier = WignerSeitzAnalysisModifier
ovito.modifiers.VoronoiAnalysisModifier = VoronoiAnalysisModifier
ovito.modifiers.IdentifyDiamondModifier = IdentifyDiamondModifier
ovito.modifiers.LoadTrajectoryModifier = LoadTrajectoryModifier
ovito.modifiers.PolyhedralTemplateMatchingModifier = PolyhedralTemplateMatchingModifier
ovito.modifiers.CoordinationPolyhedraModifier = CoordinationPolyhedraModifier
ovito.modifiers.SmoothTrajectoryModifier = SmoothTrajectoryModifier
ovito.modifiers.GenerateTrajectoryLinesModifier = GenerateTrajectoryLinesModifier
ovito.modifiers.UnwrapTrajectoriesModifier = UnwrapTrajectoriesModifier
ovito.modifiers.ChillPlusModifier = ChillPlusModifier
ovito.modifiers.ConstructSurfaceModifier = ConstructSurfaceModifier
ovito.modifiers.__all__ += [
            'AmbientOcclusionModifier',
            'WrapPeriodicImagesModifier',
            'ExpandSelectionModifier',
            'StructureIdentificationModifier',
            'CommonNeighborAnalysisModifier',
            'AcklandJonesModifier',
            'CreateBondsModifier',
            'CentroSymmetryModifier',
            'ClusterAnalysisModifier',
            'CoordinationAnalysisModifier',
            'CalculateDisplacementsModifier',
            'AtomicStrainModifier',
            'WignerSeitzAnalysisModifier',
            'VoronoiAnalysisModifier',
            'IdentifyDiamondModifier',
            'LoadTrajectoryModifier',
            'PolyhedralTemplateMatchingModifier',
            'CoordinationPolyhedraModifier',
            'SmoothTrajectoryModifier',
            'GenerateTrajectoryLinesModifier',
            'UnwrapTrajectoriesModifier',
            'ChillPlusModifier',
            'ConstructSurfaceModifier']

# For backward compatibility with OVITO 2.9.0:
ovito.modifiers.CoordinationNumberModifier = CoordinationAnalysisModifier
ovito.modifiers.InterpolateTrajectoryModifier = SmoothTrajectoryModifier
ovito.modifiers.__all__ += ['CoordinationNumberModifier', 'InterpolateTrajectoryModifier']
