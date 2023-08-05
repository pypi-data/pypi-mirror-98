from tcell_agent.agent import TCellAgent
from tcell_agent.instrumentation.decorators import catches_generic_exception
from tcell_agent.instrumentation.startup import instrument_lfi_os
from tcell_agent.events.server_agent_framework_event import ServerAgentFrameworkEvent


@catches_generic_exception(__name__, "Error starting agent")
def start_agent():
    if TCellAgent.startup():
        from tcell_agent.instrumentation.flaskinst.routes import report_routes
        report_routes()
        instrument_lfi_os()

        from flask import __version__
        sade = ServerAgentFrameworkEvent("Flask", __version__)
        TCellAgent.send(sade)
