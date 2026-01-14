import wx
import re
from collections import Counter

class windowClass(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(windowClass, self).__init__(*args, **kwargs)
        self.Centre()
        self.basicGUI()

    def basicGUI(self):
        panel = wx.Panel(self)
        menuBar = wx.MenuBar()
        fileButton = wx.Menu()
        
        # Create menu items
        openItem = fileButton.Append(wx.ID_ANY, 'Open Text File', 'Open a text file to analyze')
        exitItem = fileButton.Append(wx.ID_EXIT, 'Exit', 'Exit application')
        
        menuBar.Append(fileButton, 'File')
        self.SetMenuBar(menuBar)

        # Bind menu events
        self.Bind(wx.EVT_MENU, self.Quit, exitItem)
        self.Bind(wx.EVT_MENU, self.OpenFile, openItem)

        self.statusbar = self.CreateStatusBar(1)
        self.statusbar.SetStatusText('Ready - Open a text file to analyze')
        self.SetTitle('Text File Word Frequency Analyzer')
        self.Show(True)

    def count_words(self, filepath):
        """Count word frequency in a text file and return top 3 words"""
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                text = file.read().lower()
            
            # Extract words using regex
            words = re.findall(r'\b\w+\b', text)
            word_counts = Counter(words)
            return word_counts.most_common(3)
            
        except Exception as e:
            wx.MessageDialog(self, f"Error reading file: {str(e)}", "Error", wx.OK | wx.ICON_ERROR).ShowModal()
            return None

    def OpenFile(self, e):
        """Open file dialog and analyze selected text file"""
        with wx.FileDialog(self, "Open Text File", wildcard="Text files (*.txt)|*.txt") as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            filepath = fileDialog.GetPath()
            self.statusbar.SetStatusText(f"Analyzing: {filepath}")
            
            # Count words and get top 3
            top_words = self.count_words(filepath)
            
            if top_words:
                # Format results for display
                if top_words:
                    result_text = "Top 3 Most Frequent Words:\n"
                    for word, count in top_words:
                        result_text += f"'{word}': {count} times\n"
                else:
                    result_text = "No words found in file."
                
                # Show results in message dialog
                wx.MessageDialog(self, result_text, "Analysis Results", wx.OK | wx.ICON_INFORMATION).ShowModal()
            
            self.statusbar.SetStatusText('Analysis complete')

    def Quit(self, e):
        yesNoBox = wx.MessageDialog(None, 'Are you sure you want to Quit?', 'Question', wx.YES_NO)
        yesNoAnswer = yesNoBox.ShowModal()
        yesNoBox.Destroy()
        if yesNoAnswer == wx.ID_YES:
            self.Close()

def main():
    app = wx.App()
    windowClass(None, size=(600, 400))
    app.MainLoop()

if __name__ == "__main__":
    main()