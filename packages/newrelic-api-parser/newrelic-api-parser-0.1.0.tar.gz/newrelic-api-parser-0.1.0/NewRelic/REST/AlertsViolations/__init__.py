from NewRelic.Base import BaseNewRelic

class AlertsViolations(BaseNewRelic):

    def __init__(self, API_KEY):
        super().__init__(API_KEY)

    def get_list(self, options: dict = {}) -> dict:
        """
        fetch the alert violations for new relic
        """
        url = self.BASE_URI + '/alerts_violations.json'
        return super().get_data(url, options=options)