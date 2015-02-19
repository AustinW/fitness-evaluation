import plotly.plotly as py
from plotly.graph_objs import *

class Plot:

	API_KEY = 'n9w9sqqtwg'

	def get_graph_from_category(self, category_data, category_name):

		scatter_plot = Scatter(
			x = [i[0] for i in category_data],
			y = [i[1] for i in category_data]
		)

		data = Data([scatter_plot])

		plot_url = py.plot(data, filename=category_name)

		return plot_url