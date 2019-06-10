from testcase import WhyisTestCase
from base64 import b64encode
from rdflib import *
import json
import requests
import tempfile
from flask_testing import TestCase
from StringIO import StringIO
import nanopub
import autonomic
file_under_test = "L102_S3_Hu_2007"
files = {
    "template" : '''<replace> a <http://nanomine.org/ns/NanomineXMLFile>,
        <http://schema.org/DataDownload>,
        <https://www.iana.org/assignments/media-types/text/xml> ;
    <http://vocab.rpi.edu/whyis/hasContent> "data:text/xml;charset=UTF-8;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz4KPFBvbHltZXJOYW5vY29tcG9zaXRlPjxJRD5MMTAyX1MzX0h1XzIwMDc8L0lEPjxDb250cm9sX0lEPkwxMDJfUzFfSHVfMjAwNzwvQ29udHJvbF9JRD48REFUQV9TT1VSQ0U+PENpdGF0aW9uPjxDb21tb25GaWVsZHM+PENpdGF0aW9uVHlwZT5yZXNlYXJjaCBhcnRpY2xlPC9DaXRhdGlvblR5cGU+PFB1YmxpY2F0aW9uPkpvdXJuYWwgb2YgdGhlIEV1cm9wZWFuIENlcmFtaWMgU29jaWV0eTwvUHVibGljYXRpb24+PFRpdGxlPkRpZWxlY3RyaWMgcHJvcGVydGllcyBvZiBCU1QvcG9seW1lciBjb21wb3NpdGU8L1RpdGxlPjxBdXRob3I+SHUsIFRhbzwvQXV0aG9yPjxBdXRob3I+SnV1dGksIEphcmk8L0F1dGhvcj48QXV0aG9yPkphbnR1bmVuLCBIZWxpPC9BdXRob3I+PEF1dGhvcj5WaWxrbWFuLCBUYWlzdG88L0F1dGhvcj48S2V5d29yZD5Db21wb3NpdGVzPC9LZXl3b3JkPjxLZXl3b3JkPkRpZWxlY3RyaWMgcHJvcGVydGllczwvS2V5d29yZD48S2V5d29yZD5NaWNyb3N0cnVjdHVyZS1maW5hbDwvS2V5d29yZD48S2V5d29yZD5CU1QtQ09DPC9LZXl3b3JkPjxQdWJsaXNoZXI+RWxzZXZpZXI8L1B1Ymxpc2hlcj48UHVibGljYXRpb25ZZWFyPjIwMDc8L1B1YmxpY2F0aW9uWWVhcj48RE9JPjEwLjEwMTYvai5qZXVyY2VyYW1zb2MuMjAwNy4wMi4wODI8L0RPST48Vm9sdW1lPjI3PC9Wb2x1bWU+PFVSTD5odHRwczovL3d3dy5zY2llbmNlZGlyZWN0LmNvbS9zY2llbmNlL2FydGljbGUvcGlpL1MwOTU1MjIxOTA3MDAxMjUyP3ZpYSUzRGlodWI8L1VSTD48TGFuZ3VhZ2U+RW5nbGlzaDwvTGFuZ3VhZ2U+PExvY2F0aW9uPk1pY3JvZWxlY3Ryb25pY3MgYW5kIE1hdGVyaWFscyBQaHlzaWNzIExhYm9yYXRvcmllcywgRU1QQVJUIFJlc2VhcmNoIEdyb3VwIG9mIEluZm90ZWNoIE91bHUsIFAuTy4gQm94IDQ1MDAsIEZJTi05MDAxNCBVbml2ZXJzaXR5IG9mIE91bHUsIEZpbmxhbmQ8L0xvY2F0aW9uPjxEYXRlT2ZDaXRhdGlvbj4yMDE1LTA3LTI0PC9EYXRlT2ZDaXRhdGlvbj48L0NvbW1vbkZpZWxkcz48Q2l0YXRpb25UeXBlPjxKb3VybmFsPjxJU1NOPjA5NTUtMjIxOTwvSVNTTj48SXNzdWU+MTMtMTU8L0lzc3VlPjwvSm91cm5hbD48L0NpdGF0aW9uVHlwZT48L0NpdGF0aW9uPjwvREFUQV9TT1VSQ0U+PE1BVEVSSUFMUz48TWF0cml4PjxNYXRyaXhDb21wb25lbnQ+PENoZW1pY2FsTmFtZT5jeWNsbyBvbGVmaW4gY29wb2x5bWVyPC9DaGVtaWNhbE5hbWU+PEFiYnJldmlhdGlvbj5DT0M8L0FiYnJldmlhdGlvbj48UG9seW1lclR5cGU+Y29wb2x5bWVyPC9Qb2x5bWVyVHlwZT48TWFudWZhY3R1cmVyT3JTb3VyY2VOYW1lPlRpY29uYSBHbWJILCBHZXJtYW55PC9NYW51ZmFjdHVyZXJPclNvdXJjZU5hbWU+PFRyYWRlTmFtZT5Ub3BhcyA4MDA3Uy0wNDwvVHJhZGVOYW1lPjxEZW5zaXR5Pjx2YWx1ZT4xLjAyPC92YWx1ZT48dW5pdD5nL2NtXjM8L3VuaXQ+PC9EZW5zaXR5PjwvTWF0cml4Q29tcG9uZW50PjwvTWF0cml4PjxGaWxsZXI+PEZpbGxlckNvbXBvbmVudD48Q2hlbWljYWxOYW1lPmJhcml1bSBzdHJvbnRpdW0gdGl0YW5hdGU8L0NoZW1pY2FsTmFtZT48QWJicmV2aWF0aW9uPkJTVDwvQWJicmV2aWF0aW9uPjxNYW51ZmFjdHVyZXJPclNvdXJjZU5hbWU+U2lnbWHigJNBbGRyaWNoIENoZW1pZSBHbWJILCBHZXJtYW55PC9NYW51ZmFjdHVyZXJPclNvdXJjZU5hbWU+PERlbnNpdHk+PHZhbHVlPjQuOTwvdmFsdWU+PHVuaXQ+Zy9jbV4zPC91bml0PjwvRGVuc2l0eT48U3BoZXJpY2FsUGFydGljbGVEaWFtZXRlcj48ZGVzY3JpcHRpb24+bGVzcyB0aGFuIDIwMCBubTwvZGVzY3JpcHRpb24+PHZhbHVlPjIwMDwvdmFsdWU+PHVuaXQ+bm08L3VuaXQ+PC9TcGhlcmljYWxQYXJ0aWNsZURpYW1ldGVyPjwvRmlsbGVyQ29tcG9uZW50PjxGaWxsZXJDb21wb3NpdGlvbj48RnJhY3Rpb24+PHZvbHVtZT4wLjA1PC92b2x1bWU+PC9GcmFjdGlvbj48L0ZpbGxlckNvbXBvc2l0aW9uPjxEZXNjcmlwdGlvbj5CYTAuNVNyMC41VGlPMzwvRGVzY3JpcHRpb24+PC9GaWxsZXI+PC9NQVRFUklBTFM+PFBST0NFU1NJTkc+PE1lbHRNaXhpbmc+PENob29zZVBhcmFtZXRlcj48TWl4aW5nPjxNaXhlcj5Ub3JxdWUgUmhlb21ldGVyPC9NaXhlcj48UlBNPjxkZXNjcmlwdGlvbj4zMi02NCBycG08L2Rlc2NyaXB0aW9uPjx2YWx1ZT40ODwvdmFsdWU+PHVuaXQ+cnBtPC91bml0PjwvUlBNPjxUaW1lPjx2YWx1ZT4xNTwvdmFsdWU+PHVuaXQ+bWludXRlczwvdW5pdD48dW5jZXJ0YWludHk+PHR5cGU+YWJzb2x1dGU8L3R5cGU+PHZhbHVlPjU8L3ZhbHVlPjwvdW5jZXJ0YWludHk+PC9UaW1lPjxUZW1wZXJhdHVyZT48dmFsdWU+MjMwPC92YWx1ZT48dW5pdD5DZWxzaXVzPC91bml0PjwvVGVtcGVyYXR1cmU+PC9NaXhpbmc+PC9DaG9vc2VQYXJhbWV0ZXI+PENob29zZVBhcmFtZXRlcj48TW9sZGluZz48TW9sZGluZ01vZGU+aG90LXByZXNzaW5nPC9Nb2xkaW5nTW9kZT48TW9sZGluZ0luZm8+PFRlbXBlcmF0dXJlPjx2YWx1ZT4yMDA8L3ZhbHVlPjx1bml0PkNlbHNpdXM8L3VuaXQ+PC9UZW1wZXJhdHVyZT48L01vbGRpbmdJbmZvPjwvTW9sZGluZz48L0Nob29zZVBhcmFtZXRlcj48L01lbHRNaXhpbmc+PC9QUk9DRVNTSU5HPjxDSEFSQUNURVJJWkFUSU9OPjxTY2FubmluZ19FbGVjdHJvbl9NaWNyb3Njb3B5PjxFcXVpcG1lbnRVc2VkPkpFT0wgSlNNLTY0MDA8L0VxdWlwbWVudFVzZWQ+PC9TY2FubmluZ19FbGVjdHJvbl9NaWNyb3Njb3B5PjxEaWVsZWN0cmljX2FuZF9JbXBlZGFuY2VfU3BlY3Ryb3Njb3B5X0FuYWx5c2lzPjxFcXVpcG1lbnQ+QWdpbGVudCBFNDk5MUE8L0VxdWlwbWVudD48L0RpZWxlY3RyaWNfYW5kX0ltcGVkYW5jZV9TcGVjdHJvc2NvcHlfQW5hbHlzaXM+PFhSYXlfRGlmZnJhY3Rpb25fYW5kX1NjYXR0ZXJpbmc+PEVxdWlwbWVudD5TaWVtZW5zIEQ1MDAwPC9FcXVpcG1lbnQ+PC9YUmF5X0RpZmZyYWN0aW9uX2FuZF9TY2F0dGVyaW5nPjwvQ0hBUkFDVEVSSVpBVElPTj48UFJPUEVSVElFUz48RWxlY3RyaWNhbD48QUNfRGllbGVjdHJpY0Rpc3BlcnNpb24+PERpZWxlY3RyaWNfUmVhbF9QZXJtaXR0aXZpdHk+PGRlc2NyaXB0aW9uPlJlbGF0aXZlIHBlcm1pdHRpdml0eSBhdCAxR0h6PC9kZXNjcmlwdGlvbj48dmFsdWU+Mi45PC92YWx1ZT48L0RpZWxlY3RyaWNfUmVhbF9QZXJtaXR0aXZpdHk+PERpZWxlY3RyaWNfTG9zc19UYW5nZW50PjxkZXNjcmlwdGlvbj5Mb3NzIFRhbmdlbnQgYXQgMSBHSHo8L2Rlc2NyaXB0aW9uPjx2YWx1ZT41ZS0wNTwvdmFsdWU+PC9EaWVsZWN0cmljX0xvc3NfVGFuZ2VudD48L0FDX0RpZWxlY3RyaWNEaXNwZXJzaW9uPjwvRWxlY3RyaWNhbD48L1BST1BFUlRJRVM+PC9Qb2x5bWVyTmFub2NvbXBvc2l0ZT4=" .'''
}
class XMLIngestTest(WhyisTestCase):
    first_run = bool()
    @classmethod
    def setUpClass(cls):
        print("Setting Up Class")
        XMLIngestTest.first_run = True

    def setUp(self):
        # Initialization
        if not XMLIngestTest.first_run:
            return
        XMLIngestTest.first_run = False
        self.login(*self.create_user("user@example.com","password"))
        
        r = requests.get('http://nanomine.org/nmr/xml/' + file_under_test + '.xml')
        j = json.loads(r.text)
        xml_str = j["data"][0]["xml_str"]
        temp = tempfile.NamedTemporaryFile()
        temp.write(xml_str)
        temp.seek(0)
        
        files[file_under_test] = files["template"].replace("replace", temp.name)
        upload = files[file_under_test]

        
        response = self.client.post("/pub", data=upload, content_type="text/turtle",follow_redirects=True)
        self.assertEquals(response.status,'201 CREATED')


        response = self.client.post("/pub", data=open('/apps/nanomine-graph/setl/xml_ingest.setl.ttl','rb').read(),
                                    content_type="text/turtle", follow_redirects=True)
        self.assertEquals(response.status,'201 CREATED')
        

        setlmaker = autonomic.SETLMaker()
        results = self.run_agent(setlmaker)

        # confirm this is creating a SETL script for the XML file.
        self.assertTrue(len(results) > 0)

        setlr = autonomic.SETLr()

        print len(self.app.db)
        for setlr_np in results:
            setlr_results = self.run_agent(setlr, nanopublication=setlr_np)

        temp.close()

        
    def test_nanocomposites(self):
        # Testing
        # Ensure there is a nanocomposite in the graph
        nanocomposites = list(self.app.db.subjects(RDF.type,URIRef("http://nanomine.org/ns/PolymerNanocomposite")))
        print nanocomposites, len(self.app.db)
        self.assertEquals(len(nanocomposites),1)
        print("Correct Number of Nanocomposites")
	
    def test_authors(self):
        # Ensure that the proper number of authors are in the graph
        print("\n\nauthors")
        authors = self.app.db.query(
        """SELECT ?name 
        WHERE {
            <http://dx.doi.org/10.1016/j.jeurceramsoc.2007.02.082> <http://purl.org/dc/terms/creator> ?author .
            ?author <http://xmlns.com/foaf/0.1/name> ?name .
        }
        """
        )
        # for author in authors:
            # print(author)
        self.assertEquals(len(authors), 4)
        print("Correct Number of Authors")
        authors = [str(author[0]) for author in authors]
        expected_authors = ["Hu, Tao", 
                            "Juuti, Jari",
                            "Vilkman, Taisto",
                            "Jantunen, Heli"]
        self.assertItemsEqual(expected_authors, authors)
        print("Expected Authors Found")

    def test_language(self):
        # Ensure the paper is marked as being in English
        languages = list(self.app.db.objects(URIRef("http://dx.doi.org/10.1016/j.jeurceramsoc.2007.02.082"), URIRef("http://purl.org/dc/terms/language")))
        print("\n\nLanguage")
        processed_langs = [language.n3() for language in languages]
        # print(processed_langs)
        self.assertTrue(u'<http://nanomine.org/language/english>' in processed_langs)
        print("Correct Language")

    def test_keywords(self):
        # Check how many keywords exist
        print("\n\nKeywords")
        keywords_lst = list(self.app.db.objects(URIRef("http://dx.doi.org/10.1016/j.jeurceramsoc.2007.02.082"), URIRef("http://www.w3.org/ns/dcat#keyword")))
        keywords = [str(keyword) for keyword in keywords_lst]
        # print(keywords)
        self.assertEquals(len(keywords), 4)
        print("Correct Number of Keywords")
        expected_keywords = ["Composites",
                             "Dielectric Properties",
                             "Microstructure-Final",
                             "Bst-Coc"]
        self.assertItemsEqual(expected_keywords, keywords)
        print("Expected Keywords Found")
                             
    def test_devices(self):
        # Check if all used devices are showing up
        print("\n\nDevices")
        devices_lst = list(self.app.db.subjects(URIRef("http://www.w3.org/2000/01/rdf-schema#subClassOf"), URIRef("http://semanticscience.org/resource/Device")))
        devices_lst = [str(device) for device in devices_lst]
        # self.assertEquals(len(devices), 3)
        print("Correct number of Devices")
        expected_devices = ["http://nanomine.org/ns/jeol-jsm-6400",
                            "http://nanomine.org/ns/agilent-e4991a",
                            "http://nanomine.org/ns/siemens-d5000"]
        self.assertItemsEqual(expected_devices, devices_lst)
        print("Expected Devices Found")
        
    # def test_properties(self):
    #     # Check how many properties are shown
    #      print("\n\nProperties of Cyclo Olefin Copolymer")
    #      properties = list(self.app.db.predicate_objects(URIRef("http://nanomine.org/compound/CycloOlefinCopolymer")))
    #      for p, o in properties:
    #          print(p.n3(), o.n3())
    #      print("Correct number of properties")

    def test_values(self):
        # Check how many values are given
        print("\n\nMeasurement Values")
        measurement_lst = list(self.app.db.subject_objects(URIRef("http://semanticscience.org/resource/hasValue")))
        # for source, measurement in measurement_lst:
            # print(source.n3(), measurement.n3())
        self.assertEqual(len(measurement_lst), 10)

    def test_units(self):
        # Check if enough units are present
        print("\n\nChecking if temperature and density have units")
        unit_pass = self.app.db.query(
        """
        SELECT ?value ?what 
        WHERE { 
            <http://nanomine.org/sample/l102-s3-hu-2007_filler_0> <http://semanticscience.org/resource/hasAttribute> ?attr . 
            ?attr <http://semanticscience.org/resource/hasValue> ?value .
            ?attr a ?what .
        }
        """)

        # for attribute in unit_pass:
            # print(attribute)
        self.assertEqual(len(unit_pass), 7)



        #  print("Printing SPO Triples")
        #  for s, p, o in self.app.db.triples((None, None, None)):
        #      print("<", str(s.n3()), str(p.n3()), str(o.n3()), "> .")
        



