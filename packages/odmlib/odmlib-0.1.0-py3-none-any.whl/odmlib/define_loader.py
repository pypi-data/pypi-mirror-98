import odmlib.define_2_0.model as DEF
import odmlib.document_loader as DL
import odmlib.odm_parser as P
import odmlib.ns_registry as NS
import json
import xml.etree.ElementTree as ET


class XMLDefineLoader(DL.DocumentLoader):
    def __init__(self):
        self.filename = None
        self.parser = None
        self.nsr = NS.NamespaceRegistry()

    def load_document(self, elem, *args):
        elem_name = elem.tag[elem.tag.find('}') + 1:]
        #prefix, namespace = self.nsr.get_prefix_ns_from_uri(elem.tag[:elem.tag.find('}') + 1])
        if elem.text and not elem.text.isspace():
            attrib = {**elem.attrib, **{"_content": elem.text}}
            odm_obj = eval("DEF." + elem_name + "(**" + str(attrib) + ")")
        else:
            odm_obj = eval("DEF." + elem_name + "(**" + str(elem.attrib) + ")")
        odm_obj_dict = eval("DEF." + elem_name + ".__dict__.items()")
        for k, v in odm_obj_dict:
            if type(v).__name__ == "ODMObject":
                namespace = self.nsr.get_ns_entry_dict(v.namespace)
                e = elem.find(v.namespace + ":" + k, namespace)
                if e is not None:
                    odm_child_obj = self.load_document(e)
                    exec("odm_obj." + k + " = odm_child_obj")
            elif type(v).__name__ == "ODMListObject":
                namespace = self.nsr.get_ns_entry_dict(v.namespace)
                for e in elem.findall(v.namespace + ":" + k, namespace):
                    odm_child_obj = self.load_document(e)
                    eval("odm_obj." + k + ".append(odm_child_obj)")
        return odm_obj

    def create_document(self, filename, namespace_registry=None):
        self.filename = filename
        self._set_registry(namespace_registry)
        self.parser = P.ODMParser(self.filename, self.nsr)
        root = self.parser.parse()
        return root

    def create_document_from_string(self, odm_string, namespace_registry=None):
        self._set_registry(namespace_registry)
        self.parser = P.ODMStringParser(odm_string, self.nsr)
        root = self.parser.parse()
        return root

    def _set_registry(self, namespace_registry):
        if namespace_registry:
            self.nsr = namespace_registry
        else:
            NS.NamespaceRegistry(prefix="odm", uri="http://www.cdisc.org/ns/odm/v1.3", is_default=True)
            self.nsr = NS.NamespaceRegistry(prefix="def", uri="http://www.cdisc.org/ns/def/v2.0")

    def load_odm(self):
        root = self.parser.ODM()
        root_odmlib = self.load_document(root)
        return root_odmlib

    def load_metadataversion(self, idx=0):
        mdv = self.parser.MetaDataVersion()
        mdv_odmlib = self.load_document(mdv[idx])
        return mdv_odmlib

    def load_study(self, idx=0):
        study = self.parser.Study()
        study_odmlib = self.load_document(study[idx])
        return study_odmlib


class JSONDefineLoader(DL.DocumentLoader):
    def __init__(self):
        self.filename = None
        self.odm_dict = {}

    def load_document(self, odm_dict, key):
        attrib = {key: value for key, value in odm_dict.items() if not isinstance(value, (list, dict))}
        odm_obj = eval("DEF." + key + "(**" + str(attrib) + ")")
        odm_obj_items = eval("DEF." + key + ".__dict__.items()")
        for k, v in odm_obj_items:
            if type(v).__name__ == "ODMObject":
                if k in odm_dict:
                    odm_child_obj = self.load_document(odm_dict[k], k)
                    exec("odm_obj." + k + " = odm_child_obj")
            elif type(v).__name__ == "ODMListObject":
                if k in odm_dict:
                    for val in odm_dict[k]:
                        odm_child_obj = self.load_document(val, k)
                        eval("odm_obj." + k + ".append(odm_child_obj)")
        return odm_obj

    def create_document(self, filename):
        self.filename = filename
        with open(self.filename) as json_in:
            self.odm_dict = json.load(json_in)
        return self.odm_dict

    def create_document_from_string(self, odm_string):
        self.odm_dict = json.loads(odm_string)
        return self.odm_dict

    def load_odm(self):
        if not self.odm_dict:
            raise ValueError("create_document must be used to create the document before executing load_odm")
        odm_odmlib = self.load_document(self.odm_dict, "MetaDataVersion")
        return odm_odmlib

    def load_metadataversion(self, idx=0):
        if not self.odm_dict:
            raise ValueError("create_document must be used to create the document before executing load_metadataversion")
        mdv_dict = self.odm_dict["MetaDataVersion"][idx]
        mdv_odmlib = self.load_document(mdv_dict, "MetaDataVersion")
        return mdv_odmlib
