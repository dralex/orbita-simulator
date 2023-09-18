# ./venus/global_config.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:c8721b651877e875de2bb1e7a1f0988806e26562
# Generated 2023-09-18 15:19:28.659564 by PyXB version 1.2.6 using Python 3.10.12.final.0
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
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:9d2f779e-561d-11ee-a2f3-e1473c71107c')

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
    _XSDLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 5, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element logging uses Python identifier logging
    __logging = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'logging'), 'logging', '__venus_CTD_ANON_logging', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 7, 1), )

    
    logging = property(__logging.value, __logging.set, None, None)

    _ElementMap.update({
        __logging.name() : __logging
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
    _XSDLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 8, 3)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element debug_diagn_period uses Python identifier debug_diagn_period
    __debug_diagn_period = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'debug_diagn_period'), 'debug_diagn_period', '__venus_CTD_ANON__debug_diagn_period', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 10, 7), )

    
    debug_diagn_period = property(__debug_diagn_period.value, __debug_diagn_period.set, None, None)

    
    # Element short_log_len uses Python identifier short_log_len
    __short_log_len = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'short_log_len'), 'short_log_len', '__venus_CTD_ANON__short_log_len', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 12, 7), )

    
    short_log_len = property(__short_log_len.value, __short_log_len.set, None, None)

    
    # Element empty_image uses Python identifier empty_image
    __empty_image = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'empty_image'), 'empty_image', '__venus_CTD_ANON__empty_image', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 14, 7), )

    
    empty_image = property(__empty_image.value, __empty_image.set, None, None)

    
    # Element mission uses Python identifier mission
    __mission = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'mission'), 'mission', '__venus_CTD_ANON__mission', True, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 16, 7), )

    
    mission = property(__mission.value, __mission.set, None, None)

    _ElementMap.update({
        __debug_diagn_period.name() : __debug_diagn_period,
        __short_log_len.name() : __short_log_len,
        __empty_image.name() : __empty_image,
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
    _XSDLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 17, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element debug_constants uses Python identifier debug_constants
    __debug_constants = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'debug_constants'), 'debug_constants', '__venus_CTD_ANON_2_debug_constants', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 20, 12), )

    
    debug_constants = property(__debug_constants.value, __debug_constants.set, None, None)

    
    # Element debug_probe uses Python identifier debug_probe
    __debug_probe = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'debug_probe'), 'debug_probe', '__venus_CTD_ANON_2_debug_probe', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 21, 12), )

    
    debug_probe = property(__debug_probe.value, __debug_probe.set, None, None)

    
    # Element landing uses Python identifier landing
    __landing = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'landing'), 'landing', '__venus_CTD_ANON_2_landing', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 22, 6), )

    
    landing = property(__landing.value, __landing.set, None, None)

    
    # Element surface_activity uses Python identifier surface_activity
    __surface_activity = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'surface_activity'), 'surface_activity', '__venus_CTD_ANON_2_surface_activity', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 51, 6), )

    
    surface_activity = property(__surface_activity.value, __surface_activity.set, None, None)

    
    # Element launch uses Python identifier launch
    __launch = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'launch'), 'launch', '__venus_CTD_ANON_2_launch', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 80, 6), )

    
    launch = property(__launch.value, __launch.set, None, None)

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__venus_CTD_ANON_2_name', pyxb.binding.datatypes.string)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 18, 4)
    __name._UseLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 18, 4)
    
    name = property(__name.value, __name.set, None, None)

    _ElementMap.update({
        __debug_constants.name() : __debug_constants,
        __debug_probe.name() : __debug_probe,
        __landing.name() : __landing,
        __surface_activity.name() : __surface_activity,
        __launch.name() : __launch
    })
    _AttributeMap.update({
        __name.name() : __name
    })
_module_typeBindings.CTD_ANON_2 = CTD_ANON_2


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_3 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 23, 8)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element mission_log uses Python identifier mission_log
    __mission_log = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'mission_log'), 'mission_log', '__venus_CTD_ANON_3_mission_log', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 25, 5), )

    
    mission_log = property(__mission_log.value, __mission_log.set, None, None)

    
    # Element debug_log uses Python identifier debug_log
    __debug_log = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'debug_log'), 'debug_log', '__venus_CTD_ANON_3_debug_log', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 35, 5), )

    
    debug_log = property(__debug_log.value, __debug_log.set, None, None)

    
    # Element short_log uses Python identifier short_log
    __short_log = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'short_log'), 'short_log', '__venus_CTD_ANON_3_short_log', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 37, 5), )

    
    short_log = property(__short_log.value, __short_log.set, None, None)

    
    # Element image uses Python identifier image
    __image = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'image'), 'image', '__venus_CTD_ANON_3_image', True, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 39, 5), )

    
    image = property(__image.value, __image.set, None, None)

    _ElementMap.update({
        __mission_log.name() : __mission_log,
        __debug_log.name() : __debug_log,
        __short_log.name() : __short_log,
        __image.name() : __image
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
    _XSDLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 26, 7)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element diagnostics uses Python identifier diagnostics
    __diagnostics = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'diagnostics'), 'diagnostics', '__venus_CTD_ANON_4_diagnostics', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 28, 4), )

    
    diagnostics = property(__diagnostics.value, __diagnostics.set, None, None)

    
    # Element adv_diagnostics uses Python identifier adv_diagnostics
    __adv_diagnostics = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'adv_diagnostics'), 'adv_diagnostics', '__venus_CTD_ANON_4_adv_diagnostics', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 30, 4), )

    
    adv_diagnostics = property(__adv_diagnostics.value, __adv_diagnostics.set, None, None)

    _ElementMap.update({
        __diagnostics.name() : __diagnostics,
        __adv_diagnostics.name() : __adv_diagnostics
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_4 = CTD_ANON_4


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_5 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 40, 7)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute params uses Python identifier params
    __params = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'params'), 'params', '__venus_CTD_ANON_5_params', pyxb.binding.datatypes.string)
    __params._DeclarationLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 41, 9)
    __params._UseLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 41, 9)
    
    params = property(__params.value, __params.set, None, None)

    
    # Attribute ymin uses Python identifier ymin
    __ymin = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ymin'), 'ymin', '__venus_CTD_ANON_5_ymin', pyxb.binding.datatypes.decimal)
    __ymin._DeclarationLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 42, 9)
    __ymin._UseLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 42, 9)
    
    ymin = property(__ymin.value, __ymin.set, None, None)

    
    # Attribute ymax uses Python identifier ymax
    __ymax = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ymax'), 'ymax', '__venus_CTD_ANON_5_ymax', pyxb.binding.datatypes.decimal)
    __ymax._DeclarationLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 43, 9)
    __ymax._UseLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 43, 9)
    
    ymax = property(__ymax.value, __ymax.set, None, None)

    
    # Attribute label uses Python identifier label
    __label = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'label'), 'label', '__venus_CTD_ANON_5_label', pyxb.binding.datatypes.string)
    __label._DeclarationLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 45, 9)
    __label._UseLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 45, 9)
    
    label = property(__label.value, __label.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __params.name() : __params,
        __ymin.name() : __ymin,
        __ymax.name() : __ymax,
        __label.name() : __label
    })
_module_typeBindings.CTD_ANON_5 = CTD_ANON_5


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_6 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 52, 8)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element mission_log uses Python identifier mission_log
    __mission_log = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'mission_log'), 'mission_log', '__venus_CTD_ANON_6_mission_log', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 54, 5), )

    
    mission_log = property(__mission_log.value, __mission_log.set, None, None)

    
    # Element debug_log uses Python identifier debug_log
    __debug_log = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'debug_log'), 'debug_log', '__venus_CTD_ANON_6_debug_log', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 64, 5), )

    
    debug_log = property(__debug_log.value, __debug_log.set, None, None)

    
    # Element short_log uses Python identifier short_log
    __short_log = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'short_log'), 'short_log', '__venus_CTD_ANON_6_short_log', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 66, 5), )

    
    short_log = property(__short_log.value, __short_log.set, None, None)

    
    # Element image uses Python identifier image
    __image = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'image'), 'image', '__venus_CTD_ANON_6_image', True, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 68, 5), )

    
    image = property(__image.value, __image.set, None, None)

    _ElementMap.update({
        __mission_log.name() : __mission_log,
        __debug_log.name() : __debug_log,
        __short_log.name() : __short_log,
        __image.name() : __image
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
    _XSDLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 55, 7)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element diagnostics uses Python identifier diagnostics
    __diagnostics = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'diagnostics'), 'diagnostics', '__venus_CTD_ANON_7_diagnostics', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 57, 4), )

    
    diagnostics = property(__diagnostics.value, __diagnostics.set, None, None)

    
    # Element adv_diagnostics uses Python identifier adv_diagnostics
    __adv_diagnostics = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'adv_diagnostics'), 'adv_diagnostics', '__venus_CTD_ANON_7_adv_diagnostics', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 59, 4), )

    
    adv_diagnostics = property(__adv_diagnostics.value, __adv_diagnostics.set, None, None)

    _ElementMap.update({
        __diagnostics.name() : __diagnostics,
        __adv_diagnostics.name() : __adv_diagnostics
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
    _XSDLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 69, 7)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute params uses Python identifier params
    __params = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'params'), 'params', '__venus_CTD_ANON_8_params', pyxb.binding.datatypes.string)
    __params._DeclarationLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 70, 9)
    __params._UseLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 70, 9)
    
    params = property(__params.value, __params.set, None, None)

    
    # Attribute ymin uses Python identifier ymin
    __ymin = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ymin'), 'ymin', '__venus_CTD_ANON_8_ymin', pyxb.binding.datatypes.decimal)
    __ymin._DeclarationLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 71, 9)
    __ymin._UseLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 71, 9)
    
    ymin = property(__ymin.value, __ymin.set, None, None)

    
    # Attribute ymax uses Python identifier ymax
    __ymax = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ymax'), 'ymax', '__venus_CTD_ANON_8_ymax', pyxb.binding.datatypes.decimal)
    __ymax._DeclarationLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 72, 9)
    __ymax._UseLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 72, 9)
    
    ymax = property(__ymax.value, __ymax.set, None, None)

    
    # Attribute label uses Python identifier label
    __label = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'label'), 'label', '__venus_CTD_ANON_8_label', pyxb.binding.datatypes.string)
    __label._DeclarationLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 74, 9)
    __label._UseLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 74, 9)
    
    label = property(__label.value, __label.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __params.name() : __params,
        __ymin.name() : __ymin,
        __ymax.name() : __ymax,
        __label.name() : __label
    })
_module_typeBindings.CTD_ANON_8 = CTD_ANON_8


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_9 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 81, 8)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element mission_log uses Python identifier mission_log
    __mission_log = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'mission_log'), 'mission_log', '__venus_CTD_ANON_9_mission_log', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 83, 5), )

    
    mission_log = property(__mission_log.value, __mission_log.set, None, None)

    
    # Element debug_log uses Python identifier debug_log
    __debug_log = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'debug_log'), 'debug_log', '__venus_CTD_ANON_9_debug_log', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 93, 5), )

    
    debug_log = property(__debug_log.value, __debug_log.set, None, None)

    
    # Element short_log uses Python identifier short_log
    __short_log = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'short_log'), 'short_log', '__venus_CTD_ANON_9_short_log', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 95, 5), )

    
    short_log = property(__short_log.value, __short_log.set, None, None)

    
    # Element image uses Python identifier image
    __image = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'image'), 'image', '__venus_CTD_ANON_9_image', True, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 97, 5), )

    
    image = property(__image.value, __image.set, None, None)

    _ElementMap.update({
        __mission_log.name() : __mission_log,
        __debug_log.name() : __debug_log,
        __short_log.name() : __short_log,
        __image.name() : __image
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_9 = CTD_ANON_9


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_10 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 84, 7)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element diagnostics uses Python identifier diagnostics
    __diagnostics = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'diagnostics'), 'diagnostics', '__venus_CTD_ANON_10_diagnostics', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 86, 4), )

    
    diagnostics = property(__diagnostics.value, __diagnostics.set, None, None)

    
    # Element adv_diagnostics uses Python identifier adv_diagnostics
    __adv_diagnostics = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'adv_diagnostics'), 'adv_diagnostics', '__venus_CTD_ANON_10_adv_diagnostics', False, pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 88, 4), )

    
    adv_diagnostics = property(__adv_diagnostics.value, __adv_diagnostics.set, None, None)

    _ElementMap.update({
        __diagnostics.name() : __diagnostics,
        __adv_diagnostics.name() : __adv_diagnostics
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_10 = CTD_ANON_10


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_11 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 98, 7)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute params uses Python identifier params
    __params = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'params'), 'params', '__venus_CTD_ANON_11_params', pyxb.binding.datatypes.string)
    __params._DeclarationLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 99, 9)
    __params._UseLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 99, 9)
    
    params = property(__params.value, __params.set, None, None)

    
    # Attribute ymin uses Python identifier ymin
    __ymin = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ymin'), 'ymin', '__venus_CTD_ANON_11_ymin', pyxb.binding.datatypes.decimal)
    __ymin._DeclarationLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 100, 9)
    __ymin._UseLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 100, 9)
    
    ymin = property(__ymin.value, __ymin.set, None, None)

    
    # Attribute ymax uses Python identifier ymax
    __ymax = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ymax'), 'ymax', '__venus_CTD_ANON_11_ymax', pyxb.binding.datatypes.decimal)
    __ymax._DeclarationLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 101, 9)
    __ymax._UseLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 101, 9)
    
    ymax = property(__ymax.value, __ymax.set, None, None)

    
    # Attribute label uses Python identifier label
    __label = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'label'), 'label', '__venus_CTD_ANON_11_label', pyxb.binding.datatypes.string)
    __label._DeclarationLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 103, 9)
    __label._UseLocation = pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 103, 9)
    
    label = property(__label.value, __label.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __params.name() : __params,
        __ymin.name() : __ymin,
        __ymax.name() : __ymax,
        __label.name() : __label
    })
_module_typeBindings.CTD_ANON_11 = CTD_ANON_11


global_config = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'global_config'), CTD_ANON, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 4, 2))
Namespace.addCategoryObject('elementBinding', global_config.name().localName(), global_config)



CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'logging'), CTD_ANON_, scope=CTD_ANON, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 7, 1)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, 'logging')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 7, 1))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton()




CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'debug_diagn_period'), pyxb.binding.datatypes.decimal, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 10, 7)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'short_log_len'), pyxb.binding.datatypes.positiveInteger, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 12, 7)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'empty_image'), pyxb.binding.datatypes.string, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 14, 7)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'mission'), CTD_ANON_2, scope=CTD_ANON_, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 16, 7)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'debug_diagn_period')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 10, 7))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'short_log_len')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 12, 7))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'empty_image')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 14, 7))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'mission')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 16, 7))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
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
    transitions.append(fac.Transition(st_3, [
         ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_._Automaton = _BuildAutomaton_()




CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'debug_constants'), pyxb.binding.datatypes.string, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 20, 12)))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'debug_probe'), pyxb.binding.datatypes.string, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 21, 12)))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'landing'), CTD_ANON_3, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 22, 6)))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'surface_activity'), CTD_ANON_6, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 51, 6)))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'launch'), CTD_ANON_9, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 80, 6)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 20, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 21, 12))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 22, 6))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 51, 6))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 80, 6))
    counters.add(cc_4)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, 'debug_constants')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 20, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, 'debug_probe')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 21, 12))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, 'landing')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 22, 6))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, 'surface_activity')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 51, 6))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, 'launch')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 80, 6))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_4, True) ]))
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_2._Automaton = _BuildAutomaton_2()




CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'mission_log'), CTD_ANON_4, scope=CTD_ANON_3, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 25, 5)))

CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'debug_log'), pyxb.binding.datatypes.string, scope=CTD_ANON_3, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 35, 5)))

CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'short_log'), pyxb.binding.datatypes.string, scope=CTD_ANON_3, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 37, 5)))

CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'image'), CTD_ANON_5, scope=CTD_ANON_3, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 39, 5)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 39, 5))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(None, 'mission_log')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 25, 5))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(None, 'debug_log')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 35, 5))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(None, 'short_log')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 37, 5))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(None, 'image')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 39, 5))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
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
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_3._Automaton = _BuildAutomaton_3()




CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'diagnostics'), pyxb.binding.datatypes.string, scope=CTD_ANON_4, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 28, 4)))

CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'adv_diagnostics'), pyxb.binding.datatypes.string, scope=CTD_ANON_4, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 30, 4)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, 'diagnostics')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 28, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, 'adv_diagnostics')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 30, 4))
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




CTD_ANON_6._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'mission_log'), CTD_ANON_7, scope=CTD_ANON_6, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 54, 5)))

CTD_ANON_6._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'debug_log'), pyxb.binding.datatypes.string, scope=CTD_ANON_6, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 64, 5)))

CTD_ANON_6._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'short_log'), pyxb.binding.datatypes.string, scope=CTD_ANON_6, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 66, 5)))

CTD_ANON_6._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'image'), CTD_ANON_8, scope=CTD_ANON_6, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 68, 5)))

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 68, 5))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(None, 'mission_log')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 54, 5))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(None, 'debug_log')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 64, 5))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(None, 'short_log')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 66, 5))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(None, 'image')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 68, 5))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
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
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_6._Automaton = _BuildAutomaton_5()




CTD_ANON_7._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'diagnostics'), pyxb.binding.datatypes.string, scope=CTD_ANON_7, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 57, 4)))

CTD_ANON_7._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'adv_diagnostics'), pyxb.binding.datatypes.string, scope=CTD_ANON_7, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 59, 4)))

def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_7._UseForTag(pyxb.namespace.ExpandedName(None, 'diagnostics')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 57, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_7._UseForTag(pyxb.namespace.ExpandedName(None, 'adv_diagnostics')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 59, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_7._Automaton = _BuildAutomaton_6()




CTD_ANON_9._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'mission_log'), CTD_ANON_10, scope=CTD_ANON_9, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 83, 5)))

CTD_ANON_9._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'debug_log'), pyxb.binding.datatypes.string, scope=CTD_ANON_9, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 93, 5)))

CTD_ANON_9._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'short_log'), pyxb.binding.datatypes.string, scope=CTD_ANON_9, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 95, 5)))

CTD_ANON_9._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'image'), CTD_ANON_11, scope=CTD_ANON_9, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 97, 5)))

def _BuildAutomaton_7 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_7
    del _BuildAutomaton_7
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 97, 5))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_9._UseForTag(pyxb.namespace.ExpandedName(None, 'mission_log')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 83, 5))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_9._UseForTag(pyxb.namespace.ExpandedName(None, 'debug_log')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 93, 5))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_9._UseForTag(pyxb.namespace.ExpandedName(None, 'short_log')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 95, 5))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_9._UseForTag(pyxb.namespace.ExpandedName(None, 'image')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 97, 5))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
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
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_9._Automaton = _BuildAutomaton_7()




CTD_ANON_10._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'diagnostics'), pyxb.binding.datatypes.string, scope=CTD_ANON_10, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 86, 4)))

CTD_ANON_10._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'adv_diagnostics'), pyxb.binding.datatypes.string, scope=CTD_ANON_10, location=pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 88, 4)))

def _BuildAutomaton_8 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_8
    del _BuildAutomaton_8
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_10._UseForTag(pyxb.namespace.ExpandedName(None, 'diagnostics')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 86, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_10._UseForTag(pyxb.namespace.ExpandedName(None, 'adv_diagnostics')), pyxb.utils.utility.Location('/home/akoru/orbita-simulator/models/planets/xml-schemas/global_config.xsd', 88, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_10._Automaton = _BuildAutomaton_8()

