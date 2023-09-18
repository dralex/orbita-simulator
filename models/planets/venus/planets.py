# ./venus/planets.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:c8721b651877e875de2bb1e7a1f0988806e26562
# Generated 2023-09-18 15:19:28.000981 by PyXB version 1.2.6 using Python 3.10.12.final.0
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
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:9ccc0b64-561d-11ee-a2f3-e1473c71107c')

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


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 5, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element planet uses Python identifier planet
    __planet = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'planet'), 'planet', '__venus_CTD_ANON_planet', True, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 7, 7), )

    
    planet = property(__planet.value, __planet.set, None, None)

    _ElementMap.update({
        __planet.name() : __planet
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
    _XSDLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 8, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element radius uses Python identifier radius
    __radius = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'radius'), 'radius', '__venus_CTD_ANON__radius', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 11, 6), )

    
    radius = property(__radius.value, __radius.set, None, None)

    
    # Element mass uses Python identifier mass
    __mass = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'mass'), 'mass', '__venus_CTD_ANON__mass', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 13, 6), )

    
    mass = property(__mass.value, __mass.set, None, None)

    
    # Element rotation uses Python identifier rotation
    __rotation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'rotation'), 'rotation', '__venus_CTD_ANON__rotation', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 15, 6), )

    
    rotation = property(__rotation.value, __rotation.set, None, None)

    
    # Element atmosphere uses Python identifier atmosphere
    __atmosphere = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'atmosphere'), 'atmosphere', '__venus_CTD_ANON__atmosphere', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 27, 6), )

    
    atmosphere = property(__atmosphere.value, __atmosphere.set, None, None)

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__venus_CTD_ANON__name', pyxb.binding.datatypes.string)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 9, 4)
    __name._UseLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 9, 4)
    
    name = property(__name.value, __name.set, None, None)

    _ElementMap.update({
        __radius.name() : __radius,
        __mass.name() : __mass,
        __rotation.name() : __rotation,
        __atmosphere.name() : __atmosphere
    })
    _AttributeMap.update({
        __name.name() : __name
    })
_module_typeBindings.CTD_ANON_ = CTD_ANON_


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_2 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 16, 8)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element hours uses Python identifier hours
    __hours = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'hours'), 'hours', '__venus_CTD_ANON_2_hours', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 18, 5), )

    
    hours = property(__hours.value, __hours.set, None, None)

    
    # Element minutes uses Python identifier minutes
    __minutes = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'minutes'), 'minutes', '__venus_CTD_ANON_2_minutes', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 20, 5), )

    
    minutes = property(__minutes.value, __minutes.set, None, None)

    
    # Element seconds uses Python identifier seconds
    __seconds = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'seconds'), 'seconds', '__venus_CTD_ANON_2_seconds', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 22, 5), )

    
    seconds = property(__seconds.value, __seconds.set, None, None)

    _ElementMap.update({
        __hours.name() : __hours,
        __minutes.name() : __minutes,
        __seconds.name() : __seconds
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_2 = CTD_ANON_2


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_3 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 28, 8)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element height uses Python identifier height
    __height = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'height'), 'height', '__venus_CTD_ANON_3_height', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 30, 5), )

    
    height = property(__height.value, __height.set, None, None)

    
    # Element density_border uses Python identifier density_border
    __density_border = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'density_border'), 'density_border', '__venus_CTD_ANON_3_density_border', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 32, 5), )

    
    density_border = property(__density_border.value, __density_border.set, None, None)

    
    # Element T_ground uses Python identifier T_ground
    __T_ground = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'T_ground'), 'T_ground', '__venus_CTD_ANON_3_T_ground', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 34, 5), )

    
    T_ground = property(__T_ground.value, __T_ground.set, None, None)

    
    # Element T_grad uses Python identifier T_grad
    __T_grad = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'T_grad'), 'T_grad', '__venus_CTD_ANON_3_T_grad', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 36, 5), )

    
    T_grad = property(__T_grad.value, __T_grad.set, None, None)

    
    # Element P_ground uses Python identifier P_ground
    __P_ground = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'P_ground'), 'P_ground', '__venus_CTD_ANON_3_P_ground', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 38, 5), )

    
    P_ground = property(__P_ground.value, __P_ground.set, None, None)

    
    # Element P_coeff uses Python identifier P_coeff
    __P_coeff = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'P_coeff'), 'P_coeff', '__venus_CTD_ANON_3_P_coeff', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 40, 5), )

    
    P_coeff = property(__P_coeff.value, __P_coeff.set, None, None)

    
    # Element C uses Python identifier C
    __C = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'C'), 'C', '__venus_CTD_ANON_3_C', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 42, 14), )

    
    C = property(__C.value, __C.set, None, None)

    _ElementMap.update({
        __height.name() : __height,
        __density_border.name() : __density_border,
        __T_ground.name() : __T_ground,
        __T_grad.name() : __T_grad,
        __P_ground.name() : __P_ground,
        __P_coeff.name() : __P_coeff,
        __C.name() : __C
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_3 = CTD_ANON_3


planets = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'planets'), CTD_ANON, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 4, 2))
Namespace.addCategoryObject('elementBinding', planets.name().localName(), planets)



CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'planet'), CTD_ANON_, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 7, 7)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, 'planet')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 7, 7))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton()




CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'radius'), pyxb.binding.datatypes.float, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 11, 6)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'mass'), pyxb.binding.datatypes.float, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 13, 6)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'rotation'), CTD_ANON_2, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 15, 6)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'atmosphere'), CTD_ANON_3, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 27, 6)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 15, 6))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'radius')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 11, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'mass')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 13, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'rotation')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 15, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'atmosphere')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 27, 6))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
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
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_._Automaton = _BuildAutomaton_()




CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'hours'), pyxb.binding.datatypes.integer, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 18, 5)))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'minutes'), pyxb.binding.datatypes.integer, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 20, 5)))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'seconds'), pyxb.binding.datatypes.integer, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 22, 5)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, 'hours')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 18, 5))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, 'minutes')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 20, 5))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, 'seconds')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 22, 5))
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
CTD_ANON_2._Automaton = _BuildAutomaton_2()




CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'height'), pyxb.binding.datatypes.decimal, scope=CTD_ANON_3, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 30, 5)))

CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'density_border'), pyxb.binding.datatypes.decimal, scope=CTD_ANON_3, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 32, 5)))

CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'T_ground'), pyxb.binding.datatypes.decimal, scope=CTD_ANON_3, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 34, 5)))

CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'T_grad'), pyxb.binding.datatypes.decimal, scope=CTD_ANON_3, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 36, 5)))

CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'P_ground'), pyxb.binding.datatypes.decimal, scope=CTD_ANON_3, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 38, 5)))

CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'P_coeff'), pyxb.binding.datatypes.decimal, scope=CTD_ANON_3, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 40, 5)))

CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'C'), pyxb.binding.datatypes.float, scope=CTD_ANON_3, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 42, 14)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 42, 14))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(None, 'height')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 30, 5))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(None, 'density_border')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 32, 5))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(None, 'T_ground')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 34, 5))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(None, 'T_grad')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 36, 5))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(None, 'P_ground')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 38, 5))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(None, 'P_coeff')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 40, 5))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(None, 'C')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/planets.xsd', 42, 14))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
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
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_6._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_3._Automaton = _BuildAutomaton_3()

