"""
An application that searches for the best deals from Ebay.
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from .serpApi import search, accountSearch
from toga.constants import LIGHTCORAL, YELLOW, LIGHTGREEN
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
        self.APIDrop = toga.Selection(items = ['Ebay', 'Google Shopping', 'Walmart', 'Home Depot'], style = Pack(width = 120))
        input_label2 = toga.Label(": ", style = Pack(padding = (0,5)))
        self.search_input = toga.TextInput(style = Pack(flex = 1))

        search_box.add(input_label)
        search_box.add(self.APIDrop)
        search_box.add(input_label2)
        search_box.add(self.search_input)

        input_box.add(search_box)
        
        price_box = toga.Box(style = Pack(direction = ROW, padding = inputPadding))

        price_label = toga.Label("What are you looking to pay for it? : ", style = Pack(padding = (0,5)))
        self.price_input = toga.NumberInput(style = Pack(flex = 1))

        price_box.add(price_label)
        price_box.add(self.price_input)

        input_box.add(price_box)

        leeway_box = toga.Box(style = Pack(direction = ROW, padding = inputPadding))

        leeway_label = toga.Label("What amount of leeway would you like? : ", style = Pack(padding = (0,5)))
        self.leeway_input = toga.NumberInput(style = Pack(flex = 1))

        leeway_box.add(leeway_label)
        leeway_box.add(self.leeway_input)

        input_box.add(leeway_box)

        self.button_box = toga.Box(style = Pack(direction = ROW, padding = 2))

        self.resultButtonList = []

        self.search_button = toga.Button('Search', on_press = self.search, style = Pack(padding = 2))
        self.search_under_button = toga.Button('Search Below Price', on_press = self.search_under, style = Pack(padding = 2))
        self.sort_button = toga.Button('Sort By Price', on_press = self.sortByPrice, style = Pack(padding = 2))
        uses_left_button = toga.Button('Searches Left', on_press = self.uses_left, style = Pack(padding = 2))

        self.button_box.add(self.search_button)
        self.button_box.add(self.search_under_button)
        self.button_box.add(self.sort_button)
        self.button_box.add(uses_left_button)

        self.resultBox = toga.Box(style = Pack(direction = COLUMN))
        self.resultScroll = toga.ScrollContainer(style = Pack(direction = COLUMN), horizontal = False, content = self.resultBox)

        main_box.add(input_box)
        main_box.add(self.button_box)
        main_box.add(self.resultScroll)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

        # This allows an error to show incase no results show or something happens in the code
        self.Error = False

    def search(self, *args):

        if self.Error == True:
            self.button_box.remove(self.ErrorLabel)

            self.Error = False
        
        for result in self.resultButtonList:
            self.resultBox.remove(result)
        
        self.resultsList = search(self.APIDrop.value, self.search_input.value)

        if len(self.resultsList) == 0:
            self.Error = True

            self.ErrorLabel = toga.Label('No Items Found', style = Pack(padding = (6,0)))

            self.button_box.add(self.ErrorLabel)

        else:
            self.get_results()

    def search_under(self, *args):

        if self.Error == True:
            self.button_box.remove(self.ErrorLabel)

            self.Error = False

        for result in self.resultButtonList:
            self.resultBox.remove(result)

        self.resultsList = search(self.APIDrop.value, self.search_input.value, float(self.price_input.value))

        if len(self.resultsList) == 0:
            self.Error = True

            self.ErrorLabel = toga.Label('No Items Found', style = Pack(padding = (6,0)))

            self.button_box.add(self.ErrorLabel)

        else:
            self.get_results()

    def sortByPrice(self, *args):

        if self.Error == True:
            self.button_box.remove(self.ErrorLabel)

            self.Error = False

        for result in self.resultButtonList:
            self.resultBox.remove(result)

        def sortPrice(value):
            return value['price']

        try:
            if len(self.resultsList) == 0 or len(self.resultButtonList) == 0:
                self.Error = True
                self.ErrorLabel = toga.Label("No Items to Sort", style = Pack(padding = (5,0)))

                self.button_box.add(self.ErrorLabel)

            else:
                self.resultsList.sort(key = sortPrice)

                self.get_results()
        
        except:
            self.Error = True
            self.ErrorLabel = toga.Label("Error Sorting Items", style = Pack(padding = (5,0)))

            self.button_box.add(self.ErrorLabel)

    def uses_left(self, *args):

        self.Error = True

        self.ErrorLabel = toga.Label(f"{accountSearch()} Searches Left", style = Pack(padding = (5,0)))

        self.button_box.add(self.ErrorLabel)

    def get_results(self, *args):

        leeway = 0

        if self.leeway_input.value != None:
            leeway = int(self.leeway_input.value)

        if self.price_input.value == None:
            price = 0

        else:
            price = self.price_input.value

        self.resultButtonList = []

        if self.price_input.value != "":
            for result in self.resultsList:

                # If the price is not specified, keep the color white
                if type(result['price']) == str:
                    self.resultButtonList.append(toga.Button(result['message'], on_press = self.link, style = Pack()))

                elif price + leeway < result['price']:
                    self.resultButtonList.append(toga.Button(result['message'], on_press = self.link, style = Pack(background_color = LIGHTCORAL)))

                elif price - leeway > result['price']:
                    self.resultButtonList.append(toga.Button(result['message'], on_press = self.link, style = Pack(background_color = LIGHTGREEN)))
                
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
