"""
An application that searches for the best deals from Ebay.
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from .serpApiTest import search
from toga.constants import RED, GREEN, YELLOW
import webbrowser

class PriceChecker(toga.App):

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        main_box = toga.Box(style = Pack(direction = COLUMN))

        inputPadding = 2

        input_box = toga.Box(style = Pack(direction = COLUMN))

        search_box = toga.Box(style = Pack(direction = ROW, padding = inputPadding))

        input_label = toga.Label("Search on", style = Pack(padding = (0,5)))
        self.APIDrop = toga.Selection(items = ['Ebay', 'Google Shopping', 'Google Products', 'Walmart', 'Home Depot'], style = Pack(width = 120))
        input_label2 = toga.Label(": ", style = Pack(padding = (0,5)))
        self.search_input = toga.TextInput(style = Pack(flex = 1))

        search_box.add(input_label)
        search_box.add(self.APIDrop)
        search_box.add(input_label2)
        search_box.add(self.search_input)

        input_box.add(search_box)
        
        price_box = toga.Box(style = Pack(direction = ROW, padding = inputPadding))

        price_label = toga.Label("What are you looking to pay for it? : ", style = Pack(padding = (0,5)))
        self.price_input = toga.TextInput(style = Pack(flex = 1))

        price_box.add(price_label)
        price_box.add(self.price_input)

        input_box.add(price_box)

        leeway_box = toga.Box(style = Pack(direction = ROW, padding = inputPadding))

        leeway_label = toga.Label("What amount of leeway would you like? : ", style = Pack(padding = (0,5)))
        self.leeway_input = toga.TextInput(style = Pack(flex = 1))

        leeway_box.add(leeway_label)
        leeway_box.add(self.leeway_input)

        input_box.add(leeway_box)

        button_box = toga.Box(style = Pack(direction = ROW, padding = 2))

        self.resultButtonList = []

        self.search_button = toga.Button('Search', on_press = self.search, style = Pack(padding = 2))
        self.search_under_button = toga.Button('Search Below Price Input', on_press = self.search_under, style = Pack(padding = 2))

        button_box.add(self.search_button)
        button_box.add(self.search_under_button)

        self.resultBox = toga.Box(style = Pack(direction = COLUMN))
        self.resultScroll = toga.ScrollContainer(style = Pack(direction = COLUMN), horizontal = False, content = self.resultBox)

        main_box.add(input_box)
        main_box.add(button_box)
        main_box.add(self.resultScroll)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def search(self, *args):
        
        for result in self.resultButtonList:
            self.resultBox.remove(result)
        
        self.resultsList = search(self.APIDrop.value, self.search_input.value)

        self.get_results()

    def search_under(self, *args):

        for result in self.resultButtonList:
            self.resultBox.remove(result)

        self.resultsList = search(self.APIDrop.value, self.search_input.value, float(self.price_input.value))

        self.get_results()

    def get_results(self, *args):

        leeway = 50

        if self.leeway_input.value != '':
            leeway = int(self.leeway_input.value)

        self.resultButtonList = []

        if self.price_input.value != "":
            for result in self.resultsList:

                # If the price is not specified, keep the color white
                if type(result['price']) == str:
                    self.resultButtonList.append(toga.Button(result['message'], on_press = self.link, style = Pack()))

                elif int(self.price_input.value) - leeway < result['price']:
                    self.resultButtonList.append(toga.Button(result['message'], on_press = self.link, style = Pack(background_color = RED)))

                elif int(self.price_input.value) + leeway > result['price']:
                    self.resultButtonList.append(toga.Button(result['message'], on_press = self.link, style = Pack(background_color = GREEN)))
                
                else:
                    self.resultButtonList.append(toga.Button(result['message'], on_press = self.link, style = Pack(background_color = YELLOW)))

                self.resultBox.add(self.resultButtonList[-1])

        else:
            for result in self.resultsList:

                self.resultButtonList.append(toga.Button(result['message'], on_press = self.link, style = Pack()))

                self.resultBox.add(self.resultButtonList[-1])

    def link(self, button):
        
        for num in range(len(self.resultButtonList)):
            if self.resultButtonList[num] == button:
                webbrowser.open_new(self.resultsList[num]['link'])

def main():
    return PriceChecker()
