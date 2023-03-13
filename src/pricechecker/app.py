"""
An application that searches for the best deals from Ebay.
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from .serpApiTest import search
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

        search_box = toga.Box(style = Pack(direction = ROW, padding = 5))

        input_label = toga.Label("Search on Ebay: ", style = Pack(padding = (0,5)))
        self.search_input = toga.TextInput(style = Pack(flex = 1))

        search_box.add(input_label)
        search_box.add(self.search_input)
        
        price_box = toga.Box(style = Pack(direction = ROW, padding = 5))

        price_label = toga.Label("What are you looking to pay for it? : ", style = Pack(padding = (0,5)))
        self.price_input = toga.TextInput(style = Pack(flex = 1))

        price_box.add(price_label)
        price_box.add(self.price_input)

        button_box = toga.Box(style = Pack(direction = ROW, padding = 5))

        self.search_button = toga.Button('Search on Ebay', on_press = self.search, style = Pack(padding = 5))
        self.search_under_button = toga.Button('Search Below Price Input', on_press = self.search_under, style = Pack(padding = 5))

        button_box.add(self.search_button)
        button_box.add(self.search_under_button)

        self.resultBox = toga.Box(style = Pack(direction = COLUMN))

        main_box.add(search_box)
        main_box.add(price_box)
        main_box.add(button_box)
        main_box.add(self.resultBox)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()
        

    def search(self, *args):
        
        self.resultsList = search(self.search_input.value)

        self.resultButtonList = []

        for result in self.resultsList:
            self.resultButtonList.append(toga.Button(result['message'], on_press = self.link, style = Pack()))

            self.resultBox.add(self.resultButtonList[-1])

    def search_under(self, *args):

        self.resultsList = search(self.search_input.value)


    def link(self, button):
        
        for num in range(len(self.resultButtonList)):
            if self.resultButtonList[num] == button:
                webbrowser.open_new(self.resultsList[num]['link'])

def main():
    return PriceChecker()
