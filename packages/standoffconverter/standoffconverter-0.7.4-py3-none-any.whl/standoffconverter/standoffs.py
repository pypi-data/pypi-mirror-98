from lxml import etree
import numpy as np
import pandas as pd
import json
from contextlib import contextmanager

class Converter:
    """Contains a reference to the etree.Element object and the corresponding ContextItem object to link the two representations.
    """
    def __init__(self, tei_tree, namespaces={}):
        """Create a Converter from a tree element instance.
        
        arguments:
            tei_tree (etree.Element): the etree.Element instance.

        returns:
            (Converter): The created Converter instance.
        """

        if "tei" not in namespaces:
            namespaces = {"tei": ""}

        self.tei_tree = tei_tree

        texts = self.tei_tree.findall(".//tei:text", namespaces=namespaces)
        if len(texts) == 0:
            raise ValueError("No text attribute found.")
        elif len(texts)>1:
            raise ValueError("More than one text element is not supported.")
        else:
            self.text_el = texts[0]

        # Caches
        self.reset_cache()

    @contextmanager
    def cached_standoff(self):
        try:
            self.populate_cache()
            yield
        finally:
            self.reset_cache()

    def populate_cache(self):
        self.table_, self.so2el, self.el2so = tree_to_standoff(self.text_el)
        self.plaintext = "".join(self.table.text)

    def reset_cache(self):
        self.el2so = None
        self.so2el = None
        self.table_ = None
        self.plaintext = None

    def ensure_cache(self):
        if self.table_ is None:
            self.populate_cache()

    @property
    def table(self):
        """Table with each character and context of the <text> element of the tei tree. Index  is character position inside <text> element of te TEI XML."""
        self.ensure_cache()
        return self.table_
    
    @property
    def tree(self):
        """tree of the TEI XML."""
        return self.tei_tree


    @property
    def plain(self):
        """Plain text string of all text inside the <text> element of the TEI XML."""
        self.ensure_cache()
        return self.plaintext

    @property
    def standoffs(self):
        """List of standoff elements of the <text> element fo the TEI XML. Items are traversed in depth-first preorder."""

        self.ensure_cache()

        context = list(set([so for context in self.table.context for so in context]))
        
        context = sorted(
            sorted(
                sorted(
                    context,
                    key=lambda x: x.depth
                ),
                key=lambda x:  (x.begin - x.end)
            ),
            key=lambda x: x.begin
        )

        return context

    @property
    def json(self):
        """JSON string of standoff elements of the <text> element fo the TEI XML. Items are traversed in depth-first preorder."""
        return json.dumps(list(map(lambda x: x.to_dict(), self.standoffs)))
        
    @property
    def collapsed_table(self):
        """Table with text and context of the <text> element of the tei tree. All leaf/tail text with the same context is joined."""
        self.ensure_cache()
        return collapse_table(self.table)

    def get_parents(self, begin, end, depth=None):
        """Get all parent context.
        
        arguments:
        begin (int)-- beginning character position within the XML
        end (int)-- ending character position within the XML
        depth (int)-- depth of current element

        returns:
            parents (list) -- list of parent elements ordered by depth (closest is last).
        """
        mask = np.zeros(len(self.table), dtype=bool)
        # include only slightly more than all children
        mask[max(0,begin-1):min(len(self.table),end+1)] = True 
        # exlcude children
        mask[begin+1:end-1] = False
        
        filtered_table = self.table[mask]
        
        mask = np.logical_and.reduce([
            filtered_table.context.apply(lambda x: x[-1].begin<=begin),
            filtered_table.context.apply(lambda x: x[-1].end>=end)
        ])

        filtered_table = filtered_table[mask]

        context = list(set([
            so 
                for context in filtered_table.context 
                    for so in context 
                        if depth is None or so.depth < depth
        ]))

        context = sorted(context, key=lambda x: x.depth)

        return context

    def get_children(self, begin, end, depth):
        """Get all children context.
        
        arguments:
        begin (int)-- beginning character position within the XML
        end (int)-- ending character position within the XML
        depth (int)-- depth of current element

        returns:
            children (list) -- list of children elements ordered by depth (closest is first).
        """
        if depth is None:
            return []

        if end <= begin:
            return []
            
        filtered_table = self.table.loc[begin:end-1]

        mask = np.logical_and.reduce([
            filtered_table.context.apply(lambda x: x[-1].begin>=begin),
            filtered_table.context.apply(lambda x: x[-1].end<=end),
        ])

        filtered_table = filtered_table[mask]

        context = list(set([
            so 
                for context in filtered_table.context 
                    for so in context 
                        if so.depth >= depth
        ]))

        context = sorted(context, key=lambda x: x.depth)

        return context
        
    def add_standoff(self, begin, end, tag, attrib):
        raise NotImplementedError()

    def __replace_el(self, old_el, new_el):

        old_so = self.el2so[old_el]

        second_parents = self.get_parents(
            old_so.begin,
            old_so.end,
            old_so.depth
        )

        # and replace the subtree
        if len(second_parents) == 0:
            new_el.tail = self.text_el.tail
            self.text_el = new_el
        else:

            second_parent = self.so2el[second_parents[-1]]
            
            new_el.tail = old_el.tail
            second_parent.replace(
                old_el,
                new_el
            )

    def __update_so2el_lookup(self, new_so2el):

        for new_so, new_el in new_so2el.items():

            if new_so in self.so2el:
                old_el = self.so2el[new_so]
                del self.el2so[old_el]

            self.so2el[new_so] = new_el
            self.el2so[new_el] = new_so

    def __get_part_to_update(self, table, depth):
        to_update = []
        for context in table.context:
            to_update.append(context[depth:])

        return pd.DataFrame.from_dict({
            "context": to_update,
            "text": table.text
        })

    def remove_inline(self, del_so):
        """Remove a standoff element from the structure. 
        The standoff element will be removed from the caches and from the etree.
        
        arguments:
        del_so (ContextItem)-- the element that should be removed

        """

        self.ensure_cache()
        # First, get parents and children
        del_so_table = self.table.loc[del_so.begin:del_so.end-1]

        if len(del_so_table) == 0:
            del_so_table = self.table.loc[del_so.begin:del_so.end]
            del_so_table = del_so_table[
                del_so_table.T.apply(lambda x: del_so in x.context)
            ]

        parent = self.get_parents(del_so.begin, del_so.end, del_so.depth)[-1]

        parent_table = self.table.loc[parent.begin:parent.end-1]

        children = self.get_children( 
            del_so.begin,
            del_so.end,
            del_so.depth 
        )
        
        # DEPTH handling 
        # decrease children's depth by one
        for child in children:
            child.depth -= 1

        # actually removing the new standoff element
        for _,row in del_so_table.iterrows():
            row.context.remove(del_so)

        # if it was an empty element, remove the row as a cleanup operation
        if del_so.begin == del_so.end:
            self.table.drop(
                del_so_table.index,
                inplace=True
            )

        # extract part of the standoff table that needs to be recreated
        # as etree
        to_update = self.__get_part_to_update(parent_table, parent.depth)

        # now, recreate the subtree this element is in
        new_parent_el, new_so2el = standoff_to_tree(to_update)

        self.__replace_el(
            self.so2el[parent],
            new_parent_el
        )
        
        # remove deleted element from lookups
        del self.el2so[self.so2el[del_so]]
        del self.so2el[del_so]

        self.__update_so2el_lookup(new_so2el)

    
    def __validate_add_inline(self, new_so, parents, children):

        if len(parents) == 0:
            raise ValueError("no unique parent element found.")

        parent = parents[-1]
        
        new_so_table = self.table.loc[new_so.begin:new_so.end-1]
        
        spurious_children = [c for _,row in new_so_table.iterrows() for c in row.context if c.depth >= parent.depth+1 and c not in children]

        if len(spurious_children) > 0:
            raise ValueError("Spurious children found.")


    def add_inline(self, **tag_dict):
        """Add a standoff element to the structure. 
        The standoff element will be added to the caches and to the etree.
        
        arguments:
        begin (int)-- beginning character position within the XML
        end (int)-- ending character position within the XML
        tag (str)-- tag name, for example 'text' for <text>.
        depth (int)-- depth where to add the element. If None, it will be added deepest
        attrib (dict)-- dictionary of items that go into the attrib of etree.Element. Ultimately, attributes within tags. for example {"resp":"machine"} will result in <SOMETAG resp="machine">.
        """

        self.ensure_cache()
        
        # First, create new standoff element and get parents and children
        new_so = ContextItem(tag_dict)
        new_so_table = self.table.loc[new_so.begin:new_so.end-1]
        if len(new_so_table) == 0:
            # empty element requires placeholder to be inserted into `self.table`
            c_base_index = self.table.loc[new_so.begin].iloc[-1].name
            self.table.loc[(new_so.begin, c_base_index-.5), :] = np.array((
                Context(self.table.loc[new_so.begin].iloc[-1].context),
                ""
            ), dtype=object)
            self.table.sort_index(inplace=True)
            self.table.index = self.table.index.set_levels(range(len(self.table)),level=1)
            new_so_table = self.table.loc[new_so.begin:new_so.end].iloc[-2:-1]

        parents = self.get_parents(new_so.begin, new_so.end, new_so.depth)
        children = self.get_children(new_so.begin, new_so.end, new_so.depth)
        
        self.__validate_add_inline(
            new_so,
            parents,
            children
        )
        parent = parents[-1]

        parent_table = self.table.loc[parent.begin:parent.end-1]
        # DEPTH handling 
        # set own depth and increase children's depth by one
        new_so.depth = parent.depth + 1

        for child in children:
            child.depth += 1

        # actually inserting the new standoff element
        for _,row in new_so_table.iterrows():
            row.context.insert(new_so.depth, new_so)


        # extract part of the standoff table that needs to be recreated
        # as etree
        to_update = self.__get_part_to_update(parent_table, parent.depth)

        # now, recreate the subtree this element is in
        new_parent_el, new_so2el = standoff_to_tree(to_update)
        

        self.__replace_el(
            self.so2el[parent],
            new_parent_el
        )

        self.__update_so2el_lookup(new_so2el)


class Context(list):
    
    def __str__(self):
        return ">".join(map(str, self))

    def strip_ns(self):
        return ">".join(map(lambda x: x.strip_ns(), self))


class ContextItem:
    """Wrapper class for the basic standoff properties."""
    def __init__(self, dict_):
        self.tag = dict_["tag"] if "tag" in dict_ else None
        self.attrib = dict(dict_["attrib"]) if "attrib" in dict_ else None
        self.begin = dict_["begin"] if "begin" in dict_ else None
        self.end = dict_["end"] if "end" in dict_ else None
        self.depth = dict_["depth"] if "depth" in dict_ else None

    def strip_ns(self):
        return (
            self.tag[self.tag.index("}")+1:]
            if "}" in self.tag else
            self.tag
        )

    def __str__(self):
        return self.tag

    def __repr__(self):
        return f"{self.tag}-{hex(id(self))}"

    def to_dict(self):
        return {
            "tag": self.tag,
            "attrib": self.attrib,
            "begin": self.begin,
            "end": self.end,
            "depth": self.depth
        }


class View:

    def __init__(self, so, mask):
        
        self.filtered_table = so.table[mask]
        self.viewinds2soinds = self.filtered_table.index
        self.plain = "".join(self.filtered_table.text)

    def standoff_char_pos(self, ind):
        return self.viewinds2soinds[ind]


def collapse_table(table):
        """Pandas Dataframe with standoff elements and texts aligned. text within the same element is grouped"""
        context = table.context.apply(tuple)
        grouper = (context != context.shift()).cumsum()
        collapsed = []
        for group, subdf in table.groupby(grouper):
            collapsed.append({
                "context": subdf.iloc[0].context,
                "text": "".join(subdf.text)
            })

        return pd.DataFrame(collapsed)


def create_el_from_so(c_so):
    el = etree.Element(c_so.tag)
    for k,v in c_so.attrib.items():
        el.set(k,v)
    return el


def get_table_from_pair_collection(plain, pair_collection):
    order = __get_order_for_traversal(pair_collection)

    plain = [c for c in plain]
    positions = list(range(len(plain)))
    pos2so = [Context() for _ in range(len(plain))]
    so2el = {}
    el2so = {}

    for c_so, c_el in order:

        so2el[c_so] = c_el
        el2so[c_el] = c_so

        for pos in range(c_so.begin, c_so.end):
            pos2so[pos].append(c_so)

        
        # handling of empty elements
        if c_so.begin == c_so.end:
            pos = c_so.begin
            pos2so.insert(pos, Context(pos2so[pos]))
            pos2so[pos].append(c_so)
            
            plain.insert(pos, "")
            positions.insert(pos, positions[pos])



    index = [
    ]

    table = pd.DataFrame([
            positions,
            list(range(len(positions))),
            pos2so,
            plain
        ],
        index=['position', 'base_index', 'context', 'text']
    ).T

    table = table.set_index(["position", "base_index"])
    return table, so2el, el2so
    

def tree_to_standoff(tree):
    """traverse the tree and create a standoff representation.

    arguments:
        tree -- the root element of an lxml etree

    returns:
        plain (str) -- the plain text of the tree
        collection (list) -- the list of standoff annotations
    """
    stand_off_props = {}
    plain = []

    def __traverse_and_parse(el, plain, stand_off_props, depth=0):
        
        so = {
            "begin": len(plain),
            "tag": el.tag,
            "attrib": el.attrib,
            "depth": depth
        }
        
        so = ContextItem(so)

        stand_off_props[el] = (so, el)

        if el.text is not None:
            plain += [char for char in el.text]

        for gen in el:
            __traverse_and_parse(gen, plain, stand_off_props, depth=depth+1)

        depth -= 1
        stand_off_props[el][0].end = len(plain)

        if el.tail is not None and depth>0: # (depth>0) shouldn't add tail for root
            plain += [char for char in el.tail]

    __traverse_and_parse(tree, plain, stand_off_props)

    plain, pair_collection = "".join(plain), [v for k,v in stand_off_props.items()]
    
    table, so2el, el2so = get_table_from_pair_collection(plain, pair_collection)

    return table, so2el, el2so


def __get_order_for_traversal(so):
    return sorted(
        sorted(
            sorted(
                so,
                key=lambda x: x[0].depth
            ),
            key=lambda x:  (x[0].begin - x[0].end)
        ),
        key=lambda x: x[0].begin
    )


def standoff_to_tree(table):
    """convert the standoff representation to a etree representation

    arguments:
        table -- standoff object

    returns:
        tree (str) -- the root element of the resulting tree
    """
    so2el = {}
    collapsed_table = collapse_table(table)
    for _,row in collapsed_table.iterrows():
        
        c_parents = []
        for it in row.context:
            if it not in so2el:
                new_el = create_el_from_so(it)
                so2el[it] = new_el

            c_parents.append(so2el[it])
                
        for i_parent in range(len(c_parents)-1):
            c_parent = c_parents[i_parent]
            c_child = c_parents[i_parent+1]
            if c_child not in c_parent:
                c_parent.append(c_child)
        if len(c_parents[-1]) == 0:
            if row.text != "":
                c_parents[-1].text = row.text
        else:
            if c_parents[-1][-1].tail is None:
                c_parents[-1][-1].tail = ""
            c_parents[-1][-1].tail += row.text

    root = so2el[collapsed_table.iloc[0].context[0]].getroottree().getroot()

    return root, so2el
