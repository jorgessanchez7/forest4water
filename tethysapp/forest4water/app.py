from tethys_sdk.base import TethysAppBase, url_map_maker


class Forest4Water(TethysAppBase):
    """
    Tethys app class for Forest and Flow Variability.
    """

    name = 'Forest and Flow Variability'
    index = 'forest4water:home'
    icon = 'forest4water/images/f4r_logo.jpeg'
    package = 'forest4water'
    root_url = 'forest4water'
    color = '#197a43'
    description = 'This apps compares the time series for Mean, Max, and Min Monthly Discharge and Monthly Forest Cover in Colombia'
    tags = '"Ecohydrology", "Time Series", "Forest Water Nexus"'
    enable_feedback = False
    feedback_emails = []

    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (
            UrlMap(
                name='home',
                url='forest4water',
                controller='forest4water.controllers.home'
            ),
            UrlMap(
                name='get_discharge_data',
                url='get-discharge-data',
                controller='forest4water.controllers.get_discharge_data'
            ),
        )

        return url_maps