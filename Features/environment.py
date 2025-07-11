# Variables Declaration
from utils.logger import get_logger
def before_all(context):
    context.logger = get_logger()
    context.base_url = f"https://concacaf-api.dev.sdp.deltatre.digital"
    context.token = None
    context.config_data = {"env": "dev"}
    context.competitionId = "cpl::Football_Competition::854b8253300c4811a11094bbe0da81ee"
    context.projectCode = "cpl"
    context.teamId = "cpl::Football_Team::a92c57ab1d2041c4bfb1856a00645ace"
    context.stadiumId = "cpl::Football_Stadium::0b84d157b99d4a22abe15dc4c3a59216"
    context.seasonId = "cpl::Football_Season::ef4074023d99497e9c973a1dc98007fb"
    context.seasonIds = "cpl::Football_Season::ef4074023d99497e9c973a1dc98007fb"
    context.seasonId = "cpl::Football_Season::ef4074023d99497e9c973a1dc98007fb"
