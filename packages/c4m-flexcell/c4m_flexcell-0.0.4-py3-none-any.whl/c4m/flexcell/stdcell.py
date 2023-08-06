# SPDX-License-Identifier: GPL-2.0-or-later OR AGPL-3.0-or-later OR CERN-OHL-S-2.0+
import itertools
from six import add_metaclass
from abc import ABCMeta, abstractmethod

import shapely.geometry as sh_geo

from pdkmaster.technology import primitive as prm, technology_ as tch
from pdkmaster.design import circuit as ckt, layout as lay

__all__ = ["BBox", "Wire", "Via", "Device", "StdCell"]

def _mean(v):
    return sum(v)/len(v)


class _OrderedPoint:
    def __init__(self, point):
        self.x = point.x
        self.y = point.y
    def __lt__(self, other):
        return self.x < other.x if self.x != other.x else self.y < other.y
    def __gt__(self, other):
        return self.x > other.x if self.x != other.x else self.y > other.y
    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)
    def __le__(self, other):
        return self.x < other.x if self.x != other.x else self.y <= other.y
    def __ge__(self, other):
        return self.x > other.x if self.x != other.x else self.y >= other.y
    def __ne__(self, other):
        return (self.x != other.x) or (self.y != other.y)


class BBox(object):
    def __init__(self, x1, y1, x2, y2):
        assert x1 <= x2 and y1 <= y2
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def __repr__(self):
        return "({},{})-({},{})".format(self.x1, self.y1, self.x2, self.y2)

    def overlaps(self, box):
        return ((self.x2 >= box.x1)
                and (box.x2 >= self.x1)
                and (self.y2 >= box.y1)
                and (box.y2 >= self.y1)
               )

    def encloses(self, box):
        return ((self.x1 <= box.x1)
                and (self.y1 <= box.y1)
                and (self.x2 >= box.x2)
                and (self.y2 >= box.y2)
               )

    def copy(self):
        return self.__class__(self.x1, self.y1, self.x2, self.y2)

class _LayerBox(BBox):
    def __init__(self, layer, x1, y1, x2, y2):
        super(_LayerBox, self).__init__(x1, y1, x2, y2)
        self.layer = layer
        
    def __repr__(self):
        return "{}({})".format(self.layer, super(_LayerBox, self).__repr__())
        
    def overlaps(self, box):
        return (self.layer == box.layer) and super(_LayerBox, self).overlaps(box)
    
    def encloses(self, box):
        return (self.layer == box.layer) and super(_LayerBox, self).encloses(box)

    def copy(self):
        return self.__class__(self.layer, self.x1, self.y1, self.x2, self.y2)

class _UniqueNetName(object):
    def __init__(self):
        self.netnr = 0

    def new(self):
        s = "*{:04d}".format(self.netnr)
        self.netnr += 1
        return s

class _LayerBoxesNets(object):
    def __init__(self):
        self._layerboxes = {}
        self._netaliases = {}
        self._uniquenet = _UniqueNetName()

    def add_alias(self, net1, net2):
        assert (net1 != "fused_net") and (net1 in self._netaliases)
        net1 = self.from_alias(net1)
        if net2 == "fused_net":
            net2 = self._uniquenet.new()
        if net2 not in self._netaliases:
            if net2[0] == "*":
                return net1
            else:
                assert net1[0] == "*", "Shorted net {} and {}".format(net1, net2)
                self._netaliases[net1] = net2
                # It can be that net2 is not in aliases when called for first time
                if net2 not in self._netaliases:
                    self._netaliases[net2] = net2
                return net2
        else:
            # net1 and net2 are there, really join them
            net2 = self.from_alias(net2)
            if net1 == net2:
                net = net1
            elif net2[0] != "*":
                assert net1[0] == "*", "Shorted nets {} and {}".format(net1, net2)
                net = net2
                self._netaliases[net1] = net
            else:
                net = net1
                self._netaliases[net2] = net

            return net

    def from_alias(self, net):
        while self._netaliases[net] != net:
            net = self._netaliases[net]
        return net

    def finalize_nets(self):
        starnets = set()
        for net in self._netaliases.keys():
            net2 = self.from_alias(net)
            if net2[0] == "*":
                starnets.add(net2)
        newnets = dict(
            (net, "_net{}".format(i)) for i, net in enumerate(starnets)
        )
        self._netaliases.update(newnets)
        self._netaliases.update(dict(
            (net, net) for net in newnets.values()
        ))
        return set(self.from_alias(net) for net in self._netaliases)

    def add_box(self, net, box):
        layer = box.layer
        try:
            boxes = self._layerboxes[layer]
        except KeyError:
            self._layerboxes[layer] = boxes = []

        for box2, net2 in boxes:
            if box.overlaps(box2):
                net = self.add_alias(net2, net)

        if net == "fused_net":
            # Get name for unnamed net
            net = self._uniquenet.new()
        if net not in self._netaliases:
            self._netaliases[net] = net

        boxes.append((box, net))

        return net

@add_metaclass(ABCMeta)
class _Element(object):
    # Sizing parameters for bounding box derivation

    def __init__(self, *, external, boxes, name, conn, space):
        self.external = external
        self._ignore = False
        self.boxes = boxes
        if name is not None:
            self.name = name
        if conn is not None:
            self.conn = conn
        if space is not None:
            self.space = space

        self.connects = {}

    def iterate_anchors(self):
        try:
            for s in self.conn.values():
                yield s
        except AttributeError:
            pass
        try:
            for s in self.space.values():
                yield s
        except AttributeError:
            pass
    
    def _str_indent(self, level, str_elem, prefix, level_str, net, recursive=True):
        s = level*level_str + prefix + str_elem

        if recursive:
            if net is None:
                if len(self.connects) > 0:
                    for subnet, elems in self.connects.items():
                        s += "\n{}{}Net: {}".format((level + 1)*level_str, prefix, subnet)
                        for elem in elems:
                            s += "\n"+elem.str_indent(level+2, prefix=prefix, level_str=level_str, net=subnet)
            elif net in self.connects:
                for elem in self.connects[net]:
                    s += "\n"+elem.str_indent(level+1, prefix=prefix, level_str=level_str, net=net)
    
        return s

    @abstractmethod
    def str_indent(self, level, prefix="", level_str="  ", net=None, recursive=True):
        raise NotImplementedError("Abstract method not implemented")
    
    def __str__(self):
        return self.str_indent(0)
    
    def overlaps(self, other):
        for box1, box2 in itertools.product(self.boxes, other.boxes):
            if box1.overlaps(box2):
                return True
        
        return False
    
    def add_boxes(self, layerboxes):
        if hasattr(self, "net"):
            for box in self.boxes:
                self.net = layerboxes.add_box(self.net, box)
        else:
            for i, box in enumerate(self.boxes):
                self.nets[i] = layerboxes.add_box(self.nets[i], box)

    def add_connects(self, net, connects):
        self.connects[net] = connects

    def iterate_connects(self, net=None, include_ignored=False):
        stack = [self.connects]
        
        while stack:
            connects = stack.pop()
            for elems_net, elems in connects.items():
                if (net is None) or (net == elems_net):
                    for elem in elems:
                        if (not elem._ignore) or include_ignored:
                            yield elem
                        stack.append(elem.connects)

    def get_nets(self):
        try:
            nets = [self.net]
        except AttributeError:
            nets = self.nets
        
        return nets

    def update_nets(self, layerboxes):
        try:
            self.net = layerboxes.from_alias(self.net)
        except AttributeError:
            self.nets = [layerboxes.from_alias(net) for net in self.nets]

    def _merge(self, elem):
        return False
    
    def merge(self, elem):
        if self._ignore or elem._ignore:
            return False
        else:
            return self._merge(elem) or elem._merge(self)

    @abstractmethod
    def python_code(self):
        raise NotImplementedError("Abstract method not implemented")

    @abstractmethod
    def get_center(self):
        raise NotImplementedError("Abstract method not implemented")

class Wire(_Element):
    layers = ("NWELL", "PWELL", "NTIE", "PTIE", "NDIF", "PDIF", "POLY", "METAL1", "METAL2", "METAL3")
    dhw = {
        "NWELL": 0, "PWELL": 0, "NTIE": 2, "PTIE": 2, "NDIF": 2, "PDIF": 2,
        "POLY": 0, "METAL1": 0, "METAL2": 0, "METAL3": 0
    }
    dhl = {
        "NWELL": 0, "PWELL": 0, "NTIE": 2, "PTIE": 2, "NDIF": 2, "PDIF": 2,
        "POLY": 2, "METAL1": 2, "METAL2": 2, "METAL3": 2
    }

    def __init__(
        self, layer, x, y, width, external=False, *,
        name=None, conn=None, space=None,
    ):
        assert isinstance(x, tuple) ^ isinstance(y, tuple)
        assert layer in self.layers

        self.layer = layer
        self.x = x
        self.y = y
        self.width = width

        dhw = self.dhw[layer]
        dhl = self.dhl[layer]
        if not isinstance(x, tuple):
            x1 = x - width//2 - dhw
            x2 = x + width//2 + dhw
        else:
            x1 = x[0] - dhl
            x2 = x[1] + dhl
        if not isinstance(y, tuple):
            y1 = y - width//2 - dhw
            y2 = y + width//2 + dhw
        else:
            y1 = y[0] - dhl
            y2 = y[1] + dhl
        boxes = [_LayerBox(layer, x1, y1, x2, y2)]
        if layer == "NTIE": # Make NWELL connection
            boxes.append(_LayerBox("NWELL", x1, y1, x2, y2))
        super(Wire, self).__init__(
            external=external, boxes=boxes, name=name, conn=conn, space=space,
        )

    def _merge(self, elem):
        if not (isinstance(elem, Wire) and (self.layer == elem.layer)):
            return False

        merged = False

        box_self = self.boxes[0]
        box_elem = elem.boxes[0]
        hor_self = isinstance(self.x, tuple)
        hor_elem = isinstance(elem.x, tuple)
        if box_self.encloses(box_elem):
            self.external |= elem.external
            elem._ignore = True
            merged = True
        elif box_elem.encloses(box_self):
            self._ignore = True
            elem.external |= self.external
            merged = True
        elif (not hor_self) and (not hor_elem): # Both vertical
            if (self.x == elem.x) and (self.width == elem.width) and (self.y[1] >= elem.y[0]) and (elem.y[1] >= self.y[0]):
                self.y1 = box_self.y1 = min(box_self.y1, box_elem.y1)
                self.y2 = box_self.y2 = max(box_self.y2, box_elem.y2)
                self.y = (min(self.y[0], elem.y[0]), max(self.y[1], elem.y[1]))
                self.external |= elem.external
                elem._ignore = True
                merged = True
        elif hor_self and hor_elem: # Both horizontal
            if (self.y == elem.y) and (self.width == elem.width) and (self.x[1] >= elem.x[0]) and (elem.x[1] >= self.x[0]):
                self.x1 = box_self.x1 = min(box_self.x1, box_elem.x1)
                self.x2 = box_self.x2 = max(box_self.x2, box_elem.x2)
                self.x = (min(self.x[0], elem.x[0]), max(self.x[1], elem.x[1]))
                self.external |= elem.external
                elem._ignore = True
                merged = True

        if merged:
            # Some segments may have more than one box for connectivity, f.ex. NTIE with NWELL
            for box in self.boxes[1:]:
                box.x1 = box_self.x1
                box.x2 = box_self.x2
                box.y1 = box_self.y1
                box.y2 = box_self.y2
            for box in elem.boxes[1:]:
                box.x1 = box_elem.x1
                box.x2 = box_elem.x2
                box.y1 = box_elem.y1
                box.y2 = box_elem.y2

        return merged

    def str_indent(self, level, prefix="", level_str="  ", net=None, recursive=True):
        box = self.boxes[0]
        str_elem = "{}{}(({},{})-({},{}))".format(
            "EXT_" if self.external else "",
            self.layer,
            box.x1, box.y1, box.x2, box.y2,
        )

        return self._str_indent(level, str_elem, prefix, level_str, net, recursive)

    def python_code(self, lookup={}):
        classstr = lookup.get("Wire", "Wire")
        return "{}({!r}, {!r}, {!r}, {!r}, {!r})".format(
            classstr, self.layer, self.x, self.y, self.width, self.external,
        )

    def get_center(self):
        x = self.x if not isinstance(self.x, tuple) else _mean(self.x)
        y = self.y if not isinstance(self.y, tuple) else _mean(self.y)
        return sh_geo.Point(x, y)


class Via(_Element):
    dhw = {
        "NTIE": 6,
        "PTIE": 6,
        "NDIF": 6,
        "PDIF": 6,
        "POLY": 6,
        "METAL1": 4,
    }

    def __init__(
        self, bottom, top, x, y, width, *,
        name=None, conn=None, space=None,
    ):
        self.x = x
        self.y = y
        self.width = width
        self.bottom = bottom
        self.top = top

        dhw_bottom = width//2 + self.dhw[bottom]
        dhw_top = width//2 + self.dhw[top]
        boxes = [
            _LayerBox(bottom, x - dhw_bottom, y - dhw_bottom, x + dhw_bottom, y + dhw_bottom),
            _LayerBox(top, x - dhw_top, y - dhw_top, x + dhw_top, y + dhw_top),
        ]

        super(Via, self).__init__(
            external=False, boxes=boxes, name=name, conn=conn, space=space,
        )

    def str_indent(self, level, prefix="", level_str="  ", net=None, recursive=True):
        str_elem = "{}<->{}(({},{}))".format(
            self.bottom, self.top,
            self.x, self.y,
        )

        return self._str_indent(level, str_elem, prefix, level_str, net, recursive)

    def python_code(self, lookup={}):
        classstr = lookup.get("Via", "Via")
        return "{}({!r}, {!r}, {!r}, {!r}, {!r})".format(
            classstr, self.bottom, self.top, self.x, self.y, self.width,
        )

    def get_center(self):
        return sh_geo.Point(self.x, self.y)

class Device(_Element):
    type2gatelayer = {
        "nmos": "POLY",
        "pmos": "POLY",
    }
    type2difflayer = {
        "nmos": "NDIF",
        "pmos": "PDIF",
    }
    dhl = 0
    dhw = 4
    diffwidth = 6

    def __init__(
        self, type_, x, y, l, w, direction, *,
        name=None, source_net="fused_net", drain_net="fused_net",
    ):
        assert type_ in ("nmos", "pmos")

        self.type = type_
        self.x = x
        self.y = y
        self.l = l
        self.w = w
        assert direction in ("vertical") # Todo support horizontal transistors
        self.direction = direction
        self.source = source = {"net": source_net}
        self.drain = drain = {"net": drain_net}
        difflayer = self.type2difflayer[type_]
        dhl = l//2 + self.dhl
        dhw = w//2 + self.dhw
        x1_gate = x - dhl
        x2_gate = x + dhl
        y1_gate = y - dhw
        y2_gate = y + dhw
        x2_source = x1_gate
        x1_source = x2_source - self.diffwidth
        y1_source = y - w//2
        y2_source = y + w//2
        x1_drain = x2_gate
        x2_drain = x1_drain + self.diffwidth
        y1_drain = y1_source
        y2_drain = y2_source
        boxes = [_LayerBox(self.type2gatelayer[type_], x1_gate, y1_gate, x2_gate, y2_gate)]
        source["box"] = _LayerBox(difflayer, x1_source, y1_source, x2_source, y2_source)
        drain["box"] = _LayerBox(difflayer, x1_drain, y1_drain, x2_drain, y2_drain)
        super(Device, self).__init__(
            external=False, boxes=boxes, name=name, conn=None, space=None,
        )

    def str_indent(self, level, prefix="", level_str="  ", net=None, recursive=True):
        str_elem = "{}(({},{}),l={},w={})".format(
            self.type,
            self.x, self.y,
            self.l, self.w,
        )

        return self._str_indent(level, str_elem, prefix, level_str, net, recursive)

    def python_code(self, lookup={}):
        classstr = lookup.get("Device", "Device")
        return "{}({!r}, {!r}, {!r}, {!r}, {!r}, {!r}, source_net={!r}, drain_net={!r})".format(
            classstr, self.type,
            self.x, self.y, self.l, self.w,
            self.direction, self.source["net"], self.drain["net"],
        )

    def get_center(self):
        return sh_geo.Point(self.x, self.y)

class StdCell(object):
    def __init__(self, name="NoName", width=0, height=0, nets={}, finalize=False):
        self.name = name
        self.width = width
        self.height = height
        self.ports = set()
        self.nets = {}
        self.namedelems = {}

        self._layerboxesnets = _LayerBoxesNets()

        elem = Wire("METAL1", (0, width), 12, 24, external=True)
        elem._ignore = True
        self.add_elem(elem, net="vss")
        elem = Wire("METAL1", (0, width), 188, 24, external=True)
        elem._ignore = True
        self.add_elem(elem, net="vdd")
        elem = Wire("NWELL", (-6, width+6), 156, 120)
        elem._ignore = True
        self.add_elem(elem, net="vdd")

        for net, elems in nets.items():
            for elem in elems:
                self.add_elem(elem, net)

        if finalize:
            self.finalize()

    def add_elem(self, elem, net="fused_net"):
        assert self._layerboxesnets is not None, "add_elem() called on cell {} in finalized state".format(self.name)

        for box in elem.boxes:
            net = self._layerboxesnets.add_box(net, box)
        if isinstance(elem, Device):
            elem.source["net"] = self._layerboxesnets.add_box(elem.source["net"], elem.source["box"])
            elem.drain["net"] = self._layerboxesnets.add_box(elem.drain["net"], elem.drain["box"])
        
        try:
            self.nets[net].append(elem)
        except KeyError:
            self.nets[net] = [elem]
        if elem.external:
            self.ports |= {net}

        if hasattr(elem, "name"):
            self.namedelems[elem.name] = elem

    def _add_elem2net(self, net, elem):
        try:
            self.nets[net].append(elem)
        except KeyError:
            self.nets[net] = [elem]

    def _add_elems2net(self, net, elems):
        assert isinstance(elems, list)
        try:
            self.nets[net] += elems
        except KeyError:
            self.nets[net] = elems

    def _update_devicenets(self, elems):
        for elem in elems:
            if isinstance(elem, Device):
                source_net = elem.source["net"]
                elem.source["net"] = new_net = self._layerboxesnets.from_alias(source_net)
                try:
                    elem.connects[new_net] = elem.connects.pop(source_net)
                except KeyError:
                    pass

                drain_net = elem.drain["net"]
                elem.drain["net"] = new_net = self._layerboxesnets.from_alias(drain_net)
                try:
                    elem.connects[new_net] = elem.connects.pop(drain_net)
                except KeyError:
                    pass

            for _, elems in elem.connects.items():
                self._update_devicenets(elems)

    @staticmethod
    def _connect_elem(net, elem, todo):
        # Try to connect elem in todo set of elems and remove the connected ones from todo
        conns = set(filter(lambda other: elem.overlaps(other), todo))
        if conns:
            todo -= conns
            map(lambda elem: StdCell._connect_elem(net, elem, todo), conns)
            elem.add_connects(net, list(conns))

    def iterate_net(self, net, include_ignored=False):
        for elem in self.nets[net]:
            if (not elem._ignore) or include_ignored:
                yield elem
            for elem2 in elem.iterate_connects(net, include_ignored=include_ignored):
                yield elem2

    def iterate_devices(self, include_ignored=False):
        for net in self.nets.keys():
            for elem in self.iterate_net(net, include_ignored=include_ignored):
                if isinstance(elem, Device):
                    yield (net, elem)

    def finalize(self):
        netnames = self._layerboxesnets.finalize_nets()
        retval = {}

        # Add elems in nets that disappeared to the final net
        removednets = set(self.nets.keys()) - netnames
        for net in removednets:
            self._add_elems2net(self._layerboxesnets.from_alias(net), self.nets.pop(net))
        # Check that all ports have a net associated with it
        assert self.ports.issubset(set(self.nets.keys()))

        # Update the net names
        for elems in self.nets.values():
            self._update_devicenets(elems)

        # Merge elems in a net if possible
        merged = 0
        for net in self.nets.keys():
            for elem1, elem2 in itertools.combinations(self.iterate_net(net), 2):
                if elem1.merge(elem2):
                    merged += 1
        retval["merged"] = merged

        # (Re)connect the overlapping interconnects in a net
        # Do ignore the ignored elems
        for net, elems in self.nets.items(): # Only connect within the same net.
            tops = []
            # Set todo to all elems in the net that are not ignored
            todo = set(self.iterate_net(net))
            assert len(todo) > 0 or net in ("vss", "vdd"), "empty todo for net {}".format(net)
            while len(todo) > 0:
                elem = None
                # First search for external net for a port
                for it in todo:
                    if it.external:
                        elem = it
                        break
                # Then for a METAL1 segment
                if elem is None:
                    for it in todo:
                        if isinstance(it, Wire) and (it.layer == "METAL1"):
                            elem = it
                            break
                # Then first non-device
                if elem is None:
                    for it in todo:
                        if not isinstance(it, Device):
                            elem = it
                            break
                if elem is None:
                    elem = todo.pop()
                else:
                    # Remove selected elem
                    todo -= {elem}
                self._connect_elem(net, elem, todo)
                tops.append(elem)
            # Only retain the top elements in elems
            elems[:] = tops[:]
            #assert len(elems) == 1 or net in ("vss", "vdd")
            # if len(elems) != 1 and net not in ("vss", "vdd"):
            #     print("{} has {} top elems on net {}".format(self.name, len(elems), net))

        self._layerboxesnets = None

        return retval

    def python_code(self, level=0, level_str="    ", lookup={}):
        classstr = lookup.get("StdCell", "StdCell")

        def indent_str():
            return level*level_str
        
        s = indent_str() + classstr + "(\n"
        level += 1
        s += indent_str() + "name={!r}, width={!r}, height={!r},\n".format(
            self.name, self.width, self.height,
        )

        s += indent_str() + "nets={\n"
        level += 1
        for netname in sorted(self.nets.keys()):
            s += indent_str() + "{!r}: [\n".format(netname)
            level += 1
            # Sort elems to have same code for same cell
            for elem in sorted(
                self.iterate_net(netname),
                key=lambda elem: _OrderedPoint(elem.get_center()),
            ):
                s += indent_str() + "{},\n".format(elem.python_code(lookup=lookup))
            level -= 1
            s += indent_str() + "],\n"
        level -= 1
        s += indent_str() + "},\n"

        if not self._layerboxesnets:
            s += "{}finalize=True,".format(indent_str())
        level -= 1
        s += "\n" + indent_str() + "),\n"

        return s

    def spice_netlist(self, lambda_=0.09):
        ports = sorted(self.ports - {"vss", "vdd"})
        s = ".subckt {} {} vss vdd\n".format(self.name, " ".join(ports))
        for i, (net, device) in enumerate(sorted(
            self.iterate_devices(),
            key=lambda elem: _OrderedPoint(elem[1].get_center()),
        )):
            s += "M{} {} {} {} {} {} l={}u w={}u\n".format(
                i + 1,
                device.source["net"], net, device.drain["net"], "vss" if device.type == "nmos" else "vdd",
                device.type,
                device.l*lambda_/2.0, device.w*lambda_/2.0,
            )
        s += ".ends {}\n".format(self.name)

        return s


class _StdCellConverter:
    def __init__(self, *,
        pdklib, nmos, pmos, l=None, lambda_, nimplant=None, pimplant=None,
    ):
        self.pdklib = pdklib
        self.layoutfab = pdklib.layoutfab
        if not (
            isinstance(nmos, prm.MOSFET)
            and isinstance(pmos, prm.MOSFET)
        ):
            raise TypeError("nmos and pmos have to be of type 'MOSFET'")
        self.nmos = nmos
        self.pmos = pmos
        if l is None:
            l = nmos.computed.min_l
            if nmos.computed.min_l != pmos.computed.min_l:
                raise NotImplementedError("Different l for nmos and pmos")
        try:
            l = float(l)
        except:
            raise TypeError("l has to be a float")
        self.l = l
        self.lambda_ = lambda_

        # TODO: Check other parameters
        astrans = "Unsupported transistor composition"
        asconn = "Unsupported interconnect config"

        ngate = nmos.gate
        pgate = pmos.gate
        tech = pdklib.tech
        self.vias = vias = tuple(tech.primitives.tt_iter_type(prm.Via))
        self.nwell = pmos.well
        self.pwell = getattr(nmos, "well", None)
        if nimplant is None:
            assert len(nmos.implant) == 1, astrans
            self.nimplant = nmos.implant[0]
        else:
            self.nimplant = nimplant
        if pimplant is None:
            assert len(pmos.implant) == 1, astrans
            self.pimplant = pmos.implant[0]
        else:
            self.pimplant = pimplant
        self.active = active = ngate.active
        assert pgate.active == ngate.active, astrans
        self.poly = poly = ngate.poly
        assert pgate.poly == ngate.poly, astrans
        for via in vias:
            assert len(via.top) == 1, asconn
        for via in vias[1:]:
            assert len(via.bottom) == 1, asconn
        self.contact = contact = vias[0]
        assert (
            (active in contact.bottom) and (poly in contact.bottom), asconn
        )
        self.metal1 = contact.top[0]
        self.via1 = via1 = vias[1]
        assert len(via1.bottom) == 1, asconn

        enc = via1.min_bottom_enclosure[0].spec
        if isinstance(enc, tuple):
            enc = min(enc)
        self.pin_width = via1.width + 2*enc

    def l2r(self, v):
        return round(v*self.lambda_, 6)

    def __call__(self, cell):
        self.cell = cell

        self.pdkcell = pdkcell = self.pdklib.new_cell(cell.name)

        self.circuit = pdkcell.new_circuit()
        self.layouter = pdkcell.new_circuitlayouter(boundary=lay.Rect(
            0.0, 0.0, self.l2r(cell.width), self.l2r(cell.height),
        ))

        self.nets = {}
        self.named_layouts = {}

        self.place_mosfets()
        self.connect_wires()

        self.pdkcell = None
        self.circuit = None
        self.layouter = None
        self.names_layouts = None
        self.vssnet = None
        self.vddnet = None

        return pdkcell

    def get_net(self, name):
        try:
            return self.nets[name]
        except KeyError:
            net = self.circuit.new_net(name, external=(name in self.cell.ports))
            self.nets[name] = net
            return net

    def place_mosfets(self):
        places = []
        for i, (net, device) in enumerate(self.cell.iterate_devices()):
            is_nmos = device.type == "nmos"

            prim = self.nmos if is_nmos else self.pmos
            w = self.l2r(device.w)

            source = self.get_net(device.source["net"])
            drain = self.get_net(device.drain["net"])
            gate = self.get_net(net)
            bulk = self.get_net("vss" if is_nmos else "vdd")

            name = getattr(device, "name", f"mos{i+1}")
            mos = self.circuit.new_instance(name, prim, l=self.l, w=w)
            source.childports += mos.ports.sourcedrain1
            drain.childports += mos.ports.sourcedrain2
            gate.childports += mos.ports.gate
            bulk.childports += mos.ports.bulk

            places.append((mos, self.l2r(device.x), self.l2r(device.y)))

        # Place the transistors
        for mos, x, y in places:
            # TODO: Fix so dup() is not needed here.
            self.named_layouts[mos.name] = self.layouter.place(mos, x=x, y=y).dup()

    def connect_wires(self):
        # Standard cell frame wires
        self.vssnet = vssnet = self.get_net("vss")
        self.vddnet = vddnet = self.get_net("vdd")

        elems_spec = (
            (vssnet, "vssrail", Wire("METAL1", (0, self.cell.width), 12, 24)),
            (vddnet, "vddrail", Wire("METAL1", (0, self.cell.width), 188, 24)),
            (vddnet, "well", Wire("NWELL", (-6, self.cell.width + 6), 156, 120)),
        )
        if self.pwell is not None:
            elems_spec += (
                (vssnet, "pwell", Wire("PWELL", (-6, self.cell.width + 6), 40, 112)),
            )
        for net, name, elem in elems_spec:
            wire_params = {
                "net": net,
                "x": self.l2r(sum(elem.x)/2.0),
                "y": self.l2r(elem.y),
                "width": self.l2r(elem.x[1] - elem.x[0]),
                "height": self.l2r(elem.width),
            }

            if elem.layer == "METAL1":
                wire_params["wire"] = self.metal1
                if hasattr(self.metal1, "pin"):
                    assert len(self.metal1.pin) == 1
                    wire_params["pin"] = self.metal1.pin[0]
            elif elem.layer == "NWELL":
                wire_params["wire"] = self.nwell
            elif elem.layer == "PWELL":
                wire_params["wire"] = self.pwell
            else:
                raise AssertionError("Internal error")

            # TODO: Fix so dup() is not needed here.
            self.named_layouts[name] = self.layouter.add_wire(**wire_params).dup()

        # Cell wires
        to_process = tuple()
        for net in self.cell.nets.keys():
            to_process += tuple(
                (net, elem, set(elem.iterate_anchors()))
                for elem in self.cell.iterate_net(net)
            )

        def try_place(v):
            net, elem, anchors = v
            if all(s in self.named_layouts for s in anchors):
                self.place_elem(elem, self.get_net(net))
                return True
            else:
                return False

        while to_process:
            n_process = len(to_process)
            to_process = tuple(filter(
                lambda v: not try_place(v), to_process
            ))
            if n_process == len(to_process):
                raise ValueError("Unfound anchor")

    def place_elem(self, elem, cktnet):
        if isinstance(elem, Via):
            wire_layout = self.place_Via(elem, cktnet)
        elif isinstance(elem, Wire):
            wire_layout = self.place_Wire(elem, cktnet)
        elif not isinstance(elem, Device):
            raise AssertionError("Internal error")

        if hasattr(elem, "name") and not isinstance(elem, Device):
            assert elem.name not in self.named_layouts
            # TODO: Fix so dup() is not needed here.
            self.named_layouts[elem.name] = wire_layout.dup()

    def place_Via(self, elem, cktnet):
        # print(f"place via: {cktnet.name}")
        x = self.l2r(elem.x)
        y = self.l2r(elem.y)
        wire_params = {
            "net": cktnet, "wire": self.contact, "x": x, "columns": 1,
        }
        if not (
            hasattr(elem, "space") or hasattr(elem, "conn")
        ):
            wire_params.update({"y": y, "rows": 1})
        else:
            hasspace = hasattr(elem, "space") and (len(elem.space) > 0)
            if (
                (hasspace and not hasattr(elem, "conn"))
                or (elem.bottom == "POLY")
            ):
                wire_params.update({"y": y, "rows": 1})
            else:
                bound_spec = {}

                if "left" in elem.conn:
                    conn_elem = self.cell.namedelems[elem.conn["left"]]
                    bottom = conn_elem.y - 0.5*conn_elem.w
                    top = bottom + conn_elem.w
                    if "right" in elem.conn:
                        conn_elem = self.cell.namedelems[elem.conn["right"]]
                        assert isinstance(conn_elem, Device)
                        bottom = min(bottom, conn_elem.y - 0.5*conn_elem.w)
                        top = max(top, conn_elem.y + 0.5*conn_elem.w)
                elif "right" in elem.conn:
                    conn_elem = self.cell.namedelems[elem.conn["right"]]
                    bottom = conn_elem.y - 0.5*conn_elem.w
                    top = bottom + conn_elem.w
                else:
                    raise AssertionError("Internal error")
                if bottom <= elem.y <= top:
                    # Only extend bottom and top if original y was between
                    # the new bottom and top.
                    bound_spec = {
                        "bottom_bottom": self.l2r(bottom),
                        "bottom_top": self.l2r(top),
                    }

                    if "up" in elem.conn:
                        if (hasspace
                            and (("bottom" in elem.space) or ("top" in elem.space))
                        ):
                            raise ValueError(
                                "Clash between up connection and bottom/top spacing"
                            )
                        conn_layout = self.named_layouts[elem.conn["up"]]
                        bounds = conn_layout.bounds(mask=self.metal1.mask)
                        bound_spec.update({
                            "top_bottom": bounds.bottom, "top_top": bounds.top,
                        })
                    if hasspace:
                        if "bottom" in elem.space:
                            space_layout = self.named_layouts[elem.space["bottom"]]
                            bounds = space_layout.bounds(mask=self.metal1.mask)
                            bound_spec.update({
                                "top_bottom": bounds.top + self.metal1.min_space,
                            })
                        if "top" in elem.space:
                            space_layout = self.named_layouts[elem.space["top"]]
                            bounds = space_layout.bounds(mask=self.metal1.mask)
                            bound_spec.update({
                                "top_top": bounds.bottom - self.metal1.min_space,
                            })

                    specs = self.layoutfab.spec4bound(
                        via=self.contact, bound_spec=bound_spec,
                    )
                    wire_params.update(specs)

                else:
                    wire_params.update({"y": y, "rows": 1})

        if len(self.contact.top) > 1:
            wire_params["top"] = self.metal1
        assert (
            (elem.bottom in ("NDIF", "NTIE", "PDIF", "PTIE", "POLY"))
            and (elem.top == "METAL1")
        ), "Internal error"
        if elem.bottom in ("NDIF", "NTIE"):
            wire_params.update({
                "bottom": self.active, "bottom_implant": self.nimplant,
            })
        if elem.bottom in ("PDIF", "PTIE"):
            wire_params.update({
                "bottom": self.active, "bottom_implant": self.pimplant,
            })
        if (elem.bottom in ("NTIE", "PDIF")) and (self.nwell is not None):
            wire_params.update({
                "well_net": self.vddnet, "bottom_well": self.nwell,
            })
        if (elem.bottom in ("PTIE", "NDIF")) and (self.pwell is not None):
            wire_params.update({
                "well_net": self.vssnet, "bottom_well": self.pwell,
            })
        if elem.bottom == "POLY":
            wire_params["bottom"] = self.poly

        wire_layout = self.layouter.add_wire(**wire_params).dup()

        if hasattr(elem, "conn"):
            bottom_wire = wire_params["bottom"]
            bottom_bounds = wire_layout.bounds(mask=bottom_wire.mask)

            if "bottom_implant" in wire_params:
                extra_params = {"implant": wire_params["bottom_implant"]}
            else:
                extra_params = {}
            if "bottom_well" in wire_params:
                well_params = {
                    "well": wire_params["bottom_well"],
                    "well_net": wire_params["well_net"],
                }
            elif "well_net" in wire_params:
                well_params = {"well_net": wire_params["well_net"]}
            else:
                well_params = {}
            extra_params.update(well_params)

            if "left" in elem.conn:
                conn_layout = self.named_layouts[elem.conn["left"]]
                conn_bounds = conn_layout.bounds(mask=bottom_wire.mask)
                self._connect_left(
                    net=cktnet, wire=bottom_wire, **extra_params,
                    from_rect=bottom_bounds, to_rect=conn_bounds,
                )

            if "right" in elem.conn:
                conn_layout = self.named_layouts[elem.conn["right"]]
                conn_bounds = conn_layout.bounds(mask=bottom_wire.mask)
                self._connect_right(
                    net=cktnet, wire=bottom_wire, **extra_params,
                    from_rect=bottom_bounds, to_rect=conn_bounds
                )

            if "bottom" in elem.conn:
                # conn = self.cell.namedelems[elem.conn["bottom"]]
                # assert isinstance(conn, Wire) and conn.layer == "METAL1", "Unsupported"
                conn_layout = self.named_layouts[elem.conn["bottom"]]
                _, _, _, bottom = conn_layout.bounds(mask=self.metal1.mask)
                left, _, right, top = wire_layout.bounds(mask=self.metal1.mask)

                x = 0.5*(left + right)
                y = 0.5*(bottom + top)
                width = right - left
                height = top - bottom

                self.layouter.add_wire(
                    net=cktnet, wire=self.metal1,
                    x=x, y=y, width=width, height=height,
                )

            if "top" in elem.conn:
                # conn = self.cell.namedelems[elem.conn["top"]]
                # assert isinstance(conn, Wire) and conn.layer == "METAL1", "Unsupported"
                conn_layout = self.named_layouts[elem.conn["top"]]
                _, top, _, _ = conn_layout.bounds(mask=self.metal1.mask)
                left, bottom, right, _ = wire_layout.bounds(mask=self.metal1.mask)

                x = 0.5*(left + right)
                y = 0.5*(bottom + top)
                width = right - left
                height = top - bottom

                self.layouter.add_wire(
                    net=cktnet, wire=self.metal1,
                    x=x, y=y, width=width, height=height,
                )

        return wire_layout

    def place_Wire(self, elem, cktnet):
        # print(f"place wire: {cktnet.name}")
        wire_params = {"net": cktnet}

        if isinstance(elem.x, tuple):
            left = self.l2r(elem.x[0])
            right = self.l2r(elem.x[1])
            bottom = self.l2r(elem.y - 0.5*elem.width)
            top = bottom + self.l2r(elem.width)
        elif isinstance(elem.y, tuple):
            left = self.l2r(elem.x - 0.5*elem.width)
            right = left + self.l2r(elem.width)
            bottom = self.l2r(elem.y[0])
            top = self.l2r(elem.y[1])
        else:
            raise AssertionError("Internal error")

        if elem.layer in ("NDIF", "NTIE"):
            wire = self.active
            wire_params.update({
                "wire": wire, "implant": self.nimplant,
            })
        if elem.layer in ("PDIF", "PTIE"):
            wire = self.active
            wire_params.update({
                "wire": wire, "implant": self.pimplant,
            })
        if (elem.layer in ("NTIE", "PDIF")) and (self.nwell is not None):
            wire_params.update({
                "well_net": self.vddnet, "well": self.nwell,
            })
        if (elem.layer in ("PTIE", "NDIF")) and (self.pwell is not None):
            wire_params.update({
                "well_net": self.vssnet, "well": self.pwell,
            })
        if elem.layer == "POLY":
            wire_params["wire"] = wire = self.poly
        elif elem.layer == "METAL1":
            wire_params["wire"] = wire = self.metal1
            if elem.external and hasattr(wire, "pin"):
                wire_params["pin"] = self.metal1.pin[0]

        if hasattr(elem, "conn"):
            if "bottom" in elem.conn:
                conn_layout = self.named_layouts[elem.conn["bottom"]]
                bottom = (
                    conn_layout.bounds(mask=wire.mask).top - wire.min_width
                )
            if "top" in elem.conn:
                conn_layout = self.named_layouts[elem.conn["top"]]
                top = (
                    conn_layout.bounds(mask=wire.mask).bottom + wire.min_width
                )

        if hasattr(elem, "space"):
            if "left" in elem.space:
                space_layout = self.named_layouts[elem.space["left"]]
                left = space_layout.bounds(mask=wire.mask).right + wire.min_space

            if "bottom" in elem.space:
                space_layout = self.named_layouts[elem.space["bottom"]]
                bottom = space_layout.bounds(mask=wire.mask).top + wire.min_space

            if "right" in elem.space:
                space_layout = self.named_layouts[elem.space["right"]]
                right = space_layout.bounds(mask=wire.mask).left - wire.min_space

            if "top" in elem.space:
                space_layout = self.named_layouts[elem.space["top"]]
                top = space_layout.bounds(mask=wire.mask).bottom - wire.min_space

        x = (left + right)/2.0
        y = (bottom + top)/2.0
        width = right - left
        height = top - bottom

        if hasattr(elem, "space") or hasattr(elem, "conn") or hasattr(elem, "name"):
            if elem.external:
                assert elem.layer == "METAL1"
                min_width = self.pin_width
            else:
                min_width = wire.min_width

            if isinstance(elem.x, tuple):
                height = min_width
            else:
                width = min_width

        wire_params.update({
            "x": x, "y": y, "width": width, "height": height,
        })

        assert "wire" in wire_params, "Internal error"
        wire_layout = self.layouter.add_wire(**wire_params)

        if hasattr(elem, "conn"):
            for key in ("x", "y", "width", "height"):
                wire_params.pop(key)

            wire_bounds = wire_layout.bounds(mask=wire.mask)
            if "left" in elem.conn:
                conn_layout = self.named_layouts[elem.conn["left"]]
                conn_bounds = conn_layout.bounds(mask=wire.mask)
                self._connect_left(
                    from_rect=wire_bounds, to_rect=conn_bounds, **wire_params,
                )
            if "right" in elem.conn:
                conn_layout = self.named_layouts[elem.conn["right"]]
                conn_bounds = conn_layout.bounds(mask=wire.mask)
                self._connect_right(
                    from_rect=wire_bounds, to_rect=conn_bounds, **wire_params,
                )

        return wire_layout

    def _connect_left(self, *, net, wire, from_rect, to_rect, **wire_params):
        if wire == self.active:
            rect = lay.Rect(
                to_rect.right, to_rect.bottom, from_rect.right, to_rect.top,
            )

            self.layouter.add_wire(
                net=net, wire=wire, **wire_params,
                **self.layoutfab.spec4bound(bound_spec=rect),
            )

            left = from_rect.left
            right = from_rect.right
            try:
                minw = wire.min_width
            except:
                pass
            else:
                if (right - left) < minw:
                    left, right = (
                        0.5*(left + right - minw),
                        0.5*(left + right + minw),
                    )
            if from_rect.top < to_rect.bottom:
                rect = lay.Rect(
                    left, from_rect.bottom, right, to_rect.top,
                )
                self.layouter.add_wire(
                    net=net, wire=wire, **wire_params,
                    **self.layoutfab.spec4bound(bound_spec=rect),
                )
            elif from_rect.bottom > to_rect.top:
                rect = lay.Rect(
                    left, to_rect.bottom, right, from_rect.top,
                )
                self.layouter.add_wire(
                    net=net, wire=wire, **wire_params,
                    **self.layoutfab.spec4bound(bound_spec=rect),
                )
        else:
            rect = lay.Rect(
                to_rect.right - wire.min_width, from_rect.bottom,
                from_rect.right, from_rect.top,
            )
            self.layouter.add_wire(
                net=net, wire=wire, **wire_params,
                **self.layoutfab.spec4bound(bound_spec=rect),
            )

            if from_rect.top < to_rect.bottom:
                rect = lay.Rect(
                    rect.left, rect.bottom, to_rect.right, to_rect.bottom,
                )
                self.layouter.add_wire(
                    net=net, wire=wire, **wire_params,
                    **self.layoutfab.spec4bound(bound_spec=rect),
                )
            elif from_rect.bottom > to_rect.top:
                rect = lay.Rect(
                    rect.left, to_rect.top, to_rect.right, rect.top,
                )
                self.layouter.add_wire(
                    net=net, wire=wire, **wire_params,
                    **self.layoutfab.spec4bound(bound_spec=rect),
                )

    def _connect_right(self, *, net, wire, from_rect, to_rect, **wire_params):
        if wire == self.active:
            rect = lay.Rect(
                from_rect.left, to_rect.bottom, to_rect.left, to_rect.top,
            )

            self.layouter.add_wire(
                net=net, wire=wire, **wire_params,
                **self.layoutfab.spec4bound(bound_spec=rect),
            )

            left = from_rect.left
            right = from_rect.right
            try:
                minw = wire.min_width
            except:
                pass
            else:
                if (right - left) < minw:
                    left, right = (
                        0.5*(left + right - minw),
                        0.5*(left + right + minw),
                    )
            if from_rect.top < to_rect.bottom:
                rect = lay.Rect(
                    left, from_rect.bottom, right, to_rect.top,
                )
                self.layouter.add_wire(
                    net=net, wire=wire, **wire_params,
                    **self.layoutfab.spec4bound(bound_spec=rect),
                )
            elif from_rect.bottom > to_rect.top:
                rect = lay.Rect(
                    left, to_rect.bottom, right, from_rect.top,
                )
                self.layouter.add_wire(
                    net=net, wire=wire, **wire_params,
                    **self.layoutfab.spec4bound(bound_spec=rect),
                )
        else:
            rect = lay.Rect(
                from_rect.left, from_rect.bottom,
                to_rect.left + wire.min_width, from_rect.top,
            )
            self.layouter.add_wire(
                net=net, wire=wire, **wire_params,
                **self.layoutfab.spec4bound(bound_spec=rect),
            )

            if from_rect.top < to_rect.bottom:
                rect = lay.Rect(
                    to_rect.left, rect.bottom, rect.right, to_rect.bottom,
                )
                self.layouter.add_wire(
                    net=net, wire=wire, **wire_params,
                    **self.layoutfab.spec4bound(bound_spec=rect),
                )
            elif from_rect.bottom > to_rect.top:
                rect = lay.Rect(
                    to_rect.left, to_rect.top, rect.right, rect.top,
                )
                self.layouter.add_wire(
                    net=net, wire=wire, **wire_params,
                    **self.layoutfab.spec4bound(bound_spec=rect),
                )
