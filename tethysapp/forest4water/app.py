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
            UrlMap(
                name='get_sediments_data',
                url='get-sediments-data',
                controller='forest4water.controllers.get_sediments_data'
            ),
            UrlMap(
                name='get_temperature_data',
                url='get-temperature-data',
                controller='forest4water.controllers.get_temperature_data'
            ),
            UrlMap(
                name='get_precipitation_data',
                url='get-precipitation-data',
                controller='forest4water.controllers.get_precipitation_data'
            ),
            UrlMap(
                name='get_forest_cover_data',
                url='get-forest-cover-data',
                controller='forest4water.controllers.get_forest_cover_data'
            ),
            UrlMap(
	            name='get_monthly_mean_discharge_data',
	            url='get-monthly-mean-discharge-data',
	            controller='forest4water.controllers.get_monthly_mean_discharge_data'
            ),
            UrlMap(
                name='get_monthly_std_discharge_data',
                url='get-monthly-std-discharge-data',
                controller='forest4water.controllers.get_monthly_std_discharge_data'
            ),
            UrlMap(
	            name='get_monthly_max_discharge_data',
	            url='get-monthly-max-discharge-data',
	            controller='forest4water.controllers.get_monthly_max_discharge_data'
            ),
            UrlMap(
	            name='get_monthly_min_discharge_data',
	            url='get-monthly-min-discharge-data',
	            controller='forest4water.controllers.get_monthly_min_discharge_data'
            ),
            UrlMap(
	            name='get_monthly_mean_sediments_data',
	            url='get-monthly-mean-sediments-data',
	            controller='forest4water.controllers.get_monthly_mean_sediments_data'
            ),
            UrlMap(
	            name='get_monthly_std_sediments_data',
	            url='get-monthly-std-sediments-data',
	            controller='forest4water.controllers.get_monthly_std_sediments_data'
            ),
            UrlMap(
	            name='get_scatterPlot_Q_FC',
	            url='get-scatterPlot-Q-FC',
	            controller='forest4water.controllers.get_scatterPlot_Q_FC'
            ),
            UrlMap(
	            name='get_scatterPlot_S_FC',
	            url='get-scatterPlot-S-FC',
	            controller='forest4water.controllers.get_scatterPlot_S_FC'
            ),
        )

        return url_maps