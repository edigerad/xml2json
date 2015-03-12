import unittest
import xml2json
import optparse
import json
import os
#from xml.etree.ElementTree import ElementTree
xmlstring = ""
options = None

class SimplisticTest(unittest.TestCase):

    def setUp(self):
        global xmlstring, options
        filename = os.path.join(os.path.dirname(__file__), 'xml_ns2.xml')
        xmlstring = open(filename).read()
        options = optparse.Values({"pretty": False})

    def test_default_namespace_attribute(self):
        strip_ns = 0
        json_string = xml2json.xml2json(xmlstring,options,strip_ns)
        # check string
        self.assertTrue(json_string.find("{http://www.w3.org/TR/html4/}table") != -1)
        self.assertTrue(json_string.find("{http://www.w3.org/TR/html4/}tr") != -1)
        self.assertTrue(json_string.find("@class") != -1)

        # check the simple name is not exist
        json_data = json.loads(json_string)
        self.assertFalse("table" in json_data["root"])

    def test_strip_namespace(self):
        strip_ns = 1
        json_string = xml2json.xml2json(xmlstring,options,strip_ns)
        json_data = json.loads(json_string)

        # namespace is stripped
        self.assertFalse(json_string.find("{http://www.w3.org/TR/html4/}table") != -1)

        # TODO , attribute shall be kept
        #self.assertTrue(json_string.find("@class") != -1)

        #print json_data["root"]["table"]
        #print json_data["root"]["table"][0]["tr"]
        self.assertTrue("table" in json_data["root"])
        self.assertEqual(json_data["root"]["table"][0]["tr"]["td"] , ["Apples", "Bananas"])
        self.assertEqual(json_data["root"]["table"][0]["tr"]["td"] , ["Apples", "Bananas"])

    def test_json2xml(self):
        json_data = '{"e": { "@name": "value", "#text": "text" }}'
        xml_data = '<e name="value">text</e>'
        res = xml2json.json2xml(json_data)
        self.assertEqual(res, xml_data)

        json_data = '{"e": { "a": "text", "b": "text" }}'
        xml_data = '<e><a>text</a><b>text</b></e>'
        res = xml2json.json2xml(json_data)
        self.assertEqual(res, xml_data)

        json_data = '{"e": { "a": ["text", "text"] }}'
        xml_data = '<e><a>text</a><a>text</a></e>'
        res = xml2json.json2xml(json_data)
        self.assertEqual(res, xml_data)

        json_data = '{"e": { "#text": "text", "a": "text" }}'
        xml_data = '<e>text<a>text</a></e>'
        res = xml2json.json2xml(json_data)
        self.assertEqual(res, xml_data)
      
        test = '{"dict":{"first":"1","second":"2"}}'
        result = xml2json.json2xml(test)
        xml = "<dict><second>2</second><first>1</first></dict>"
        self.assertEqual(result , xml)

        json_data = '{"e": { "@name": "value" }}'
        xml_data = '<e name="value" />'
        res = xml2json.json2xml(json_data)
        self.assertEqual(res, xml_data)
        
        json_data = '{"e": null}'
        xml_data = '<e />'
        res = xml2json.json2xml(json_data)
        self.assertEqual(res, xml_data)

        json_data = '{"e": "text"}'
        xml_data = '<e>text</e>'
        res = xml2json.json2xml(json_data)
        self.assertEqual(res, xml_data)

       



    def test_xml2json(self):
        json = '{"list":{"@":"1","#text":"1","#tail":"2","asd":["sadf","qweqw"],"a":"1"}}'
        result = xml2json.json2xml(json)
        xml1 = '<list ="1">1<a>1</a><asd>sadf</asd><asd>qweqw</asd></list>2'
        self.assertEqual(result ,xml1)

    def test_strip_tag(self):
        test = '{"list":{"@":"1","#text":"1","#tail":"2","asd":["sadf","qweqw"],"a":"1"}}'
        result = xml2json.strip_tag(test)
        self.assertEqual(result, '')

    def test_json2elem(self):
        test ='{"list":{"@":"1","#text":"1","#tail":"2","asd":["sadf","qweqw"],"a":"1"}}'
        result = xml2json.json2elem(test,options)
        self.assertEqual(test == result)


 
 
    def test_main(self):
        xml2json.main()        
if __name__ == '__main__':
    unittest.main()
