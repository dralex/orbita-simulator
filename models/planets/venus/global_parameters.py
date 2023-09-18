# ./venus/global_parameters.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:c8721b651877e875de2bb1e7a1f0988806e26562
# Generated 2023-09-18 15:19:28.492651 by PyXB version 1.2.6 using Python 3.10.12.final.0
# Namespace venus

from __future__ import unicode_literals
import pyxb
import pyxb.binding
import pyxb.binding.saxer
import io
import pyxb.utils.utility
import pyxb.utils.domutils
import sys
import pyxb.utils.six as _six
# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:9d16229e-561d-11ee-a2f3-e1473c71107c')

# Version of PyXB used to generate the bindings
_PyXBVersion = '1.2.6'
# Generated bindings are not compatible across PyXB versions
if pyxb.__version__ != _PyXBVersion:
    raise pyxb.PyXBVersionError(_PyXBVersion)

# A holder for module-level binding classes so we can access them from
# inside class definitions where property names may conflict.
_module_typeBindings = pyxb.utils.utility.Object()

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('venus', create_if_missing=True)
Namespace.configureCategories(['typeBinding', 'elementBinding'])

def CreateFromDocument (xml_text, default_namespace=None, location_base=None):
    """Parse the given XML and use the document element to create a
    Python instance.

    @param xml_text An XML document.  This should be data (Python 2
    str or Python 3 bytes), or a text (Python 2 unicode or Python 3
    str) in the L{pyxb._InputEncoding} encoding.

    @keyword default_namespace The L{pyxb.Namespace} instance to use as the
    default namespace where there is no default namespace in scope.
    If unspecified or C{None}, the namespace of the module containing
    this function will be used.

    @keyword location_base: An object to be recorded as the base of all
    L{pyxb.utils.utility.Location} instances associated with events and
    objects handled by the parser.  You might pass the URI from which
    the document was obtained.
    """

    if pyxb.XMLStyle_saxer != pyxb._XMLStyle:
        dom = pyxb.utils.domutils.StringToDOM(xml_text)
        return CreateFromDOM(dom.documentElement, default_namespace=default_namespace)
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    saxer = pyxb.binding.saxer.make_parser(fallback_namespace=default_namespace, location_base=location_base)
    handler = saxer.getContentHandler()
    xmld = xml_text
    if isinstance(xmld, _six.text_type):
        xmld = xmld.encode(pyxb._InputEncoding)
    saxer.parse(io.BytesIO(xmld))
    instance = handler.rootObject()
    return instance

def CreateFromDOM (node, default_namespace=None):
    """Create a Python instance from the given DOM node.
    The node tag must correspond to an element declaration in this module.

    @deprecated: Forcing use of DOM interface is unnecessary; use L{CreateFromDocument}."""
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    return pyxb.binding.basis.element.AnyCreateFromDOM(node, default_namespace)


# Atomic simple type: [anonymous]
class STD_ANON (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 62, 7)
    _Documentation = None
STD_ANON._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON, enum_prefix=None)
STD_ANON.hard = STD_ANON._CF_enumeration.addEnumeration(unicode_value='hard', tag='hard')
STD_ANON.liquid = STD_ANON._CF_enumeration.addEnumeration(unicode_value='liquid', tag='liquid')
STD_ANON._InitializeFacetMap(STD_ANON._CF_enumeration)
_module_typeBindings.STD_ANON = STD_ANON

# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 5, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element G uses Python identifier G
    __G = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'G'), 'G', '__venus_CTD_ANON_G', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 7, 1), )

    
    G = property(__G.value, __G.set, None, None)

    
    # Element MaxLaunchTime uses Python identifier MaxLaunchTime
    __MaxLaunchTime = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'MaxLaunchTime'), 'MaxLaunchTime', '__venus_CTD_ANON_MaxLaunchTime', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 9, 1), )

    
    MaxLaunchTime = property(__MaxLaunchTime.value, __MaxLaunchTime.set, None, None)

    
    # Element missions uses Python identifier missions
    __missions = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'missions'), 'missions', '__venus_CTD_ANON_missions', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 11, 1), )

    
    missions = property(__missions.value, __missions.set, None, None)

    _ElementMap.update({
        __G.name() : __G,
        __MaxLaunchTime.name() : __MaxLaunchTime,
        __missions.name() : __missions
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON = CTD_ANON


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_ (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 12, 3)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element mission uses Python identifier mission
    __mission = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'mission'), 'mission', '__venus_CTD_ANON__mission', True, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 14, 7), )

    
    mission = property(__mission.value, __mission.set, None, None)

    _ElementMap.update({
        __mission.name() : __mission
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_ = CTD_ANON_


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_2 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 15, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element planet uses Python identifier planet
    __planet = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'planet'), 'planet', '__venus_CTD_ANON_2_planet', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 19, 6), )

    
    planet = property(__planet.value, __planet.set, None, None)

    
    # Element models uses Python identifier models
    __models = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'models'), 'models', '__venus_CTD_ANON_2_models', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 21, 6), )

    
    models = property(__models.value, __models.set, None, None)

    
    # Element devices uses Python identifier devices
    __devices = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'devices'), 'devices', '__venus_CTD_ANON_2_devices', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 23, 6), )

    
    devices = property(__devices.value, __devices.set, None, None)

    
    # Element start_braking_koeff uses Python identifier start_braking_koeff
    __start_braking_koeff = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'start_braking_koeff'), 'start_braking_koeff', '__venus_CTD_ANON_2_start_braking_koeff', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 25, 6), )

    
    start_braking_koeff = property(__start_braking_koeff.value, __start_braking_koeff.set, None, None)

    
    # Element max_mass uses Python identifier max_mass
    __max_mass = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'max_mass'), 'max_mass', '__venus_CTD_ANON_2_max_mass', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 27, 6), )

    
    max_mass = property(__max_mass.value, __max_mass.set, None, None)

    
    # Element max_radius uses Python identifier max_radius
    __max_radius = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'max_radius'), 'max_radius', '__venus_CTD_ANON_2_max_radius', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 29, 6), )

    
    max_radius = property(__max_radius.value, __max_radius.set, None, None)

    
    # Element max_length uses Python identifier max_length
    __max_length = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'max_length'), 'max_length', '__venus_CTD_ANON_2_max_length', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 31, 6), )

    
    max_length = property(__max_length.value, __max_length.set, None, None)

    
    # Element max_acceleration uses Python identifier max_acceleration
    __max_acceleration = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'max_acceleration'), 'max_acceleration', '__venus_CTD_ANON_2_max_acceleration', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 33, 6), )

    
    max_acceleration = property(__max_acceleration.value, __max_acceleration.set, None, None)

    
    # Element T_start uses Python identifier T_start
    __T_start = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'T_start'), 'T_start', '__venus_CTD_ANON_2_T_start', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 35, 12), )

    
    T_start = property(__T_start.value, __T_start.set, None, None)

    
    # Element aerodynamic_coeff uses Python identifier aerodynamic_coeff
    __aerodynamic_coeff = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'aerodynamic_coeff'), 'aerodynamic_coeff', '__venus_CTD_ANON_2_aerodynamic_coeff', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 37, 6), )

    
    aerodynamic_coeff = property(__aerodynamic_coeff.value, __aerodynamic_coeff.set, None, None)

    
    # Element construction uses Python identifier construction
    __construction = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'construction'), 'construction', '__venus_CTD_ANON_2_construction', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 39, 6), )

    
    construction = property(__construction.value, __construction.set, None, None)

    
    # Element isolator uses Python identifier isolator
    __isolator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'isolator'), 'isolator', '__venus_CTD_ANON_2_isolator', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 48, 6), )

    
    isolator = property(__isolator.value, __isolator.set, None, None)

    
    # Element absorber uses Python identifier absorber
    __absorber = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'absorber'), 'absorber', '__venus_CTD_ANON_2_absorber', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 58, 6), )

    
    absorber = property(__absorber.value, __absorber.set, None, None)

    
    # Element surface_max_time uses Python identifier surface_max_time
    __surface_max_time = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'surface_max_time'), 'surface_max_time', '__venus_CTD_ANON_2_surface_max_time', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 82, 6), )

    
    surface_max_time = property(__surface_max_time.value, __surface_max_time.set, None, None)

    
    # Element score uses Python identifier score
    __score = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'score'), 'score', '__venus_CTD_ANON_2_score', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 83, 6), )

    
    score = property(__score.value, __score.set, None, None)

    
    # Element result uses Python identifier result
    __result = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'result'), 'result', '__venus_CTD_ANON_2_result', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 84, 12), )

    
    result = property(__result.value, __result.set, None, None)

    
    # Element launch uses Python identifier launch
    __launch = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'launch'), 'launch', '__venus_CTD_ANON_2_launch', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 85, 6), )

    
    launch = property(__launch.value, __launch.set, None, None)

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__venus_CTD_ANON_2_name', pyxb.binding.datatypes.string)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 16, 4)
    __name._UseLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 16, 4)
    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute full_name uses Python identifier full_name
    __full_name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'full_name'), 'full_name', '__venus_CTD_ANON_2_full_name', pyxb.binding.datatypes.string)
    __full_name._DeclarationLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 17, 4)
    __full_name._UseLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 17, 4)
    
    full_name = property(__full_name.value, __full_name.set, None, None)

    _ElementMap.update({
        __planet.name() : __planet,
        __models.name() : __models,
        __devices.name() : __devices,
        __start_braking_koeff.name() : __start_braking_koeff,
        __max_mass.name() : __max_mass,
        __max_radius.name() : __max_radius,
        __max_length.name() : __max_length,
        __max_acceleration.name() : __max_acceleration,
        __T_start.name() : __T_start,
        __aerodynamic_coeff.name() : __aerodynamic_coeff,
        __construction.name() : __construction,
        __isolator.name() : __isolator,
        __absorber.name() : __absorber,
        __surface_max_time.name() : __surface_max_time,
        __score.name() : __score,
        __result.name() : __result,
        __launch.name() : __launch
    })
    _AttributeMap.update({
        __name.name() : __name,
        __full_name.name() : __full_name
    })
_module_typeBindings.CTD_ANON_2 = CTD_ANON_2


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_3 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 40, 8)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element density uses Python identifier density
    __density = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'density'), 'density', '__venus_CTD_ANON_3_density', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 42, 5), )

    
    density = property(__density.value, __density.set, None, None)

    
    # Element program uses Python identifier program
    __program = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'program'), 'program', '__venus_CTD_ANON_3_program', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 44, 5), )

    
    program = property(__program.value, __program.set, None, None)

    _ElementMap.update({
        __density.name() : __density,
        __program.name() : __program
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_3 = CTD_ANON_3


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_4 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 49, 8)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element k uses Python identifier k
    __k = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'k'), 'k', '__venus_CTD_ANON_4_k', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 51, 5), )

    
    k = property(__k.value, __k.set, None, None)

    
    # Element density uses Python identifier density
    __density = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'density'), 'density', '__venus_CTD_ANON_4_density', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 53, 5), )

    
    density = property(__density.value, __density.set, None, None)

    _ElementMap.update({
        __k.name() : __k,
        __density.name() : __density
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_4 = CTD_ANON_4


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_5 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 59, 8)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element state uses Python identifier state
    __state = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'state'), 'state', '__venus_CTD_ANON_5_state', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 61, 5), )

    
    state = property(__state.value, __state.set, None, None)

    
    # Element density uses Python identifier density
    __density = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'density'), 'density', '__venus_CTD_ANON_5_density', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 69, 5), )

    
    density = property(__density.value, __density.set, None, None)

    
    # Element T_melting uses Python identifier T_melting
    __T_melting = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'T_melting'), 'T_melting', '__venus_CTD_ANON_5_T_melting', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 71, 5), )

    
    T_melting = property(__T_melting.value, __T_melting.set, None, None)

    
    # Element L uses Python identifier L
    __L = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'L'), 'L', '__venus_CTD_ANON_5_L', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 73, 5), )

    
    L = property(__L.value, __L.set, None, None)

    
    # Element C_hard uses Python identifier C_hard
    __C_hard = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'C_hard'), 'C_hard', '__venus_CTD_ANON_5_C_hard', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 75, 5), )

    
    C_hard = property(__C_hard.value, __C_hard.set, None, None)

    
    # Element C_liquid uses Python identifier C_liquid
    __C_liquid = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'C_liquid'), 'C_liquid', '__venus_CTD_ANON_5_C_liquid', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 77, 5), )

    
    C_liquid = property(__C_liquid.value, __C_liquid.set, None, None)

    _ElementMap.update({
        __state.name() : __state,
        __density.name() : __density,
        __T_melting.name() : __T_melting,
        __L.name() : __L,
        __C_hard.name() : __C_hard,
        __C_liquid.name() : __C_liquid
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_5 = CTD_ANON_5


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_6 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 86, 8)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element target_distance uses Python identifier target_distance
    __target_distance = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'target_distance'), 'target_distance', '__venus_CTD_ANON_6_target_distance', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 88, 18), )

    
    target_distance = property(__target_distance.value, __target_distance.set, None, None)

    
    # Element accuracy uses Python identifier accuracy
    __accuracy = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'accuracy'), 'accuracy', '__venus_CTD_ANON_6_accuracy', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 90, 18), )

    
    accuracy = property(__accuracy.value, __accuracy.set, None, None)

    
    # Element cycles uses Python identifier cycles
    __cycles = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'cycles'), 'cycles', '__venus_CTD_ANON_6_cycles', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 92, 18), )

    
    cycles = property(__cycles.value, __cycles.set, None, None)

    
    # Element max_height uses Python identifier max_height
    __max_height = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'max_height'), 'max_height', '__venus_CTD_ANON_6_max_height', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 94, 18), )

    
    max_height = property(__max_height.value, __max_height.set, None, None)

    
    # Element max_wait_time uses Python identifier max_wait_time
    __max_wait_time = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'max_wait_time'), 'max_wait_time', '__venus_CTD_ANON_6_max_wait_time', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 96, 18), )

    
    max_wait_time = property(__max_wait_time.value, __max_wait_time.set, None, None)

    _ElementMap.update({
        __target_distance.name() : __target_distance,
        __accuracy.name() : __accuracy,
        __cycles.name() : __cycles,
        __max_height.name() : __max_height,
        __max_wait_time.name() : __max_wait_time
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_6 = CTD_ANON_6


global_parameters = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'global_parameters'), CTD_ANON, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 4, 2))
Namespace.addCategoryObject('elementBinding', global_parameters.name().localName(), global_parameters)



CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'G'), pyxb.binding.datatypes.float, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 7, 1)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'MaxLaunchTime'), pyxb.binding.datatypes.integer, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 9, 1)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'missions'), CTD_ANON_, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 11, 1)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, 'G')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 7, 1))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, 'MaxLaunchTime')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 9, 1))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, 'missions')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 11, 1))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton()




CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'mission'), CTD_ANON_2, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 14, 7)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'mission')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 14, 7))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_._Automaton = _BuildAutomaton_()




CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'planet'), pyxb.binding.datatypes.string, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 19, 6)))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'models'), pyxb.binding.datatypes.string, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 21, 6)))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'devices'), pyxb.binding.datatypes.string, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 23, 6)))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'start_braking_koeff'), pyxb.binding.datatypes.decimal, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 25, 6)))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'max_mass'), pyxb.binding.datatypes.decimal, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 27, 6)))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'max_radius'), pyxb.binding.datatypes.decimal, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 29, 6)))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'max_length'), pyxb.binding.datatypes.decimal, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 31, 6)))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'max_acceleration'), pyxb.binding.datatypes.decimal, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 33, 6)))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'T_start'), pyxb.binding.datatypes.decimal, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 35, 12)))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'aerodynamic_coeff'), pyxb.binding.datatypes.decimal, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 37, 6)))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'construction'), CTD_ANON_3, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 39, 6)))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'isolator'), CTD_ANON_4, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 48, 6)))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'absorber'), CTD_ANON_5, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 58, 6)))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'surface_max_time'), pyxb.binding.datatypes.decimal, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 82, 6)))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'score'), pyxb.binding.datatypes.string, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 83, 6)))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'result'), pyxb.binding.datatypes.string, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 84, 12)))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'launch'), CTD_ANON_6, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 85, 6)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 31, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 37, 6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 48, 6))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 58, 6))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 82, 6))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 83, 6))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 85, 6))
    counters.add(cc_6)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, 'planet')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 19, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, 'models')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 21, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, 'devices')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 23, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, 'start_braking_koeff')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 25, 6))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, 'max_mass')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 27, 6))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, 'max_radius')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 29, 6))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, 'max_length')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 31, 6))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, 'max_acceleration')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 33, 6))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, 'T_start')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 35, 12))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, 'aerodynamic_coeff')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 37, 6))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, 'construction')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 39, 6))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, 'isolator')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 48, 6))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, 'absorber')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 58, 6))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, 'surface_max_time')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 82, 6))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, 'score')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 83, 6))
    st_14 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, 'result')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 84, 12))
    st_15 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, 'launch')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 85, 6))
    st_16 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_16)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
         ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
         ]))
    transitions.append(fac.Transition(st_7, [
         ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
         ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
         ]))
    transitions.append(fac.Transition(st_10, [
         ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
         ]))
    transitions.append(fac.Transition(st_12, [
         ]))
    transitions.append(fac.Transition(st_13, [
         ]))
    transitions.append(fac.Transition(st_14, [
         ]))
    transitions.append(fac.Transition(st_15, [
         ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_16, [
         ]))
    st_15._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_6, True) ]))
    st_16._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_2._Automaton = _BuildAutomaton_2()




CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'density'), pyxb.binding.datatypes.decimal, scope=CTD_ANON_3, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 42, 5)))

CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'program'), pyxb.binding.datatypes.string, scope=CTD_ANON_3, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 44, 5)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 44, 5))
    counters.add(cc_0)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(None, 'density')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 42, 5))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(None, 'program')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 44, 5))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_3._Automaton = _BuildAutomaton_3()




CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'k'), pyxb.binding.datatypes.decimal, scope=CTD_ANON_4, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 51, 5)))

CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'density'), pyxb.binding.datatypes.decimal, scope=CTD_ANON_4, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 53, 5)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, 'k')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 51, 5))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, 'density')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 53, 5))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_4._Automaton = _BuildAutomaton_4()




CTD_ANON_5._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'state'), STD_ANON, scope=CTD_ANON_5, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 61, 5)))

CTD_ANON_5._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'density'), pyxb.binding.datatypes.decimal, scope=CTD_ANON_5, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 69, 5)))

CTD_ANON_5._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'T_melting'), pyxb.binding.datatypes.decimal, scope=CTD_ANON_5, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 71, 5)))

CTD_ANON_5._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'L'), pyxb.binding.datatypes.decimal, scope=CTD_ANON_5, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 73, 5)))

CTD_ANON_5._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'C_hard'), pyxb.binding.datatypes.decimal, scope=CTD_ANON_5, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 75, 5)))

CTD_ANON_5._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'C_liquid'), pyxb.binding.datatypes.decimal, scope=CTD_ANON_5, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 77, 5)))

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_5._UseForTag(pyxb.namespace.ExpandedName(None, 'state')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 61, 5))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_5._UseForTag(pyxb.namespace.ExpandedName(None, 'density')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 69, 5))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_5._UseForTag(pyxb.namespace.ExpandedName(None, 'T_melting')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 71, 5))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_5._UseForTag(pyxb.namespace.ExpandedName(None, 'L')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 73, 5))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_5._UseForTag(pyxb.namespace.ExpandedName(None, 'C_hard')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 75, 5))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_5._UseForTag(pyxb.namespace.ExpandedName(None, 'C_liquid')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 77, 5))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
         ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_5._Automaton = _BuildAutomaton_5()




CTD_ANON_6._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'target_distance'), pyxb.binding.datatypes.integer, scope=CTD_ANON_6, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 88, 18)))

CTD_ANON_6._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'accuracy'), pyxb.binding.datatypes.decimal, scope=CTD_ANON_6, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 90, 18)))

CTD_ANON_6._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'cycles'), pyxb.binding.datatypes.integer, scope=CTD_ANON_6, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 92, 18)))

CTD_ANON_6._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'max_height'), pyxb.binding.datatypes.integer, scope=CTD_ANON_6, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 94, 18)))

CTD_ANON_6._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'max_wait_time'), pyxb.binding.datatypes.integer, scope=CTD_ANON_6, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 96, 18)))

def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 88, 18))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 90, 18))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(None, 'target_distance')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 88, 18))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(None, 'accuracy')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 90, 18))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(None, 'cycles')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 92, 18))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(None, 'max_height')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 94, 18))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(None, 'max_wait_time')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_parameters.xsd', 96, 18))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_6._Automaton = _BuildAutomaton_6()

