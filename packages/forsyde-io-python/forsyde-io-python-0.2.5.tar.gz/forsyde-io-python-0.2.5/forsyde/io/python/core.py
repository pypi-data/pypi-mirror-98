from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Dict
from typing import List
from typing import Iterable
from typing import Optional
from typing import Set
from typing import Tuple

from lxml import etree  # type: ignore
import networkx as nx  # type: ignore
import networkx.drawing.nx_pydot as nx_pydot  # type: ignore

_port_id_counter = 0
_vertex_id_counter = 0


def _generate_vertex_id() -> str:
    global _vertex_id_counter
    _vertex_id_counter += 1
    return "vertex" + str(_vertex_id_counter)


def _generate_port_id() -> str:
    global _port_id_counter
    _port_id_counter += 1
    return "port" + str(_port_id_counter)


# class ModelType(object):
#     """Type associated with a vertex or a port.

#     Though Python already keeps many runtime amenities that would make this
#     explicit runtime representation of Types unnecesary, having it explicitly can
#     ease porting to other langauges and also usability for users that are not
#     familiar with Python 'meta' built-in facilities.

#     This clas is meant to be used more of a interface than a concrete class.
#     """

#     _instance = None

#     @classmethod
#     def get_instance(cls):
#         if not cls._instance:
#             cls._instance = cls()
#         return cls._instance

#     def __repr__(self):
#         return self.get_type_tag()

#     def __eq__(self, other):
#         return self.get_type_tag() == other.get_type_tag()

#     def __hash__(self):
#         return hash(self.get_type_tag())

#     def is_refinement(self, other: "ModelType") -> bool:
#         return (self == other) or any(
#             s.is_refinement(other) for s in self.get_super_types())

#     def get_super_types(self) -> Iterable["ModelType"]:
#         yield from ()

#     def get_type_tag(self) -> str:
#         return "UnknownType"

#     def get_required_ports(self) -> Iterable[Tuple[str, "ModelType"]]:
#         yield from ()

#     def get_required_properties(self) -> Iterable[Tuple[str, Any]]:
#         yield from ()


@dataclass
class Port(object):
    """Port of a vertex.
    
    This class is intended to help synthesis of components and also
    to keep things semantically sane when dealing with the model, for instance,
    to denote which slot of a time-division a piece of code is executed or
    to denote which input argument of a function is to be used.
    """

    identifier: str = field(default_factory=_generate_port_id, hash=True)

    # port_type: Optional["Vertex"] = field(default=None,
    #                                     compare=False,
    #                                     hash=False)

    def __hash__(self):
        return hash(self.identifier)

    def get_type_tag(self) -> str:
        return "Port"

    def serialize(self) -> dict:
        return {}

    # def is_type(self, t: ModelType) -> bool:
    #     return self.port_type and self.port_type.is_refinement(t)


@dataclass
class Vertex(object):
    """Class holding data regarding Vertexes.

    Every vertex representes a main element in a ForSyDe model.
    Every vertex contains a number of ports (which are repeated in the
    vertexed to increase reliability in the model, since putting
    them in edges would have been sufficient).
    Also, every vertex contains "Properties" which are arbitrary slef-contained 
    associated data, such as the size of bits in a Signal or the time slots in 
    a Time Division Multiplexer.
    """

    identifier: str = field(default_factory=_generate_vertex_id, hash=True)
    ports: List[Port] = field(default_factory=list, compare=False, hash=False)
    properties: Dict[str, Any] = field(default_factory=dict,
                                       compare=False,
                                       hash=False)

    # vertex_type: ModelType = field(default=ModelType(),
    #                                compare=False,
    #                                hash=False)

    def __eq__(self, other):
        return self.identifier == other.identifier

    def __hash__(self):
        return hash(self.identifier)

    def get_type_tag(self) -> str:
        return self.__class__.__name__

    def get_port(self, name: str) -> Port:
        try:
            return next(p for p in self.ports if p.identifier == name)
        except StopIteration:
            raise AttributeError(
                f"Required port {name} of {self.identifier} does not exist.")

    def get_neigh(self, name: str, model) -> "Vertex":
        out_port = self.get_port(name)
        for n in model.adj[self]:
            for (_, edata) in model.edges[self][n]:
                edge = edata["object"]
                if edge.source_vertex_port == out_port:
                    return edge.target_vertex


@dataclass
class Edge(object):
    """Class containing all information for an Edge.

    The edge contains references to the source and target 'Vertex'es
    as well as the 'Port's being connect on both ends, in case
    they exist. The edges also have types associated with them
    so that extra deductions can be made along the EDA flow.
    """
    source_vertex: Vertex = field(default=Vertex())
    target_vertex: Vertex = field(default=Vertex())
    source_vertex_port: Optional[Port] = field(default=None)
    target_vertex_port: Optional[Port] = field(default=None)

    # edge_type: ModelType = field(default=ModelType(), compare=False)

    def __hash__(self):
        return hash((self.source_vertex, self.target_vertex))

    def get_type_tag(self) -> str:
        return self.__class__.__name__

    # def ids_tuple(self):
    #     return (self.source_vertex.identifier, self.target_vertex.identifier,
    #             self.source_vertex_port.identifier if self.source_vertex_port
    #             else None, self.target_vertex_port.identifier
    #             if self.target_vertex_port else None,
    #             self.edge_type.get_type_tag())

    # def is_type(self, tsource: ModelType, ttarget: ModelType) -> bool:
    #     return self.source_vertex.is_type(
    #         tsource) and self.target_vertex.is_type(ttarget)


class ForSyDeModel(nx.MultiDiGraph):
    """The main graph holder element representing a ForSyDe Model

    A subclass of MultiDiGraph from the networkX library, this class
    holds the model (a graph model therefore) which can be used for
    any purpose in the ForSyDe design flow. In addition to all standard
    graph algorithms and facilities given by networkX, this subclass
    also provides parsing and dumping from the canonical ForSyDe IO
    disk persistent file and other output formats that can be used for
    visualization, such as GraphML.

    It also provides additional methods building on top of standard graph
    methods to make development easier, such as directly iterating vertexes
    by their associated types.
    """
    def __init__(self,
                 standard_views=[
                     'create_tables.sql', 'types.sql', 'create_views.sql'
                 ],
                 *args,
                 **kwargs):
        """TODO: to be defined. """
        nx.MultiDiGraph.__init__(self, *args, **kwargs)

    def _rectify_model(self) -> None:
        pass
        # for v in self.nodes:
        #     for (k, val) in v.vertex_type.get_required_properties():
        #         if k not in v.properties:
        #             v.properties[k] = val
        #     for (name, port) in v.vertex_type.get_required_ports():
        #         if name not in (p.identifier for p in v.ports):
        #             v.ports.add(Port(identifier=name, port_type=port))

    def write(self, sink: str) -> None:
        self._rectify_model()
        # if '.pro' in sink or '.pl' in sink:
        #     self.write_prolog(sink)
        if '.gexf' in sink:
            nx.write_gexf(self.stringified(), sink)
        elif '.graphml' in sink:
            nx.write_graphml(self.stringified(), sink)
        elif '.dot' in sink:
            nx_pydot.write_dot(self.stringified(), sink)
        elif '.xml' in sink:
            self.write_xml(sink)
        else:
            raise NotImplementedError

    def read(self, source: str) -> None:
        # if '.pro' in source or '.pl' in source:
        #     self.read_prolog(source)
        if '.db' in source:
            self.read_db(source)
        elif '.xml' in source:
            self.read_xml(source)
        else:
            raise NotImplementedError
        self._rectify_model()

    def stringified(self) -> nx.MultiDiGraph:
        strg = nx.MultiDiGraph()
        for v in self.nodes:
            strg.add_node(f"{v.identifier}\\n{v.get_type_tag()}")
        for (s, t, e) in self.edges.data("object"):
            sp = e.source_vertex_port
            tp = e.target_vertex_port
            strg.add_edge(f"{s.identifier}\\n{s.get_type_tag()}",
                          f"{t.identifier}\\n{t.get_type_tag()}",
                          label=f"{e.get_type_tag()}\\n" +
                          (f"{s.identifier}.{sp.identifier}"
                           if sp else f"{s.identifier}") + "\\n" +
                          (f"{t.identifier}.{tp.identifier}"
                           if tp else f"{t.identifier}"))
        return strg

    # def get_vertexes(
    #         self,
    #         v_type: Union[Type, Optional[ModelType]] = None,
    #         filters: List[Callable[[Vertex], bool]] = []) -> Iterable[Vertex]:
    #     '''Query vertexes based on their attached type and additional filters

    #     Arguments:
    #         v_type:
    #             Either a `ModelType` instance for a `ModelType` `type` itself,
    #             which serves as a hard filter for the query.
    #         filters:
    #             The callables are called with every vertex fed as argument. If
    #             they evaluate to `True`, then the vertex is in the result,
    #             otherwise it is skipped.
    #     '''
    #     for v in self.nodes:
    #         if v_type and v.is_type(v_type):
    #             if all(f(v) for f in filters):
    #                 yield v
    #         elif all(f(v) for f in filters):
    #             yield v

    def neighs(self, v: Vertex) -> Iterable[Vertex]:
        yield from self.nodes.adj[v]

    def neighs_rev(self, v: Vertex) -> Iterable[Vertex]:
        yield from nx.reverse_view(self).adj[v]

    def get_vertex(self,
                   label: str,
                   label_name: str = 'label') -> Optional[Vertex]:
        for (v, d) in self.nodes.data():
            if d[label_name] == label:
                return v
        return None

    def property_to_xml(self, parent: etree.Element, prop: Any) -> None:
        '''Transform an object into the expected XML element layout
        
        The library 'dicttoxml' was considered but dropped for the moment
        since there seemed to be no easy way to control the tag generation
        as this function does by always creating "Property".
        '''
        if isinstance(prop, dict):
            for (k, v) in prop.items():
                child = etree.SubElement(parent, 'Property')
                child.set('name', k)
                self.property_to_xml(child, v)
        elif isinstance(prop, list):
            for (i, v) in enumerate(prop):
                child = etree.SubElement(parent, 'Property')
                child.set('index', i)
                self.property_to_xml(child, v)
        elif isinstance(prop, set):
            for v in prop:
                child = etree.SubElement(parent, 'Property')
                self.property_to_xml(child, v)
        else:
            if isinstance(prop, int):
                parent.set('type', 'Integer')
            elif isinstance(prop, float):
                parent.set('type', 'Float')
            parent.text = str(prop)

    def xml_to_property(self, elem: etree.Element) -> Any:
        '''Collect children of the element to expected property layout

        It collects the children recursively of 'elem' to the expected
        formats and types.
        '''
        if len(elem.xpath("Property[@index]")) > 0:
            elems = elem.xpath("Property[@index]")
            l = [None for i in range(len(elems))]
            for e in elems:
                l[int(e.get('index'))] = self.xml_to_property(e)
            return l
        elif len(elem.xpath("Property[@name]")) > 0:
            return {
                e.get("name"): self.xml_to_property(e)
                for e in elem.xpath("Property[@name]")
            }
        elif len(elem.xpath("Property")) > 0:
            return set(self.xml_to_property(e) for e in elem.xpath("Property"))
        elif elem.text and elem.text.strip():
            if elem.xpath('Property[@type="Integer"]'):
                return int(elem.text.strip())
            elif elem.xpath('Property[@type="Float"]'):
                return float(elem.text.strip())
            else:
                return elem.text.strip()
        else:
            return dict()

    # def write_xml(self, sink: str) -> None:
    #     tree = etree.Element('ForSyDe')
    #     for v in self.nodes:
    #         node_elem = etree.SubElement(tree, 'Vertex')
    #         node_elem.set('id', v.identifier)
    #         node_elem.set('type', v.get_type_tag())
    #         for port in v.ports:
    #             port_elem = etree.SubElement(node_elem, 'Port')
    #             port_elem.set('id', port.identifier)
    #             if port.port_type == int:
    #                 port_elem.set('type', 'Integer')
    #             elif port.port_type == float:
    #                 port_elem.set('type', 'Integer')
    #             elif issubclass(port.port_type, Vertex):
    #                 port_elem.set('type', str(port.port_type))
    #             else:
    #                 port_elem.set('type', 'String')
    #         for (prop, val) in v.properties.items():
    #             prop_elem = etree.SubElement(node_elem, 'Property')
    #             prop_elem.set('name', prop)
    #             # prop_elem.text = json.dumps(val)
    #             self.property_to_xml(prop_elem, val)
    #     for (s, t, edge) in self.edges.data("object"):
    #         edge_elem = etree.SubElement(tree, 'Edge')
    #         edge_elem.set('source_id', s.identifier)
    #         edge_elem.set('target_id', t.identifier)
    #         edge_elem.set('type', edge.get_type_tag())
    #         if edge.source_vertex_port:
    #             edge_elem.set('source_port_id',
    #                           edge.source_vertex_port.identifier)
    #         if edge.target_vertex_port:
    #             edge_elem.set('target_port_id',
    #                           edge.target_vertex_port.identifier)
    #     with open(sink, 'w') as sinkstream:
    #         sinkstream.write(
    #             etree.tostring(tree, pretty_print=True, encoding='unicode'))

    # def read_xml(self, source: str) -> None:
    #     with open(source, 'r') as instream:
    #         tree = etree.parse(instream)
    #         for vnode in tree.xpath('/ForSyDeModel/Vertex'):
    #             vertex = VertexFactory.build(identifier=vnode.get('id'),
    #                                          type_name=vnode.get('type'))
    #             self.add_node(vertex, label=vertex.identifier)
    #             for portnode in vnode.xpath("Port"):
    #                 port = Port(identifier=portnode.get('id'))
    #                 if portnode.get('type') == "Integer":
    #                     port.port_type = int
    #                 elif portnode.get('type') == "Float":
    #                     port.port_type = float
    #                 else:
    #                     try:
    #                         port.port_type = VertexFactory.get_type_from_name(
    #                             portnode.get('type'))
    #                     except NotImplementedError:
    #                         port.port_type = str
    #                 vertex.ports.add(port)
    #             vertex.properties = self.xml_to_property(vnode)
    #             # for propnode in vnode.xpath('Property'):
    #             #     prop_name = propnode.get('name')
    #             #     prop_val = self.xml_to_property(
    #             #         propnode)  # json.loads(propnode.text)
    #             #     vertex.properties[prop_name] = prop_val
    #         for vedge in tree.xpath('/ForSyDeModel/Edge'):
    #             source_vertex = next(n for (n, nid) in self.nodes.data('label')
    #                                  if nid == vedge.get('source_id'))
    #             target_vertex = next(n for (n, nid) in self.nodes.data('label')
    #                                  if nid == vedge.get('target_id'))
    #             edge = EdgeFactory.build(source=source_vertex,
    #                                      target=target_vertex,
    #                                      type_name=vedge.get('type'))
    #             if vedge.get('source_port_id'):
    #                 edge.source_vertex_port = source_vertex.get_port(
    #                     vedge.get('source_port_id'))
    #             if vedge.get('target_port_id'):
    #                 edge.target_vertex_port = target_vertex.get_port(
    #                     vedge.get('target_port_id'))
    #             key = (
    #                 f"{vedge.get('source_id')}:{vedge.get('source_port_id')}->"
    #                 +
    #                 f"{vedge.get('target_id')}:{vedge.get('target_port_id')}")
    #             self.add_edge(source_vertex,
    #                           target_vertex,
    #                           key=key,
    #                           object=edge)

