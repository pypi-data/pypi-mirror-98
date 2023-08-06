"""
This module make writing Burp modules under Burp easier
Version: 1.0

Author: Erlend Leiknes
Based on Extender API documentation: https://portswigger.net/burp/extender/api/
"""

try:
    from typing import List, Union, Optional, Dict
except ImportError:
    pass


class IBurpCollaboratorClientContext(object):
    """
    This interface represents an instance of a Burp Collaborator client context, which can be used to generate Burp
    Collaborator payloads and poll the Collaborator server for any network interactions that result from using those
    payloads. Extensions can obtain new instances of this class by calling
    IBurpExtenderCallbacks.createBurpCollaboratorClientContext(). Note that each Burp Collaborator client context is
    tied to the Collaborator server configuration that was in place at the time the context was created.
    """

    def fetchAllCollaboratorInteractions(self):
        # type: () -> List[IBurpCollaboratorInteraction]
        """
        This method is used to retrieve all interactions received by the Collaborator server resulting from payloads
        that were generated for this context.

        :raises java.net.IllegalStateException: if Burp Collaborator is disabled
        :return: The Collaborator interactions that have occurred resulting from payloads that were generated for
        this context.
        """
        pass

    def fetchAllInfiltratorInteractions(self):
        # type: () -> List[IBurpCollaboratorInteraction]
        """
        This method is used to retrieve all interactions made by Burp Infiltrator instrumentation resulting from
        payloads that were generated for this context.

        :raises java.net.IllegalStateException: if Burp Collaborator is disabled
        :return: The interactions triggered by the Burp Infiltrator instrumentation that have occurred resulting from
        payloads that were generated for this context.
        """
        pass

    def fetchCollaboratorInteractionsFor(self, payload):
        # type: (str) -> List[IBurpCollaboratorInteraction]
        """
        This method is used to retrieve interactions received by the Collaborator server resulting from a single
        payload that was generated for this context.

        :raises java.net.IllegalStateException: if Burp Collaborator is disabled
        :param payload: The payload for which interactions will be retrieved.
        :return: The Collaborator interactions that have occurred resulting from the given payload.
        """
        pass

    def fetchInfiltratorInteractionsFor(self, payload):
        # type: (str) -> List[IBurpCollaboratorInteraction]
        """
        This method is used to retrieve interactions made by Burp Infiltrator instrumentation resulting from a single
        payload that was generated for this context.

        :param payload: The payload for which interactions will be retrieved.
        :raises java.net.IllegalStateException: if Burp Collaborator is disabled
        :return: The interactions triggered by
        the Burp Infiltrator instrumentation that have occurred resulting from the given payload.
        """
        pass

    def generatePayload(self, includeCollaboratorServerLocation):
        # type: (bool) -> str
        """
        This method is used to generate new Burp Collaborator payloads.

        :raises java.net.IllegalStateException: if Burp Collaborator is disabled
        :param includeCollaboratorServerLocation:   Specifies whether to include the Collaborator server location in
                                                    the generated payload.
        :return: The payload that was generated.
        """
        pass

    def getCollaboratorServerLocation(self):
        # type: () -> str
        """
        This method is used to retrieve the network location of the Collaborator server.

        :raises java.net.IllegalStateException: if Burp Collaborator is disabled
        :return: The hostname or IP address of the Collaborator server.
        """
        pass


class IBurpCollaboratorInteraction(object):
    """
    This interface represents a network interaction that occurred with the Burp Collaborator server.
    """

    def getProperties(self):
        # type: () -> Dict[str]
        """
        This method is used to retrieve a map containing all properties of the interaction.

        :return: A map containing all properties of the interaction.

        TODO: implement java.net.Map prototype
        """
        pass

    def getProperty(self, name):
        # type: (str) -> str
        """
        This method is used to retrieve a property of the interaction. Properties of all interactions are:
        interaction_id, type, client_ip, and time_stamp. Properties of DNS interactions are: query_type and
        raw_query. The raw_query value is Base64-encoded. Properties of HTTP interactions are: protocol, request,
        and response. The request and response values are Base64-encoded.

        :param name: The name of the property to retrieve.
        :return: A string representing the property value, or null if not present.
        """
        pass


class IBurpExtender(object):
    """
    All extensions must implement this interface. Implementations must be called BurpExtender, in the package burp,
    must be declared public, and must provide a default (public, no-argument) constructor.
    """

    def registerExtenderCallbacks(self, callbacks):
        # type: (IBurpExtenderCallbacks) -> ()
        """
        This method is invoked when the extension is loaded.
        """
        pass


class IBurpExtenderCallbacks(object):
    """
    This interface is used by Burp Suite to pass to extensions a set of callback methods that can be used by
    extensions to perform various actions within Burp. When an extension is loaded, Burp invokes its
    registerExtenderCallbacks() method and passes an instance of the IBurpExtenderCallbacks interface. The extension
    may then invoke the methods of this interface as required in order to extend Burp's functionality.
    """
    TOOL_COMPARER = 0
    TOOL_DECODER = 0
    TOOL_EXTENDER = 0
    TOOL_INTRUDER = 0
    TOOL_PROXY = 0
    TOOL_REPEATER = 0
    TOOL_SCANNER = 0
    TOOL_SEQUENCER = 0
    TOOL_SPIDER = 0
    TOOL_SUITE = 0
    TOOL_TARGET = 0

    def setExtensionName(self, name):
        # type: (str) -> ()
        """
        This method is used to set the display name for the current extension, which will be displayed within the
        user interface for the Extender tool.

        :param name: The extension name.
        :return: None
        """

    def getHelpers(self):
        # type: () -> IExtensionHelpers
        """
        This method is used to obtain an IExtensionHelpers object, which can be used by the extension to perform
        numerous useful tasks.

        :return: An object containing numerous helper methods, for tasks such as building and analyzing HTTP requests.
        """

    def getStdout(self):
        # type: () -> java.io.OutputStream
        """
        This method is used to obtain the current extension's standard output stream. Extensions should write all
        output to this stream, allowing the Burp user to configure how that output is handled from within the UI.

        :return: The extension's standard output stream.
        """

    def getStderr(self):
        # type: () -> java.io.OutputStream
        """
        This method is used to obtain the current extension's standard error stream. Extensions should write all
        error messages to this stream, allowing the Burp user to configure how that output is handled from within the
        UI.

        :return: The extension's standard error stream.
        """

    def printOutput(self, output):
        # type: (str) -> ()
        """
        This method prints a line of output to the current extension's standard output stream.

        :param output: The message to print.
        :return: None
        """

    def printError(self, error):
        # type: (str) -> ()
        """
        This method prints a line of output to the current extension's standard error stream.

        :param error: The message to print.
        :return: None
        """

    def registerExtensionStateListener(self, listener):
        # type: (IExtensionStateListener) -> object
        """
        This method is used to register a listener which will be notified of changes to the extension's state.
        Note:
        Any extensions that start background threads or open system resources (such as files or database connections)
        should register a listener and terminate threads / close resources when the extension is unloaded.

        :param listener: An object created by the extension that implements the IExtensionStateListener interface.
        :return: None
        """

    def getExtensionStateListeners(self):
        # type: () -> List[IExtensionStateListener]
        """
        This method is used to retrieve the extension state listeners that are registered by the extension.

        :return: A list of extension state listeners that are currently registered by this extension.
        """

    def removeExtensionStateListener(self, listener):
        # type: (IExtensionStateListener) -> None
        """
        This method is used to remove an extension state listener that has been registered by the extension.

        :param listener: The extension state listener to be removed.
        :return: None
        """

    def registerHttpListener(self, listener):
        # type: (IHttpListener) -> None
        """
        This method is used to register a listener which will be notified of requests and responses made by any Burp
        tool. Extensions can perform custom analysis or modification of these messages by registering an HTTP listener.

        :param listener: An object created by the extension that implements the IHttpListener interface.
        :return: None
        """

    def getHttpListeners(self):
        # type: () -> List[IHttpListener]
        """
        This method is used to retrieve the HTTP listeners that are registered by the extension.

        :return: A list of HTTP listeners that are currently registered by this extension.
        """

    def removeHttpListener(self, listener):
        # type: (IHttpListener) -> None
        """
        This method is used to remove an HTTP listener that has been registered by the extension.

        :param listener: The HTTP listener to be removed.
        :return: None
        """

    def registerProxyListener(self, listener):
        # type: (IProxyListener) -> ()
        """
        This method is used to register a listener which will be notified of requests and responses being processed
        by the Proxy tool. Extensions can perform custom analysis or modification of these messages, and control
        in-UI message interception, by registering a proxy listener.

        :param listener: An object created by the extension that implements the IProxyListener interface.
        :return: None
        """

    def getProxyListeners(self):
        # type: () -> List[IProxyListener]
        """
        This method is used to retrieve the Proxy listeners that are registered by the extension.

        :return: A list of Proxy listeners that are currently registered by this extension.
        """

    def removeProxyListener(self, listener):
        # type: (IProxyListener) -> ()
        """
        This method is used to remove a Proxy listener that has been registered by the extension.

        :param listener: The Proxy listener to be removed.
        :return:
        """

    def registerScannerListener(self, listener):
        # type: (IScannerListener) -> ()
        """
        This method is used to register a listener which will be notified of new issues that are reported by the
        Scanner tool. Extensions can perform custom analysis or logging of Scanner issues by registering a Scanner
        listener.

        :param listener: An object created by the extension that implements the IScannerListener interface.
        :return: None
        """

    def getScannerListeners(self):
        # type: () -> List[IScannerListener]
        """
        This method is used to retrieve the Scanner listeners that are registered by the extension.

        :return: A list of Scanner listeners that are currently registered by this extension.
        """

    def removeScannerListener(self, listener):
        # type: (IScannerListener) -> ()
        """
        This method is used to remove a Scanner listener that has been registered by the extension

        :param listener: The Scanner listener to be removed.
        :return: None
        """

    def registerScopeChangeListener(self, listener):
        # type: (IScopeChangeListener) -> ()
        """
        This method is used to register a listener which will be notified of changes to Burp's suite-wide target scope.

        :param listener: An object created by the extension that implements the IScopeChangeListener interface.
        :return: None
        """

    def getScopeChangeListeners(self):
        # type: () -> List[IScopeChangeListener]
        """
        This method is used to retrieve the scope change listeners that are registered by the extension.

        :return: A list of scope change listeners that are currently registered by this extension.
         """

    def removeScopeChangeListener(self, listener):
        # type: (IScopeChangeListener) -> ()
        """
        This method is used to remove a scope change listener that has been registered by the extension.

        :param listener: The scope change listener to be removed.
        :return:
        """

    def registerContextMenuFactory(self, factory):
        # type: (IContextMenuFactory) -> ()
        """
        This method is used to register a factory for custom context menu items. When the user invokes a context menu
        anywhere within Burp, the factory will be passed details of the invocation event, and asked to provide any
        custom context menu items that should be shown.

        :param factory: An object created by the extension that implements the IContextMenuFactory interface.
        :return: None
        """

    def getContextMenuFactories(self):
        # type: () -> List[IContextMenuFactory]
        """
        This method is used to retrieve the context menu factories that are registered by the extension.

        :return: A list of context menu factories that are currently registered by this extension.
        """

    def removeContextMenuFactory(self, factory):
        # type: (IContextMenuFactory) -> ()
        """
        This method is used to remove a context menu factory that has been registered by the extension.

        :param factory: The context menu factory to be removed.
        :return: None
        """

    def registerMessageEditorTabFactory(self, factory):
        # type: (IMessageEditorTabFactory) -> ()
        """
        This method is used to register a factory for custom message editor tabs. For each message editor that
        already exists, or is subsequently created, within Burp, the factory will be asked to provide a new instance
        of an IMessageEditorTab object, which can provide custom rendering or editing of HTTP messages.

        :param factory: An object created by the extension that implements the IMessageEditorTabFactory interface.
        :return: None
        """

    def getMessageEditorTabFactories(self):
        # type: () -> List[IMessageEditorTabFactory]
        """
        This method is used to retrieve the message editor tab factories that are registered by the extension.

        :return: A list of message editor tab factories that are currently registered by this extension.
        """

    def removeMessageEditorTabFactory(self, factory):
        # type: (IMessageEditorTabFactory) -> ()
        """
        This method is used to remove a message editor tab factory that has been registered by the extension.

        :param factory: The message editor tab factory to be removed.
        :return: None
        """

    def registerScannerInsertionPointProvider(self, provider):
        # type: (IScannerInsertionPointProvider) -> ()
        """
        This method is used to register a provider of Scanner insertion points. For each base request that is
        actively scanned, Burp will ask the provider to provide any custom scanner insertion points that are
        appropriate for the request.

        :param provider: An object created by the extension that implements the IScannerInsertionPointProvider interface
        :return: None
        """

    def getScannerInsertionPointProviders(self):
        # type: () -> List[IScannerInsertionPointProvider]
        """
        This method is used to retrieve the Scanner insertion point providers that are registered by the extension.

        :return: A list of Scanner insertion point providers that are currently registered by this extension.
        """

    def removeScannerInsertionPointProvider(self, provider):
        # type: (IScannerInsertionPointProvider) -> ()
        """
        This method is used to remove a Scanner insertion point provider that has been registered by the extension.

        :param provider: The Scanner insertion point provider to be removed.
        :return: None
        """

    def registerScannerCheck(self, check):
        # type: (IScannerCheck) -> object
        """
        This method is used to register a custom Scanner check. When performing scanning, Burp will ask the check to
        perform active or passive scanning on the base request, and report any Scanner issues that are identified.

        :param check: An object created by the extension that implements the IScannerCheck interface.
        :return: None
        """

    def getScannerChecks(self):
        # type: () -> List[IScannerCheck]
        """
        This method is used to retrieve the Scanner checks that are registered by the extension.

        :return: A list of Scanner checks that are currently registered by this extension.
        """

    def removeScannerCheck(self, check):
        # type: (IScannerCheck) -> ()
        """
        This method is used to remove a Scanner check that has been registered by the extension.

        :param check: The Scanner check to be removed.
        :return: None
        """

    def registerIntruderPayloadGeneratorFactory(self, factory):
        # type: (IIntruderPayloadGeneratorFactory) -> ()
        """
        This method is used to register a factory for Intruder payloads. Each registered factory will be available
        within the Intruder UI for the user to select as the payload source for an attack. When this is selected,
        the factory will be asked to provide a new instance of an IIntruderPayloadGenerator object, which will be
        used to generate payloads for the attack.

        :param factory:
            An object created by the extension that implements the IIntruderPayloadGeneratorFactory interface.
        :return: None
        """

    def getIntruderPayloadGeneratorFactories(self):
        # type: () -> List[IIntruderPayloadGeneratorFactory]
        """
        This method is used to retrieve the Intruder payload generator factories that are registered by the extension.

        :return: A list of Intruder payload generator factories that are currently registered by this extension.
        """

    def removeIntruderPayloadGeneratorFactory(self, factory):
        # type: (IIntruderPayloadGeneratorFactory) -> ()
        """

        :param factory: The Intruder payload generator factory to be removed.
        :return: None
        """

    def registerIntruderPayloadProcessor(self, processor):
        # type: (IIntruderPayloadProcessor) -> ()
        """
        This method is used to register a custom Intruder payload processor. Each registered processor will be
        available within the Intruder UI for the user to select as the action for a payload processing rule.

        :param processor: An object created by the extension that implements the IIntruderPayloadProcessor interface.
        :return:
        """

    def getIntruderPayloadProcessors(self):
        # type: () -> List[IIntruderPayloadProcessor]
        """
        This method is used to retrieve the Intruder payload processors that are registered by the extension.

        :return: A list of Intruder payload processors that are currently registered by this extension.
        """

    def removeIntruderPayloadProcessor(self, processor):
        # type: (IIntruderPayloadProcessor) -> ()
        """
        This method is used to remove an Intruder payload processor that has been registered by the extension.

        :param processor:
        :return: The Intruder payload processor to be removed.
        """

    def registerSessionHandlingAction(self, action):
        # type: (ISessionHandlingAction) -> ()
        """
        This method is used to register a custom session handling action. Each registered action will be available
        within the session handling rule UI for the user to select as a rule action. Users can choose to invoke an
        action directly in its own right, or following execution of a macro.

        :param action: An object created by the extension that implements the ISessionHandlingAction interface.
        :return: None
        """

    def getSessionHandlingActions(self):
        # type: () -> List[ISessionHandlingAction]
        """
        This method is used to retrieve the session handling actions that are registered by the extension.

        :return:
        """

    def removeSessionHandlingActions(self, action):
        # type: (ISessionHandlingAction) -> object
        """
        This method is used to remove a session handling action that has been registered by the extension.

        :param action:
        :return:
        """

    def unloadExtension(self):
        # type: () -> ()
        """
        This method is used to unload the extension from Burp Suite.

        :return: None
        """

    def addSuiteTab(self, tab):
        # type: (ITab) -> ()
        """
        This method is used to add a custom tab to the main Burp Suite window.

        :param tab: An object created by the extension that implements the ITab interface.
        :return: None
        """
        pass

    def removeSuiteTab(self, tab):
        # type: (ITab) -> ()
        """
        This method is used to remove a previously-added tab from the main Burp Suite window.

        :param tab: An object created by the extension that implements the ITab interface.
        :return: None
        """
        pass

    def customizeUiComponent(self, component):
        # type: (java.awt.Component) -> None
        """
        This method is used to customize UI components in line with Burp's UI style, including font size, colors,
        table line spacing, etc. The action is performed recursively on any child components of the passed-in
        component.

        :param component: The UI component to be customized.
        :return: None
        """

    def createMessageEditor(self, controller, editable):
        # type: (IMessageEditorController, bool) -> IMessageEditor
        """
        This method is used to create a new instance of Burp's HTTP message editor, for the extension
        to use in its own UI.

        :param controller: An object created by the extension that implements the IMessageEditorController interface.
        This parameter is optional and may be null. If it is provided, then the message editor will query the
        controller when required to obtain details about the currently displayed message, including the IHttpService
        for the message, and the associated request or response message. If a controller is not provided,
        then the message editor will not support context menu actions, such as sending requests to other Burp tools.

        :param editable: Indicates whether the editor created should be editable, or used only for message viewing.

        :return: An object that implements the IMessageEditor interface, and which the extension can use in its own UI.
        """
        pass

    def getCommandLineArguments(self):
        # type: () -> List[str]
        """
        This method returns the command line arguments that were passed to Burp on startup.

        :return: The command line arguments that were passed to Burp on startup.
        """

    def saveExtensionSetting(self, name, value):
        # type: (str, str) -> ()
        """
        This method is used to save configuration settings for the extension in a persistent way that survives
        reloads of the extension and of Burp Suite. Saved settings can be retrieved using the method
        loadExtensionSetting().

        :param name: The name of the setting.
        :param value:
            The value of the setting. If this value is null then any existing setting with the specified
            name will be removed.
        :return: None
        """

    def loadExtensionSetting(self, name):
        # type: (str) -> Union[str,None]
        """
        This method is used to load configuration settings for the extension that were saved using the method
        saveExtensionSetting().

        :param name: The name of the setting.
        :return: The value of the setting, or null if no value is set.
        """

    def createTextEditor(self):
        # type: () -> ITextEditor
        """
        This method is used to create a new instance of Burp's plain text editor, for the extension to use in its own
        UI.

        :return: An object that implements the ITextEditor interface, and which the extension can use in its own UI.
        """

    def sendToRepeater(self, host, port, useHttp, request, tabCaption):
        # type: (str, int, bool, bytearray, Union[str, None]) -> ()
        """
        This method can be used to send an HTTP request to the Burp Repeater tool. The request will be displayed in
        the user interface, but will not be issued until the user initiates this action.

        :param host: The hostname of the remote HTTP server.
        :param port: The port of the remote HTTP server.
        :param useHttp: Flags whether the protocol is HTTPS or HTTP.
        :param request: The full HTTP request.
        :param tabCaption: An optional caption which will appear on the Repeater tab containing the request. If this
                           value is null then a default tab index will be displayed.
        :return: None
        """

    def sendToIntruder(self, host, port, useHttp, request, payloadPositionOffsets):
        # type: (str, int, bool, bytearray, Optional[List[List[int]]]) -> ()
        """
        This method can be used to send an HTTP request to the Burp Intruder tool. The request will be displayed in
        the user interface, and markers for attack payloads will be placed into default locations within the request.

        :param host: The hostname of the remote HTTP server.
        :param port: The port of the remote HTTP server.
        :param useHttp: Flags whether the protocol is HTTPS or HTTP.
        :param request: The full HTTP request.
        :param payloadPositionOffsets: A list of index pairs representing the payload positions to be used. Each item
                                       in the list must be an int[2] array containing the start and end offsets for the
                                       payload position.
        :return: None
        """

    def sendToComparer(self, data):
        # type: (bytearray) -> ()
        """
        This method can be used to send data to the Comparer tool.

        :param data: The data to be sent to Comparer.
        :return: None
        """

    def sendToSpider(self, url):
        # type: (java.net.URL) -> ()
        """
        This method can be used to send a seed URL to the Burp Spider tool. If the URL is not within the current
        Spider scope, the user will be asked if they wish to add the URL to the scope. If the Spider is not currently
        running, it will be started. The seed URL will be requested, and the Spider will process the application's
        response in the normal way.

        :param url: The new seed URL to begin spidering from.
        :return: None
        """

    def doActiveScan(self, host, port, useHttps, request, insertionPointOffsets):
        # type: (str, int, bool, bytearray, Optional[List[List[int]]]) -> IScanQueueItem
        """
        This method can be used to send an HTTP request to the Burp Scanner tool to perform an active vulnerability
        scan, based on a custom list of insertion points that are to be scanned. If the request is not within the
        current active scanning scope, the user will be asked if they wish to proceed with the scan.

        :param host: The hostname of the remote HTTP server.
        :param port: The port of the remote HTTP server.
        :param useHttps: Flags whether the protocol is HTTPS or HTTP.
        :param request: The full HTTP request.
        :param insertionPointOffsets:
            A list of index pairs representing the positions of the insertion points that should be scanned.
            Each item in the list must be an int[2] array containing the start and end offsets for the insertion point.
        :return: The resulting scan queue item.
        """

    def doPassiveScan(self, host, port, useHttps, request, response):
        # type: (str, int, bool, bytearray, bytearray) -> ()
        """
        This method can be used to send an HTTP request to the Burp Scanner tool to perform a passive vulnerability scan

        :param host: The hostname of the remote HTTP server.
        :param port: The port of the remote HTTP server.
        :param useHttps: Flags whether the protocol is HTTPS or HTTP.
        :param request: The full HTTP request.
        :param response: The full HTTP response.
        :return: None
        """

    def makeHttpRequest(self, httpService, request, hey_see_docstring=True):
        # type: (IHttpService, bytearray, Optional[bool]) -> ()
        """
        This method can be used to issue HTTP requests and retrieve their responses.
        NOTE: This method also exists with signature (host: str, port: int, useHttps: bool, request: bytearray)
              Python do not support having a function with multiple signatures.

        :param httpService: The HTTP service to which the request should be sent.
        :param request: The full HTTP request.
        :return: The full response retrieved from the remote server.
        """

    def isInScope(self, url):
        # type: (java.net.url) -> bool
        """
        This method can be used to query whether a specified URL is within the current Suite-wide scope.

        :param url: The URL to query.
        :return: Returns true if the URL is within the current Suite-wide scope.
        """

    def includeInScope(self, url):
        # type: (java.net.URL) -> ()
        """
        This method can be used to include the specified URL in the Suite-wide scope.

        :param url: The URL to include in the Suite-wide scope.
        :return: None
        """

    def excludeFromScope(self, url):
        # type: (java.net.URL) -> ()
        """
        This method can be used to exclude the specified URL from the Suite-wide scope.

        :param url: The URL to exclude from the Suite-wide scope.
        :return: None
        """

    def issueAlert(self, message):
        # type: (str) -> ()
        """
        This method can be used to display a specified message in the Burp Suite alerts tab.

        :param message: The alert message to display.
        :return: None
        """

    def getProxyHistory(self):
        # type: () -> List[IHttpRequestResponse]
        """
        This method returns details of all items in the Proxy history.

        :return: The contents of the Proxy history.
        """

    def getSiteMap(self, urlPrefix):
        # type: (str) -> IHttpRequestResponse
        """
        This method returns details of items in the site map.

        :param urlPrefix: This parameter can be used to specify a URL prefix, in order to extract a specific subset of
            the site map. The method performs a simple case-sensitive text match, returning all site map items whose URL
            begins with the specified prefix. If this parameter is null, the entire site map is returned.

        :return: Details of items in the site map.
        """

    def getScanIssues(self, urlPrefix):
        # type: (List[IScanIssue]) -> ()
        """
        This method returns all of the current scan issues for URLs matching the specified literal prefix.

        :param urlPrefix:
            This parameter can be used to specify a URL prefix, in order to extract a specific subset
            of scan issues. The method performs a simple case-sensitive text match, returning all scan issues whose URL
            begins with the specified prefix. If this parameter is null, all issues are returned.

        :return: Details of the scan issues.
        """

    def generateScanReport(self, format, issues, file):
        # type: (str, List[IScanIssue], java.io.File) -> ()
        """
        This method is used to generate a report for the specified Scanner issues. The report format can be
        specified. For all other reporting options, the default settings that appear in the reporting UI wizard are
        used.

        :param format: The format to be used in the report. Accepted values are HTML and XML.
        :param issues: The Scanner issues to be reported.
        :param file: The file to which the report will be saved.
        :return: None
        """

    def getCookieJarContents(self):
        # type: () -> List[ICookie]
        """
        This method is used to retrieve the contents of Burp's session handling cookie jar. Extensions that provide
        an ISessionHandlingAction can query and update the cookie jar in order to handle unusual session handling
        mechanisms.

        :return: A list of ICookie objects representing the contents of Burp's session handling cookie jar.
        """

    def updateCookieJar(self, cookie):
        # type: (ICookie) -> ()
        """
        This method is used to update the contents of Burp's session handling cookie jar. Extensions that provide an
        ISessionHandlingAction can query and update the cookie jar in order to handle unusual session handling
        mechanisms.

        :param cookie:
            An ICookie object containing details of the cookie to be updated. If the cookie jar already
            contains a cookie that matches the specified domain and name, then that cookie will be updated with the new
            value and expiration, unless the new value is null, in which case the cookie will be removed. If the cookie
            jar does not already contain a cookie that matches the specified domain and name, then the cookie will be
            added.
        :return: None
        """

    def addToSiteMap(self, item):
        # type: (IHttpRequestResponse) -> ()
        """
        This method can be used to add an item to Burp's site map with the specified request/response details. This
        will overwrite the details of any existing matching item in the site map.

        :param item: Details of the item to be added to the site map
        :return:
        """

    def saveConfigAsJson(self, configPaths):
        # type: (List[str]) -> str
        """
        This method causes Burp to save its current project-level configuration in JSON format. This is the same
        format that can be saved and loaded via the Burp user interface. To include only certain sections of the
        configuration, you can optionally supply the path to each section that should be included, for example:
        "project_options.connections". If no paths are provided, then the entire configuration will be saved.

        :param configPaths:
            A list of Strings representing the path to each configuration section that should be included.
        :return: A String representing the current configuration in JSON format.
        """

    def loadConfigFromJson(self, config):
        # type: (str) -> ()
        """
        This method causes Burp to load a new project-level configuration from the JSON String provided. This is the
        same format that can be saved and loaded via the Burp user interface. Partial configurations are acceptable,
        and any settings not specified will be left unmodified. Any user-level configuration options contained in the
        input will be ignored.

        :param config: A JSON String containing the new configuration.
        :return:
        """

    def setProxyInterceptionEnabled(self, enabled):
        # type: (bool) -> ()
        """
        This method sets the master interception mode for Burp Proxy.

        :param enabled: Indicates whether interception of Proxy messages should be enabled.
        :return: None
        """

    def getBurpVersion(self):
        # type: () -> str
        """
        This method retrieves information about the version of Burp in which the extension is running. It can be used
        by extensions to dynamically adjust their behavior depending on the functionality and APIs supported by the
        current version.

        :return:
            An array of Strings comprised of: the product name (e.g. Burp Suite Professional), the major version
            (e.g. 1.5), the minor version (e.g. 03)
        """

    def getExtensionFilename(self):
        # type: () -> str
        """
        This method retrieves the absolute path name of the file from which the current extension was loaded.

        :return: The absolute path name of the file from which the current extension was loaded.
        """

    def isExtensionBapp(self):
        # type: () -> bool
        """
        This method determines whether the current extension was loaded as a BApp (a Burp App from the BApp Store).

        :return: Returns true if the current extension was loaded as a BApp.
        """

    def exitSuite(self, promptUser):
        # type: (bool) -> ()
        """
        This method can be used to shut down Burp programmatically, with an optional prompt to the user. If the
        method returns, the user canceled the shutdown prompt.

        :param promptUser: Indicates whether to prompt the user to confirm the shutdown.
        :return: Will only return if user cancelled shutdown prompt
        """

    def saveToTempFile(self, buffer):
        # type: (bytearray) -> ITempFile
        """
        This method is used to create a temporary file on disk containing the provided data. Extensions can use
        temporary files for long-term storage of runtime data, avoiding the need to retain that data in memory.

        :param buffer: The data to be saved to a temporary file.
        :return: An object that implements the ITempFile interface.
        """

    def saveBuffersToTempFiles(self, httpRequestResponse):
        # type: (IHttpRequestResponse) -> IHttpRequestResponsePersisted
        """
        This method is used to save the request and response of an IHttpRequestResponse object to temporary files,
        so that they are no longer held in memory. Extensions can used this method to convert IHttpRequestResponse
        objects into a form suitable for long-term storage.

        :param httpRequestResponse:
            The IHttpRequestResponse object whose request and response messages are to be
            saved to temporary files.
        :return: An object that implements the IHttpRequestResponsePersisted interface.
        """

    def applyMarkers(self, httpRequestResponse, requestMarkers, responseMarksers):
        # type: (IHttpRequestResponse, Optional[List[List[int]]], Optional[List[List[int]]]) -> IHttpRequestResponseWithMarkers
        """
        This method is used to apply markers to an HTTP request or response, at offsets into the message that are
        relevant for some particular purpose. Markers are used in various situations, such as specifying Intruder
        payload positions, Scanner insertion points, and highlights in Scanner issues.

        :param httpRequestResponse: he IHttpRequestResponse object to which the markers should be applied.
        :param requestMarkers:
            A list of index pairs representing the offsets of markers to be applied to the request
            message. Each item in the list must be an int[2] array containing the start and end offsets for the marker.
            The markers in the list should be in sequence and not overlapping. This parameter is optional and may be
            null  if no request markers are required.
        :param responseMarksers:
            A list of index pairs representing the offsets of markers to be applied to the
            response message. Each item in the list must be an int[2] array containing the start and end offsets for the
            marker. The markers in the list should be in sequence and not overlapping. This parameter is optional and
            may be null if no response markers are required.
        :return: An object that implements the IHttpRequestResponseWithMarkers interface.
        """

    def getToolName(self, toolFlag):
        # type: (int) -> str
        """
        This method is used to obtain the descriptive name for the Burp tool identified by the tool flag provided.

        :type toolFlag: A flag identifying a Burp tool ( TOOL_PROXY, TOOL_SCANNER, etc.). Tool flags are defined
        within this interface.
        :return: The descriptive name for the specified tool.
        """

    def addScanIssue(self, issue):
        # type: (IScanIssue) -> ()
        """
        This method is used to register a new Scanner issue.

        Note: Wherever possible, extensions should implement custom Scanner checks using IScannerCheck and report
        issues via those checks, so as to integrate with Burp's user-driven workflow, and ensure proper consolidation
        of duplicate reported issues. This method is only designed for tasks outside of the normal testing workflow,
        such as importing results from other scanning tools.

        :param issue: An object created by the extension that implements the IScanIssue interface.
        :return: None
        """

    def createBurpCollaboratorClientContext(self):
        # type: () -> IBurpCollaboratorClientContext
        """
        This method is used to create a new Burp Collaborator client context, which can be used to generate Burp
        Collaborator payloads and poll the Collaborator server for any network interactions that result from using
        those payloads.

        :return:
            A new instance of IBurpCollaboratorClientContext that can be used to generate Collaborator payloads
            and retrieve interactions.
        """


class IContextMenuFactory(object):
    def createMenuItems(self, invocation):
        # type: (IContextMenuInvocation) -> List[javax.swing.JMenuItem]
        """
        This method will be called by Burp when the user invokes a context menu anywhere within Burp. The factory can
        then provide any custom context menu items that should be displayed in the context menu, based on the details
        of the menu invocation.

        :param invocation:
            An object that implements the IContextMenuInvocation interface, which the extension can
            query to obtain details of the context menu invocation.
        :return:
            A list of custom menu items (which may include sub-menus, checkbox menu items, etc.) that should be
            displayed. Extensions may return null from this method, to indicate that no menu items are required.
        """


class IContextMenuInvocation(object):
    # TODO: implement interfaces
    def getInputEvent(self):
        pass

    def getToolFlag(self):
        pass

    def getInvocationContext(self):
        pass

    def getSelectionBounds(self):
        pass

    def getSelectedMessages(self):
        pass

    def getSelectedIssues(self):
        pass


class ICookie(object):
    """ This interface is used to hold details about an HTTP cookie. """

    def getDomain(self):
        # type: () -> Union[str, None]
        """
        This method is used to retrieve the domain for which the cookie is in scope.

        :return: The domain for which the cookie is in scope. Note: For cookies that have been analyzed from
        responses (by calling IExtensionHelpers.analyzeResponse() and then IResponseInfo.getCookies(), the domain
        will be null if the response did not explicitly set a domain attribute for the cookie.
        """
        pass

    def getPath(self):
        # type: () -> Union[str, None]
        """
        This method is used to retrieve the path for which the cookie is in scope.

        :return: The path for which the cookie is in scope or null if none is set.
        """

    def getExpiration(self):
        # type: () -> Union[java.util.Date, None]
        """
        This method is used to retrieve the expiration time for the cookie.

        :return: The expiration time for the cookie, or null if none is set (i.e., for non-persistent session cookies).
        """

    def getName(self):
        # type: () -> str
        """
        This method is used to retrieve the name of the cookie.

        :return: The name of the cookie.
        """

    def getValue(self):
        # type: () -> str
        """
        This method is used to retrieve the value of the cookie.

        :return: The value of the cookie.
        """


class IExtensionHelpers(object):
    def analyzeRequest(self, http_service, request, hey_see_docstrings=True):
        # type: (Union[IHttpRequestResponse, IHttpService], Optional[bytearray], Optional[bool]) -> IRequestInfo
        """
        This method can be used to analyze an HTTP request, and obtain various key details about it.

        There are three signatures for this method:
            IRequestInfo analyzeRequest(IHttpRequestResponse request)
            IRequestInfo analyzeRequest(IHttpService httpService, byte[] request)
            IRequestInfo analyzeRequest(byte[] request)

        Python is do not support multiple signatures for same method, hence its not possible to provide accurate
        typing hints.
        This interface typing implementation support (IHttpService, bytearray) and (IHttpRequestResponse)
        You should be free to also use the third one (bytearray).

        :param http_service: The HTTP service associated with the request. This is optional and may be null,
        in which case the resulting IRequestInfo object will not include the full request URL.

        :param request: The request to be analyzed.

        :return: An IRequestInfo object that can be queried to obtain details about the request.
        """

    def analyzeResponse(self, response):
        # type: (bytearray) -> IResponseInfo
        """
        This method can be used to analyze an HTTP response, and obtain various key details about it.

        :param response: The response to be analyzed.
        :return: An IResponseInfo object that can be queried to obtain details about the response.
        """

    def getRequestParameter(self, request, parameterName):
        # type: (bytearray, str) -> Union[IParameter, None]
        """
        This method can be used to retrieve details of a specified parameter within an HTTP request. Note: Use
        analyzeRequest() to obtain details of all parameters within the request.

        :param request: The request to be inspected for the specified parameter.
        :param parameterName: The name of the parameter to retrieve.
        :return:
            An IParameter object that can be queried to obtain details about the parameter,
            or null if the parameter was not found.
        """

    def urlDecode(self, data):
        # type: (Union[str, bytearray]) -> Union[str, bytearray]
        """
        This method can be used to URL-decode the specified data.

        :param data: The data to be decoded.
        :return: The decoded data.
        """

    def urlEncode(self, data):
        # type: (Union[str, bytearray]) -> Union[str,bytearray]
        """
        This method can be used to URL-encode the specified data. Any characters that do not need to be encoded
        within HTTP requests are not encoded.

        :param data: The data to be encoded.
        :return: The encoded data.
        """

    def base64Decode(self, data):
        # type: (Union[str, bytearray]) -> Union[str, bytearray]
        """
        This method can be used to Base64-decode the specified data.

        :param data: The data to be decoded.
        :return: The decoded data.
        """

    def base64Encode(self, data):
        # type: (Union[str, bytearray]) -> Union[str,bytearray]
        """
        This method can be used to Base64-encode the specified data.

        :param data: The data to be encoded.
        :return: The encoded data.
        """

    def stringToBytes(self, data):
        # type: (str) -> bytearray
        """
        This method can be used to convert data from String form into an array of bytes. The conversion does not
        reflect any particular character set, and a character with the hex representation 0xWXYZ will always be
        converted into a byte with the representation 0xYZ. It performs the opposite conversion to the method
        bytesToString(), and byte-based data that is converted to a String and back again using these two methods is
        guaranteed to retain its integrity (which may not be the case with conversions that reflect a given character
        set).

        :param data: The data to be converted.
        :return: The converted data.
        """
        pass

    def bytesToString(self, data):
        # type: (bytearray) -> str
        """
        This method can be used to convert data from an array of bytes into String form. The conversion does not
        reflect any particular character set, and a byte with the representation 0xYZ will always be converted into a
        character with the hex representation 0x00YZ. It performs the opposite conversion to the method
        stringToBytes(), and byte-based data that is converted to a String and back again using these two methods is
        guaranteed to retain its integrity (which may not be the case with conversions that reflect a given character
        set).

        :param data: The data to be converted.
        :return: The converted data.
        """

    def indexOf(self, data, pattern, caseSensitive, from_pos, to_pos):
        # type: (bytearray, bytearray, bool, int, int) -> int
        # Original signature had "from" and "to", from is a reserved keyword in python
        """
        This method searches a piece of data for the first occurrence of a specified pattern. It works on byte-based
        data in a way that is similar to the way the native Java method String.indexOf() works on String-based data.

        :param data: The data to be searched.
        :param pattern: The pattern to be searched for.
        :param caseSensitive: Flags whether or not the search is case-sensitive.
        :param from_pos: The offset within data where the search should begin.
        :param to_pos: The offset within data where the search should end.
        :return:
            The offset of the first occurrence of the pattern within the specified bounds, or -1 if no match is found.
        """

    def buildHttpMessage(self, headers, body):
        # type: (List[str], Union[bytearray, None]) -> bytearray
        """
        This method builds an HTTP message containing the specified headers and message body. If applicable,
        the Content-Length header will be added or updated, based on the length of the body.

        :param headers: A list of headers to include in the message.
        :param body: The body of the message, of null if the message has an empty body.
        :return:
        """

    def buildHttpRequest(self, url):
        # type: (java.net.URL) -> bytearray
        """
        This method creates a GET request to the specified URL. The headers used in the request are determined by the
        Request headers settings as configured in Burp Spider's options.

        :param url: The URL to which the request should be made.
        :return: A request to the specified URL.
        """
        pass

    def addParameter(self, request, parameter):
        # type: (bytearray, IParameter) -> bytearray
        """
        This method adds a new parameter to an HTTP request, and if appropriate updates the Content-Length header.

        :param request: The request to which the parameter should be added.
        :param parameter:
            An IParameter object containing details of the parameter to be added.
            Supported parameter types are: PARAM_URL, PARAM_BODY and PARAM_COOKIE.

        :return:
        """
        pass

    def removeParameter(self, request, parameter):
        # type: (bytearray, IParameter) -> bytearray
        """
        This method removes a parameter from an HTTP request, and if appropriate updates the Content-Length header.

        :param request: The request from which the parameter should be removed.
        :param parameter:
            An IParameter object containing details of the parameter to be removed.
            Supported parameter types are: PARAM_URL, PARAM_BODY and PARAM_COOKIE.
        :return: A new HTTP request with the parameter removed.
        """

    def updateParameter(self, request, parameter):
        # type: (bytearray, IParameter) -> bytearray
        """
        This method updates the value of a parameter within an HTTP request, and if appropriate updates the
        Content-Length header. Note: This method can only be used to update the value of an existing parameter of a
        specified type. If you need to change the type of an existing parameter, you should first call
        removeParameter() to remove the parameter with the old type, and then call addParameter() to add a parameter
        with the new type.

        :param request: The request containing the parameter to be updated.
        :param parameter:
            An IParameter object containing details of the parameter to be updated.
            Supported parameter types are: PARAM_URL, PARAM_BODY and PARAM_COOKIE.
        :return: A new HTTP request with the parameter updated.
        """

    def toggleRequestMethod(self, request):
        # type: (bytearray) -> bytearray
        """
        This method can be used to toggle a request's method between GET and POST. Parameters are relocated between
        the URL query string and message body as required, and the Content-Length header is created or removed as
        applicable.

        :param request: The HTTP request whose method should be toggled.
        :return: A new HTTP request using the toggled method.
        """

    def buildHttpService(self, host, port, protocol_or_useHttps):
        # type: (str, int, Union[str,bool]) -> IHttpService
        """
        This method constructs an IHttpService object based on the details provided.

        Note: This function have multiple signatures, but support both.

        :param host: The HTTP service host.
        :param port: The HTTP service port.
        :param protocol_or_useHttps:
            str: The HTTP service protocol.
            bool: Flags whether the HTTP service protocol is HTTPS or HTTP.
        :return: An IHttpService object based on the details provided.
        """
        pass

    # noinspection PyShadowingBuiltins
    def buildParameter(self, name, value, type):
        # type: (str, str, int) -> IParameter
        """
        This method constructs an IParameter object based on the details provided.

        :param name: The parameter name.
        :param value: The parameter value.
        :param type: The parameter type, as defined in the IParameter interface.
        :return: An IParameter object based on the details provided.
        """

    def makeInsertionPoint(self, insertionPointName, baseRequest, from_pos, to_pos):
        # type: (str, bytearray, int, int) -> IScannerInsertionPoint
        # original signature had "from" and "to". renamed due to reserved keyword "from"
        """
        This method constructs an IScannerInsertionPoint object based on the details provided. It can be used to
        quickly create a simple insertion point based on a fixed payload location within a base request.

        :param insertionPointName: The name of the insertion point.
        :param baseRequest: The request from which to build scan requests.
        :param from_pos: The offset of the start of the payload location.
        :param to_pos: The offset of the end of the payload location.
        :return:
        """

    def analyzeResponseVariations(self, responses):
        # type: (List[bytearray]) -> IResponseVariations
        """
        This method analyzes one or more responses to identify variations in a number of attributes and returns an
        IResponseVariations object that can be queried to obtain details of the variations.

        :param responses: The responses to analyze.
        :return: An IResponseVariations object representing the variations in the responses.
        """

    def analyzeResponseKeywords(self, keywords, responses):
        # type: (List[str], List[bytearray]) -> IResponseKeywords
        """
        This method analyzes one or more responses to identify the number of occurrences of the specified keywords
        and returns an IResponseKeywords object that can be queried to obtain details of the number of occurrences of
        each keyword.

        :param keywords: The keywords to look for.
        :param responses: The responses to analyze.
        :return: An IResponseKeywords object representing the counts of the keywords appearing in the responses.
        """


class IExtensionStateListener(object):
    """
    Extensions can implement this interface and then call IBurpExtenderCallbacks.registerExtensionStateListener() to
    register an extension state listener. The listener will be notified of changes to the extension's state. Note:
    Any extensions that start background threads or open system resources (such as files or database connections)
    should register a listener and terminate threads / close resources when the extension is unloaded.
    """

    def extensionUnloaded(self):
        # type: () -> ()
        """
        This method is called when the extension is unloaded.

        :return: None
        """


class IHttpListener(object):
    """
    Extensions can implement this interface and then call IBurpExtenderCallbacks.registerHttpListener() to register
    an HTTP listener. The listener will be notified of requests and responses made by any Burp tool. Extensions can
    perform custom analysis or modification of these messages by registering an HTTP listener.
    """

    def processHttpMessage(self, toolFlag, messageIsRequest, messageInfo):
        # type: (int, bool, IHttpRequestResponse) -> ()
        """
        This method is invoked when an HTTP request is about to be issued, and when an HTTP response has been received.

        :param toolFlag:
            A flag indicating the Burp tool that issued the request. Burp tool flags are defined
            in the IBurpExtenderCallbacks interface.
        :param messageIsRequest: Flags whether the method is being invoked for a request or response.
        :param messageInfo:
            Details of the request / response to be processed. Extensions can call the setter methods on
            this object to update the current message and so modify Burp's behavior.
        :return: None
        """


class IHttpRequestResponse(object):
    """
    This interface is used to retrieve and update details about HTTP messages. Note: The setter methods generally can
    only be used before the message has been processed, and not in read-only contexts. The getter methods relating to
    response details can only be used after the request has been issued.
    """

    def getRequest(self):
        # type: () -> bytearray
        """
        This method is used to retrieve the request message.

        :return: The request message.
        """

    def setRequest(self, message):
        # type: (bytearray) -> ()
        """
        This method is used to update the request message.

        :param message: The new request message
        :return: None
        """

    def getResponse(self):
        # type: () -> bytearray
        """
        This method is used to retrieve the response message.

        :return: The response message.
        """

    def setResponse(self, message):
        # type: (bytearray) -> ()
        """
        This method is used to update the response message.

        :param message: The new response message
        :return: None
        """

    def getComment(self):
        # type: () -> str
        """
        This method is used to retrieve the user-annotated comment for this item, if applicable.

        :return: The comment to be assigned to this item.
        """

    def setComment(self, comment):
        # type: (str) -> ()
        """
        This method is used to update the user-annotated comment for this item.

        :param comment: The comment to be assigned to this item.
        :return: None
        """

    def getHighlight(self):
        # type: () -> Union[str, None]
        """
        This method is used to retrieve the user-annotated highlight for this item, if applicable.

        :return: The user-annotated highlight for this item, or null if none is set.
        """
        pass

    def setHighlight(self, color):
        # type: (str) -> ()
        """
        This method is used to update the user-annotated highlight for this item.

        :param color:
            The highlight color to be assigned to this item.
            Accepted values are: red, orange, yellow, green, cyan, blue, pink, magenta, gray,
            or a null String to clear any existing highlight.
        :return: None
        """

    def getHttpService(self):
        # type: () -> IHttpService
        """
        This method is used to retrieve the HTTP service for this request / response.

        :return: An IHttpService object containing details of the HTTP service.
        """

    def setHttpService(self, http_service):
        # type: (IHttpService) -> ()
        """
        This method is used to update the HTTP service for this request / response.

        :param http_service: An IHttpService object containing details of the new HTTP service.
        :return: None
        """


class IHttpRequestResponsePersisted(IHttpRequestResponse):
    """
    This interface is used for an IHttpRequestResponse object whose request and response messages have been saved to
    temporary files using IBurpExtenderCallbacks.saveBuffersToTempFiles().

    """


class IHttpRequestResponseWithMarkers(IHttpRequestResponse):
    """
    This interface is used for an IHttpRequestResponse object that has had markers applied. Extensions can create
    instances of this interface using IBurpExtenderCallbacks.applyMarkers(), or provide their own implementation.
    Markers are used in various situations, such as specifying Intruder payload positions, Scanner insertion points,
    and highlights in Scanner issues.
    """

    def getRequestMarkers(self):
        # type: () -> List[List[int]]
        """
        This method returns the details of the request markers.

        :return:
            A list of index pairs representing the offsets of markers for the request message. Each item in the list
            is an int[2] array containing the start and end offsets for the marker. The method may return null if no
            request markers are defined.
        """

    def getResponseMarkers(self):
        # type: () -> List[List[int]]
        """
        This method returns the details of the response markers.

        :return:
            A list of index pairs representing the offsets of markers for the response message. Each item in the list
            is an int[2] array containing the start and end offsets for the marker. The method may return null if no
            response markers are defined.
        """


class IHttpService(object):
    """
    This interface is used to provide details about an HTTP service, to which HTTP requests can be sent.
    """

    def getHost(self):
        # type: () -> str
        """
        This method returns the hostname or IP address for the service.

        :return: The hostname or IP address for the service.
        """

    def getPort(self):
        # type: () -> str
        """
        This method returns the port number for the service.

        :return: The port number for the service.
        """

    def getProtocol(self):
        # type: () -> str
        """
        This method returns the protocol for the service.

        :return: The protocol for the service. Expected values are "http" or "https".
        """


class IInterceptedProxyMessage(object):
    """ This interface is used to represent an HTTP message that has been intercepted by Burp Proxy. Extensions can
    register an IProxyListener to receive details of proxy messages using this interface. """

    ACTION_DO_INTERCEPT = 0
    ACTION_DO_INTERCEPT_AND_REHOOK = 0
    ACTION_DONT_INTERCEPT = 0
    ACTION_DONT_INTERCEPT_AND_REHOOK = 0
    ACTION_DROP = 0
    ACTION_FOLLOW_RULES = 0
    ACTION_FOLLOW_RULES_AND_REHOOK = 0

    def getClientIpAddress(self):
        # type: () -> java.net.InetAddress
        """
        This method retrieves the client IP address from which the request for the intercepted message was received

        :return: The client IP address from which the request for the intercepted message was received.
        """

    def getInterceptAction(self):
        # type: () -> int
        """
        This method retrieves the currently defined interception action. The default action is ACTION_FOLLOW_RULES.
        If multiple proxy listeners are registered, then other listeners may already have modified the interception
        action before it reaches the current listener. This method can be used to determine whether this has occurred.

        :return: The currently defined interception action. Possible values are defined within this interface.
        """

    def getListenerInterface(self):
        # type: () -> str
        """
        This method retrieves the name of the Burp Proxy listener that is processing the intercepted message.

        :return:
            The name of the Burp Proxy listener that is processing the intercepted message. The format is the same as
            that shown in the Proxy Listeners UI - for example, "127.0.0.1:8080".
        """

    def getMessageInfo(self):
        # type: () -> IHttpRequestResponse
        """
        This method retrieves details of the intercepted message.

        :return: An IHttpRequestResponse object containing details of the intercepted message.
        """

    def getMessageReference(self):
        # type: () -> int
        """
        This method retrieves a unique reference number for this request/response.

        :return:
            An identifier that is unique to a single request/response pair. Extensions can use this to correlate
            details of requests and responses and perform processing on the response message accordingly.
        """

    def setInterceptAction(self, interceptAction):
        # type: (int) -> ()
        """
        This method is used to update the interception action.

        :param interceptAction: The new interception action. Possible values are defined within this interface.
        :return: None
        """
        pass


class IIntruderAttack(object):
    """ This interface is used to hold details about an Intruder attack. """

    def getHttpService(self):
        # type: () -> IHttpService
        """
        This method is used to retrieve the HTTP service for the attack.

        :return: The HTTP service for the attack.
        """

    def getRequestTemplate(self):
        # type: () -> bytearray
        """
        This method is used to retrieve the request template for the attack.

        :return: The request template for the attack.
        """


class IIntruderPayloadGenerator(object):
    """
    This interface is used for custom Intruder payload generators. Extensions that have registered an
    IIntruderPayloadGeneratorFactory must return a new instance of this interface when required as part of a new
    Intruder attack.
    """

    def getNextPayload(self, baseValue):
        # type: (bytearray) -> bytearray
        """
        This method is used by Burp to obtain the value of the next payload.

        :param baseValue:
            The base value of the current payload position. This value may be null if the concept of a base value is
            not applicable (e.g. in a battering ram attack).
        :return: The next payload to use in the attack.
        """

    def hasMorePayloads(self):
        # type: () -> bool
        """
        This method is used by Burp to determine whether the payload generator is able to provide any further payloads.

        :return: Extensions should return false when all the available payloads have been used up, otherwise true.
        """

    def reset(self):
        # type: () -> ()
        """
        This method is used by Burp to reset the state of the payload generator so that the next call to
        getNextPayload() returns the first payload again. This method will be invoked when an attack uses the same
        payload generator for more than one payload position, for example in a sniper attack.

        :return: None
        """


class IIntruderPayloadGeneratorFactory(object):
    """
    Extensions can implement this interface and then call
    IBurpExtenderCallbacks.registerIntruderPayloadGeneratorFactory() to register a factory for custom Intruder
    payloads.
    """

    def createNewInstance(self, attack):
        # type: (IIntruderAttack) -> IIntruderPayloadGenerator
        """
        This method is used by Burp to obtain the name of the payload generator. This will be displayed as an option
        within the Intruder UI when the user selects to use extension-generated payloads.

        :param attack:
            An IIntruderAttack object that can be queried to obtain details about the attack in which the payload
            generator will be used.
        :return: A new instance of IIntruderPayloadGenerator that will be used to generate payloads for the attack.
        """

    def getGeneratorName(self):
        # type: () -> str
        """
        This method is used by Burp to obtain the name of the payload generator. This will be displayed as an option
        within the Intruder UI when the user selects to use extension-generated payloads.

        :return: The name of the payload generator.
        """


class IIntruderPayloadProcessor(object):
    """
    Extensions can implement this interface and then call IBurpExtenderCallbacks.registerIntruderPayloadProcessor()
    to register a custom Intruder payload processor.
    """

    def getProcessorName(self):
        # type: () -> str
        """
        This method is used by Burp to obtain the name of the payload processor. This will be displayed as an option
        within the Intruder UI when the user selects to use an extension-provided payload processor.

        :return: The name of the payload processor.
        """

    def processPayload(self, currentPayload, originalPayload, baseValue):
        # type: (bytearray, bytearray, bytearray) -> Union[bytearray, None]
        """
        This method is invoked by Burp each time the processor should be applied to an Intruder payload.

        :param currentPayload: The value of the payload to be processed.
        :param originalPayload:
            The value of the original payload prior to processing by any already-applied processing rules.
        :param baseValue: The base value of the payload position, which will be replaced with the current payload.
        :return:
            The value of the processed payload. This may be null to indicate that the current payload should
            be skipped, and the attack will move directly to the next payload.
        """


class IMessageEditor(object):
    """
    This interface is used to provide extensions with an instance of Burp's HTTP message editor, for the extension to
    use in its own UI. Extensions should call IBurpExtenderCallbacks.createMessageEditor() to obtain an instance of
    this interface.
    """

    def getComponent(self):
        # type: () -> java.awt.Component
        """
        This method returns the UI component of the editor, for extensions to add to their own UI.

        :return: The UI component of the editor.
        """

    def getMessage(self):
        # type: () -> bytearray
        """
        This method is used to retrieve the currently displayed message, which may have been modified by the user.

        :return: The currently displayed HTTP message.
        """

    def getSelectedData(self):
        # type: () -> bytearray
        """
        This method returns the data that is currently selected by the user.

        :return: The data that is currently selected by the user, or null if no selection is made.
        """

    def getSelectionBounds(self):
        # type: () -> Union[List[int], None]
        """
        This method returns the data that is currently selected by the user.

        :return: The data that is currently selected by the user, or null if no selection is made.
        """

    def isMessageModified(self):
        # type: () -> bool
        """
        This method is used to determine whether the current message has been modified by the user.

        :return: An indication of whether the current message has been modified by the user since it was first displayed.
        """

    def setMessage(self, message, isRequest):
        # type: (bytearray, bool) -> ()
        """
        This method is used to display an HTTP message in the editor

        :param message: The HTTP message to be displayed.
        :param isRequest: Flags whether the message is an HTTP request or response.
        :return:
        """


class IMessageEditorController(object):
    """
    This interface is used by an IMessageEditor to obtain details about the currently displayed message. Extensions
    that create instances of Burp's HTTP message editor can optionally provide an implementation of
    IMessageEditorController, which the editor will invoke when it requires further information about the current
    message (for example, to send it to another Burp tool). Extensions that provide custom editor tabs via an
    IMessageEditorTabFactory will receive a reference to an IMessageEditorController object for each tab instance
    they generate, which the tab can invoke if it requires further information about the current message.
    """

    def getHttpService(self):
        # type: () -> IHttpService
        """
        This method is used to retrieve the HTTP service for the current message.

        :return: The HTTP service for the current message.
        """

    def getRequest(self):
        # type: () -> bytearray
        """
        This method is used to retrieve the HTTP request associated with the current message
        (which may itself be a response).

        :return: The HTTP request associated with the current message
        """

    def getResponse(self):
        # type: () -> bytearray
        """
        This method is used to retrieve the HTTP response associated with the current message
        (which may itself be a request).

        :return: The HTTP response associated with the current message.
        """


class IMessageEditorTab(object):
    """ Extensions that register an IMessageEditorTabFactory must return instances of this interface, which Burp will
    use to create custom tabs within its HTTP message editors. """

    def getMessage(self):
        # type: () -> bytearray
        """
        This method returns the currently displayed message.

        :return: The currently displayed message.
        """

    def getSelectedData(self):
        # type: () -> bytearray
        """
        This method is used to retrieve the data that is currently selected by the user.

        :return: The data that is currently selected by the user. This may be null if no selection is currently made.
        """

    def getTabCaption(self):
        # type: () -> str
        """
        This method returns the caption that should appear on the custom tab when it is displayed. Note: Burp invokes
        this method once when the tab is first generated, and the same caption will be used every time the tab is
        displayed.

        :return: The caption that should appear on the custom tab when it is displayed.
        """

    def getUiComponent(self):
        # type: () -> java.awt.Component
        """
        This method returns the component that should be used as the contents of the custom tab when it is displayed.
        Note: Burp invokes this method once when the tab is first generated, and the same component will be used
        every time the tab is displayed.

        :return: The component that should be used as the contents of the custom tab when it is displayed.
        """

    def isEnabled(self, content, isRequest):
        # type: (bytearray, bool) -> bool
        """
        The hosting editor will invoke this method before it displays a new HTTP message, so that the custom tab can
        indicate whether it should be enabled for that message.

        :param content:
            The message that is about to be displayed, or a zero-length array if the existing message is to be cleared.
        :param isRequest: Indicates whether the message is a request or a response.
        :return:
            The method should return true if the custom tab is able to handle the specified message, and so will be
            displayed within the editor. Otherwise, the tab will be hidden while this message is displayed.

        """

    def isModified(self):
        # type: () -> bool
        """
        This method is used to determine whether the currently displayed message has been modified by the user. The
        hosting editor will always call getMessage() before calling this method, so any pending edits should be
        completed within getMessage().

        :return: The method should return true if the user has modified the current message since it was first displayed.
        """

    def setMessage(self, content, isRequest):
        # type: (Union[bytearray,None], bool) -> ()
        """
        The hosting editor will invoke this method to display a new message or to clear the existing message. This
        method will only be called with a new message if the tab has already returned true to a call to isEnabled()
        with the same message details.

        :param content:
            The message that is to be displayed, or null if the tab should clear its contents and disable
            any editable controls.
        :param isRequest: Indicates whether the message is a request or a response.
        :return:
        """


class IMessageEditorTabFactory(object):
    """
    Extensions can implement this interface and then call IBurpExtenderCallbacks.registerMessageEditorTabFactory() to
    register a factory for custom message editor tabs. This allows extensions to provide custom rendering or editing
    of HTTP messages, within Burp's own HTTP editor.
    """

    def createNewInstance(self, controller, editable):
        """
        Burp will call this method once for each HTTP message editor, and the factory should provide a new instance
        of an IMessageEditorTab object.

        :param controller:
            An IMessageEditorController object, which the new tab can query to retrieve details about the
            currently displayed message. This may be null for extension-invoked message editors where the
            extension has not provided an editor controller.
        :param editable: Indicates whether the hosting editor is editable or read-only.
        :return: A new IMessageEditorTab object for use within the message editor.
        """


class IParameter(object):
    """
    This interface is used to hold details about an HTTP request parameter.
    """
    PARAM_URL = 0
    PARAM_BODY = 1
    PARAM_COOKIE = 2
    PARAM_XML = 3
    PARAM_XML_ATTR = 4
    PARAM_MULTIPART_ATTR = 5
    PARAM_JSON = 6

    def getType(self):
        # type: () -> int
        """
        This method is used to retrieve the parameter type.

        :return: The parameter type. The available types are defined within this interface.
        """

    def getName(self):
        # type: () -> str
        """
        This method is used to retrieve the parameter name.

        :return: The parameter name.
        """

    def getValue(self):
        # type: () -> str
        """
        This method is used to retrieve the parameter value.

        :return: The parameter value.
        """

    def getNameStart(self):
        # type: () -> int
        """
        This method is used to retrieve the start offset of the parameter name within the HTTP request.

        :return:
            The start offset of the parameter name within the HTTP request, or -1 if the parameter is not associated
            with a specific request.
        """

    def getNameEnd(self):
        # type: () -> int
        """
        This method is used to retrieve the end offset of the parameter name within the HTTP request.

        :return:
            The end offset of the parameter name within the HTTP request, or -1 if the parameter is not associated
            with a specific request.
        """
        pass

    def getValueStart(self):
        # type: () -> int
        """
        This method is used to retrieve the start offset of the parameter value within the HTTP request.

        :return:
            The start offset of the parameter value within the HTTP request, or -1 if the parameter is not associated
            with a specific request.
        """

    def getValueEnd(self):
        # type: () -> int
        """
        This method is used to retrieve the end offset of the parameter value within the HTTP request.

        :return:
            The end offset of the parameter value within the HTTP request, or -1 if the parameter is not associated
            with a specific request.
        """


class IProxyListener(object):
    """
    Extensions can implement this interface and then call IBurpExtenderCallbacks.registerProxyListener() to register
    a Proxy listener. The listener will be notified of requests and responses being processed by the Proxy tool.
    Extensions can perform custom analysis or modification of these messages, and control in-UI message interception,
    by registering a proxy listener.
    """

    def processProxyMessage(self, messageIsRequest, message):
        # type: (bool, IInterceptedProxyMessage) -> ()
        """
        This method is invoked when an HTTP message is being processed by the Proxy.

        :param messageIsRequest: Indicates whether the HTTP message is a request or a response.
        :param message:
            An IInterceptedProxyMessage object that extensions can use to query and update details of the message,
            and control whether the message should be intercepted and displayed to the user for manual
            review or modification.
        :return:
        """


class IRequestInfo(object):
    """
    This interface is used to retrieve key details about an HTTP request. Extensions can obtain an IRequestInfo
    object for a given request by calling IExtensionHelpers.analyzeRequest().
    """
    CONTENT_TYPE_NONE = 0
    CONTENT_TYPE_URL_ENCODED = 1
    CONTENT_TYPE_MULTIPART = 2
    CONTENT_TYPE_XML = 3
    CONTENT_TYPE_JSON = 4
    CONTENT_TYPE_AMF = 5
    CONTENT_TYPE_UNKNOWN = -1

    def getMethod(self):
        # type: () -> str
        """
        This method is used to obtain the HTTP method used in the request.

        :return: The HTTP method used in the request.
        """

    def getUrl(self):
        # type: () -> java.net.URL
        # java url object
        """
        This method is used to obtain the URL in the request.

        :return: The URL in the request.
        """

    def getHeaders(self):
        # type: () -> List[str]
        """
        This method is used to obtain the HTTP headers contained in the request.

        :return: The HTTP headers contained in the request.
        """

    def getParameters(self):
        # type: () -> List[IParameter]
        """
        This method is used to obtain the parameters contained in the request.

        :return: The parameters contained in the request.
        """

    def getBodyOffset(self):
        # type: () -> int
        """
        This method is used to obtain the offset within the request where the message body begins.

        :return: The offset within the request where the message body begins.
        """

    def getContentType(self):
        # type: () -> int
        """
        This method is used to obtain the content type of the message body.

        :return:
            An indication of the content type of the message body. Available types are defined within this interface.
        """


class IResponseInfo(object):
    """
    This interface is used to retrieve key details about an HTTP response. Extensions can obtain an IResponseInfo
    object for a given response by calling IExtensionHelpers.analyzeResponse().
    """

    def getHeaders(self):
        # type: () -> List[str]
        """
        This method is used to obtain the HTTP headers contained in the response.

        :return: The HTTP headers contained in the response.
        """

    def getBodyOffset(self):
        # type: () -> int
        """
        This method is used to obtain the offset within the response where the message body begins.

        :return: The offset within the response where the message body begins.
        """

    def getStatusCode(self):
        # type: () -> int
        """
        This method is used to obtain the HTTP status code contained in the response.

        :return: The HTTP status code contained in the response.
        """

    def getCookies(self):
        # type: () -> List[ICookie]
        """
        This method is used to obtain details of the HTTP cookies set in the response.

        :return: A list of ICookie objects representing the cookies set in the response, if any.
        """

    def getStatedMimeType(self):
        # type: () -> str
        """
        This method is used to obtain the MIME type of the response, as stated in the HTTP headers

        :return:
            A textual label for the stated MIME type, or an empty String if this is not known or recognized. The
            possible labels are the same as those used in the main Burp UI.
        """

    def getInferredMimeType(self):
        # type: () -> str
        """
        This method is used to obtain the MIME type of the response, as inferred from the contents of the HTTP
        message body.

        :return:
            A textual label for the inferred MIME type, or an empty String if this is not known or recognized. The
            possible labels are the same as those used in the main Burp UI.
        """


class IResponseKeywords(object):
    """
    This interface is used to represent the counts of keywords appearing in a number of HTTP responses.
    """

    def getInvariantKeywords(self):
        # type: () -> List[str]
        """
        This method is used to obtain the list of keywords whose counts vary between the analyzed responses.

        :return: The keywords whose counts vary between the analyzed responses.
        """

    def getKeywordCount(self, keyword, responseIndex):
        # type: (str, int) -> int
        """
        This method is used to obtain the number of occurrences of an individual keyword in a response.

        :param keyword: The keyword whose count will be retrieved.
        :param responseIndex:
            The index of the response. Note responses are indexed from zero in the order they were originally
            supplied to the IExtensionHelpers.analyzeResponseKeywords() and IResponseKeywords.updateWith() methods.
        :return: The number of occurrences of the specified keyword for the specified response.
        """

    def getVariantKeywords(self):
        # type: () -> List[str]
        """
        This method is used to obtain the list of keywords whose counts vary between the analyzed responses.

        :return: The keywords whose counts vary between the analyzed responses.
        """

    def updateWith(self, responses):
        # type: (List[bytearray]) -> ()
        # (byte[].. responses)
        """
        This method is used to update the analysis based on additional responses.

        :param responses: The new responses to include in the analysis.
        :return: None
        """


class IResponseVariations(object):
    """
    This interface is used to represent variations between a number HTTP responses, according to various attributes.
    """

    def getVariantAttributes(self):
        # type: () -> List[str]
        """
        This method is used to obtain the list of attributes that vary between the analyzed responses.

        :return: The attributes that vary between the analyzed responses.
        """

    def getInvariantAttributes(self):
        # type: () -> List[str]
        """
        This method is used to obtain the list of attributes that do not vary between the analyzed responses.

        :return: The attributes that do not vary between the analyzed responses.
        """

    def getAttributeValue(self, attributeName, responseIndex):
        # type: (str, int) -> str
        """
        This method is used to obtain the value of an individual attribute in a response. Note that the values of
        some attributes are intrinsically meaningful (e.g. a word count) while the values of others are less so (e.g.
        a checksum of the HTML tag names).

        :param attributeName:
            The name of the attribute whose value will be retrieved. Extension authors can obtain the list of
            supported attributes by generating an IResponseVariations object for a single response and calling
            IResponseVariations.getInvariantAttributes().

        :param responseIndex:
            The index of the response. Note that responses are indexed from zero in the order they were originally
            supplied to the IExtensionHelpers.analyzeResponseVariations() and IResponseVariations.updateWith() methods.

        :return: The value of the specified attribute for the specified response.
        """

    def updateWith(self, responses):
        # type: (List[bytearray]) -> ()
        """
        This method is used to update the analysis based on additional responses.

        :param responses: The new responses to include in the analysis.
        :return: None
        """


class IScanIssue(object):
    """
    This interface is used to retrieve details of Scanner issues. Extensions can obtain details of issues by
    registering an IScannerListener or by calling IBurpExtenderCallbacks.getScanIssues(). Extensions can also add
    custom Scanner issues by registering an IScannerCheck or calling IBurpExtenderCallbacks.addScanIssue(),
    and providing their own implementations of this interface. Note that issue descriptions and other text generated
    by extensions are subject to an HTML whitelist that allows only formatting tags and simple hyperlinks.
    """

    def getUrl(self):
        # type: () -> java.net.URL
        """
        This method returns the URL for which the issue was generated.

        :return: The URL for which the issue was generated.
        """

    def getIssueName(self):
        # type: () -> str
        """
        This method returns the name of the issue type.

        :return: The name of the issue type (e.g. "SQL injection").
        """

    def getIssueType(self):
        # type: () -> str
        """
        This method returns a numeric identifier of the issue type. See the Burp Scanner help documentation for a
        listing of all the issue types.

        :return: A numeric identifier of the issue type.
        """

    def getSeverity(self):
        # type: () -> str
        """
        This method returns the issue severity level

        :return: The issue severity level. Expected values are "High", "Medium", "Low", "Information"
        or "False positive".
        """

    def getConfidence(self):
        # type: () -> str
        """
        This method returns the issue confidence level.

        :return: The issue confidence level. Expected values are "Certain", "Firm" or "Tentative".
        """

    def getIssueBackground(self):
        # type: () -> Union[str, None]
        """
        This method returns a background description for this type of issue.

        :return:
            A background description for this type of issue, or null if none applies. A limited set of HTML tags may
            be used.
        """

    def getRemediationBackground(self):
        # type: () -> Union[str, None]
        """
        This method returns a background description of the remediation for this type of issue.

        :return:
            A background description of the remediation for this type of issue, or null if none applies. A limited
            set of HTML tags may be used.
        """

    def getIssueDetail(self):
        # type: () -> Union[str, None]
        """
        This method returns detailed information about this specific instance of the issue.

        :return:
            Detailed information about this specific instance of the issue, or null if none applies. A limited set of
            HTML tags may be used.
        """

    def getRemediationDetail(self):
        # type: () -> Union[str, None]
        """
        This method returns detailed information about the remediation for this specific instance of the issue.

        :return:
            Detailed information about the remediation for this specific instance of the issue, or null if none
            applies. A limited set of HTML tags may be used.
        """

    def getHttpMessages(self):
        # type: () -> List[IHttpRequestResponseWithMarkers]
        """
        This method returns the HTTP messages on the basis of which the issue was generated.

        :return:
            The HTTP messages on the basis of which the issue was generated. Note: The items in this array should be
            instances of IHttpRequestResponseWithMarkers if applicable, so that details of the relevant portions of
            the request and response messages are available.
        """

    def getHttpService(self):
        # type: () -> IHttpService
        """
        This method returns the HTTP service for which the issue was generated.

        :return: The HTTP service for which the issue was generated.
        """


class IScannerCheck(object):
    """
    Extensions can implement this interface and then call IBurpExtenderCallbacks.registerScannerCheck() to register a
    custom Scanner check. When performing scanning, Burp will ask the check to perform active or passive scanning on
    the base request, and report any Scanner issues that are identified.
    """

    def doPassiveScan(self, baseRequestResponse):
        # type: (IHttpRequestResponse) -> List[IScanIssue]
        """
        The Scanner invokes this method for each base request / response that is passively scanned. Note: Extensions
        should only analyze the HTTP messages provided during passive scanning, and should not make any new HTTP
        requests of their own.

        :param baseRequestResponse: The base HTTP request / response that should be passively scanned.
        :return: A list of IScanIssue objects, or null if no issues are identified.
        """

    def doActiveScan(self, baseRequestResponse, insertionPoint):
        # type: (IHttpRequestResponse, IScannerInsertionPoint) -> List[IScanIssue]
        """
        The Scanner invokes this method for each insertion point that is actively scanned. Extensions may issue HTTP
        requests as required to carry out active scanning, and should use the IScannerInsertionPoint object provided
        to build scan requests for particular payloads. Note: Scan checks should submit raw non-encoded payloads to
        insertion points, and the insertion point has responsibility for performing any data encoding that is
        necessary given the nature and location of the insertion point.

        :param baseRequestResponse: The base HTTP request / response that should be actively scanned.
        :param insertionPoint:
            An IScannerInsertionPoint object that can be queried to obtain details of the insertion point being
            tested, and can be used to build scan requests for particular payloads.
        :return: A list of IScanIssue objects, or null if no issues are identified.
        """

    def consolidateDuplicateIssues(self, existingIssue, newIssue):
        # type: (IScanIssue, IScanIssue) -> int
        """
        The Scanner invokes this method when the custom Scanner check has reported multiple issues for the same URL
        path. This can arise either because there are multiple distinct vulnerabilities, or because the same (or a
        similar) request has been scanned more than once. The custom check should determine whether the issues are
        duplicates. In most cases, where a check uses distinct issue names or descriptions for distinct issues,
        the consolidation process will simply be a matter of comparing these features for the two issues.

        :param existingIssue: An issue that was previously reported by this Scanner check.
        :param newIssue: An issue that was previously reported by this Scanner check.
        :return:
            An indication of which issue(s) should be reported in the main Scanner results. The method should return
            -1 to report the existing issue only, 0 to report both issues, and 1 to report the new issue only.
        """
        pass


class IScannerInsertionPointProvider(object):
    """
    Extensions can implement this interface and then call
    IBurpExtenderCallbacks.registerScannerInsertionPointProvider() to register a factory for custom Scanner insertion
    points.
    """

    def getInsertionPints(self, baseRequestResponse):
        # type: (IHttpRequestResponse) -> List[IScannerInsertionPoint]
        """
        When a request is actively scanned, the Scanner will invoke this method, and the provider should provide a
        list of custom insertion points that will be used in the scan. Note: these insertion points are used in
        addition to those that are derived from Burp Scanner's configuration, and those provided by any other Burp
        extensions.

        :param baseRequestResponse: The base request that will be actively scanned.

        :return: A list of IScannerInsertionPoint objects that should be used in the scanning, or null if no
                 custom insertion points are applicable for this request.
        """


class IScannerInsertionPoint(object):
    """
    This interface is used to define an insertion point for use by active Scanner checks. Extensions can obtain
    instances of this interface by registering an IScannerCheck, or can create instances for use by Burp's own scan
    checks by registering an IScannerInsertionPointProvider.
    """

    INS_PARAM_URL = 0x00
    INS_PARAM_BODY = 0x01
    INS_PARAM_COOKIE = 0x02
    INS_PARAM_XML = 0x03
    INS_PARAM_XML_ATTR = 0x04
    INS_PARAM_MULTIPART_ATTR = 0x05
    INS_PARAM_JSON = 0x06
    INS_PARAM_AMF = 0x07
    INS_HEADER = 0x20
    INS_URL_PATH_FOLDER = 0x21
    INS_URL_PATH_REST = INS_URL_PATH_FOLDER
    INS_PARAM_NAME_URL = 0x22
    INS_PARAM_NAME_BODY = 0x23
    INS_ENTIRE_BODY = 0x24
    INS_URL_PATH_FILENAME = 0x25
    INS_USER_PROVIDED = 0x40
    INS_EXTENSION_PROVIDED = 0x41
    INS_UNKNOWN = 0x7f

    def getInsertionPointName(self):
        # type: () -> str
        """
        This method returns the name of the insertion point.

        :return: The name of the insertion point (for example, a description of a particular request parameter).
        """

    def getBaseValue(self):
        # type: () -> str
        """
        This method returns the base value for this insertion point.

        :return: the base value that appears in this insertion point in the base request being scanned, or null if
        there is no value in the base request that corresponds to this insertion point.
        """
        pass

    def buildRequest(self, payload):
        # type: (bytearray) -> bytearray
        """
        This method is used to build a request with the specified payload placed into the insertion point. There is
        no requirement for extension-provided insertion points to adjust the Content-Length header in requests if the
        body length has changed, although Burp-provided insertion points will always do this and will return a
        request with a valid Content-Length header. Note: Scan checks should submit raw non-encoded payloads to
        insertion points, and the insertion point has responsibility for performing any data encoding that is
        necessary given the nature and location of the insertion point.

        :param payload: The payload that should be placed into the insertion point.
        :return: The resulting request.
        """
        pass

    def getInsertionPointType(self):
        # type: () -> int
        """
        This method returns the type of the insertion point.
        TODO: make java.net.Byte prototype
        """
        pass

    def getPayloadOffsets(self, payload):
        # type: (bytearray) -> Union[List[int],None]
        """
        This method is used to determine the offsets of the payload value within the request, when it is placed into
        the insertion point. Scan checks may invoke this method when reporting issues, so as to highlight the
        relevant part of the request within the UI.

        :param payload: The payload that should be placed into the insertion point.

        :return: An int[2] array containing the start and end offsets of the payload within the request, or null if
        this is not applicable (for example, where the insertion point places a payload into a serialized data
        structure, the raw payload may not literally appear anywhere within the resulting request).
        """
        pass


class IScannerListener(object):
    """
    Extensions can implement this interface and then call IBurpExtenderCallbacks.registerScannerListener() to
    register a Scanner listener. The listener will be notified of new issues that are reported by the Scanner tool.
    Extensions can perform custom analysis or logging of Scanner issues by registering a Scanner listener.
    """

    def newScanIssue(self, issue):
        """
        This method is invoked when a new issue is added to Burp Scanner's results.

        :param issue: An IScanIssue object that the extension can query to obtain details about the new issue.
        :return: None
        """


class IScanQueueItem(object):
    """
    This interface is used to retrieve details of items in the Burp Scanner active scan queue. Extensions can obtain
    references to scan queue items by calling IBurpExtenderCallbacks.doActiveScan().
    """

    def cancel(self):
        # type: () -> ()
        """
        This method allows the scan queue item to be canceled.

        :return: None
        """

    def getIssues(self):
        # type: () -> IScanIssue
        """
        This method returns details of the issues generated for the scan queue item. Note: different items within the
        scan queue may contain duplicated versions of the same issues - for example, if the same request has been
        scanned multiple times. Duplicated issues are consolidated in the main view of scan results. Extensions can
        register an IScannerListener to get details only of unique, newly discovered Scanner issues post-consolidation.

        :return: Details of the issues generated for the scan queue item.
        """

    def getNumErrors(self):
        # type: () -> int
        """
        This method returns the number of network errors that have occurred for the scan queue item.

        :return: The number of network errors that have occurred for the scan queue item.
        """

    def getNumInsertionPoints(self):
        # type: () -> int
        """
        This method returns the number of attack insertion points being used for the scan queue item.

        :return: The number of attack insertion points being used for the scan queue item.
        """

    def getNumRequests(self):
        # type: () -> int
        """
        This method returns the number of requests that have been made for the scan queue item.

        :return: The number of requests that have been made for the scan queue item.
        """

    def getStatus(self):
        # type: () -> str
        """
        This method returns a description of the status of the scan queue item.

        :return: A description of the status of the scan queue item.
        """


class IScopeChangeListener(object):
    """
    Extensions can implement this interface and then call IBurpExtenderCallbacks.registerScopeChangeListener() to
    register a scope change listener. The listener will be notified whenever a change occurs to Burp's suite-wide
    target scope.
    """

    def scopeChanged(self):
        # type: () -> ()
        """
        This method is invoked whenever a change occurs to Burp's suite-wide target scope.

        :return: None
        """


class ISessionHandlingAction(object):
    """
    Extensions can implement this interface and then call IBurpExtenderCallbacks.registerSessionHandlingAction() to
    register a custom session handling action. Each registered action will be available within the session handling
    rule UI for the user to select as a rule action. Users can choose to invoke an action directly in its own right,
    or following execution of a macro.
    """

    def getActionName(self):
        # type: () -> str
        """
        This method is used by Burp to obtain the name of the session handling action. This will be displayed as an
        option within the session handling rule editor when the user selects to execute an extension-provided action.

        :return:
        """

    def performAction(self, currentRequest, macroItems):
        # type: (IHttpRequestResponse, List[IHttpRequestResponse]) -> ()
        """
        This method is invoked when the session handling action should be executed. This may happen as an action in
        its own right, or as a sub-action following execution of a macro.

        :param currentRequest:
        :param macroItems:
        :return:
        """


class ITab(object):
    """
    This interface is used to provide Burp with details of a custom tab that will be added to Burp's UI,
    using a method such as IBurpExtenderCallbacks.addSuiteTab().
    """

    def getTabCaption(self):
        # type: () -> str
        """
        Burp uses this method to obtain the caption that should appear on the custom tab when it is displayed.

        :return: The caption that should appear on the custom tab when it is displayed.
        """

    def getUiComponent(self):
        # type: () -> java.awt.Component
        """
        Burp uses this method to obtain the component that should be used as the contents of the custom tab when it
        is displayed.

        :return: The component that should be used as the contents of the custom tab when it is displayed.
        """


class ITempFile(object):
    """ This interface is used to hold details of a temporary file that has been created via a call to
    IBurpExtenderCallbacks.saveToTempFile(). """

    def getBuffer(self):
        """
        This method is used to retrieve the contents of the buffer that was saved in the temporary file.

        :return: The contents of the buffer that was saved in the temporary file.
        """


class ITextEditor(object):
    """
    This interface is used to provide extensions with an instance of Burp's raw text editor, for the extension to use
    in its own UI. Extensions should call IBurpExtenderCallbacks.createTextEditor() to obtain an instance of this
    interface.
    """

    def getComponent(self):
        # type: () -> java.awt.Component
        """
        This method returns the UI component of the editor, for extensions to add to their own UI.

        :return: The UI component of the editor.
        """

    def getSelectedText(self):
        # type: () -> bytearray
        """
        This method is used to obtain the currently selected text.

        :return: The currently selected text, or null if the user has not made any selection.
        """

    def getSelectionBounds(self):
        # type: () -> List[List[int]]
        """
        This method can be used to retrieve the bounds of the user's selection into the displayed text, if applicable.

        :return:
            An int[2] array containing the start and end offsets of the user's selection within the displayed text.
            If the user has not made any selection in the current message, both offsets indicate the position of the
            caret within the editor.
        """

    def getText(self):
        # type: () -> bytearray
        """
        This method is used to retrieve the currently displayed text.

        :return: The currently displayed text.
        """

    def isTextModified(self):
        # type: () -> bool
        """
        This method is used to determine whether the user has modified the contents of the editor.

        :return: An indication of whether the user has modified the contents of the editor since the last call to
        setText().
        """

    def setEditable(self, editable):
        # type: (bool) -> ()
        """
        This method is used to control whether the editor is currently editable. This status can be toggled on and
        off as required.

        :param editable: Indicates whether the editor should be currently editable.
        :return:
        """

    def setSearchExpression(self, expression):
        # type: (str) -> ()
        """
        This method is used to update the search expression that is shown in the search bar below the editor. The
        editor will automatically highlight any regions of the displayed text that match the search expression.

        :param expression: The search expression.
        :return:
        """

    def setText(self, text):
        # type: (str) -> ()
        """
        This method is used to update the currently displayed text in the editor.

        :param text: The text to be displayed.
        :return:
        """
