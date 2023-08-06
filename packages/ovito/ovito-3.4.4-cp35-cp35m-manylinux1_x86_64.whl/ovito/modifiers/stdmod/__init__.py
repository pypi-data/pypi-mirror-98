# Load dependencies
import ovito.modifiers
import ovito.modifiers.stdobj
import ovito.modifiers.mesh

# Load the native code module.
from ovito.plugins.StdModPython import (SliceModifier, AffineTransformationModifier, ClearSelectionModifier,
                                InvertSelectionModifier, ColorCodingModifier, AssignColorModifier,
                                DeleteSelectedModifier, ScatterPlotModifier, ReplicateModifier,
                                ExpressionSelectionModifier, FreezePropertyModifier, ManualSelectionModifier,
                                ComputePropertyModifier, CombineDatasetsModifier)

# Load submodules.
from .select_type_modifier import SelectTypeModifier
from .histogram_modifier import HistogramModifier

# Inject modifier classes into parent module.
ovito.modifiers.SliceModifier = SliceModifier
ovito.modifiers.AffineTransformationModifier = AffineTransformationModifier
ovito.modifiers.ClearSelectionModifier = ClearSelectionModifier
ovito.modifiers.InvertSelectionModifier = InvertSelectionModifier
ovito.modifiers.ColorCodingModifier = ColorCodingModifier
ovito.modifiers.AssignColorModifier = AssignColorModifier
ovito.modifiers.DeleteSelectedModifier = DeleteSelectedModifier
ovito.modifiers.ScatterPlotModifier = ScatterPlotModifier
ovito.modifiers.ReplicateModifier = ReplicateModifier
ovito.modifiers.SelectTypeModifier = SelectTypeModifier
ovito.modifiers.HistogramModifier = HistogramModifier
ovito.modifiers.ExpressionSelectionModifier = ExpressionSelectionModifier
ovito.modifiers.FreezePropertyModifier = FreezePropertyModifier
ovito.modifiers.ManualSelectionModifier = ManualSelectionModifier
ovito.modifiers.ComputePropertyModifier = ComputePropertyModifier
ovito.modifiers.CombineDatasetsModifier = CombineDatasetsModifier
ovito.modifiers.__all__ += ['SliceModifier', 'AffineTransformationModifier',
            'ClearSelectionModifier', 'InvertSelectionModifier', 'ColorCodingModifier',
            'AssignColorModifier', 'DeleteSelectedModifier', 'SelectTypeModifier', 'HistogramModifier',
            'ScatterPlotModifier', 'ReplicateModifier', 'ExpressionSelectionModifier',
            'FreezePropertyModifier', 'ManualSelectionModifier', 'ComputePropertyModifier',
            'CombineDatasetsModifier']

# For backward compatibility with OVITO 2.9.0:
def _ColorCodingModifier_set_particle_property(self, v): self.property = v
ColorCodingModifier.particle_property = property(lambda self: self.property, _ColorCodingModifier_set_particle_property)
def _ColorCodingModifier_set_bond_property(self, v):
    self.operate_on = 'bonds'
    self.property = v
ColorCodingModifier.bond_property = property(lambda self: self.property, _ColorCodingModifier_set_bond_property)
class _ColorCodingModifier_AssignmentMode:
    Particles = 'particles'
    Bonds = 'bonds'
    Vectors = 'vectors'
ColorCodingModifier.AssignmentMode = _ColorCodingModifier_AssignmentMode
def _ColorCodingModifier_set_assign_to(self, v): self.operate_on = v
ColorCodingModifier.assign_to = property(lambda self: self.operate_on, _ColorCodingModifier_set_assign_to)
ColorCodingModifier.Custom = ColorCodingModifier.Image

# For backward compatibility with OVITO 2.9.0:
def _AffineTransformationModifier_set_transform_particles(self, v): 
    if v: self.operate_on.add('particles')
    else: self.operate_on.remove('particles')
AffineTransformationModifier.transform_particles = property(lambda self: 'particles' in self.operate_on, _AffineTransformationModifier_set_transform_particles)
def _AffineTransformationModifier_set_transform_box(self, v): 
    if v: self.operate_on.add('cell')
    else: self.operate_on.remove('cell')
AffineTransformationModifier.transform_box = property(lambda self: 'box' in self.operate_on, _AffineTransformationModifier_set_transform_box)
def _AffineTransformationModifier_set_transform_surface(self, v): 
    if v: self.operate_on.add('surfaces')
    else: self.operate_on.remove('surfaces')
AffineTransformationModifier.transform_surface = property(lambda self: 'surfaces' in self.operate_on, _AffineTransformationModifier_set_transform_surface)
def _AffineTransformationModifier_set_transform_vector_properties(self, v): 
    if v: self.operate_on.add('vector_properties')
    else: self.operate_on.remove('vector_properties')
AffineTransformationModifier.transform_vector_properties = property(lambda self: 'vector_properties' in self.operate_on, _AffineTransformationModifier_set_transform_vector_properties)

# For backward compatibility with OVITO 2.9.0:
ovito.modifiers.DeleteSelectedParticlesModifier = DeleteSelectedModifier
ovito.modifiers.SelectParticleTypeModifier = SelectTypeModifier
ovito.modifiers.ShowPeriodicImagesModifier = ReplicateModifier
ovito.modifiers.SelectExpressionModifier = ExpressionSelectionModifier
ovito.modifiers.CombineParticleSetsModifier = CombineDatasetsModifier
ovito.modifiers.__all__ += ['DeleteSelectedParticlesModifier', 'SelectParticleTypeModifier', 'ShowPeriodicImagesModifier', 'SelectExpressionModifier', 'CombineParticleSetsModifier']
