# ./venus/probe.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:c8721b651877e875de2bb1e7a1f0988806e26562
# Generated 2023-09-18 15:19:28.321614 by PyXB version 1.2.6 using Python 3.10.12.final.0
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
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:9cfb8a38-561d-11ee-a2f3-e1473c71107c')

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
    _XSDLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 42, 2)
    _Documentation = None
STD_ANON._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON, enum_prefix=None)
STD_ANON.OFF = STD_ANON._CF_enumeration.addEnumeration(unicode_value='OFF', tag='OFF')
STD_ANON.ON = STD_ANON._CF_enumeration.addEnumeration(unicode_value='ON', tag='ON')
STD_ANON._InitializeFacetMap(STD_ANON._CF_enumeration)
_module_typeBindings.STD_ANON = STD_ANON

# Atomic simple type: [anonymous]
class STD_ANON_ (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 50, 2)
    _Documentation = None
STD_ANON_._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_, enum_prefix=None)
STD_ANON_.OFF = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='OFF', tag='OFF')
STD_ANON_.ON = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='ON', tag='ON')
STD_ANON_._InitializeFacetMap(STD_ANON_._CF_enumeration)
_module_typeBindings.STD_ANON_ = STD_ANON_

# Atomic simple type: [anonymous]
class STD_ANON_2 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 68, 20)
    _Documentation = None
STD_ANON_2._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_2, enum_prefix=None)
STD_ANON_2.cylinder = STD_ANON_2._CF_enumeration.addEnumeration(unicode_value='cylinder', tag='cylinder')
STD_ANON_2.sphere = STD_ANON_2._CF_enumeration.addEnumeration(unicode_value='sphere', tag='sphere')
STD_ANON_2._InitializeFacetMap(STD_ANON_2._CF_enumeration)
_module_typeBindings.STD_ANON_2 = STD_ANON_2

# Atomic simple type: [anonymous]
class STD_ANON_3 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 92, 6)
    _Documentation = None
STD_ANON_3._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_3, enum_prefix=None)
STD_ANON_3.OFF = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value='OFF', tag='OFF')
STD_ANON_3.ON = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value='ON', tag='ON')
STD_ANON_3._InitializeFacetMap(STD_ANON_3._CF_enumeration)
_module_typeBindings.STD_ANON_3 = STD_ANON_3

# Atomic simple type: [anonymous]
class STD_ANON_4 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 100, 6)
    _Documentation = None
STD_ANON_4._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_4, enum_prefix=None)
STD_ANON_4.OFF = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value='OFF', tag='OFF')
STD_ANON_4.ON = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value='ON', tag='ON')
STD_ANON_4._InitializeFacetMap(STD_ANON_4._CF_enumeration)
_module_typeBindings.STD_ANON_4 = STD_ANON_4

# Atomic simple type: [anonymous]
class STD_ANON_5 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 125, 5)
    _Documentation = None
STD_ANON_5._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_5, enum_prefix=None)
STD_ANON_5.TURNOFF = STD_ANON_5._CF_enumeration.addEnumeration(unicode_value='TURNOFF', tag='TURNOFF')
STD_ANON_5.TURNON = STD_ANON_5._CF_enumeration.addEnumeration(unicode_value='TURNON', tag='TURNON')
STD_ANON_5.PERIOD = STD_ANON_5._CF_enumeration.addEnumeration(unicode_value='PERIOD', tag='PERIOD')
STD_ANON_5.ANGLE = STD_ANON_5._CF_enumeration.addEnumeration(unicode_value='ANGLE', tag='ANGLE')
STD_ANON_5.DROP_STAGE = STD_ANON_5._CF_enumeration.addEnumeration(unicode_value='DROP STAGE', tag='DROP_STAGE')
STD_ANON_5._InitializeFacetMap(STD_ANON_5._CF_enumeration)
_module_typeBindings.STD_ANON_5 = STD_ANON_5

# Atomic simple type: [anonymous]
class STD_ANON_6 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 140, 6)
    _Documentation = None
STD_ANON_6._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_6, enum_prefix=None)
STD_ANON_6.Landing = STD_ANON_6._CF_enumeration.addEnumeration(unicode_value='Landing', tag='Landing')
STD_ANON_6.Surface_activity = STD_ANON_6._CF_enumeration.addEnumeration(unicode_value='Surface activity', tag='Surface_activity')
STD_ANON_6.Launch = STD_ANON_6._CF_enumeration.addEnumeration(unicode_value='Launch', tag='Launch')
STD_ANON_6._InitializeFacetMap(STD_ANON_6._CF_enumeration)
_module_typeBindings.STD_ANON_6 = STD_ANON_6

# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 5, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element flight uses Python identifier flight
    __flight = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'flight'), 'flight', '__venus_CTD_ANON_flight', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 7, 1), )

    
    flight = property(__flight.value, __flight.set, None, None)

    
    # Element parameters uses Python identifier parameters
    __parameters = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'parameters'), 'parameters', '__venus_CTD_ANON_parameters', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 34, 1), )

    
    parameters = property(__parameters.value, __parameters.set, None, None)

    
    # Element contruction uses Python identifier contruction
    __contruction = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'contruction'), 'contruction', '__venus_CTD_ANON_contruction', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 60, 1), )

    
    contruction = property(__contruction.value, __contruction.set, None, None)

    
    # Element devices uses Python identifier devices
    __devices = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'devices'), 'devices', '__venus_CTD_ANON_devices', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 82, 1), )

    
    devices = property(__devices.value, __devices.set, None, None)

    
    # Element python_code uses Python identifier python_code
    __python_code = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'python_code'), 'python_code', '__venus_CTD_ANON_python_code', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 113, 1), )

    
    python_code = property(__python_code.value, __python_code.set, None, None)

    
    # Element program uses Python identifier program
    __program = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'program'), 'program', '__venus_CTD_ANON_program', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 114, 1), )

    
    program = property(__program.value, __program.set, None, None)

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__venus_CTD_ANON_name', pyxb.binding.datatypes.string)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 154, 6)
    __name._UseLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 154, 6)
    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute team uses Python identifier team
    __team = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'team'), 'team', '__venus_CTD_ANON_team', pyxb.binding.datatypes.string)
    __team._DeclarationLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 155, 6)
    __team._UseLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 155, 6)
    
    team = property(__team.value, __team.set, None, None)

    
    # Attribute tournament uses Python identifier tournament
    __tournament = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'tournament'), 'tournament', '__venus_CTD_ANON_tournament', pyxb.binding.datatypes.string)
    __tournament._DeclarationLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 156, 6)
    __tournament._UseLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 156, 6)
    
    tournament = property(__tournament.value, __tournament.set, None, None)

    _ElementMap.update({
        __flight.name() : __flight,
        __parameters.name() : __parameters,
        __contruction.name() : __contruction,
        __devices.name() : __devices,
        __python_code.name() : __python_code,
        __program.name() : __program
    })
    _AttributeMap.update({
        __name.name() : __name,
        __team.name() : __team,
        __tournament.name() : __tournament
    })
_module_typeBindings.CTD_ANON = CTD_ANON


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_ (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 8, 3)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element mission uses Python identifier mission
    __mission = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'mission'), 'mission', '__venus_CTD_ANON__mission', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 10, 7), )

    
    mission = property(__mission.value, __mission.set, None, None)

    
    # Element time uses Python identifier time
    __time = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'time'), 'time', '__venus_CTD_ANON__time', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 16, 7), )

    
    time = property(__time.value, __time.set, None, None)

    
    # Element start_height uses Python identifier start_height
    __start_height = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'start_height'), 'start_height', '__venus_CTD_ANON__start_height', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 21, 7), )

    
    start_height = property(__start_height.value, __start_height.set, None, None)

    
    # Element target_distance uses Python identifier target_distance
    __target_distance = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'target_distance'), 'target_distance', '__venus_CTD_ANON__target_distance', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 23, 7), )

    
    target_distance = property(__target_distance.value, __target_distance.set, None, None)

    
    # Element team uses Python identifier team
    __team = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'team'), 'team', '__venus_CTD_ANON__team', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 25, 7), )

    
    team = property(__team.value, __team.set, None, None)

    
    # Element tournament uses Python identifier tournament
    __tournament = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'tournament'), 'tournament', '__venus_CTD_ANON__tournament', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 27, 7), )

    
    tournament = property(__tournament.value, __tournament.set, None, None)

    
    # Element cycle_time uses Python identifier cycle_time
    __cycle_time = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'cycle_time'), 'cycle_time', '__venus_CTD_ANON__cycle_time', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 29, 10), )

    
    cycle_time = property(__cycle_time.value, __cycle_time.set, None, None)

    _ElementMap.update({
        __mission.name() : __mission,
        __time.name() : __time,
        __start_height.name() : __start_height,
        __target_distance.name() : __target_distance,
        __team.name() : __team,
        __tournament.name() : __tournament,
        __cycle_time.name() : __cycle_time
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_ = CTD_ANON_


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_2 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 11, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__venus_CTD_ANON_2_name', pyxb.binding.datatypes.string)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 12, 4)
    __name._UseLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 12, 4)
    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute view uses Python identifier view
    __view = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'view'), 'view', '__venus_CTD_ANON_2_view', pyxb.binding.datatypes.string)
    __view._DeclarationLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 13, 4)
    __view._UseLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 13, 4)
    
    view = property(__view.value, __view.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __name.name() : __name,
        __view.name() : __view
    })
_module_typeBindings.CTD_ANON_2 = CTD_ANON_2


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_3 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 17, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute start uses Python identifier start
    __start = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'start'), 'start', '__venus_CTD_ANON_3_start', pyxb.binding.datatypes.string)
    __start._DeclarationLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 18, 4)
    __start._UseLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 18, 4)
    
    start = property(__start.value, __start.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __start.name() : __start
    })
_module_typeBindings.CTD_ANON_3 = CTD_ANON_3


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_4 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 35, 3)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element radius_external uses Python identifier radius_external
    __radius_external = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'radius_external'), 'radius_external', '__venus_CTD_ANON_4_radius_external', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 37, 7), )

    
    radius_external = property(__radius_external.value, __radius_external.set, None, None)

    
    # Element radius_internal uses Python identifier radius_internal
    __radius_internal = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'radius_internal'), 'radius_internal', '__venus_CTD_ANON_4_radius_internal', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 39, 7), )

    
    radius_internal = property(__radius_internal.value, __radius_internal.set, None, None)

    
    # Element absorber uses Python identifier absorber
    __absorber = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'absorber'), 'absorber', '__venus_CTD_ANON_4_absorber', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 41, 7), )

    
    absorber = property(__absorber.value, __absorber.set, None, None)

    
    # Element isolator uses Python identifier isolator
    __isolator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'isolator'), 'isolator', '__venus_CTD_ANON_4_isolator', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 49, 7), )

    
    isolator = property(__isolator.value, __isolator.set, None, None)

    _ElementMap.update({
        __radius_external.name() : __radius_external,
        __radius_internal.name() : __radius_internal,
        __absorber.name() : __absorber,
        __isolator.name() : __isolator
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
    _XSDLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 61, 3)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element stage uses Python identifier stage
    __stage = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'stage'), 'stage', '__venus_CTD_ANON_5_stage', True, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 63, 12), )

    
    stage = property(__stage.value, __stage.set, None, None)

    _ElementMap.update({
        __stage.name() : __stage
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
    _XSDLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 83, 3)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element device uses Python identifier device
    __device = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'device'), 'device', '__venus_CTD_ANON_6_device', True, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 85, 7), )

    
    device = property(__device.value, __device.set, None, None)

    _ElementMap.update({
        __device.name() : __device
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_6 = CTD_ANON_6


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_7 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 115, 3)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element stage uses Python identifier stage
    __stage = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'stage'), 'stage', '__venus_CTD_ANON_7_stage', True, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 117, 7), )

    
    stage = property(__stage.value, __stage.set, None, None)

    _ElementMap.update({
        __stage.name() : __stage
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_7 = CTD_ANON_7


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_8 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 64, 16)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute number uses Python identifier number
    __number = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'number'), 'number', '__venus_CTD_ANON_8_number', pyxb.binding.datatypes.positiveInteger)
    __number._DeclarationLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 65, 18)
    __number._UseLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 65, 18)
    
    number = property(__number.value, __number.set, None, None)

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__venus_CTD_ANON_8_name', pyxb.binding.datatypes.string)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 66, 18)
    __name._UseLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 66, 18)
    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute geometry uses Python identifier geometry
    __geometry = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'geometry'), 'geometry', '__venus_CTD_ANON_8_geometry', _module_typeBindings.STD_ANON_2)
    __geometry._DeclarationLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 67, 18)
    __geometry._UseLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 67, 18)
    
    geometry = property(__geometry.value, __geometry.set, None, None)

    
    # Attribute radius uses Python identifier radius
    __radius = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'radius'), 'radius', '__venus_CTD_ANON_8_radius', pyxb.binding.datatypes.decimal)
    __radius._DeclarationLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 75, 18)
    __radius._UseLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 75, 18)
    
    radius = property(__radius.value, __radius.set, None, None)

    
    # Attribute length uses Python identifier length
    __length = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'length'), 'length', '__venus_CTD_ANON_8_length', pyxb.binding.datatypes.decimal)
    __length._DeclarationLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 76, 18)
    __length._UseLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 76, 18)
    
    length = property(__length.value, __length.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __number.name() : __number,
        __name.name() : __name,
        __geometry.name() : __geometry,
        __radius.name() : __radius,
        __length.name() : __length
    })
_module_typeBindings.CTD_ANON_8 = CTD_ANON_8


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_9 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 86, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute number uses Python identifier number
    __number = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'number'), 'number', '__venus_CTD_ANON_9_number', pyxb.binding.datatypes.positiveInteger)
    __number._DeclarationLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 87, 4)
    __number._UseLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 87, 4)
    
    number = property(__number.value, __number.set, None, None)

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__venus_CTD_ANON_9_name', pyxb.binding.datatypes.string)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 88, 4)
    __name._UseLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 88, 4)
    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute springs uses Python identifier springs
    __springs = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'springs'), 'springs', '__venus_CTD_ANON_9_springs', pyxb.binding.datatypes.positiveInteger)
    __springs._DeclarationLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 89, 10)
    __springs._UseLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 89, 10)
    
    springs = property(__springs.value, __springs.set, None, None)

    
    # Attribute springs_length uses Python identifier springs_length
    __springs_length = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'springs_length'), 'springs_length', '__venus_CTD_ANON_9_springs_length', pyxb.binding.datatypes.float)
    __springs_length._DeclarationLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 90, 10)
    __springs_length._UseLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 90, 10)
    
    springs_length = property(__springs_length.value, __springs_length.set, None, None)

    
    # Attribute start_state uses Python identifier start_state
    __start_state = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'start_state'), 'start_state', '__venus_CTD_ANON_9_start_state', _module_typeBindings.STD_ANON_3)
    __start_state._DeclarationLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 91, 4)
    __start_state._UseLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 91, 4)
    
    start_state = property(__start_state.value, __start_state.set, None, None)

    
    # Attribute in_safe_mode uses Python identifier in_safe_mode
    __in_safe_mode = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'in_safe_mode'), 'in_safe_mode', '__venus_CTD_ANON_9_in_safe_mode', _module_typeBindings.STD_ANON_4)
    __in_safe_mode._DeclarationLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 99, 4)
    __in_safe_mode._UseLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 99, 4)
    
    in_safe_mode = property(__in_safe_mode.value, __in_safe_mode.set, None, None)

    
    # Attribute stage uses Python identifier stage
    __stage = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'stage'), 'stage', '__venus_CTD_ANON_9_stage', pyxb.binding.datatypes.positiveInteger)
    __stage._DeclarationLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 107, 10)
    __stage._UseLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 107, 10)
    
    stage = property(__stage.value, __stage.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __number.name() : __number,
        __name.name() : __name,
        __springs.name() : __springs,
        __springs_length.name() : __springs_length,
        __start_state.name() : __start_state,
        __in_safe_mode.name() : __in_safe_mode,
        __stage.name() : __stage
    })
_module_typeBindings.CTD_ANON_9 = CTD_ANON_9


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_10 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 118, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element command uses Python identifier command
    __command = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'command'), 'command', '__venus_CTD_ANON_10_command', True, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 120, 6), )

    
    command = property(__command.value, __command.set, None, None)

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', '__venus_CTD_ANON_10_id', _module_typeBindings.STD_ANON_6)
    __id._DeclarationLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 139, 4)
    __id._UseLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 139, 4)
    
    id = property(__id.value, __id.set, None, None)

    _ElementMap.update({
        __command.name() : __command
    })
    _AttributeMap.update({
        __id.name() : __id
    })
_module_typeBindings.CTD_ANON_10 = CTD_ANON_10


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_11 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 121, 8)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute time uses Python identifier time
    __time = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'time'), 'time', '__venus_CTD_ANON_11_time', pyxb.binding.datatypes.nonNegativeInteger)
    __time._DeclarationLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 122, 3)
    __time._UseLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 122, 3)
    
    time = property(__time.value, __time.set, None, None)

    
    # Attribute device uses Python identifier device
    __device = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'device'), 'device', '__venus_CTD_ANON_11_device', pyxb.binding.datatypes.string)
    __device._DeclarationLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 123, 3)
    __device._UseLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 123, 3)
    
    device = property(__device.value, __device.set, None, None)

    
    # Attribute action uses Python identifier action
    __action = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'action'), 'action', '__venus_CTD_ANON_11_action', _module_typeBindings.STD_ANON_5)
    __action._DeclarationLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 124, 3)
    __action._UseLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 124, 3)
    
    action = property(__action.value, __action.set, None, None)

    
    # Attribute argument uses Python identifier argument
    __argument = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'argument'), 'argument', '__venus_CTD_ANON_11_argument', pyxb.binding.datatypes.string)
    __argument._DeclarationLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 135, 3)
    __argument._UseLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 135, 3)
    
    argument = property(__argument.value, __argument.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __time.name() : __time,
        __device.name() : __device,
        __action.name() : __action,
        __argument.name() : __argument
    })
_module_typeBindings.CTD_ANON_11 = CTD_ANON_11


probe = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'probe'), CTD_ANON, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 4, 2))
Namespace.addCategoryObject('elementBinding', probe.name().localName(), probe)



CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'flight'), CTD_ANON_, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 7, 1)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'parameters'), CTD_ANON_4, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 34, 1)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'contruction'), CTD_ANON_5, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 60, 1)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'devices'), CTD_ANON_6, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 82, 1)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'python_code'), pyxb.binding.datatypes.string, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 113, 1)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'program'), CTD_ANON_7, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 114, 1)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 60, 1))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 113, 1))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 114, 1))
    counters.add(cc_2)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, 'flight')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 7, 1))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, 'parameters')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 34, 1))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, 'contruction')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 60, 1))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, 'devices')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 82, 1))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, 'python_code')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 113, 1))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, 'program')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 114, 1))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
         ]))
    transitions.append(fac.Transition(st_5, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton()




CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'mission'), CTD_ANON_2, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 10, 7)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'time'), CTD_ANON_3, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 16, 7)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'start_height'), pyxb.binding.datatypes.decimal, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 21, 7)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'target_distance'), pyxb.binding.datatypes.decimal, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 23, 7)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'team'), pyxb.binding.datatypes.string, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 25, 7)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'tournament'), pyxb.binding.datatypes.string, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 27, 7)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'cycle_time'), pyxb.binding.datatypes.float, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 29, 10)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 16, 7))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 23, 7))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 25, 7))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 27, 7))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 29, 10))
    counters.add(cc_4)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'mission')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 10, 7))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'time')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 16, 7))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'start_height')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 21, 7))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'target_distance')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 23, 7))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'team')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 25, 7))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'tournament')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 27, 7))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'cycle_time')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 29, 10))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, True) ]))
    st_6._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_._Automaton = _BuildAutomaton_()




CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'radius_external'), pyxb.binding.datatypes.decimal, scope=CTD_ANON_4, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 37, 7)))

CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'radius_internal'), pyxb.binding.datatypes.decimal, scope=CTD_ANON_4, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 39, 7)))

CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'absorber'), STD_ANON, scope=CTD_ANON_4, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 41, 7)))

CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'isolator'), STD_ANON_, scope=CTD_ANON_4, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 49, 7)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 39, 7))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, 'radius_external')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 37, 7))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, 'radius_internal')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 39, 7))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, 'absorber')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 41, 7))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, 'isolator')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 49, 7))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_4._Automaton = _BuildAutomaton_2()




CTD_ANON_5._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'stage'), CTD_ANON_8, scope=CTD_ANON_5, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 63, 12)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 63, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_5._UseForTag(pyxb.namespace.ExpandedName(None, 'stage')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 63, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_5._Automaton = _BuildAutomaton_3()




CTD_ANON_6._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'device'), CTD_ANON_9, scope=CTD_ANON_6, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 85, 7)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 85, 7))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(None, 'device')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 85, 7))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_6._Automaton = _BuildAutomaton_4()




CTD_ANON_7._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'stage'), CTD_ANON_10, scope=CTD_ANON_7, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 117, 7)))

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=1, max=3, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 117, 7))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_7._UseForTag(pyxb.namespace.ExpandedName(None, 'stage')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 117, 7))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_7._Automaton = _BuildAutomaton_5()




CTD_ANON_10._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'command'), CTD_ANON_11, scope=CTD_ANON_10, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 120, 6)))

def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 120, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_10._UseForTag(pyxb.namespace.ExpandedName(None, 'command')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/probe.xsd', 120, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_10._Automaton = _BuildAutomaton_6()

