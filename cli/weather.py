from rich.console import Console
from .api import CLIInterface


class Weather(CLIInterface):
    def retrieve_menu(self):
        return [
            {
                "menu_info": ["weather", "Retrieve weather information", "weather_command"],
                "weather_children": [
                    {"menu_info": ["five_day_forecast", "5 day weather forecast", "five_day_forecast_command"]},
                    {"menu_info": ["hourly_forecast", "hourly weather forecast", "hourly_forecast_command"]},
                    {
                        "menu_info": ["comparison", "Make weather comparison", ""],
                        "comparison_children": [
                            {"menu_info": ["temperature", "Compare temperature from cities", "temperature_command"]},
                            {"menu_info": ["humidity", "Compare humidity from cities", "humidity_command"]},
                        ],
                    },
                ],
            }
        ]

    def __init__(self):
        super().__init__()
        self.console = Console()

    def weather_command(self):
        self.console.print('Weather')

    def five_day_forecast_command(self):
        self.console.print('5_day_forecast')

    def hourly_forecast_command(self):
        city = self.console.input('Enter your city: ')
        self.console.print(f'hourly_forecast for {city}')

    def temperature_command(self):
        self.console.print('temperature')

    def humidity_command(self):
        self.console.print('humidity')
