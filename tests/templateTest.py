import unittest
from waffleweb.request import Request
from waffleweb import WaffleProject
from waffleweb.template import AppNotFoundError, ViewNotFoundError, getRelativeUrl, renderErrorPage, renderTemplate

class RenderTemplateTest(unittest.TestCase):
    def test_renderWithoutContext(self):
        res = renderTemplate('testWithoutContext.html')
        self.assertEqual('<h1>Testing Testing 1 2 3</h1>', res)

    def test_renderWithContext(self):
        res = renderTemplate('testWithContext.html', {'testVar': 'Testing 1 2 3'})
        self.assertEqual('<h1>Testing Testing 1 2 3</h1>', res)

class RenderErrorPageTest(unittest.TestCase):
    def test_onlyMainMessage(self):
        page = renderErrorPage('Test')
        self.maxDiff = None
        self.assertEqual(page, '''
        <!DOCTYPE html>
        <html>
            <head>
                <title>Test</title>
            </head>
            
            <body style="font-family: Arial, Helvetica, sans-serif; margin:0px; padding:0;">
                <h1 style="background-color: #f6c486; display: block; margin:0px; padding:15px;">Test</h1>
                
                
            </body>
        </html>
    ''')

    def test_MainAndSub(self):
        page = renderErrorPage('test', 'testSub')
        self.maxDiff = None
        self.assertEqual(page, '''
        <!DOCTYPE html>
        <html>
            <head>
                <title>test</title>
            </head>
            
            <body style="font-family: Arial, Helvetica, sans-serif; margin:0px; padding:0;">
                <h1 style="background-color: #f6c486; display: block; margin:0px; padding:15px;">test</h1>
                <h2 style="color: #7a7a7a; display: block; margin:15px; padding:0px;">testSub</h2>
                
            </body>
        </html>
    ''')
    
    def test_MainAndTrace(self):
        page = renderErrorPage('test', traceback='testTrace')
        self.maxDiff = None
        self.assertEqual(page, '''
        <!DOCTYPE html>
        <html>
            <head>
                <title>test</title>
            </head>
            
            <body style="font-family: Arial, Helvetica, sans-serif; margin:0px; padding:0;">
                <h1 style="background-color: #f6c486; display: block; margin:0px; padding:15px;">test</h1>
                
                
                <fieldset style="display: block; margin:15px; padding:0px;">
                    <legend style="margin-left:15px; margin-top:0px margin-bottom:0px padding:0px;"><h2 style="margin:0; padding:0px;">Traceback</h2></legend>
                    <h3 style="margin-left:15px; margin-top:5px; margin-bottom:10px; padding:0px;">testTrace</h3>
                </fieldset>
                
            </body>
        </html>
    ''')
    
class GetRelativeUrlTest(unittest.TestCase):
    def test_basicTest(self):
        url = getRelativeUrl('test:BasicTest')
        self.assertEqual(url, 'BasicTest/')
    
    def test_noKwargs(self):
        with self.assertRaises(KeyError):
            getRelativeUrl('test:WithArgsTest')
    
    def test_kwargsRight(self):
        url = getRelativeUrl('test:WithArgsTest', testArg1='test1', testArg2='test2')
        self.assertEqual(url, '/WithArgsTest/test1/test/test2/')
    
    def test_notEnoughtKwargs(self):
        with self.assertRaises(KeyError):
            getRelativeUrl('test:WithArgsTest', testArg1='test1')
    
    def test_appNotFound(self):
        with self.assertRaises(AppNotFoundError):
            getRelativeUrl('Existnt:bolony')
    
    def test_appFoundViewNotFound(self):
        with self.assertRaises(ViewNotFoundError):
            getRelativeUrl('test:bolony')
            
    def test_noViewInViewStr(self):
        with self.assertRaises(ValueError):
            getRelativeUrl('test')
            
    def test_extraPartInViewStr(self):
        with self.assertRaises(ValueError):
            getRelativeUrl('test:bolony:foo')
            
    def test_inTemplate(self):
        render = renderTemplate('inTemplateTest.html')
        self.assertEqual(render, 'BasicTest/')
    