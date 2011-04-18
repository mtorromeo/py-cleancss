# -*- coding: utf-8 -*-
import unittest, cleancss
from textwrap import dedent
from StringIO import StringIO

class TestConvert(unittest.TestCase):
    def test_01_convert(self):
        ccss = StringIO()
        ccss.write(dedent('''
            // Comment
            #header, #footer:
                margin: 0
                padding: 0
                font->
                    family: Verdana, sans-serif
                    size: .9em // Comment

                li:
                    padding: 0.4em
                    margin: 0.8em 0 0.8em

                    a:
                        background-image: url('abc.png')
                        &:hover:
                            background-color: red

                    h3:
                        background-image: url('http://test.com/abc.png')
                        font-size: 1.2em
                    p, div.p:
                        padding: 0.3em
                    p.meta:
                        text-align: right
                        color: #ddd
        '''))

        expected_result = dedent('''
            #header,
            #footer {
                margin: 0;
                padding: 0;
                font-family: Verdana, sans-serif;
                font-size: .9em;
            }
            #header li,
            #footer li {
                padding: 0.4em;
                margin: 0.8em 0 0.8em;
            }
            #header li a,
            #footer li a {
                background-image: url('abc.png');
            }
            #header li a:hover,
            #footer li a:hover {
                background-color: red;
            }
            #header li h3,
            #footer li h3 {
                background-image: url('http://test.com/abc.png');
                font-size: 1.2em;
            }
            #header li p,
            #header li div.p,
            #footer li p,
            #footer li div.p {
                padding: 0.3em;
            }
            #header li p.meta,
            #footer li p.meta {
                text-align: right;
                color: #ddd;
            }
        ''').lstrip().replace("    ", "\t")

        ccss.seek(0)
        self.assertEqual(cleancss.convert(ccss), expected_result)

    def test_02_callback(self):
        def callback(prop, value):
            return [
                (prop + "-variant", value)
            ]


        ccss = StringIO()
        ccss.write(dedent('''
            #header, #footer:
                margin: 0
                padding: 0
        '''))

        expected_result = dedent('''
            #header,
            #footer {
                margin-variant: 0;
                padding-variant: 0;
            }
        ''').lstrip().replace("    ", "\t")


        c = cleancss.Parser(ccss)
        c.registerPropertyCallback( callback )


        ccss.seek(0)
        self.assertEqual(c.toCss(), expected_result)
        ccss.seek(0)
        self.assertEqual(cleancss.convert(ccss, callback), expected_result)

    def test_03_variants_callback(self):
        ccss = StringIO()
        ccss.write(dedent('''
            #header, #footer:
                border-radius: 5px
                padding: 0
                text-overflow: ellipsis
                display: box
                border-top-left-radius: 5px
                -ms-filter: "test"
                opacity: 0.5
                opacity: notvalid
                background: linear-gradient(top left, #000 0%, #FFF 100%)
        '''))

        expected_result = dedent('''
            #header,
            #footer {
                border-radius: 5px;
                -o-border-radius: 5px;
                -moz-border-radius: 5px;
                -webkit-border-radius: 5px;
                padding: 0;
                text-overflow: ellipsis;
                -o-text-overflow: ellipsis;
                display: box;
                display: -moz-box;
                display: -webkit-box;
                border-top-left-radius: 5px;
                -moz-border-radius-topleft: 5px;
                -webkit-border-top-left-radius: 5px;
                -ms-filter: "test";
                filter: test;
                opacity: 0.5;
                filter: alpha(opacity=50);
                opacity: notvalid;
                background: linear-gradient(top left, #000 0%, #FFF 100%);
                background: -o-linear-gradient(top left, #000 0%, #FFF 100%);
                background: -moz-linear-gradient(top left, #000 0%, #FFF 100%);
                background: -webkit-linear-gradient(top left, #000 0%, #FFF 100%);
            }
        ''').lstrip().replace("    ", "\t")


        ccss.seek(0)
        self.assertEqual(cleancss.convert(ccss, cleancss.callbacks.browser_variants), expected_result)

