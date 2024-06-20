#!/usr/bin/python3
import argparse
import json
from xml.dom.minidom import parseString

import cbor
import dicttoxml
import qtoml
import yaml
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef

parser = argparse.ArgumentParser(description='Process CGDL documents.')
parser.add_argument('file', type=str, help='a CGDL file')

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-m", "--metadata", help="display CGDL metadata", action="store_true")
group.add_argument("-j", "--json", help="display CGDL in JSON", action="store_true")
group.add_argument("-pj", "--prettyjson", help="display CGDL in pretty JSON", action="store_true")
group.add_argument("-cb", "--cbor", help="display CGDL in CBOR (binary JSON)", action="store_true")
group.add_argument("-x", "--xml", help="display CGDL in XML", action="store_true")
group.add_argument("-px", "--prettyxml", help="display CGDL in pretty XML", action="store_true")
group.add_argument("-t", "--toml", help="display TOML", action="store_true")
group.add_argument("-y", "--yaml", help="display CGDL in compact YAML", action="store_true")
# parser.add_argument("-py", "--prettyyaml", help="display CGDL in compact YAML",
#                     action="store_true")
group.add_argument("-c", "--cgdl", help="display CGDL (in YAML)", action="store_true")
group.add_argument("-g", "--graphql", help="display GraphQL", action="store_true")
group.add_argument("-s", "--shacl", help="display SHACL (in RDF, Turtle)", action="store_true")
group.add_argument("-sx", "--shex", help="display ShEx", action="store_true")
group.add_argument("-p", "--pgschema", help="display PG-Schema", action="store_true")

args = parser.parse_args()

if args.file:
    with open(args.file, 'r') as stream:
        try:
            data = yaml.load(stream, Loader=yaml.SafeLoader)
            with open(args.file, 'r') as s:
                raw = s.read()
        except yaml.YAMLError as exc:
            print(exc)
            exit()

    if args.metadata:
        try:
            print('CGDL domument data creation: ' + data['metadata']['created'])
        except:
            print('There are not any information about CGDL data creation')
        try:
            print('Document is created by ' + data['metadata']['creator'])
        except:
            print('There are not any information about CGDL creator')
        exit()
        print(data['shapes'][0]['target'])

    if args.json:
        json = json.dumps(data)
        print(json)
    if args.cbor:
        cbor = cbor.dumps(data)
        print(cbor)
    if args.prettyjson:
        json = json.dumps(data, indent=2, sort_keys=True)
        print(json)
    if args.xml:
        xml = dicttoxml.dicttoxml(data, attr_type=False, custom_root='cgdl')
        print(xml.decode("utf-8"))
    if args.prettyxml:
        xml = dicttoxml.dicttoxml(data, attr_type=False, custom_root='cgdl')
        x = xml.decode("utf-8")
        dom = parseString(x)
        print(dom.toprettyxml())
    if args.toml:
        toml = qtoml.dumps(data)
        print(toml)
    if args.yaml:
        print(yaml.dump(data))
    if args.cgdl:
        print(raw)
    if args.graphql:
        indentation = '  '


        def set_datatype(f):
            if f == 'string':
                return 'String'
            elif f == 'int':
                return 'Int'
            elif f == 'integer':
                return 'Int'
            elif f == 'boolean':
                return 'Boolean'
            elif f == 'decimal':
                return 'Float'
            elif f == 'float':
                return 'Float'
            elif f == 'double':
                return 'Float'
            elif f == 'dateTime':
                return 'String'
            elif f == 'time':
                return 'String'
            elif f == 'date':
                return 'String'


        def print_edge_details(pnd):
            print(indentation + pnd.lower() + 's: [' + pnd + ']')


        for shape in data.get('shapes', []):
            try:
                tn1 = shape['target']
                print('type ' + tn1 + ' {')
            except:
                print('# There is no information about target node')

            for predicate in shape.get('predicates', []):
                if 'datatype' in predicate:
                    try:
                        pn1 = predicate['name']
                        pdt1 = predicate['datatype']
                        pdt1 = set_datatype(pdt1)
                        print(indentation + pn1 + ': ' + pdt1 + '!')
                    except:
                        print(indentation + '# There is no information about property name or data type')
                else:
                    try:
                        pp1 = predicate['name']
                        pnd1 = predicate['node']
                        print_edge_details(pnd1)
                    except:
                        print(indentation + '# Error while printing edge details')

            print('}\n')
    if args.shacl:
        g = Graph()
        doc = BNode()
        dct = Namespace("http://purl.org/dc/terms/")
        sh = Namespace("http://www.w3.org/ns/shacl#")
        pg = Namespace("urn:cgdl:1.0:")
        xsd = Namespace("http://www.w3.org/2001/XMLSchema#")

        def set_datatype(f):
            return {'string': xsd.string, 'int': xsd.int, 'integer': xsd.integer, 'boolean': xsd.boolean,
                    'decimal': xsd.decimal, 'float': xsd.float, 'double': xsd.double, 'dateTime': xsd.dateTime,
                    'time': xsd.time, 'date': xsd.date, }.get(f)

        try:
            created = data['metadata']['created']
            g.add((doc, dct.created, Literal(created, datatype=xsd.date)))
        except KeyError:
            print('# There is no information about date of creation')

        try:
            creator = data['metadata']['creator']
            g.add((doc, dct.creator, Literal(creator)))
        except KeyError:
            print('# There is no information about creator')

        for shape in data.get('shapes', []):
            try:
                tn1 = shape['target']
                shape_ref = URIRef(f"urn:cgdl:1.0:{tn1}Shape")
                g.add((shape_ref, RDF.type, sh.NodeShape))
                g.add((shape_ref, sh.targetClass, URIRef("urn:cgdl:1.0:" + tn1)))
            except KeyError:
                print('# There is no information about target node')

            for predicate in shape.get('predicates', []):
                if 'datatype' in predicate:
                    prop = BNode()
                    try:
                        pn1 = predicate['name']
                        g.add((shape_ref, sh.property, prop))
                        g.add((prop, sh.path, URIRef("urn:cgdl:1.0:" + pn1)))
                        pdt1 = set_datatype(predicate.get('datatype'))
                        if pdt1:
                            g.add((prop, sh.datatype, pdt1))
                    except KeyError as e:
                        print(f'# There is no information about property: {e}')
                else:
                    prop2 = BNode()
                    try:
                        pp1 = predicate['name']
                        g.add((shape_ref, sh.property, prop2))
                        g.add((prop2, sh.path, URIRef("urn:cgdl:1.0:" + pp1)))
                        pnd1 = predicate['node']
                        g.add((prop2, sh.node, URIRef("urn:cgdl:1.0:" + pnd1)))
                    except KeyError as e:
                        print(f'# There is no information about edge: {e}')

        print(g.serialize(format='turtle'))
    if args.shex:
        print('PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>')
        for shape in data.get('shapes', []):
            print(f"<urn:cgdl:1.0:{shape['target']}> {{")
            for pred in shape.get('predicates', []):
                if 'datatype' in pred:
                    print(f"  {pred['name']} xsd:{pred['datatype']} ;")
                elif 'node' in pred:
                    print(f"  {pred['name']} @<urn:cgdl:1.0:{pred['node']}> ;")
            print("}")
    if args.pgschema:
        for shape in data.get('shapes', []):
            target_node = shape.get('target')
            if target_node:
                node_properties = []
                for predicate in shape.get('predicates', []):
                    property_name = predicate.get('name')
                    if 'datatype' in predicate:
                        property_datatype = predicate.get('datatype')
                        node_properties.append(f"{property_name} {property_datatype.upper()}")
                if node_properties:
                    formatted_properties = ", ".join(node_properties)
                    print(f"CREATE NODE TYPE ({target_node}Type: {target_node} {{{formatted_properties}}})")
                else:
                    print(f"CREATE NODE TYPE ({target_node}Type: {target_node})")

        for shape in data.get('shapes', []):
            source_node = shape.get('target')
            if source_node:
                for predicate in shape.get('predicates', []):
                    if 'node' in predicate:
                        edge_name = predicate.get('name')
                        target_node = predicate.get('node')
                        edge_type_name = edge_name.replace("_", "") + "Type"
                        print(
                            f"CREATE EDGE TYPE (:{source_node}Type)-[{edge_type_name}: {edge_name}]->(:{target_node}Type)")

else:
    parser.print_help()
