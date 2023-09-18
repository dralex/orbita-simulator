# ./venus/devices.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:c8721b651877e875de2bb1e7a1f0988806e26562
# Generated 2023-09-18 15:19:28.157134 by PyXB version 1.2.6 using Python 3.10.12.final.0
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
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:9ce37600-561d-11ee-a2f3-e1473c71107c')

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
    _XSDLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 11, 2)
    _Documentation = None
STD_ANON._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON, enum_prefix=None)
STD_ANON.Generators = STD_ANON._CF_enumeration.addEnumeration(unicode_value='Generators', tag='Generators')
STD_ANON.Transmitters = STD_ANON._CF_enumeration.addEnumeration(unicode_value='Transmitters', tag='Transmitters')
STD_ANON.Base_diagnostics = STD_ANON._CF_enumeration.addEnumeration(unicode_value='Base diagnostics', tag='Base_diagnostics')
STD_ANON.Advanced_diagnostics = STD_ANON._CF_enumeration.addEnumeration(unicode_value='Advanced diagnostics', tag='Advanced_diagnostics')
STD_ANON.Scientific_equipment = STD_ANON._CF_enumeration.addEnumeration(unicode_value='Scientific equipment', tag='Scientific_equipment')
STD_ANON.Control = STD_ANON._CF_enumeration.addEnumeration(unicode_value='Control', tag='Control')
STD_ANON.Engines = STD_ANON._CF_enumeration.addEnumeration(unicode_value='Engines', tag='Engines')
STD_ANON.Fuel_tanks = STD_ANON._CF_enumeration.addEnumeration(unicode_value='Fuel tanks', tag='Fuel_tanks')
STD_ANON.Parachutes = STD_ANON._CF_enumeration.addEnumeration(unicode_value='Parachutes', tag='Parachutes')
STD_ANON.Dampers = STD_ANON._CF_enumeration.addEnumeration(unicode_value='Dampers', tag='Dampers')
STD_ANON.Accumulators = STD_ANON._CF_enumeration.addEnumeration(unicode_value='Accumulators', tag='Accumulators')
STD_ANON.Solar_panels = STD_ANON._CF_enumeration.addEnumeration(unicode_value='Solar panels', tag='Solar_panels')
STD_ANON._InitializeFacetMap(STD_ANON._CF_enumeration)
_module_typeBindings.STD_ANON = STD_ANON

# Atomic simple type: [anonymous]
class STD_ANON_ (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 50, 16)
    _Documentation = None
STD_ANON_._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_, enum_prefix=None)
STD_ANON_.springs_length = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='springs_length', tag='springs_length')
STD_ANON_.springs = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='springs', tag='springs')
STD_ANON_._InitializeFacetMap(STD_ANON_._CF_enumeration)
_module_typeBindings.STD_ANON_ = STD_ANON_

# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 5, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element device uses Python identifier device
    __device = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'device'), 'device', '__venus_CTD_ANON_device', True, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 7, 1), )

    
    device = property(__device.value, __device.set, None, None)

    _ElementMap.update({
        __device.name() : __device
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
    _XSDLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 8, 3)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element type uses Python identifier type
    __type = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'type'), 'type', '__venus_CTD_ANON__type', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 10, 7), )

    
    type = property(__type.value, __type.set, None, None)

    
    # Element mass uses Python identifier mass
    __mass = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'mass'), 'mass', '__venus_CTD_ANON__mass', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 28, 7), )

    
    mass = property(__mass.value, __mass.set, None, None)

    
    # Element volume uses Python identifier volume
    __volume = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'volume'), 'volume', '__venus_CTD_ANON__volume', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 29, 7), )

    
    volume = property(__volume.value, __volume.set, None, None)

    
    # Element power_generation uses Python identifier power_generation
    __power_generation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'power_generation'), 'power_generation', '__venus_CTD_ANON__power_generation', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 30, 7), )

    
    power_generation = property(__power_generation.value, __power_generation.set, None, None)

    
    # Element solar_power uses Python identifier solar_power
    __solar_power = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'solar_power'), 'solar_power', '__venus_CTD_ANON__solar_power', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 31, 10), )

    
    solar_power = property(__solar_power.value, __solar_power.set, None, None)

    
    # Element capacity uses Python identifier capacity
    __capacity = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'capacity'), 'capacity', '__venus_CTD_ANON__capacity', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 32, 10), )

    
    capacity = property(__capacity.value, __capacity.set, None, None)

    
    # Element period_min uses Python identifier period_min
    __period_min = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'period_min'), 'period_min', '__venus_CTD_ANON__period_min', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 33, 7), )

    
    period_min = property(__period_min.value, __period_min.set, None, None)

    
    # Element period_max uses Python identifier period_max
    __period_max = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'period_max'), 'period_max', '__venus_CTD_ANON__period_max', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 34, 7), )

    
    period_max = property(__period_max.value, __period_max.set, None, None)

    
    # Element traffic_generation uses Python identifier traffic_generation
    __traffic_generation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'traffic_generation'), 'traffic_generation', '__venus_CTD_ANON__traffic_generation', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 35, 7), )

    
    traffic_generation = property(__traffic_generation.value, __traffic_generation.set, None, None)

    
    # Element critical_temperature uses Python identifier critical_temperature
    __critical_temperature = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'critical_temperature'), 'critical_temperature', '__venus_CTD_ANON__critical_temperature', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 36, 7), )

    
    critical_temperature = property(__critical_temperature.value, __critical_temperature.set, None, None)

    
    # Element fuel_speed uses Python identifier fuel_speed
    __fuel_speed = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'fuel_speed'), 'fuel_speed', '__venus_CTD_ANON__fuel_speed', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 37, 7), )

    
    fuel_speed = property(__fuel_speed.value, __fuel_speed.set, None, None)

    
    # Element traction uses Python identifier traction
    __traction = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'traction'), 'traction', '__venus_CTD_ANON__traction', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 38, 7), )

    
    traction = property(__traction.value, __traction.set, None, None)

    
    # Element max_speed uses Python identifier max_speed
    __max_speed = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'max_speed'), 'max_speed', '__venus_CTD_ANON__max_speed', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 39, 7), )

    
    max_speed = property(__max_speed.value, __max_speed.set, None, None)

    
    # Element energy_compensation uses Python identifier energy_compensation
    __energy_compensation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'energy_compensation'), 'energy_compensation', '__venus_CTD_ANON__energy_compensation', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 40, 10), )

    
    energy_compensation = property(__energy_compensation.value, __energy_compensation.set, None, None)

    
    # Element parachute_square uses Python identifier parachute_square
    __parachute_square = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'parachute_square'), 'parachute_square', '__venus_CTD_ANON__parachute_square', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 41, 7), )

    
    parachute_square = property(__parachute_square.value, __parachute_square.set, None, None)

    
    # Element scientific_limit uses Python identifier scientific_limit
    __scientific_limit = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'scientific_limit'), 'scientific_limit', '__venus_CTD_ANON__scientific_limit', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 42, 7), )

    
    scientific_limit = property(__scientific_limit.value, __scientific_limit.set, None, None)

    
    # Element thermal_protection uses Python identifier thermal_protection
    __thermal_protection = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'thermal_protection'), 'thermal_protection', '__venus_CTD_ANON__thermal_protection', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 43, 7), )

    
    thermal_protection = property(__thermal_protection.value, __thermal_protection.set, None, None)

    
    # Element k_spring uses Python identifier k_spring
    __k_spring = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'k_spring'), 'k_spring', '__venus_CTD_ANON__k_spring', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 44, 7), )

    
    k_spring = property(__k_spring.value, __k_spring.set, None, None)

    
    # Element m_spring uses Python identifier m_spring
    __m_spring = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'm_spring'), 'm_spring', '__venus_CTD_ANON__m_spring', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 45, 10), )

    
    m_spring = property(__m_spring.value, __m_spring.set, None, None)

    
    # Element max_springs uses Python identifier max_springs
    __max_springs = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'max_springs'), 'max_springs', '__venus_CTD_ANON__max_springs', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 46, 10), )

    
    max_springs = property(__max_springs.value, __max_springs.set, None, None)

    
    # Element max_springs_length uses Python identifier max_springs_length
    __max_springs_length = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'max_springs_length'), 'max_springs_length', '__venus_CTD_ANON__max_springs_length', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 47, 10), )

    
    max_springs_length = property(__max_springs_length.value, __max_springs_length.set, None, None)

    
    # Element custom uses Python identifier custom
    __custom = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'custom'), 'custom', '__venus_CTD_ANON__custom', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 48, 10), )

    
    custom = property(__custom.value, __custom.set, None, None)

    
    # Element custom_param uses Python identifier custom_param
    __custom_param = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'custom_param'), 'custom_param', '__venus_CTD_ANON__custom_param', True, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 49, 10), )

    
    custom_param = property(__custom_param.value, __custom_param.set, None, None)

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__venus_CTD_ANON__name', pyxb.binding.datatypes.string)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 58, 5)
    __name._UseLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 58, 5)
    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute full_name uses Python identifier full_name
    __full_name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'full_name'), 'full_name', '__venus_CTD_ANON__full_name', pyxb.binding.datatypes.string)
    __full_name._DeclarationLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 59, 5)
    __full_name._UseLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 59, 5)
    
    full_name = property(__full_name.value, __full_name.set, None, None)

    
    # Attribute code uses Python identifier code
    __code = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'code'), 'code', '__venus_CTD_ANON__code', pyxb.binding.datatypes.string)
    __code._DeclarationLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 60, 5)
    __code._UseLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 60, 5)
    
    code = property(__code.value, __code.set, None, None)

    _ElementMap.update({
        __type.name() : __type,
        __mass.name() : __mass,
        __volume.name() : __volume,
        __power_generation.name() : __power_generation,
        __solar_power.name() : __solar_power,
        __capacity.name() : __capacity,
        __period_min.name() : __period_min,
        __period_max.name() : __period_max,
        __traffic_generation.name() : __traffic_generation,
        __critical_temperature.name() : __critical_temperature,
        __fuel_speed.name() : __fuel_speed,
        __traction.name() : __traction,
        __max_speed.name() : __max_speed,
        __energy_compensation.name() : __energy_compensation,
        __parachute_square.name() : __parachute_square,
        __scientific_limit.name() : __scientific_limit,
        __thermal_protection.name() : __thermal_protection,
        __k_spring.name() : __k_spring,
        __m_spring.name() : __m_spring,
        __max_springs.name() : __max_springs,
        __max_springs_length.name() : __max_springs_length,
        __custom.name() : __custom,
        __custom_param.name() : __custom_param
    })
    _AttributeMap.update({
        __name.name() : __name,
        __full_name.name() : __full_name,
        __code.name() : __code
    })
_module_typeBindings.CTD_ANON_ = CTD_ANON_


devices = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'devices'), CTD_ANON, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 4, 2))
Namespace.addCategoryObject('elementBinding', devices.name().localName(), devices)



CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'device'), CTD_ANON_, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 7, 1)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, 'device')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 7, 1))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton()




CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'type'), STD_ANON, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 10, 7)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'mass'), pyxb.binding.datatypes.decimal, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 28, 7)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'volume'), pyxb.binding.datatypes.decimal, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 29, 7)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'power_generation'), pyxb.binding.datatypes.float, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 30, 7)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'solar_power'), pyxb.binding.datatypes.float, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 31, 10)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'capacity'), pyxb.binding.datatypes.float, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 32, 10)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'period_min'), pyxb.binding.datatypes.positiveInteger, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 33, 7)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'period_max'), pyxb.binding.datatypes.positiveInteger, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 34, 7)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'traffic_generation'), pyxb.binding.datatypes.float, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 35, 7)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'critical_temperature'), pyxb.binding.datatypes.float, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 36, 7)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'fuel_speed'), pyxb.binding.datatypes.float, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 37, 7)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'traction'), pyxb.binding.datatypes.float, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 38, 7)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'max_speed'), pyxb.binding.datatypes.decimal, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 39, 7)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'energy_compensation'), pyxb.binding.datatypes.decimal, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 40, 10)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'parachute_square'), pyxb.binding.datatypes.decimal, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 41, 7)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'scientific_limit'), pyxb.binding.datatypes.decimal, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 42, 7)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'thermal_protection'), pyxb.binding.datatypes.decimal, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 43, 7)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'k_spring'), pyxb.binding.datatypes.float, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 44, 7)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'm_spring'), pyxb.binding.datatypes.float, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 45, 10)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'max_springs'), pyxb.binding.datatypes.positiveInteger, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 46, 10)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'max_springs_length'), pyxb.binding.datatypes.float, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 47, 10)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'custom'), pyxb.binding.datatypes.boolean, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 48, 10)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'custom_param'), STD_ANON_, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 49, 10)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 30, 7))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 31, 10))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 32, 10))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 33, 7))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 34, 7))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 35, 7))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 37, 7))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 38, 7))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 39, 7))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 40, 10))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 41, 7))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 42, 7))
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 43, 7))
    counters.add(cc_12)
    cc_13 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 44, 7))
    counters.add(cc_13)
    cc_14 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 45, 10))
    counters.add(cc_14)
    cc_15 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 46, 10))
    counters.add(cc_15)
    cc_16 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 47, 10))
    counters.add(cc_16)
    cc_17 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 48, 10))
    counters.add(cc_17)
    cc_18 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 49, 10))
    counters.add(cc_18)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'type')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 10, 7))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'mass')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 28, 7))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'volume')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 29, 7))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'power_generation')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 30, 7))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'solar_power')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 31, 10))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'capacity')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 32, 10))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'period_min')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 33, 7))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'period_max')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 34, 7))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'traffic_generation')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 35, 7))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'critical_temperature')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 36, 7))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'fuel_speed')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 37, 7))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'traction')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 38, 7))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'max_speed')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 39, 7))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'energy_compensation')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 40, 10))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'parachute_square')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 41, 7))
    st_14 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_11, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'scientific_limit')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 42, 7))
    st_15 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'thermal_protection')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 43, 7))
    st_16 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_16)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_13, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'k_spring')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 44, 7))
    st_17 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_17)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_14, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'm_spring')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 45, 10))
    st_18 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_18)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_15, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'max_springs')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 46, 10))
    st_19 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_19)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_16, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'max_springs_length')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 47, 10))
    st_20 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_20)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_17, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'custom')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 48, 10))
    st_21 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_21)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_18, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'custom_param')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/devices.xsd', 49, 10))
    st_22 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_22)
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
    transitions.append(fac.Transition(st_4, [
         ]))
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
    transitions.append(fac.Transition(st_7, [
         ]))
    transitions.append(fac.Transition(st_8, [
         ]))
    transitions.append(fac.Transition(st_9, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
         ]))
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
    transitions.append(fac.Transition(st_16, [
         ]))
    transitions.append(fac.Transition(st_17, [
         ]))
    transitions.append(fac.Transition(st_18, [
         ]))
    transitions.append(fac.Transition(st_19, [
         ]))
    transitions.append(fac.Transition(st_20, [
         ]))
    transitions.append(fac.Transition(st_21, [
         ]))
    transitions.append(fac.Transition(st_22, [
         ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_7, False) ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_8, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_8, False) ]))
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_9, False) ]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_10, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_10, False) ]))
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_11, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_11, False) ]))
    st_15._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_12, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_12, False) ]))
    st_16._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_13, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_13, False) ]))
    st_17._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_14, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_14, False) ]))
    st_18._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_15, True) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_15, False) ]))
    st_19._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_16, True) ]))
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_16, False) ]))
    st_20._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_21, [
        fac.UpdateInstruction(cc_17, True) ]))
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_17, False) ]))
    st_21._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_22, [
        fac.UpdateInstruction(cc_18, True) ]))
    st_22._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_._Automaton = _BuildAutomaton_()

